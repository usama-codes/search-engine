from flask import Flask, request, jsonify
import subprocess
import json
from flask_cors import CORS
import traceback
import os
from ADDFile import ADDFile
import pathlib

app = Flask(__name__)

# Automatically determine the base directory
base_dir = pathlib.Path(__file__).parent.parent

lexicon_file = base_dir / 'engine_data' / 'lexicon.csv'
barrels_dir = base_dir / 'engine_data' / 'barrels'
doc_id_file = base_dir / 'engine_data' / 'doc_id.txt'

# Enable CORS for my frontend app running on port 5173
CORS(app, origins="http://localhost:5173")

# path to the compiled C++ executable
CPP_EXECUTABLE = base_dir / 'backend' / 'ProcessQuery.exe'

# directory for the uploaded files to be stored
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# start the cpp process on start of server 
cpp_process = None
#function to start the cpp process
def start_cpp_process():
    """Start the C++ program as a persistent process."""
    global cpp_process
    cpp_process = subprocess.Popen(
        [CPP_EXECUTABLE],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding='utf-8'
    )
#function to handle the query within the cpp process
def handle_cpp_query(query):
    """Send the query to the running C++ process and get the result."""
    if cpp_process:
        # Send the query to C++ program via stdin
        cpp_process.stdin.write(query + '\n')
        cpp_process.stdin.flush()

        # Read the response from the C++ program
        result = cpp_process.stdout.readline()
        return result
    else:
        raise Exception("C++ process is not running")
#route to handle the query from the frontend
@app.route('/query', methods=['POST'])
def query():
    data = request.json
    if not data or 'query' not in data:
        return jsonify({"status": "error", "message": "No query provided"}), 400

    query = data['query']

    try:
        # Handle the query by passing it to the already running C++ process
        print(query)
        result = handle_cpp_query(query)
        
        if result:
            # Parse JSON output from C++ program
            try:
                cpp_output = json.loads(result)
            except json.JSONDecodeError as e:
                return jsonify({"status": "error", "message": "Invalid JSON from C++ program", "stderr": result.strip()}), 500

            # Extract and process the 'results' field
            if 'results' not in cpp_output or not isinstance(cpp_output['results'], list):
                return jsonify({"status": "error", "message": "Unexpected format in C++ program output"}), 500

            search_results = [
                {
                    "id": item.get("doc_id"),
                    "title": item.get("title"),
                    "url": item.get("url"),
                    "description": item.get("description", ""),
                    "tags": parse_tags(item.get("tags", '[]'))  # Use the parsing function
                }
                for item in cpp_output['results']
            ]
            return jsonify(search_results)
        else:
            return jsonify({"status": "error", "message": "No response from C++ program"}), 500

    except Exception as e:
        # Log the full traceback of the error
        print("Error occurred:", e)
        print("Traceback:", traceback.format_exc())
        return jsonify({"status": "error", "message": str(e)}), 500
#function to parse the tags field 
def parse_tags(raw_tags):
    """Parse the tags field safely."""
    try:
        cleaned_tags = raw_tags.strip('"').replace("'", '"')
        return json.loads(cleaned_tags)
    except json.JSONDecodeError:
        return []
#function to upload the file and update the inverted index
@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({"status": "error", "message": "No file part in the request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"status": "error", "message": "No file selected for uploading"}), 400

    try:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        index_manager = ADDFile(lexicon_file,  barrels_dir, doc_id_file)#calling the ADDFile class functions 
        index_manager.update_index(f"{filepath}") #for updating the inverted index
        start_cpp_process()#again starting the cpp process for the updated inverted index
        return jsonify({"status": "success", "message": "File uploaded successfully"})
    except Exception as e:
        print("Upload error:", e)
        return jsonify({"status": "error", "message": str(e)}), 500

# Initialize the C++ process when the server starts
if __name__ == '__main__':
    start_cpp_process()
    app.run(debug=True)

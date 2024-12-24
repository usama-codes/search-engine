#include<vector>
#include<string>
#include<unordered_map>
#include<sstream>
#include<fstream>

using namespace std;

class LoadLexicon {
private:
    unordered_map<string, int> wordToID; // Map to store Word -> Word ID

public:
    vector<string> split(const string& str, char delimiter) {
        vector<string> tokens;
        stringstream ss(str);
        string token;
        while (getline(ss, token, delimiter)) {
            tokens.push_back(token);
        }
        return tokens;
    }

    void loadLexicon(const string& filePath) {
        ifstream file(filePath);
        if (!file.is_open()) {
            throw runtime_error("Unable to open lexicon file: " + filePath);
        }

        string line;
        bool isHeader = true;

        while (getline(file, line)) {
            if (isHeader) {
                // Skip the header line
                isHeader = false;
                continue;
            }

            auto tokens = split(line, ',');
            if (tokens.size() < 2) {
                // Invalid row, skip
                continue;
            }

            string word = tokens[0];
            int wordID = stoi(tokens[1]);

            // Populate the map
            wordToID[word] = wordID;
        }

        file.close();
    }

    int getWordID(const string& word) const {
        auto it = wordToID.find(word);
        if (it != wordToID.end()) {
            return it->second;
        } 
        else {
            return -1;
        }
    }
};

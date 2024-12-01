#include <iostream>
#include <fstream>
#include <sstream>
#include <unordered_map>
#include <unordered_set>
#include <vector>
#include <algorithm>
using namespace std;


// Function to preprocess text: convert to lowercase and remove non-word characters
vector<string> preprocess_text(const string &text) {
    string clean_text;
    for (char ch : text) {
        if (isalnum(ch) || isspace(ch)) {
            clean_text += tolower(ch);
        } else {
            clean_text += ' ';
        }
    }

    istringstream iss(clean_text);
    vector<string> words;
    string word;
    while (iss >> word) {
        words.push_back(word);
    }
    return words;
}

void build_inverted_index(const string &data_file, const string &lexicon_file, const std::string &output_file) {
    // Load the lexicon into word-to-ID map
    unordered_map<string, string> word_to_id;
    ifstream lexicon_input(lexicon_file);
    string line, word, word_id;

    // Reading the lexicon file
    while (getline(lexicon_input, line)) {
        istringstream iss(line);
        getline(iss, word, ',');
        getline(iss, word_id, ',');
        word_to_id[word] = word_id;
    }
    lexicon_input.close();

    // Building the inverted index
unordered_map<string, unordered_set<int>> inverted_index;
    ifstream data_input(data_file);
    int doc_id = 0;

    // Reading the documents
    while (getline(data_input, line)) {
        doc_id++;
        vector<string> words = preprocess_text(line);
        for (const auto &word : words) {
            if (word_to_id.find(word) != word_to_id.end()) {
                inverted_index[word_to_id[word]].insert(doc_id);
            }
        }
    }
    data_input.close();

    // Writing the inverted index to output file
    ofstream output(output_file);
    output << "WordID,DocumentIDs\n";
    for (const auto &[word_id, doc_ids] : inverted_index) {
        output << word_id << ",";
        for (auto it = doc_ids.begin(); it != doc_ids.end(); ++it) {
            if (it != doc_ids.begin()) {
                output << " ";
            }
            output << *it;
        }
        output << "\n";
    }
    output.close();

    cout << "Inverted index stored at " << output_file << "\n";
}

int main() {
string data_csv = "data.csv";
string lexicon_csv = "lexicon.csv";
string output_csv = "inverted_index.csv";

    build_inverted_index(data_csv, lexicon_csv, output_csv);

    return 0;
}

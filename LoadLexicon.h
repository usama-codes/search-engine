#include<vector>
#include<string>
#include<unordered_map>
#include<sstream>
#include<fstream>

class LoadLexicon {
private:
    std::unordered_map<std::string, int> wordToID; // Map to store Word -> Word ID
    std::unordered_map<std::string, int> wordToID; // Map to store Word -> Word ID

public:
        // Function to split a string by a delimiter
    std::vector<std::string> split(const std::string& str, char delimiter) {
        std::vector<std::string> tokens;
        std::stringstream ss(str);
        std::string token;
        while (std::getline(ss, token, delimiter)) {
        // Function to split a string by a delimiter
    std::vector<std::string> split(const std::string& str, char delimiter) {
        std::vector<std::string> tokens;
        std::stringstream ss(str);
        std::string token;
        while (std::getline(ss, token, delimiter)) {
            tokens.push_back(token);
        }
        return tokens;
    }

    // Function to load the lexicon from a CSV file
    void loadLexicon(const std::string& filePath) {
        std::ifstream file(filePath);
    // Function to load the lexicon from a CSV file
    void loadLexicon(const std::string& filePath) {
        std::ifstream file(filePath);
        if (!file.is_open()) {
            throw std::runtime_error("Unable to open lexicon file: " + filePath);
            throw std::runtime_error("Unable to open lexicon file: " + filePath);
        }

        std::string line;
        std::string line;
        bool isHeader = true;

        while (std::getline(file, line)) {
        while (std::getline(file, line)) {
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

            std::string word = tokens[0];
            int wordID = std::stoi(tokens[1]);
            std::string word = tokens[0];
            int wordID = std::stoi(tokens[1]);

            // Populate the map
            wordToID[word] = wordID;
        }

        file.close();
    }

    // Function to check if a word exists and return its Word ID
    int getWordID(const std::string& word) const {
    // Function to check if a word exists and return its Word ID
    int getWordID(const std::string& word) const {
        auto it = wordToID.find(word);
        if (it != wordToID.end()) {
            return it->second;
        } else {
            return -1; // Return -1 if the word does not exist
        } else {
            return -1; // Return -1 if the word does not exist
        }
    }
};
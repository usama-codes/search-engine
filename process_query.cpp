#include <iostream>
#include "LoadLexicon.h"
#include "LoadBarrel.h"

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
int main() {
    // File path to the lexicon CSV
    std::string lexiconFilePath = "lexicon.csv";

    // Initialize Lexicon
    LoadLexicon lexicon;
    LoadBarrel barrel;

    try {
        // Load the lexicon
        lexicon.loadLexicon(lexiconFilePath);
        std::cout << "Lexicon loaded successfully.\n";
    } catch (const std::exception& e) {
        std::cerr << e.what() << std::endl;
        return 1;
    }

    // Query for words
    std::string word;
    std::cout << "Enter words to query their Word ID. Type 'exit' to quit.\n";
    while (true) {
        std::cout <<std::endl<< "Word: ";
        std::cin >> word;

        if (word == "exit") {
            std::cout << "Exiting.\n";
            break;
        }

        int wordID = lexicon.getWordID(word);
        if (wordID != -1) {
            std::cout << "Word ID for \"" << word << "\": " << wordID << "\n";
            barrel.calculateBarrelIndex(wordID);
            std::cout<<"Document IDs for word "<<word<<": ";
            std::vector<std::string> documentIDs = barrel.getDocumentIDs(wordID);
            for (const auto& id : documentIDs) {
                std::cout << id << " "; // Add a space or any separator if needed
            }
            std::cout << std::endl;
        } else {
            std::cout << "Word \"" << word << "\" not found in the lexicon.\n";
        }
    }

    return 0;
}
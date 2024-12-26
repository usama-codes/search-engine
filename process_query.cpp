#include <iostream>
#include <fstream>
#include <unordered_map>
#include <cmath>
#include <vector>
#include <bitset>
#include <stdexcept>
#include <algorithm>
#include <sstream>
#include "LoadBarrel.h"
#include "LoadLexicon.h"
#include "RankArticles.h"

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

// Main function
int main() {
    // File path to the lexicon CSV
    std::string lexiconFilePath = "lexicon.csv";

    // Initialize Lexicon, Barrel, and Ranker
    LoadLexicon lexicon;
    LoadBarrel barrel;
    TFIDFRanker ranker;

    try {
        // Load the lexicon
        lexicon.loadLexicon(lexiconFilePath);
        std::cout << "Lexicon loaded successfully.\n";

        // Set total number of documents (example value)
        ranker.setTotalDocs(25000);
    } 
    catch (const std::exception& e) {
        std::cerr << e.what() << std::endl;
        return 1;
    }

    // Query for words
    std::string word;
    std::cout << "Enter words to query their Word ID. Type 'exit' to quit.\n";

    while (true) {
        std::cout << "\nWord: ";
        std::cin >> word;

        if (word == "exit") {
            std::cout << "Exiting.\n";
            break;
        }

        int wordID = lexicon.getWordID(word);
        if (wordID != -1) {
            std::cout << "Word ID for \"" << word << "\": " << wordID << "\n";

            try {
                barrel.calculateBarrelIndex(wordID);

                std::vector<std::string> documentIDs = barrel.getDocumentIDs(wordID);
                std::vector<std::string> bitArrays = barrel.getBitArrays(wordID);

                if (documentIDs.size() != bitArrays.size()) {
                    throw std::runtime_error("Mismatch between document IDs and bit arrays.");
                }

                for (size_t i = 0; i < documentIDs.size(); ++i) {
                    int docID = std::stoi(documentIDs[i]);
                    int bitArray = std::stoi(bitArrays[i]);
                    ranker.processDocumentData(docID, wordID, bitArray);
                }

                std::vector<int> queryWordIDs = {wordID};

                // Rank the documents based on the query
                auto rankedResults = ranker.rank_documents(queryWordIDs);

                std::cout << "\nRanked Documents:\n";
                for (const auto& result : rankedResults) {
                    std::cout << "Doc " << result.first << ": Score = " << result.second << "\n";
                }

            } catch (const std::exception& ex) {
                std::cerr << "Error processing data: " << ex.what() << "\n";
            }

        } else {
            std::cout << "Word \"" << word << "\" not found in the lexicon.\n";
        }
    }
    return 0;
}

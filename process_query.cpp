#include <iostream>
#include <fstream>
#include <cstdint>
#include <unordered_map>
#include <cmath>
#include <vector>
#include <bitset>
#include <stdexcept>
#include <algorithm>
#include <sstream>
#include<map>
#include "LoadLexicon.h"
#include "RankArticles.h"
#include <string> // Include string header for string manipulation

// Function to split a string by a delimiter
std::vector<std::string> split(const std::string& str, char delimiter) {
    std::vector<std::string> tokens;
    std::stringstream ss(str);
    std::string token;
    while (std::getline(ss, token, delimiter)) {
std::vector<std::string> split(const std::string& str, char delimiter) {
    std::vector<std::string> tokens;
    std::stringstream ss(str);
    std::string token;
    while (std::getline(ss, token, delimiter)) {
        tokens.push_back(token);
    }
    return tokens;
}

// Function to retrieve document data from CSV
std::map<int, std::vector<std::string>> retrieveDocumentData(const std::string& data_file) {
    std::map<int, std::vector<std::string>> documentData;
    std::ifstream infile(data_file);
    std::string line;

    if (infile.is_open()) {
        std::getline(infile, line); // Skip header row
        while (std::getline(infile, line)) {
            std::vector<std::string> fields = split(line, ',');
            if (fields.size() >= 4) { // Ensure at least 4 fields (doc_id, title, url, tags)
                try {
                    int docID = std::stoi(fields[0]);
                    for(size_t i = 4; i < fields.size(); i++) {
                        fields[3] += "," + fields[i]; // Concatenate tags if multiple
                    }
                    std::vector<std::string> docInfo = {fields[1], fields[2], fields[3]};
                    documentData[docID] = docInfo;
                } catch (const std::invalid_argument& e) {
                    std::cerr << "Invalid docID in line: " << line << std::endl;
                }
            }
        }
        infile.close();
    } else {
        std::cerr << "Unable to open data file: " << data_file << std::endl;
    }

    return documentData;
}

// Main function
int main() {
    // File paths
    std::string lexiconFilePath = "lexicon.csv";
    std::string dataFilePath = "newdata.csv";

    // Initialize Lexicon, Barrel, and Ranker
    LoadLexicon lexicon;
    LoadBarrel barrel;
    TFIDFRanker ranker;

    std::map<int, std::vector<std::string>> documentData;
    try {
        // Load the lexicon
        lexicon.loadLexicon(lexiconFilePath);
        std::cout << "Lexicon loaded successfully.\n";

        // Set total number of documents (example value)
        ranker.setTotalDocs(190000);

        // Load document data from CSV
        documentData = retrieveDocumentData(dataFilePath);
        std::cout<<"Document data loaded successfully.\n";
    } catch (const std::exception& e) {
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
                    if (result.second == 0.0)
                        break;

                    std::cout << "Doc " << result.first << ": Score = " << result.second << std::endl;

                    // Retrieve and print document data
                    if (documentData.find(result.first) != documentData.end()) {
                        std::cout << "  Title: " << documentData[result.first][0] << std::endl;
                        std::cout << "  URL: " << documentData[result.first][1] << std::endl;
                        std::cout << "  Tags: " << documentData[result.first][2] << std::endl;
                    }
                }

            } catch (const std::exception& ex) {
                std::cerr << "Error processing data: " << ex.what() << std::endl;
            }

        } else {
            std::cout << "Word \"" << word << "\" not found in the lexicon.\n";
        }
    }
    return 0;
}

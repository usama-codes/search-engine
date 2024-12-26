#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include <unordered_map>
class LoadBarrel {

// Constants
const int NUM_BARRELS = 50; // Total number of barrels
const std::string BARRELS_DIR = "barrels"; // Directory containing barrel files
public:
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

// Function to calculate the barrel index for a given Word ID
int calculateBarrelIndex(int wordID) {
    return wordID % NUM_BARRELS;
}

// Function to search for a Word ID in a barrel file and retrieve the corresponding Document IDs
std::vector<std::string> getDocumentIDs(int wordID) {
    int barrelIndex = calculateBarrelIndex(wordID);
    std::string barrelFile = BARRELS_DIR + "/barrel_" + std::to_string(barrelIndex) + ".csv";
    
    std::ifstream file(barrelFile);
    if (!file.is_open()) {
        throw std::runtime_error("Unable to open barrel file: " + barrelFile);
    }

    std::string line;
    bool isHeader = true;

    std::vector<std::string> docIDs;  // Vector to store all document IDs found

    while (std::getline(file, line)) {
        auto tokens = split(line, ',');
        if (tokens.size() == 2) {
            int id = std::stoi(tokens[0]);  // Word ID is in the first column
            if (id == wordID) {
                std::string docInfo = tokens[1];

                // Split the docInfo by spaces to get individual "a:b" pairs
                auto docPairs = split(docInfo, ' ');

                // Loop over each "a:b" pair
                for (const auto& pair : docPairs) {
                    // Split each pair by colon and get the part before the colon
                    auto docToken = split(pair, ':');
                    if (!docToken.empty()) {
                        docIDs.push_back(docToken[0]);  // Add the part before the colon
                    }
                }
            }
        }
    }

    file.close();

    return docIDs;  // Return the vector containing all document IDs
}

};
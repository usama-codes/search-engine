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
std::string getDocumentIDs(int wordID) {
    int barrelIndex = calculateBarrelIndex(wordID);
    std::string barrelFile = BARRELS_DIR + "/barrel_" + std::to_string(barrelIndex) + ".csv";
    
    std::ifstream file(barrelFile);
    if (!file.is_open()) {
        throw std::runtime_error("Unable to open barrel file: " + barrelFile);
    }

    std::string line;
    bool isHeader = true;

    while (std::getline(file, line)) {
        if (isHeader) {
            isHeader = false; // Skip header line
            continue;
        }

        auto tokens = split(line, ',');
        if (tokens.size() >= 3) {
            int id = std::stoi(tokens[1]);
            if (id == wordID) {
                file.close();
                return tokens[2]; // Return Document IDs
            }
        }
    }

    file.close();
    return ""; // Return empty string if Word ID is not found
}};

#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include <unordered_map>

using namespace std;

class LoadBarrel {
private:
    const int NUM_BARRELS = 50;
    const string BARRELS_DIR = "barrels";
    
    // Cache for loaded barrels: barrel_index -> {word_id -> document_ids}
    unordered_map<int, unordered_map<int, string>> barrelCache;

    // Function to load an entire barrel into memory
    void loadBarrel(int barrelIndex) {
        string barrelFile = BARRELS_DIR + "/barrel_" + to_string(barrelIndex) + ".csv";
        ifstream file(barrelFile);
        
        if (!file.is_open()) {
            throw runtime_error("Unable to open barrel file: " + barrelFile);
        }

        string line;
        bool isHeader = true;
        unordered_map<int, string> wordMap;

        while (getline(file, line)) {
            if (isHeader) {
                isHeader = false;
                continue;
            }

            auto tokens = split(line, ',');
            if (tokens.size() >= 3) {
                int wordId = stoi(tokens[1]);
                wordMap[wordId] = tokens[2];
            }
        }

        barrelCache[barrelIndex] = move(wordMap);
        file.close();
    }

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

    int calculateBarrelIndex(int wordID) {
        return wordID % NUM_BARRELS;
    }

    string getDocumentIDs(int wordID) {
        int barrelIndex = calculateBarrelIndex(wordID);
        
        // Load barrel if not already cached
        if (barrelCache.find(barrelIndex) == barrelCache.end()) {
            loadBarrel(barrelIndex);
        }

        // Look up word in cached barrel
        auto& barrel = barrelCache[barrelIndex];
        auto it = barrel.find(wordID);
        return it != barrel.end() ? it->second : "";
    }
};
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
#include <map>
#include <string>
#include <set>
#include "json.hpp"

using json = nlohmann::json;
#include "LoadLexicon.h"
#include "RankArticles.h"
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

// Function to retrieve document data from CSV
std::map<int, std::vector<std::string>> retrieveDocumentData(const std::string& data_file) {
    std::map<int, std::vector<std::string>> documentData;
    std::ifstream infile(data_file);
    std::string line;

    if (infile.is_open()) {
        std::getline(infile, line); // Skip header row
        while (std::getline(infile, line)) {
            std::vector<std::string> fields = split(line, ',');
            if (fields.size() >= 4) {
                try {
                    int docID = std::stoi(fields[0]);
                    for (size_t i = 4; i < fields.size(); i++) {
                        fields[3] += "," + fields[i]; // Concatenate tags if multiple
                    }
                    std::vector<std::string> docInfo = {fields[1], fields[2], fields[3]};
                    documentData[docID] = docInfo;
                } catch (const std::invalid_argument& e) {
                }
            }
        }
        infile.close();
    } else {
        std::cerr << "Unable to open data file: " << data_file << std::endl;
    }

    return documentData;
}

// Function to handle single and multiple word queries
void handleQuery(const std::string& query, LoadLexicon& lexicon, LoadBarrel& barrel, TFIDFRanker& ranker, const std::map<int, std::vector<std::string>>& documentData, std::stringstream& response) {
    std::vector<std::string> words = split(query, ' ');
    json output;
    output["query"] = query;

    if (words.empty()) {
        output["status"] = "error";
        output["message"] = "Empty query received.";
        response << output.dump();
        return;
    }

    std::vector<int> queryWordIDs;
    std::set<int> intersectingDocs;
    bool firstWord = true;

    for (const auto& word : words) {
        int wordID = lexicon.getWordID(word);
        if (wordID != -1) {
            queryWordIDs.push_back(wordID);
            std::vector<std::string> documentIDs = barrel.getDocumentIDs(wordID);
            std::vector<std::string> bitArrays = barrel.getBitArrays(wordID);

            if (documentIDs.size() != bitArrays.size()) {
                output["status"] = "error";
                output["message"] = "Mismatch between document IDs and bit arrays.";
                response << output.dump();
                return;
            }

            std::set<int> docs;
            for (size_t i = 0; i < documentIDs.size(); ++i) {
                int docID = std::stoi(documentIDs[i]);
                int bitArray = std::stoi(bitArrays[i]);
                ranker.processDocumentData(docID, wordID, bitArray);
                docs.insert(docID);
            }

            if (firstWord) {
                intersectingDocs = docs;
                firstWord = false;
            } else {
                std::set<int> temp;
                std::set_intersection(intersectingDocs.begin(), intersectingDocs.end(),
                                      docs.begin(), docs.end(),
                                      std::inserter(temp, temp.begin()));
                intersectingDocs = temp;
            }
        }
    }

    if (queryWordIDs.empty()) {
        output["status"] = "error";
        output["message"] = "No valid words found in the lexicon.";
        response << output.dump();
        return;
    }

    auto rankedResults = ranker.rank_documents(queryWordIDs);
    output["status"] = "success";
    output["results"] = json::array();

    int docsToFetch = 100;
    for (const auto& result : rankedResults) {
        if (docsToFetch-- == 0)
            break;

        if (intersectingDocs.find(result.first) == intersectingDocs.end() || result.second == 0.0)
            continue;

        json doc;
        doc["doc_id"] = result.first;
        doc["score"] = result.second;

        if (documentData.find(result.first) != documentData.end()) {
            doc["title"] = documentData.at(result.first)[0];
            doc["url"] = documentData.at(result.first)[1];
            doc["tags"] = documentData.at(result.first)[2];
        }

        output["results"].push_back(doc);
    }

    response << output.dump();
}

// Main function that listens for queries
int main() {
    std::string lexiconFilePath = "D:\\NUST\\SEMESTER_3\\DSA\\End_Project\\test\\engine_data\\lexicon.csv";
    std::string dataFilePath = "D:\\NUST\\SEMESTER_3\\DSA\\End_Project\\test\\engine_data\\newdata.csv";

    LoadLexicon lexicon;
    LoadBarrel barrel;
    TFIDFRanker ranker;

    try {
        lexicon.loadLexicon(lexiconFilePath);
        ranker.setTotalDocs(190000);

        std::map<int, std::vector<std::string>> documentData = retrieveDocumentData(dataFilePath);

        std::string query;
        while (std::getline(std::cin, query)) {
            std::stringstream response;
            handleQuery(query, lexicon, barrel, ranker, documentData, response);
            std::cout << response.str() << std::endl;
        }
    } catch (const std::exception& e) {
        json error;
        error["status"] = "error";
        error["message"] = e.what();
        std::cerr << error.dump() << std::endl;
        return 1;
    }

    return 0;
}

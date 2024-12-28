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

// Function to Split a string by a delimiter
std::vector<std::string> Split(const std::string& str, char delimiter) {
    std::vector<std::string> tokens;
    std::stringstream ss(str);
    std::string token;
    while (std::getline(ss, token, delimiter)) {
        tokens.push_back(token);
    }
    return tokens;
}

// Class to store document data (like in the first code)
class TFIDFRanker {
private:
    struct Document {
        int doc_id;
        std::unordered_map<int, uint8_t> term_freqs;
        std::unordered_map<int, bool> term_in_title;
        std::unordered_map<int, bool> term_in_tag;
    };

    std::unordered_map<int, Document> documents;  // To store doc data (doc_id => Document)
    int total_docs;

public:
    TFIDFRanker() : total_docs(0) {}

    // Method to process the bit array and extract title, tag, and frequency
    void processDocumentData(int doc_id, int word_id, int bit_array) {
        std::bitset<10> binary_rep(bit_array); // 10 bits: 1 for title, 1 for tag, 8 for frequency

        bool in_title = binary_rep[9];  // 1st bit is for title
        bool in_tag = binary_rep[8];    // 2nd bit is for tag
        uint8_t frequency = binary_rep.to_ulong() & 0xFF;  // Extract frequency from the lower 8 bits

        if (frequency < 0) {
            throw std::invalid_argument("Frequency cannot be negative.");
        }

        // If the document does not exist, create it
        if (documents.find(doc_id) == documents.end()) {
            documents[doc_id] = Document{doc_id};
        }

        Document& doc = documents[doc_id];
        doc.term_freqs[word_id] = frequency;
        doc.term_in_title[word_id] = in_title;
        doc.term_in_tag[word_id] = in_tag;
    }

    // Method to calculate term frequency with weightage for title/tag
    double calculate_tf(uint8_t frequency, bool in_title, bool in_tag) {
        double base_tf = frequency > 0 ? 1 + std::log10(frequency) : 0;

        if (in_title) {
            base_tf *= 1.5;  // Increased weight if in title
        } else if (in_tag) {
            base_tf *= 1.2;  // Increased weight if in tag
        }

        return base_tf;
    }

    // Method to calculate IDF (for simplicity, it's based on document count here)
    double calculate_idf(int doc_frequency) {
        return std::log10(total_docs / static_cast<double>(doc_frequency));
    }

    // Method to rank documents based on multiple query word IDs
    std::vector<std::pair<int, double>> rank_documents(const std::vector<int>& query_word_ids) {
        // Maps to store documents for each query term
        std::unordered_map<int, std::vector<std::pair<int, double>>> term_doc_map;

        // Fetch documents for each query term
        for (int word_id : query_word_ids) {
            for (const auto& doc_pair : documents) {
                int doc_id = doc_pair.first;
                const Document& doc = doc_pair.second;

                if (doc.term_freqs.find(word_id) != doc.term_freqs.end()) {
                    double tf = calculate_tf(doc.term_freqs.at(word_id), doc.term_in_title.at(word_id), doc.term_in_tag.at(word_id));
                    double idf = calculate_idf(1);  // Example, using a static value for now

                    double score = tf * idf;
                    term_doc_map[word_id].push_back({doc_id, score});
                }
            }
        }

        // Find intersection of documents for all query terms
        std::unordered_map<int, double> doc_scores;
        std::unordered_map<int, int> doc_term_count;

        // Accumulate the scores for documents that appear in all query terms
        for (const auto& term_docs : term_doc_map) {
            for (const auto& doc : term_docs.second) {
                int doc_id = doc.first;
                double score = doc.second;

                if (doc_scores.find(doc_id) == doc_scores.end()) {
                    doc_scores[doc_id] = score;
                    doc_term_count[doc_id] = 1;
                } else {
                    doc_scores[doc_id] += score;
                    doc_term_count[doc_id]++;
                }
            }
        }

        // Filter out documents that don't contain all query words
        std::vector<std::pair<int, double>> final_scores;
        for (const auto& doc_score : doc_scores) {
            int doc_id = doc_score.first;
            double score = doc_score.second;

            // Check if the document contains all query terms
            if (doc_term_count[doc_id] == query_word_ids.size()) {
                // Boost the score if the document contains all query terms
                score *= 1.5;  // Boost by 1.5x for documents containing all query terms
                final_scores.push_back({doc_id, score});
            }
        }

        // Now, we add documents that contain some but not all of the query words
        for (const auto& doc_score : doc_scores) {
            int doc_id = doc_score.first;
            double score = doc_score.second;

            if (doc_term_count[doc_id] < query_word_ids.size()) {
                final_scores.push_back({doc_id, score});
            }
        }

        // Sort the final scores in descending order
        std::sort(final_scores.begin(), final_scores.end(), [](const auto& a, const auto& b) {
            return a.second > b.second;
        });

        return final_scores;
    }

    // Set the total document count
    void setTotalDocs(int total) {
        total_docs = total;
    }

    // Load document data from CSV file
    void loadDocumentData(const std::string& dataFilePath, std::map<int, std::vector<std::string>>& documentData) {
        std::ifstream infile(dataFilePath);
        std::string line;

        if (infile.is_open()) {
            std::getline(infile, line); // Skip header row
            while (std::getline(infile, line)) {
                std::vector<std::string> fields = Split(line, ',');
                if (fields.size() >= 4) { // Ensure at least 4 fields (doc_id, title, url, tags)
                    try {
                        int docID = std::stoi(fields[0]);
                        for(size_t i = 4; i < fields.size(); i++) {
                            fields[3] += "," + fields[i]; // Concatenate tags if multiple
                        }
                        std::vector<std::string> docInfo = {fields[1], fields[2], fields[3]};
                        documentData[docID] = docInfo;

                        // For simplicity, we'll just simulate a word frequency and bit array here
                        // In real use, you would extract the word frequencies and bit arrays from your data
                        int wordID = 1;  // Simulate a word ID (In reality, you'd map these from your lexicon)
                        int bitArray = 0b1000000001; // Simulated bit array (1st bit for title, last 8 bits for frequency)

                        // Process the document data
                        processDocumentData(docID, wordID, bitArray);

                    } catch (const std::invalid_argument& e) {
                        std::cerr << "Invalid docID in line: " << line << std::endl;
                    }
                }
            }
            infile.close();
        } else {
            std::cerr << "Unable to open data file: " << dataFilePath << std::endl;
        }
    }

    // Display ranked documents
    void displayRankedDocuments(const std::vector<std::pair<int, double>>& rankedResults, const std::map<int, std::vector<std::string>>& documentData) {
        std::cout << "\nRanked Documents:\n";
        for (const auto& result : rankedResults) {
            if (result.second == 0.0)
                break;

            std::cout << "Doc " << result.first << ": Score = " << result.second << std::endl;

            // Retrieve and print document data
            if (documentData.find(result.first) != documentData.end()) {
                std::cout << "  Title: " << documentData.at(result.first)[0] << std::endl;
                std::cout << "  URL: " << documentData.at(result.first)[1] << std::endl;
                std::cout << "  Tags: " << documentData.at(result.first)[2] << std::endl;
            }
        }
    }
};

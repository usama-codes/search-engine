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

    // Method to rank documents based on query word IDs
    std::vector<std::pair<int, double>> rank_documents(const std::vector<int>& query_word_ids) {
        std::vector<std::pair<int, double>> scores;

        for (const auto& doc_pair : documents) {
            int doc_id = doc_pair.first;
            const Document& doc = doc_pair.second;

            double doc_score = 0.0;

            for (int word_id : query_word_ids) {
                if (doc.term_freqs.find(word_id) != doc.term_freqs.end()) {
                    double tf = calculate_tf(doc.term_freqs.at(word_id), doc.term_in_title.at(word_id), doc.term_in_tag.at(word_id));
                    // IDF is not calculated here as we have no global word frequency data
                    double idf = calculate_idf(1);  // Example, using a static value for now

                    doc_score += tf * idf;
                }
            }

            scores.push_back({doc_id, doc_score});
        }

        std::sort(scores.begin(), scores.end(), [](const auto& a, const auto& b) {
            return a.second > b.second;
        });

        return scores;
    }

    // Set the total document count
    void setTotalDocs(int total) {
        total_docs = total;
    }
};
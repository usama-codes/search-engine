#include <iostream>
#include <unordered_map>
#include <vector>
#include <string>
#include <cmath>
#include <fstream>
#include <sstream>
#include <algorithm>
#include <stdexcept>

class TFIDFRanker {
private:
    struct Document {
        int doc_id;
        std::unordered_map<int, uint8_t> term_freqs; // word_id -> frequency
        std::unordered_map<int, double> tfidf_weights; // word_id -> tf-idf score
    };

    std::vector<Document> documents;
    std::unordered_map<int, int> doc_frequencies; // word_id -> document count
    std::unordered_map<int, double> idf_cache; // Cache for precomputed IDF values
    int total_docs = 0;

    // Get raw frequency from bit array
    uint8_t get_frequency(uint32_t bit_array) {
        return bit_array & 0xFF;
    }

    // Calculate TF score
    double calculate_tf(uint8_t frequency) {
        return frequency > 0 ? 1 + std::log10(frequency) : 0;
    }

    // Precompute IDF scores for all terms
    void precompute_idf() {
        for (const auto& entry : doc_frequencies) {
            int word_id = entry.first;
            int df = entry.second;
            idf_cache[word_id] = df > 0 ? std::log10(static_cast<double>(total_docs) / df) : 0;
        }
    }

public:
    void initialize(const std::string& forward_index_path, const std::string& inverted_index_path) {
        // Load forward index
        std::ifstream fwd_file(forward_index_path);
        if (!fwd_file.is_open()) {
            throw std::runtime_error("Failed to open forward index file");
        }

        std::string line;
        std::getline(fwd_file, line); // Skip header

        while (std::getline(fwd_file, line)) {
            Document doc;
            std::stringstream ss(line);
            std::string field;
            
            std::getline(ss, field, ',');
            doc.doc_id = std::stoi(field);

            while (std::getline(ss, field, ',')) {
                size_t colon = field.find(':');
                if (colon != std::string::npos) {
                    int word_id = std::stoi(field.substr(0, colon));
                    uint32_t bit_array = std::stoul(field.substr(colon + 1));
                    doc.term_freqs[word_id] = get_frequency(bit_array);
                }
            }
            documents.push_back(doc);
        }
        total_docs = documents.size();

        // Load document frequencies
        std::ifstream inv_file(inverted_index_path);
        if (!inv_file.is_open()) {
            throw std::runtime_error("Failed to open inverted index file");
        }

        std::getline(inv_file, line); // Skip header

        while (std::getline(inv_file, line)) {
            std::stringstream ss(line);
            std::string field;
            
            std::getline(ss, field, ','); // Skip type
            std::getline(ss, field, ','); // Word ID
            int word_id = std::stoi(field);
            
            std::getline(ss, field, ','); // Doc IDs
            std::stringstream doc_stream(field);
            std::string doc_id;
            int count = 0;
            while (std::getline(doc_stream, doc_id, ' ')) count++;
            doc_frequencies[word_id] = count;
        }

        // Precompute IDF values
        precompute_idf();

        // Compute TF-IDF weights
        for (auto& doc : documents) {
            for (const auto& term_freq : doc.term_freqs) {
                int word_id = term_freq.first;
                uint8_t freq = term_freq.second;
                if (idf_cache.find(word_id) != idf_cache.end()) {
                    doc.tfidf_weights[word_id] = calculate_tf(freq) * idf_cache[word_id];
                }
            }
        }
    }

    std::vector<std::pair<int, double>> rank_documents(const std::vector<int>& query_word_ids) {
        if (query_word_ids.empty()) return {};

        std::vector<std::pair<int, double>> scores;

        for (const auto& doc : documents) {
            double score = 0.0;
            double doc_norm = 0.0;
            double query_norm = std::sqrt(query_word_ids.size()); // Query terms weighted as 1.0

            for (int word_id : query_word_ids) {
                auto it = doc.tfidf_weights.find(word_id);
                if (it != doc.tfidf_weights.end()) {
                    score += it->second; // Dot product
                    doc_norm += it->second * it->second;
                }
            }

            doc_norm = std::sqrt(doc_norm);
            if (doc_norm > 0) {
                score /= (query_norm * doc_norm); // Cosine similarity
                scores.emplace_back(doc.doc_id, score);
            }
        }

        std::sort(scores.begin(), scores.end(),
                 [](const auto& a, const auto& b) { return a.second > b.second; });

        return scores;
    }
};

int main() {
    try {
        TFIDFRanker ranker;
        ranker.initialize("forward.csv", "inverted_index.csv");
        
        std::vector<int> query_word_ids = {1, 2, 3}; // Example word IDs
        auto results = ranker.rank_documents(query_word_ids);
        
        for (const auto& result : results) {
            std::cout << "Doc " << result.first << ": " << result.second << "\n";
        }
    } catch (const std::exception& ex) {
        std::cerr << "Error: " << ex.what() << "\n";
        return 1;
    }

    return 0;
}

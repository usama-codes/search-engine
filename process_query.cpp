#include <iostream>
#include "LoadLexicon.h"
#include "LoadBarrel.h"

using namespace std;

// Function to split a string by a delimiter
vector<string> split(const string& str, char delimiter) {
    vector<string> tokens;
    stringstream ss(str);
    string token;
    while (getline(ss, token, delimiter)) {
        tokens.push_back(token);
    }
    return tokens;
}


int main() {
    string lexiconFilePath = "lexicon.csv";

    LoadLexicon lexicon;
    LoadBarrel barrel;

    try {
        lexicon.loadLexicon(lexiconFilePath);
        cout << "Lexicon loaded successfully.\n";
    } 
    catch (const exception& e) {
        cerr << e.what() << endl;
        return 1;
    }

    // Query for words
    string word;
    cout << "Enter words to query their Word ID. Type 'exit' to quit.\n";
    while (true) {
        cout << endl << "Word: ";
        cin >> word;

        if (word == "exit") {
            cout << "Exiting.\n";
            break;
        }

        int wordID = lexicon.getWordID(word);
        if (wordID != -1) {
            cout << "Word ID for \"" << word << "\": " << wordID << "\n";
            barrel.calculateBarrelIndex(wordID);
            cout<<"Document IDs for word "<<word<<": ";
            cout<<barrel.getDocumentIDs(wordID);
        } else {
            cout << "Word \"" << word << "\" not found in the lexicon.\n";
        }
    }

    return 0;
}

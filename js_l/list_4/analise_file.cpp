#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include "spdlog/spdlog.h"
using namespace std;    

string get_file_name();
int run(string file_name);
int read_from_file(string* file_name);
int count_signs(vector <string>* lines);
int count_words(vector <string>* lines);

int main(int argc, char* argv[]) {
    if (argc == 1) {
        return 1;
    }
    else{
        return run(argv[1]);
    }
}

int run(string file_name) {
    if(file_name == "" || file_name == " ") {        
        return 1;
    }    
    return read_from_file(&file_name);
}

int read_from_file(string* file_name) {
    
    ifstream file(*file_name);
    if (!file.is_open()) {
        return 1;
    }
    vector <string> lines;
    while (file) {
        string line;
        getline(file, line);
        lines.push_back(line);
    }
    file.close();

    cout << 1 << "," << *file_name<<"\n"; 
    cout << 2 << "," << count_signs(&lines)<<"\n";    
    cout << 3 << "," << count_words(&lines)<<"\n";
    cout << 4 << "," << lines.size()-1<<"\n";
    // cout << 5 << "," << lines.size()<<"\n";
    // cout << 6 << "," << lines.size()<<"\n";
    return 0;
}

string get_file_name() {
    string input;
    getline(cin, input);
    return input;
}

int count_signs(vector <string>* lines) {
    int count = 0;
    for (int i = 0; i < lines->size(); i++) {
        count += lines->at(i).size();
    }
    return count;
}

int count_words(vector <string>* lines){
    int count = 0;
    for (int i = 0; i < lines->size(); i++) {
        bool is_word = false;
        for (int j = 0; j < lines->at(i).size(); j++) {
            if (lines->at(i)[j] == ' ' || lines->at(i)[j] == '\n'){
                if(is_word){
                    count++;
                    is_word = false;
                }
            }else{
                is_word = true;
            }
        }
    }
    return count;
}
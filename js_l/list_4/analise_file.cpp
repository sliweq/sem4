#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include "spdlog/spdlog.h"
using namespace std;    

string get_file_name();
void run(string file_name);
void read_from_file(string* file_name);
int count_signs(vector <string>* lines);
int count_words(vector <string>* lines);

int main(int argc, char* argv[]) {
    if (argc == 1) {
        spdlog::error("This program doesn't take any arguments.");
        return 0;
    }
    else{
        run(argv[1]);
    }
    return 0;
}

void run(string file_name) {
    if(file_name == "" || file_name == " ") {        
        spdlog::error("File name is empty.");
        return;
    }    
    read_from_file(&file_name);
}

void read_from_file(string* file_name) {
    
    ifstream file(*file_name);
    if (!file.is_open()) {
        spdlog::error("Can't open file or file not exist.");
        return;
    }
    vector <string> lines;
    while (file) {
        string line;
        getline(file, line);
        lines.push_back(line);
    }
    file.close();

    int signs = count_signs(&lines);
    spdlog::info("Signs in file: {}", signs);
    int words = count_words(&lines);
    spdlog::info("Words in file: {}", words);
    spdlog::info("Lines in file: {}", lines.size()-1);    
    cout << "xddd";
    cout << "xddd1";
    cout << "xddd2";

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
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
string find_most_freq_word(vector <string>* lines);
string find_most_freq_sign(vector <string>* lines);

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
    cout << 5 << "," << find_most_freq_sign(&lines) <<"\n";
    cout << 6 << "," << find_most_freq_word(&lines) <<"\n";
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

string find_most_freq_word(vector <string>* lines){
    string all_file = "";
    for (int i = 0; i < lines->size(); i++) {
        all_file += lines->at(i);
        all_file += " ";
    }
    vector<string> words;
    for (int i = 0; i < all_file.size(); i++) {
        string word = "";
        while (all_file[i] != ' ' && all_file[i] != '\n'){
            word += all_file[i];
            i++;
        }
        words.push_back(word);
    }

    string most_freq_word = "";
    int most_freq_word_count = 0;
    for (int i = 0; i < words.size(); i++) {
        if (words[i] != most_freq_word){
            int tmp = 0;
            for (int j = 0; j < words.size(); j++) {
                if (words[i] == words[j]){
                    tmp++;
                }
            }   
            if(tmp > most_freq_word_count){
                most_freq_word = words[i];
                most_freq_word_count = tmp;
            }
        }
    }
        
    
    return most_freq_word;
}

string find_most_freq_sign(vector <string>* lines){
    string all_file = "";
    for (int i = 0; i < lines->size(); i++) {
        all_file += lines->at(i);
    }

    string most_freq_sign = "";
    int most_freq_sign_count = 0;
    for (int i = 0; i < all_file.size(); i++) {
        if (all_file[i] != most_freq_sign[0]){
                int tmp = 0;
                for (int j = 0; j < all_file.size(); j++) {
                    if (all_file[i] == all_file[j]){
                        tmp++;
                    }
                }   
                if(tmp > most_freq_sign_count){
                    most_freq_sign = all_file[i];
                    most_freq_sign_count = tmp;
                }
            }
    }
    return most_freq_sign;
}
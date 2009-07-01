#pragma once

using namespace std;
#include <vector>
#include<string>

#include "words.h"
class Cword_list
{
public:
	Cword_list(void) :file_name(""),number_of_word(0)
	{
		word_list.clear();
		iter = word_list.begin();
	};
	Cword_list(const string &filepath) :file_name(filepath),number_of_word(0)
	{
		word_list.clear();
		iter = word_list.begin();
	};
	~Cword_list(void);
	
	int load_file(const string &filename);
	string show_word();
	string show_first_word();
	int move_next();
	void sort();

	vector<CWord> word_list;
	string file_name;
	int number_of_word;
	
private:
	vector<CWord>::iterator iter;
};

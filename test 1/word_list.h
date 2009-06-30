#pragma once

using namespace std;
#include <vector>
#include<string>

#include "words.h"
class word_list
{
public:
	word_list(void) :filename(""),word_number(0)
	{
		wdlist.clear();
		iter = wdlist.begin();
	};
	word_list(const string &filepath) :filename(filepath),word_number(0)
	{
		wdlist.clear();
		iter = wdlist.begin();
	};
	~word_list(void);
	
	int load_file(const string &filename);
	string show_word();
	string show_first_word();
	int move_next();


	vector<words> wdlist;
	string filename;
	int word_number;
private:
	vector<words>::iterator iter;
};

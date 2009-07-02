#pragma once

#ifndef CWORD_LIST_H_
#define CWORD_LIST_H_

using namespace std;
#include <vector>
#include<string>
#include<algorithm>

#include "words.h"

enum KEY {BYSTR,BYNUM,BYSTRR,BYNUMR};
typedef void (*Linefunc)(const string& line);

class GT
{
public:
	GT(KEY skey):key(skey){};
	bool operator()(const CWord& lhs, const CWord& rhs) const
	{
		switch(key)
		{
		case BYSTR:
			return lhs.word < rhs.word;
			break;

		case BYNUM:
			return lhs.repeat_times < rhs.repeat_times;
			break;

		case BYSTRR:
			return lhs.word > rhs.word;
			break;

		case BYNUMR:
			return lhs.repeat_times > rhs.repeat_times;
			break;

		default:
			return false;
		}
	}

	KEY key;
};

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

	int load_word_file(const string &filename);
	int load_history_file(const string &filename);
	int save_to_file(const string &desfile);

	string show_word();
	string show_first_word();
	int move_next();
	void sort_list();

	vector<CWord> word_list;
	string file_name;
	int number_of_word;
	CWord& get_word();

	void sort_mlist(KEY key)
	{
		sort(word_list.begin(), word_list.end(), GT(key));
	};
private:
	vector<CWord>::iterator iter;
	void parse_line_history(const string& line);
	void parse_line_new(const string& line);
	int load_file_func(const string& filename, Func func);
};

#endif /* CWORD_LIST_H_ */


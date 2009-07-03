#pragma once

#ifndef CWORD_LIST_H_
#define CWORD_LIST_H_

using namespace std;
#include <vector>
#include<string>
#include<algorithm>

#include "words.h"

enum KEY {BYSTR,BYNUM,BYSTRR,BYNUMR};

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
	Cword_list()
	{
		word_list.clear();
	}
	typedef void (Cword_list::*Linefunc)(const string& line);

	int init_from_file(const string& file_name);
	int load_word_file(const string& file_name);
	int save_to_file(const string &desfile);

	int add_word(CWord &word);
	int del_word(CWord &word);
	int get_repeat_times(CWord &word);
	vector<CWord>::iterator& find_word(CWord &word);
	/*vector<CWord>::iterator& begin();
	vector<CWord>::iterator& end();*/
	void sort_list(KEY key)
	{
		sort(word_list.begin(), word_list.end(), GT(key));
	};
	size_t get_word_num()
	{
		return word_list.size();
	};
	CWord& get_word_at(int pos)
	{
		return word_list[pos];
	};
	

private:	
	vector<CWord> word_list;
	vector<CWord>::iterator pos;
	void parse_line_history(const string& line);
	void parse_line_new(const string& line);
	int load_file_func(const string& filename, Linefunc func);
};


#endif /* CWORD_LIST_H_ */


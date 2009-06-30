/*
 * help.h
 *
 *  Created on: 2009-6-18
 *      Author: Robin
 */

#ifndef HELP_H_
#define HELP_H_

#include<iostream>
#include<vector>
#include<map>
#include<string>
#include<fstream>
#include<sstream>
#include<algorithm>
#include<cctype>
#include<set>

using namespace std;

#define KNOWN_FILE 		"src/data/known.txt"
#define UNKNOWN_FILE	"src/data/unknown.txt"
#define FAMILIAR_FILE	"src/data/familiar.txt"
#define NONEED_FILE 	"src/data/noneed.txt"

typedef map<string, int> MAP;
typedef set<string> SETS;



enum STATUS{NONEED = 1,KNOWN, FAMILIAR, UNKNOWN,};



class compare
{
public:
	bool operator()(const int s, const int e) const
	{
		return s > e;
	}
};
typedef multimap<int, string, compare> MMAP;


bool is_word(const string &word);

string& format_word(string& word);

bool del_suffix(string& word, const string& suffix, string& suffixed);

void print_list(MAP & word_list);

string& process_word(string& word);

int load_raw_file(const string &file_name, MAP &word_list);

int load_stored_file(const string &file_name, MAP &word_list);

int update_data_to_file(const string &file_name, MAP &word_list);

int repeat_times(const string& word, MAP word_list);

void print_sufix(int count);

void remove_intersection(MAP &base_list, MAP &op_list);

void remove_word_from_list(const string &word, MAP & word_list);

string& process_suffix(string& word);

int find_word_in_all_list(const string &word);

void clear_all_times(void);

void remove_duplicated_word(MAP &word_list);

void remove_duplicated_word_all(void);

bool is_suffixed(const string &word);
#endif /* HELP_H_ */

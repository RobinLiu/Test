/*
 * Cword_list.h
 *
 *  Created on: Jul 1, 2009
 *      Author: reliu
 */

#ifndef CWORD_LIST_H_
#define CWORD_LIST_H_

using namespace std;
#include <vector>
#include<string>
#include<algorithm>

#include "CWord.h"

bool ccompare(const CWord& lhs, const CWord& rhs);
bool bcompare(const CWord& lhs, const CWord& rhs);
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
	void sort_list();

	vector<CWord> word_list;
	string file_name;
	int number_of_word;
	CWord& get_word();

	void sort_mlist()
	{
		sort(word_list.begin(), word_list.end(), bcompare);
	};
private:
	vector<CWord>::iterator iter;
};

#endif /* CWORD_LIST_H_ */

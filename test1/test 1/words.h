#pragma once

/*
 * CWord.h
 *
 *  Created on: Jul 1, 2009
 *      Author: reliu
 */

#ifndef CWORD_H_
#define CWORD_H_

using namespace std;

#include <string>

class CWord
{
public:
	CWord(void): repeat_times(1), word(""), line_no(0), word_type(0)
	{};
	CWord(const string &wd): repeat_times(1), word(wd), line_no(0), word_type(0)
	{};
	CWord(const string &wd, int times): repeat_times(times), word(wd), line_no(0), word_type(0)
	{};
	virtual ~CWord(void){};

	long repeat_times;
	string word;
	long line_no;
	int word_type;
};

#endif /* CWORD_H_ */


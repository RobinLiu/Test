/*
 * Cword_list.cpp
 *
 *  Created on: Jul 1, 2009
 *      Author: reliu
 */

#include<iostream>
#include<vector>
#include<map>
#include<string>
#include<fstream>
#include<sstream>
#include<algorithm>
#include<cctype>
#include<set>

#include "Cword_list.h"
#include "CWord.h"

bool ccompare(const CWord& lhs, const CWord& rhs)
{
	return lhs.repeat_times>rhs.repeat_times;
}

bool bcompare(const CWord& lhs, const CWord& rhs)
{
	return lhs.word>rhs.word;
}

Cword_list::~Cword_list()
{

}

CWord& Cword_list::get_word()
{

	return (*iter++);

}


int Cword_list::load_file(const string &filepath)
{
	file_name = filepath;

	fstream infile(file_name.c_str());
	if(!infile)
	{
		cout<<"Open file "<<file_name<<" failed"<<endl;
		return -1;
	}
	string line;
	string word;

	while(!infile.eof())
	{
		getline(infile, line);
		istringstream stream1(line);
		while(stream1>>word)
		{
			CWord wd(word);
			word_list.push_back(word);
		}

	}
	number_of_word = word_list.size();
	iter = word_list.begin();
	infile.close();
	return 0;
}

string Cword_list::show_first_word()
{
	if(word_list.size())
	{
		return word_list.front().word;
	}
	else
		return string("");
}

string Cword_list::show_word()
{

	if(iter != word_list.end())
	{
		return (*iter).word;
	}
	else
		return string("");
	return 0;
}

int Cword_list::move_next()
{
	if(iter != word_list.end())
	{
			++iter;
			return 0;
	}
	else
	{
		return -1;
	}
}

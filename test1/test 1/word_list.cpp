#include "StdAfx.h"
#include "word_list.h"
#include "words.h"

#include<iostream>
#include<vector>
#include<map>
#include<string>
#include<fstream>
#include<sstream>
#include<algorithm>
#include<cctype>
#include<set>

word_list::~word_list(void)
{
}

int word_list::load_file(const string &filepath)
{
	filename = filepath;

	fstream infile(filename.c_str());
	if(!infile)
	{
		cout<<"Open file "<<filename<<" failed"<<endl;
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
			words wd(word);
			wdlist.push_back(word);
		}
	
	}
	word_number = wdlist.size();
	iter = wdlist.begin();
	infile.close();
	return 0;
}

string word_list::show_first_word()
{
	if(wdlist.size())
	{
		return wdlist.front().word;
	}
	else
		return string("");
}

string word_list::show_word()
{

	if(iter != wdlist.end())
	{
		return (*iter).word;
	}
	else
		return string("");
	return 0;
}

int word_list::move_next()
{
	if(iter != wdlist.end())
	{
			++iter;
			return 0;
	}
	else
	{
		return -1;
	}

}
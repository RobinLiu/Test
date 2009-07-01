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

#include "word_list.h"
#include "Words.h"


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
	
	word_list.clear();
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
int Cword_list::save_to_file(const string &desfile)
{
	ofstream outfile(desfile.c_str(), ofstream::out);
	if(!outfile)
	{
		cout<<"Open file "<<desfile<<" error!"<<endl;
		return -1;
	}

	for(vector<CWord>::iterator iter = word_list.begin(); 
		iter != word_list.end(); ++iter)
	{

		ostringstream line;
		string spaces((30 - iter->word.length()),' ');
		line<<iter->word<<spaces<<iter->repeat_times;
		outfile<<line.str()<<endl;
	}

	outfile.close();
	return 0;
}

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



void Cword_list::parse_line_history(const string& line)
{
	string word;
	int times;
	istringstream stream1(line);
	if(stream1>>word>>times)
	{
		CWord wd(word,times);
		word_list.push_back(wd);
	}
}

void Cword_list::parse_line_new(const string& line)
{
	string word;
	istringstream stream1(line);
	while(stream1>>word)
	{
		CWord wd(word);
		word_list.push_back(wd);
	}
}


int Cword_list::load_file_func(const string& filename, Linefunc func)
{
	fstream infile(filename.c_str());
	if(!infile)
	{
		cout<<"Open file "<<filename<<" failed"<<endl;
		return -1;
	}
	string line;
	string word;
	int times = 0;
	
	word_list.clear();
	while(!infile.eof())
	{
		getline(infile, line);
		(this->*func)(line);
	}

	infile.close();
	return 0;

}

int Cword_list::load_word_file(const string &filepath)
{
	return load_file_func(filepath, &Cword_list::parse_line_new);
}

int Cword_list::init_from_file(const string &hisfile)
{
	return load_file_func(hisfile, &Cword_list::parse_line_history);
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


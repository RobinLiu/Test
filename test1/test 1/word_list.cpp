#ifndef __TEST__
#include "StdAfx.h"
#endif
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
#include "words.h"



void Cword_list::parse_line_history(const string& line)
{
	string word;
	int times;
	istringstream stream1(line);
	if(stream1>>word>>times)
	{
		//cout<<"word: "<<word<<" times: "<<times<<endl;
		CWord wd(word,times);
		add_word(wd);
	}
}

void Cword_list::parse_line_new(const string& line)
{
	string word;
	istringstream stream1(line);
	while(stream1>>word)
	{
		//cout<<"word: "<<word<<" loaded"<<endl;
		CWord wd(word);
		add_word(wd);
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

int Cword_list::add_word(CWord &word)
{
	if(get_repeat_times(word))
	{
		pos->repeat_times += word.repeat_times;
	}
	else
	{
		word_list.push_back(word);
	}

	return 0;
}

int Cword_list::del_word(CWord &word)
{
	if(get_repeat_times(word))
	{
		word_list.erase(pos);
	}

	return 0;
}


int Cword_list::get_repeat_times(CWord &word)
{
	pos = find(word_list.begin(),word_list.end(),word);
	if(pos != word_list.end())
	{
		return pos->repeat_times;
	}
	return 0;
}

vector<CWord>::iterator& Cword_list::find_word(CWord &word)
{
	pos = find(word_list.begin(),word_list.end(),word);
	return pos;
}

vector<CWord>::iterator& Cword_list::begin()
{
	iterbegin = word_list.begin();
	return iterbegin;
}

vector<CWord>::iterator& Cword_list::end()
{
	iterend = word_list.end();
	return iterend;
}

/*
 * help.cpp
 *
 *  Created on: 2009-6-18
 *      Author: Robin
 */
#include "help.h"


MAP known_list;
MAP familiar_list;
MAP unknown_list;
MAP noneed_list;
MAP new_list;
SETS abbre_list;
vector<string> passage;

const char* suffix_list[] = {"ed","ing","es","s"};

bool is_alpha(char ch)
{
	if(ch >= 'a' && ch <= 'z'
			|| ch >= 'A' && ch <= 'Z')
		return true;
	return false;
}

bool is_word(const string &word)
{
	if(word.length() <= 2)
	{
		return false;
	}

	for(string::size_type i = 0; i < word.length(); ++i)
	{
		if(!is_alpha(word[i]))
		{
			cout<<"String contains character: "<<word[i]<<endl;
			return false;
		}
	}

	return true;
}

string pick_up_word(string& word)
{
	string tmp = word;
	string::size_type len = word.length();
	if(!is_alpha(word[0]))
	{
		string tmpword(word,1,len-1);
		tmp = tmpword;
	}

	for(string::size_type i = 0; i < tmp.length(); ++i)
	{
		if(!is_alpha(tmp[i]))
		{
			string tmpword(tmp,0,i);
			tmp = tmpword;
				break;
		}
		else if(!islower(tmp[i]))
		{
			tmp[i] = tolower(tmp[i]);
		}
	}
	word = tmp;
	return tmp;
}

void print_list(MAP & word_list)
{
	MAP::iterator iter = word_list.begin();
	for(; iter != word_list.end(); ++iter)
	{
		cout<<"Word: "<<iter->first<<"\tTimes: "<<iter->second<<endl;
	}
}

string& format_word(string& word)
{
	//string::size_type len = word.length();
	string tmp;
	if(abbre_list.count(word))
	{
		// in the abbreviation list, just ignore it, it must be a simple word
		word = "";
		return word;
	}
	//string suffixed;

	if( !is_word(word) )
	{
		word = pick_up_word(word);
		/*for(string::size_type i = 0; i < word.length(); ++i)
		{
			if(!is_alpha(word[i]))
			{
				string tmpword(word,0,i);
				word = tmpword;
				break;
			}
			else if(!islower(word[i]))
			{
				word[i] = tolower(word[i]);
			}
		}*/
	}

	for(string::size_type i = 0; i < word.length(); ++i)
	{
		if(!islower(word[i]))
		{
			word[i] = tolower(word[i]);
		}
	}

	word = process_suffix(word);

	return word;
}

int load_raw_file(const string &file_name, MAP &word_list)
{
	fstream infile(file_name.c_str());
	if(!infile)
	{
		cout<<"Open file "<<file_name<<" failed"<<endl;
		return -1;
	}
	string line;
	string word;
	passage.clear();
	while(!infile.eof())
	{
		getline(infile, line);
		istringstream stream1(line);
		while(stream1>>word)
		{
			//cout<<"Word: "<<word<<" load_raw_file"<<endl;
			format_word(word);
			if(is_word(word))
			{
				word_list[word] += 1;
				passage.push_back(word);
			}
			else
			{
				cout<<"word: \""<<word<<"\" is not considered as an English word!"<<endl;
			}
		}
		passage.push_back("\n");

	}

	string outfname = file_name + "p.txt";
	cout<<"file to write:"<<outfname<<endl;
	ofstream outfile(outfname.c_str(), ofstream::out);
	//fstream outfile(outfname.c_str());
	if(!outfile)
	{
		cout<<"error open file "<<endl;
	}
	for(vector<string>::iterator iter = passage.begin();
			iter != passage.end(); ++iter)
	{
		outfile<<*iter<<" ";
	}
	outfile.close();
	infile.close();
	return 0;
}

int load_stored_file(const string &file_name, MAP &word_list)
{
	fstream infile(file_name.c_str());
	if(!infile)
	{
		cout<<"Open file "<<file_name<<" failed"<<endl;
		return -1;
	}
	string line;
	string word;
	int times = 0;
	while(!infile.eof())
	{
		getline(infile, line);
		istringstream stream1(line);
		while(stream1>>word>>times)
		{
			//cout<<"Word: "<<word<<" load_stored_file"<<endl;
			format_word(word);
			if(is_word(word))
			{
				word_list.insert(MAP::value_type(word, times));
			}
			else
			{
				cout<<"word: \""<<word<<"\" is not considered as an English word!"<<endl;
			}
		}

	}
	infile.close();
	return 0;
}

int update_data_to_file(const string &file_name, MAP &word_list)
{
	MMAP mmap;

	for(MAP::iterator iter = word_list.begin(); iter != word_list.end(); ++iter)
	{
		mmap.insert(MMAP::value_type(iter->second, iter->first));
	}

	ofstream outfile(file_name.c_str(), ofstream::out);
	if(!outfile)
	{
		cout<<"Open file "<<file_name<<" error!"<<endl;
		return -1;
	}

	for(MMAP::iterator iter = mmap.begin(); iter != mmap.end(); ++iter)
	{
		//line.clear();
		ostringstream line;
		string spaces((30 - iter->second.length()),' ');
		line<<iter->second<<spaces<<iter->first;
		outfile<<line.str()<<endl;
	}

	outfile.close();
	return 0;
}

int repeat_times(const string& word, MAP word_list)
{
	MAP::iterator iter = word_list.find(word);
	if(iter == word_list.end())
	{
		return 0;
	}
	else
	{
		return iter->second;
	}
}

int find_word_in_all_list(const string &word)
{
	return ( repeat_times(word, known_list)
			||repeat_times(word, unknown_list)
			||repeat_times(word, noneed_list)
			||repeat_times(word, familiar_list)
			||repeat_times(word, new_list)
			||abbre_list.count(word)
			);
}

void print_sufix(int count)
{
	switch(count)
	{
	case 1:
		cout<<"first";
		break;
	case 2:
		cout<<"second";
		break;
	case 3:
		cout<<"third";
		break;
	default:
		cout<<count<<"th";
		break;
	}
}

void remove_intersection(MAP &base_list, MAP &op_list)
{
	MAP::iterator iter = op_list.begin();
	while(iter != op_list.end())
	{
		if(repeat_times(iter->first, base_list))
		{
			op_list.erase(iter++);
		}
		else
		{
			++iter;
		}
	}
}

void remove_word_from_list(const string &word, MAP & word_list)
{
	MAP::iterator iter = word_list.find(word);
	if(iter != word_list.end())
	{
		word_list.erase(iter);
	}
}

bool have_suffix(const string& word, const string& suffix)
{
	string::size_type suflen = suffix.length();
	string::size_type wdlen = word.length();

	if(suflen > wdlen)
	{
		return false;
	}
	int offset = wdlen-suflen;
	string subword(word.begin() + offset, word.end());

	return (subword == suffix) ;
}

bool is_suffixed(const string &word)
{
	int size = sizeof(suffix_list)/sizeof(char*);

	for(int i = 0; i < size; ++i)
	{
		if(have_suffix(word, suffix_list[i]))
		{
			return true;
		}
	}

	return false;
}

bool del_suffix(string& word, const string& suffix, string& suffixed)
{

	string::size_type suflen = suffix.length();
	string::size_type wdlen = word.length();
	if(suflen > wdlen)
	{
		suffixed = "";
		//return suffixed;
	}

	string tmp(word.begin(), word.begin() + (wdlen - suflen));
	suffixed = tmp;

	return true;
}

string& process_suffix(string& word)
{
	string suffixed;

	int size = sizeof(suffix_list)/sizeof(char*);

	for(int i = 0; i < size; ++i)
	{
		if(have_suffix(word, suffix_list[i]))
		{
			del_suffix(word, suffix_list[i], suffixed);
			if(find_word_in_all_list(suffixed))
			{
				word = suffixed;
			}
			break;
		}
	}

	return word;
}


void clear_times(MAP &word_list)
{
	MAP::iterator iter = word_list.begin();
	for(; iter != word_list.end(); ++iter)
	{

		iter->second = 1;
	}
}

void clear_all_times(void)
{
	clear_times(known_list);
	clear_times(unknown_list);
	clear_times(familiar_list);
	clear_times(noneed_list);
}

void remove_duplicated_word(MAP &word_list)
{
	MAP::iterator iter = word_list.begin();
	while(iter != word_list.end())
	{
		if(is_suffixed(iter->first))
		{
			string word = iter->first;
			string suffixed = process_suffix(word);
			if(is_suffixed(suffixed))
			{
				++iter;
				continue;
			}
			//cout<<"suffixed: 111"<<suffixed<<endl;
			MAP::iterator iter2 = word_list.find(suffixed);
			if(iter2 != word_list.end())
			{
				cout<<"Word: "<<iter->first<<" is duplicated"<<endl;
				word_list.erase(iter++);
				continue;
			}

		}
		++iter;
	}
}

void remove_duplicated_word_all(void)
{
	//TODO: there's a bug for as and ass
	remove_duplicated_word(known_list);
	remove_duplicated_word(unknown_list);
	remove_duplicated_word(familiar_list);
	remove_duplicated_word(noneed_list);
}

//============================================================================
// Name        : hello.cpp
// Author      : reliu
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C++, Ansi-style
//============================================================================
#include <sys/types.h>
#include<dirent.h>

#include "help.h"

/******************************************************************************
 * Global var
 *****************************************************************************/

extern MAP known_list;
extern MAP familiar_list;
extern MAP unknown_list;
extern MAP noneed_list;
extern MAP new_list;
extern SETS abbre_list;

fstream known_file;
fstream familiar_file;
fstream unkonwn_file;
fstream noneed_file;


int load_all_files(void)
{
	if(!load_stored_file(KNOWN_FILE, known_list) &&
			!load_stored_file(UNKNOWN_FILE, unknown_list)&&
			!load_stored_file(FAMILIAR_FILE, familiar_list)&&
			!load_stored_file(NONEED_FILE, noneed_list))
	{
		return 0;
	}
	else
	{
		return -1;
	}
}

int update_all_files(void)
{
	if(!update_data_to_file(KNOWN_FILE, known_list) &&
			!update_data_to_file(UNKNOWN_FILE, unknown_list)&&
			!update_data_to_file(FAMILIAR_FILE, familiar_list)&&
			!update_data_to_file(NONEED_FILE, noneed_list))
	{
		return 0;
	}
	else
	{
		return -1;
	}
}

int auto_classify(const string& word)
{
	int count = repeat_times(word,noneed_list);
	if(count)
	{
		noneed_list[word] += 1;
		return 1;
	}

	count = repeat_times(word,known_list);
	if(count)
	{
		known_list[word] += 1;
		return 1;
	}
	return 0;
}

void classify_word(const string& word, STATUS status)
{
	switch(status)
	{
	case KNOWN:
		known_list[word] += 1;
		remove_word_from_list(word, unknown_list);
		break;

	case FAMILIAR:
		familiar_list[word] += 1;
		remove_word_from_list(word, unknown_list);
		cout<<"This is the ";
		print_sufix(familiar_list[word]);
		cout<<" time you are not sure about the word: "
			<<word<<endl;
		break;

	case UNKNOWN:
		/*unknown_list[word] += 1;
		remove_word_from_list(word, known_list);
		remove_word_from_list(word, familiar_list);
		cout<<"This is the ";
		print_sufix(unknown_list[word]);
		cout<<" time you don't recognize the word: "
			<<word<<endl;*/
		break;

	case NONEED:
		noneed_list[word] += 1;
		break;
	default:
		break;
	}
}

#include "Cword_list.h"
#include "CWord.h"


int main(int argc, char** argv)
{
	CWord word1("bbb", 2);
	CWord word2("aaa", 3);
	CWord word3("eee", 5);
	Cword_list wlist;
	wlist.word_list.push_back(word1);
	wlist.word_list.push_back(word2);
	wlist.word_list.push_back(word3);
	wlist.sort_mlist(BYSTRR);

	cout<<wlist.word_list[0].word<<endl;
	cout<<wlist.word_list[1].word<<endl;
	cout<<wlist.word_list[2].word<<endl;

	//sort (vec.begin(), vec.end(), compare);
#if 0
	string filepath;
	cout<<"Please input the path of words source file:"<<endl;
	cin>>filepath;

	if(!filepath.length())
	{
		filepath = "src/data/word.txt";
	}

	if(load_all_files())
	{
		cout<<"Load file error!"<<endl;
	}

	if(load_raw_file(filepath.c_str(),new_list))
	{
		cout<<"Error to read word file "<<filepath<<endl;
		return -1;
	}

	remove_duplicated_word(new_list);
	//process the intersections
	remove_intersection(unknown_list, known_list);
	remove_intersection(known_list, noneed_list);
	remove_intersection(unknown_list, familiar_list);

	MAP::iterator iter = new_list.begin();
	int choice = 0;
	while(iter != new_list.end())
	{
		if(auto_classify(iter->first))
		{
			new_list.erase(iter++);
		}
		else
		{
			++iter;
		}

	}
	cout<<"There are "<<new_list.size()<<" need you to deal with"<<endl;
	//print_list(new_list);
	iter = new_list.begin();

	while( iter != new_list.end())
	{
		cout<<endl<<iter->first<<endl
			<<"\tchoice:1: N\t2:Know\t3:F\t4:Unknow "<<endl;
		//cin>>choice;
		choice = 4;
		classify_word(iter->first,static_cast<STATUS>(choice));
		if(choice == 1 || choice == 2)
		{
			new_list.erase(iter++);
		}
		else
		{
			++iter;
		}
	}

	//clear_all_times();
	//remove_duplicated_word(known_list);
	remove_duplicated_word_all();

	update_all_files();
	//print_list(known_list);
	if(new_list.size())
	{
		string filepathnew(filepath);
		filepathnew += ".unknown.txt";
		update_data_to_file(filepathnew, new_list);
	}

	cout<<"Congratulations, all words have been processed!"<<endl;
#endif
	return 0;
}


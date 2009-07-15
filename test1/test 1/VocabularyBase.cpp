//#if __LINUX__TEST__
#include "StdAfx.h"
//#endif

#include "VocabularyBase.h"

VocabularyBase::VocabularyBase(void)
{
}

VocabularyBase::~VocabularyBase(void)
{
}

int VocabularyBase::init_base(const string& path)
{
	return (known_list.init_from_file(path + KNOWN_FILE)
		||unknow_list.init_from_file(path + UNKNOWN_FILE)
		||noneed_list.init_from_file(path + NONEED_FILE));
}

int VocabularyBase::load_word_file(const string& filename)
{
	if(new_list.load_word_file(filename))
    {
        return -1;
    }
    filter_known_words();
    return 0;
}

int VocabularyBase::add_know_word(CWord& word)
{

	known_list.add_word(word);
	return 0;
}

int VocabularyBase::add_unknow_word(CWord& word)
{

	unknow_list.add_word(word);
	return 0;
}

int VocabularyBase::add_noneed_word(CWord& word)
{

	noneed_list.add_word(word);
	return 0;
}

int VocabularyBase::save_list_to_file(Cword_list& word_list)
{

	return 0;
}

int VocabularyBase::save_all(const string& path)
{
	return(known_list.save_to_file(path + KNOWN_FILE)
		||unknow_list.save_to_file(path + UNKNOWN_FILE)
		||noneed_list.save_to_file(path + NONEED_FILE));
}

void VocabularyBase::clssify_word(CWord& word, WORD_STATUS status)
{
	switch(status)
	{
	case KNOWN:
		known_list.add_word(word);
		unknow_list.del_word(word);
		noneed_list.del_word(word);
		break;
	case UNKNOWN:
		unknow_list.add_word(word);
		known_list.del_word(word);
		noneed_list.del_word(word);
		break;
	case NONEED:
		noneed_list.add_word(word);
		known_list.del_word(word);
		unknow_list.del_word(word);
		break;
	default:
		break;
	}
}

bool VocabularyBase::is_word_in_base(CWord& word)
{
	return(known_list.get_repeat_times(word)
		||unknow_list.get_repeat_times(word)
		||noneed_list.get_repeat_times(word)
		||new_list.get_repeat_times(word));
}

void VocabularyBase::sort_list(KEY key)
{
	known_list.sort_list(key);
	unknow_list.sort_list(key);
	noneed_list.sort_list(key);
}


void VocabularyBase::stable_sort_list(KEY key)
{
	known_list.stable_sort_list(key);
	unknow_list.stable_sort_list(key);
	noneed_list.stable_sort_list(key);
}



bool is_alpha(char ch)
{
	if(ch >= 'a' && ch <= 'z'
			|| ch >= 'A' && ch <= 'Z')
		return true;
	return false;
}

bool is_valid_word(const string &word)
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

const char* suffix_list[] = {"ed","ing","es","s"};

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

void VocabularyBase::filter_known_words()
{
	//if(known_list)
	vector<CWord>::iterator iter = new_list.word_list.begin();
	while(iter != new_list.word_list.end())
	{
		

		pick_up_word(iter->word);
		//delete word who's length is not longer than 2
		if(iter->word.length()<=2)
		{
			iter = new_list.word_list.erase(iter);
			continue;
		}

		//delete word that already in database
		else if(known_list.get_repeat_times(*iter)
			||noneed_list.get_repeat_times(*iter))
		{
			cout<<"word "<<iter->word<<" has been filtered"<<endl;
			iter = new_list.word_list.erase(iter);
			continue;
		}
		
		//delete word that have suffix
		else if(is_suffixed(iter->word))
		{
			CWord wd = *iter;
			string suffixed;

			int size = sizeof(suffix_list)/sizeof(char*);

			for(int i = 0; i < size; ++i)
			{
				if(have_suffix(wd.word, suffix_list[i]))
				{
					del_suffix(wd.word, suffix_list[i], suffixed);
					wd.word = suffixed;
					
					if(is_word_in_base(wd))
					{
						update_repeat_times(wd);
						//cout<<"word "<<iter->word<<" repeat "<<wd.repeat_times<<endl;
						iter = new_list.word_list.erase(iter);
                        break;
					}	
                    else
                    {
                        ++iter;
                    }
				}
			}
			continue;

		}
		
		else
		{
			++iter;
		}
	}
}

void VocabularyBase::print_new_words()
{
	cout<<"called"<<endl;
	vector<CWord>::iterator iter = new_list.begin();
	for(; iter != new_list.end(); ++iter)
	{
		cout<<"word: "<<iter->word<<" repeat "<<iter->repeat_times<<endl;
	}

	cout<<"There are "<<new_list.get_word_num()<<" new words"<<endl;
}

void VocabularyBase::update_repeat_times(CWord& word)
{
		if(known_list.get_repeat_times(word))
		{
			known_list.add_word(word);
		}
		else if (unknow_list.get_repeat_times(word))
		{
			unknow_list.add_word(word);
		}
		else if (noneed_list.get_repeat_times(word))
		{
			noneed_list.add_word(word);
		}
		else if (new_list.get_repeat_times(word))
		{
			new_list.add_word(word);
		}		
}


int VocabularyBase::save_word_to_file(const string& file_name)
{
    return new_list.save_to_file(file_name);
}

void VocabularyBase::filter_suffixed_word(void)
{

}
void VocabularyBase::del_dup_word(void)
{
    /*Cword_list known_list;
	Cword_list unknow_list;
	Cword_list noneed_list;
	Cword_list new_list;*/

}

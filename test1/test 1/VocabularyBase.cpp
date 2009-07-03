#ifndef __TEST__
#include "StdAfx.h"
#endif
#include "VocabularyBase.h"

VocabularyBase::VocabularyBase(void)
{
}

VocabularyBase::~VocabularyBase(void)
{
}

int VocabularyBase::init_base()
{
	return (known_list.init_from_file(KNOWN_FILE)
		||unknow_list.init_from_file(UNKNOWN_FILE)
		||noneed_list.init_from_file(NONEED_FILE));
}

int VocabularyBase::load_word_file(const string& filename)
{
	return new_list.load_word_file(filename);
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

int VocabularyBase::save_all()
{
	return(known_list.save_to_file(KNOWN_FILE)
		||unknow_list.save_to_file(UNKNOWN_FILE)
		||noneed_list.save_to_file(NONEED_FILE));
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
		||noneed_list.get_repeat_times(word));
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

void VocabularyBase::filter_known_words()
{
	//if(known_list)
	vector<CWord>::iterator iter = new_list.begin();
	while(iter != new_list.end())
	{
		if(known_list.get_repeat_times(*iter)
			||noneed_list.get_repeat_times(*iter))
		{
			cout<<"word "<<iter->word<<" has been filtered"<<endl;
			new_list.del_word(*iter++);
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
}



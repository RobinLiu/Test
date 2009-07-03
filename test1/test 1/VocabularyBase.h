#ifndef __VocabularyBase__
#define __VocabularyBase__

using namespace std;

#include "word_list.h"
#include<iostream>

class VocabularyBase
{
public:
	VocabularyBase(void);
	virtual ~VocabularyBase(void);

	int init_base();
	int load_word_file(const string& filename);

	int add_know_word(CWord& word);
	int add_unknow_word(CWord& word);
	int add_noneed_word(CWord& word);
	void update_repeat_times(CWord& word);

	void clssify_word(CWord& word,WORD_STATUS status);

	int save_list_to_file(Cword_list& word_list);
	int save_all();

	bool is_word_in_base(CWord& word);
	void sort_list(KEY key);
	void stable_sort_list(KEY key);
	void filter_known_words();
	void print_new_words();
	int get_number_of_new()
	{
		return new_list.get_word_num();
	}
	CWord& get_new_word_at(int pos)
	{
		return new_list.get_word_at(pos);
	}
	
	
private:
	Cword_list known_list;
	Cword_list unknow_list;
	Cword_list noneed_list;
	Cword_list new_list;
};

#endif


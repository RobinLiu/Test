#pragma once

using namespace std;
#include "word_list.h"
class VocabularyBase
{
public:
	VocabularyBase(void);
	virtual ~VocabularyBase(void);

	int add_know_word(CWord& word);
	int add_unknow_word(CWord& word);
	int add_noneed_word(CWord& word);

	void clssify_word(CWord& word,WORD_STATUS status);

	int save_list_to_file(Cword_list& word_list);
	int save_all();
	
private:
	Cword_list known_list;
	Cword_list unknow_list;
	Cword_list noneed_list;
};

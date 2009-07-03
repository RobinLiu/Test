#include "StdAfx.h"
#include "VocabularyBase.h"

VocabularyBase::VocabularyBase(void)
{
}

VocabularyBase::~VocabularyBase(void)
{
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

	return 0;
}

void VocabularyBase::clssify_word(CWord& word, WORD_STATUS status)
{
	switch(status)
	{
	case KNOWN:
		add_know_word(word);
		break;
	case UNKNOWN:
		add_unknow_word(word);
		break;
	case NONEED:
		add_noneed_word(word);
		break;
	}
}
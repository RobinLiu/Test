#include "VocabularyBase.h"

using namespace std;
#include<iostream>

int main()
{

	VocabularyBase vbase;
	if(vbase.init_base())
	{
		cout<<"Init history file error!"<<endl;
		return -1;
	}
	
	if(vbase.load_word_file("./data/word.txt"))
	{
		cout<<"load word file error"<<endl;	
	}

	vbase.filter_known_words();
	vbase.print_new_words();
	/*CWord wd("aaaaaaaaaaaaaaaaaaaaa");
	vbase.clssify_word(wd,NONEED);*/
	vbase.sort_list(BYSTR);
	vbase.stable_sort_list(BYNUMR);
	if(vbase.save_all())
	{
		cout<<"Save file error!"<<endl;
	}
	
}


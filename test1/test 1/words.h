#pragma once

using namespace std;

#include <string>
class words
{
public:
	words(void): repeat_times(0), word(""), line_no(0), word_type(0)
	{};
	words(const string &wd): repeat_times(0), word(wd), line_no(0), word_type(0)
	{};
	long repeat_times;
	string word;
	long line_no;
	int word_type;
	virtual ~words(void);
	
};

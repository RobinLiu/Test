
/*
 * CWord.h
 *
 *  Created on: Jul 1, 2009
 *      Author: reliu
 */

#ifndef CWORD_H_
#define CWORD_H_

using namespace std;

#include <string>

enum WORD_STATUS {KNOWN, UNKNOWN, NONEED};
enum KEY {BYSTR,BYNUM,BYSTRR,BYNUMR};

#define KNOWN_FILE 		"./data/known.txt"
#define UNKNOWN_FILE 	"./data/unknown.txt"
#define NONEED_FILE 	"./data/noneed.txt"

#if 0
#define KNOWN_FILE 		"C:/Users/code/test1/test\ 1/data/known.txt"
#define UNKNOWN_FILE 	"C:/Users/code/test1/test\ 1/data/unknown.txt"
#define NONEED_FILE 	"C:/Users/code/test1/test\ 1/data/noneed.txt"
#endif

class CWord
{
public:
	CWord(void): repeat_times(1), word(""), line_no(0), word_type(0)
	{};
	CWord(const string &wd): repeat_times(1), word(wd), line_no(0), word_type(0)
	{};
	CWord(const string &wd, int times): repeat_times(times), word(wd), line_no(0), word_type(0)
	{};
	virtual ~CWord(void){};
	bool is_same_word(CWord& other)
	{
		return (this->word == other.word);
	};
	bool operator==(const CWord& rhs) const
	{
		return (this->word == rhs.word);
	};
	CWord& operator=(const CWord& rhs)
	{
		if(this != &rhs)
		{
			repeat_times = rhs.repeat_times;
			word = rhs.word;
			line_no = rhs.line_no;
			word_type = rhs.word_type;
		}
		return *this;
	}
	long repeat_times;
	string word;
	long line_no;
	int word_type;
};

#endif /* CWORD_H_ */


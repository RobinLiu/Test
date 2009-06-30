#include "CppUTest/TestHarness.h"
#include "../src/help.h"

TEST_GROUP(FirstTest)
{
};


TEST(FirstTest, tolower)
{
	string word = "CAPITAL";
	STRCMP_EQUAL("capital",format_word(word).c_str());
}

TEST(FirstTest, possessive)
{
	string word = "CAPITAL's";
	STRCMP_EQUAL("capital",format_word(word).c_str());
}

TEST(FirstTest, ing_suffix)
{
	string word = "abinging";
	string suffixed;
	del_suffix(word, "ing", suffixed);
	STRCMP_EQUAL("abing",suffixed.c_str());
}

TEST(FirstTest, ed_suffix)
{
	string word = "abinged";
	string suffixed;
	del_suffix(word, "ed", suffixed);
	STRCMP_EQUAL("abing",suffixed.c_str());
}

TEST(FirstTest, s_suffix)
{
	string word = "abings";
	string suffixed;
	del_suffix(word, "s", suffixed);
	STRCMP_EQUAL("abing",suffixed.c_str());
}

TEST(FirstTest, isword)
{
	string word = "“the";
	CHECK(!is_word(word));
}

/*
 * Copyright (c) 2007, Michael Feathers, James Grenning and Bas Vodde
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *     * Redistributions of source code must retain the above copyright
 *       notice, this list of conditions and the following disclaimer.
 *     * Redistributions in binary form must reproduce the above copyright
 *       notice, this list of conditions and the following disclaimer in the
 *       documentation and/or other materials provided with the distribution.
 *     * Neither the name of the <organization> nor the
 *       names of its contributors may be used to endorse or promote products
 *       derived from this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE EARLIER MENTIONED AUTHORS ``AS IS'' AND ANY
 * EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
 * WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
 * DISCLAIMED. IN NO EVENT SHALL <copyright holder> BE LIABLE FOR ANY
 * DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
 * (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
 * LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
 * ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
 * SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */

#include "CppUTest/TestHarness.h"
#include "CppUTest/SimpleString.h"

TEST_GROUP(SimpleString)
{
};


TEST(SimpleString, Create)
{
  SimpleString s("hello");
}

TEST(SimpleString, CreateSequence)
{
  SimpleString expected("hellohello");
  SimpleString actual("hello", 2);
  
  CHECK_EQUAL(expected, actual);
}

TEST(SimpleString, CreateSequenceOfZero)
{
  SimpleString expected("");
  SimpleString actual("hello", 0);
  
  CHECK_EQUAL(expected, actual);
}

TEST(SimpleString, Copy)
{
  SimpleString s1("hello");
  SimpleString s2(s1);

  CHECK_EQUAL(s1, s2);
}

TEST(SimpleString, Assignment)
{
  SimpleString s1("hello");
  SimpleString s2("goodbye");

  s2 = s1;

  CHECK_EQUAL(s1, s2);
}

TEST(SimpleString, Equality)
{
  SimpleString s1("hello");
  SimpleString s2("hello");

  CHECK(s1 == s2);
}

TEST(SimpleString, InEquality)
{
  SimpleString s1("hello");
  SimpleString s2("goodbye");

  CHECK(s1 != s2);
}

TEST(SimpleString, asCharString)
{
  SimpleString s1("hello");

  STRCMP_EQUAL("hello", s1.asCharString());
}

TEST(SimpleString, Size)
{
  SimpleString s1("hello!");

  LONGS_EQUAL(6, s1.size());
}

TEST(SimpleString, Addition)
{
  SimpleString s1("hello!");
  SimpleString s2("goodbye!");
  SimpleString s3("hello!goodbye!");
  SimpleString s4;
  s4 = s1 + s2;

  CHECK_EQUAL(s3, s4);
}

TEST(SimpleString, Concatenation)
{
  SimpleString s1("hello!");
  SimpleString s2("goodbye!");
  SimpleString s3("hello!goodbye!");
  SimpleString s4;
  s4 += s1;
  s4 += s2;

  CHECK_EQUAL(s3, s4);

  SimpleString s5("hello!goodbye!hello!goodbye!");
  s4 += s4;

  CHECK_EQUAL(s5, s4);
}


TEST(SimpleString, Contains)
{
  SimpleString s("hello!");
  SimpleString empty("");
  SimpleString beginning("hello");
  SimpleString end("lo!");
  SimpleString mid("l");
  SimpleString notPartOfString("xxxx");

  CHECK(s.contains(empty));
  CHECK(s.contains(beginning));
  CHECK(s.contains(end));
  CHECK(s.contains(mid));
  CHECK(!s.contains(notPartOfString));

  CHECK(empty.contains(empty));
  CHECK(!empty.contains(s));
}

TEST(SimpleString, startsWith)
{
	SimpleString hi("Hi you!");
	SimpleString part("Hi");
	SimpleString diff("Hrrm Hi you! ffdsfd");
	CHECK(hi.startsWith(part));
	CHECK(!part.startsWith(hi));
	CHECK(!diff.startsWith(hi));
}

TEST(SimpleString, split)
{
	SimpleString hi("hello\nworld\nhow\ndo\nyou\ndo\n\n");
	SimpleString* splitted;
	int size = hi.split("\n", splitted);
	LONGS_EQUAL(7, size);
	STRCMP_EQUAL("hello\n", splitted[0].asCharString());
	STRCMP_EQUAL("world\n", splitted[1].asCharString());
	STRCMP_EQUAL("how\n", splitted[2].asCharString());
	STRCMP_EQUAL("do\n", splitted[3].asCharString());
	STRCMP_EQUAL("you\n", splitted[4].asCharString());
	STRCMP_EQUAL("do\n", splitted[5].asCharString());
	STRCMP_EQUAL("\n", splitted[6].asCharString());
	
	delete [] splitted;
}

TEST(SimpleString, splitNoTokenOnTheEnd)
{
	SimpleString string("Bah Yah oops");
	SimpleString* splitted;
	int size = string.split(" ", splitted);
	LONGS_EQUAL(3, size);
	STRCMP_EQUAL("Bah ", splitted[0].asCharString());
	STRCMP_EQUAL("Yah ", splitted[1].asCharString());
	STRCMP_EQUAL("oops", splitted[2].asCharString());
	
	delete [] splitted;
}


TEST(SimpleString, count)
{
	SimpleString str("ha ha ha ha");
	LONGS_EQUAL(4, str.count("ha"));
}

TEST(SimpleString, countTogether)
{
	SimpleString str("hahahaha");
	LONGS_EQUAL(4, str.count("ha"));
}

TEST(SimpleString, endsWith)
{
	SimpleString str("Hello World");
	CHECK(str.endsWith("World"));
	CHECK(!str.endsWith("Worl"));
	CHECK(!str.endsWith("Hello"));
	SimpleString str2("ah");
	CHECK(str2.endsWith("ah"));
	CHECK(!str2.endsWith("baah"));
	SimpleString str3("");
	CHECK(!str3.endsWith("baah"));
	
	SimpleString str4("ha ha ha ha");
	CHECK(str4.endsWith("ha"));
	
}

TEST(SimpleString, replaceCharwithChar)
{
	SimpleString str("abcabcabca");
	str.replace('a','b');
	STRCMP_EQUAL("bbcbbcbbcb", str.asCharString());
}

TEST(SimpleString, replaceStringWithString)
{
	SimpleString str("boo baa boo baa boo");
	str.replace("boo","boohoo");
	STRCMP_EQUAL("boohoo baa boohoo baa boohoo", str.asCharString());
}

TEST(SimpleString, ContainsNull)
{
	SimpleString s(0);
	CHECK(!s.contains("something"));
}

TEST(SimpleString, Characters)
{
  SimpleString s(StringFrom('a'));
  SimpleString s2(StringFrom('a'));
  CHECK(s == s2);
}

TEST(SimpleString, Doubles)
{
	SimpleString s(StringFrom(1.2));
	STRCMP_EQUAL("1.200000", s.asCharString());
	s = StringFrom(1.2,2);
	STRCMP_EQUAL("1.20", s.asCharString());
}

TEST(SimpleString, HexStrings)
{
  SimpleString h1 = HexStringFrom(0xffff);
  STRCMP_EQUAL("ffff", h1.asCharString());
}

TEST(SimpleString, cpputest_snprintf_fits)
{
    char buf[10];
    
    int count = cpputest_snprintf(buf, sizeof(buf), "%s", "12345");
    STRCMP_EQUAL("12345", buf);
    LONGS_EQUAL(5, count);
}

TEST(SimpleString, cpputest_snprintf_doesNotFit)
{
    char buf[10];
    
    int count = cpputest_snprintf(buf, sizeof(buf), "%s", "12345678901");
    STRCMP_EQUAL("123456789", buf);
    LONGS_EQUAL(-1, count);
}

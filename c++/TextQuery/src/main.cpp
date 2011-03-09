//============================================================================
// Name        : textQuery.cpp
// Author      : 
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C++, Ansi-style
//============================================================================

#include "TextQuery.h"
#include <string>
#include <vector>
#include <map>
#include <set>
#include <iostream>
#include <fstream>
#include <cctype>
#include <cstring>
#include <cstdlib>

using std::set;
using std::string;
using std::map;
using std::vector;
using std::cerr;
using std::cout;
using std::cin;
using std::ifstream;
using std::endl;

string make_plural(size_t, const string&, const string&);
ifstream& open_file(ifstream&, const string&);

void print_results(const set<TextQuery::line_no>& locs, const string& sought,
		const TextQuery &file)
{
	// if the word was found, then print count and all occurrences
	typedef set<TextQuery::line_no> line_nums;
	line_nums::size_type size = locs.size();
	cout << "\n" << sought << " occurs " << size << " " << make_plural(size,
			"time", "s") << endl;

	// print each line in which the word appeared
	line_nums::const_iterator it = locs.begin();
	for (; it != locs.end(); ++it)
	{
		cout << "\t(line "
		// don't confound user with text lines starting at 0
				<< (*it) + 1 << ") " << file.text_line(*it) << endl;
	}
}

// program takes single argument specifying the file to query
int main()
{
	// open the file from which user will query words
	ifstream infile;
	if (!open_file(infile, "D:\\code\\cworkspace\\textQuery\\Debug\\1.txt"))
	{
		cerr << "No input file!" << endl;
		return EXIT_FAILURE;
	}

	TextQuery tq;
	tq.read_file(infile); // builds query map

	// iterate with the user: prompt for a word to find and print results
	// loop indefinitely; the loop exit is inside the while
	while (true)
	{
		cout << "enter word to look for, or q to quit: ";
		string s;
		cin >> s;

		// stop if hit eof on input or a 'q' is entered
		if (!cin || s == "q")
			break;

		// get the set of line numbers on which this word appears
		set<TextQuery::line_no> locs = tq.run_query(s);

		// print count and all occurrences, if any
		print_results(locs, s, tq);
	}
	return 0;
}

string make_plural(size_t ctr, const string &word, const string &ending)
{
	return (ctr == 1) ? word : word + ending;
}

ifstream& open_file(ifstream &in, const string &file)
{
	in.close(); // close in case it was already open
	in.clear(); // clear any existing errors

	// if the open fails, the stream will be in an invalid state
	in.open(file.c_str()); // open the file we were given

	return in; // condition state is good if open succeeded
}

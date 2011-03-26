/*
 * common.cpp
 *
 *  Created on: 2011-3-23
 *      Author: Robin
 */

#include "common.h"
#include <iostream>
#include <cstdlib>
#include <vector>
#include <algorithm>
#include <time.h>

using namespace std;

void print_array(int* a, int len)
{
	int i;
	for(i = 0; i < len; ++i)
	{
		cout<<a[i]<<"\t";
	}
	cout<<endl;
}

int get_random_number(void)
{
	static bool is_set_seed = false;
	if(!is_set_seed)
	{
		time_t seconds;
		time(&seconds);
		srand((unsigned int) seconds);
		is_set_seed = true;
	}
	return rand();
}

int get_random_number_between(int start, int end)
{
	int low = start<=end?start:end;
	return (get_random_number()%(abs(end - start) + 1) + low);
}

void test_sort(SORT_FUNC sort_func)
{
	int a[] = {3,5,1,2,9,8, 6};
	cout<<"Before sort: ";
	print_array(a, sizeof(a)/sizeof(int));
	sort_func(a, sizeof(a)/sizeof(int));
	cout<<"After  sort: ";
	print_array(a, sizeof(a)/sizeof(int));
}

void swap(int* a, int* b)
{
	if(NULL != a && NULL != b)
	{
		int tmp;
		tmp = *a;
		*a = *b;
		*b = tmp;
	}
}

void contrast_print(vector<int>& vlist, int *a)
{
	vector<int>::iterator iter = vlist.begin();
	for(int i = 0; iter != vlist.end(); ++iter, ++i)
	{
		cout<<"a["<<i<<"] = "<<a[i]<<"\t"<<*iter<<endl;
	}
}
int _random_test(SORT_FUNC sort_func)
{
	int len = get_random_number();
	int* a = new int[len];
	if (NULL == a)
	{
		cout<<"new int["<<len<<"] failed"<<endl;
		return -1;
	}
	vector<int> vlist;
	for(int i = 0; i < len; ++i)
	{
		int tmp = get_random_number();
		a[i] = tmp;
		vlist.push_back(tmp);
	}
	sort_func(a, len);
	sort(vlist.begin(), vlist.end());

	vector<int>::iterator iter = vlist.begin();
	for(int i = 0; iter != vlist.end(); ++iter, ++i)
	{
		if(a[i] != *iter)
		{
			contrast_print(vlist, a);
			delete [] a;
			return -1;
		}
	}
	delete [] a;
	return 0;
}


void random_test(SORT_FUNC sort_func, string func_name)
{
	int ret = _random_test(sort_func);
	if(ret != 0)
	{
		cout<<"Sort algorithm "<<func_name<<" failed"<<endl;
	}
//	else
//	{
//		cout<<"sort algorithm ok!"<<endl;
//	}
}

void huge_sort_test(SORT_FUNC sort_func, string func_name)
{
	time_t time_start;
	time_t time_end;
	time(&time_start);
	int test_time = get_random_number_between(1, /*RAND_MAX*/100);
	for(int i = test_time; i>= 0; --i)
	{
		random_test(sort_func, func_name);
	}
	time(&time_end);
	cout<<"Test "<<test_time<<" times for "<<func_name<<" done, using "<<time_end - time_start<<" seconds"<<endl;
}




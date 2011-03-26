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
	int len = rand();
	int* a = new int[len];
	if (NULL == a)
	{
		cout<<"new int["<<len<<"] failed"<<endl;
		return -1;
	}
	vector<int> vlist;
	for(int i = 0; i < len; ++i)
	{
		int tmp = rand();
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
	int i = rand();
	cout<<"rand is "<<i<<endl;
	for(; i>= 0; --i)
	{
		random_test(sort_func, func_name);
	}
}




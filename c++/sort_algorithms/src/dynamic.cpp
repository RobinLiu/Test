/*
 * dynamic.cpp
 *
 *  Created on: 2011-3-31
 *      Author: Robin
 */
#include <iostream>
using namespace std;
int max(int a, int b)
{
	return (a>b?a:b);
}

int cut_rod(int* p, int len)
{
	if(0 == len)
	{
		return 0;
	}
	int q = 0;
	for(int i = 1; i <= len; ++i)
	{
		q = max(q, p[i-1] + cut_rod(p, len-i));
	}
	return q;
}

int memoized_cut_rod_aux(int*p, int len, int* r)
{

	if ( len == 0)
	{
		return 0;
	}
	if (r[len - 1] >= 0)
	{
		return r[len -1];
	}

	int q = -1;
	for(int i = 1; i <= len; ++i)
	{
//		cout<<"q:"<<q<<"  p["<<i-1<<"]:"<<p[i-1]<<endl;
		q = max(q, p[i-1] + memoized_cut_rod_aux(p, len-i, r));

	}
	r[len -1] = q;

	return q;

}

int memeoized_cut_rod(int* p, int len)
{
	int* r = new int[len];
	for(int i = 0; i < len; ++i)
	{
		r[i] = -1;
	}
	int ret =  memoized_cut_rod_aux(p, len, r);
	delete [] r;
	return ret;
}

void print_cut(int* s, int len)
{

	while(len > 0)
	{
		cout<<"cut "<<s[len]<<endl;
		len = len - s[len];
	}
}
int bottom_up_cut_rot(int* p, int len)
{
	int* r = new int[len + 1];
	int* s = new int[len + 1];
	r[0] = 0;
	for(int i = 1; i <= len; ++i)
	{
		int q = -1;
		for(int j = 1; j <= i; ++j)
		{
//			q = max(q, p[j-1] + r[i-j]);
			if(q < p[j-1] + r[i-j])
			{
				q = p[j-1] + r[i-j];
				s[i] = j;
			}
		}
		r[i] = q;
	}
	int ret = r[len];
//	while(len >0)
//	{
//		cout<<"cut: "<<s[len]<<endl;
//		while(len != s[len])
//		{
//			len = len - s[len];
//
//		}
//	}
	print_cut(s, len);
	delete [] r;
	delete [] s;
	return ret;
}

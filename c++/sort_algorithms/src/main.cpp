//============================================================================
// Name        : sort_algorithms.cpp
// Author      : 
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C++, Ansi-style
//============================================================================
#include "common.h"
#include "sort_algorithms.h"
#include <iostream>
using namespace std;
extern int cut_rod(int* p, int n);
extern int memeoized_cut_rod(int* p, int len);
extern int bottom_up_cut_rot(int* p, int len);


int main()
{

//	test_sort(insert_sort);
//	test_sort(bubble_sort);
//	test_sort(merge_sort);
//	test_sort(heap_sort);
//	test_sort(quicksort);
//	test_sort(randomized_quicksort);
//	random_test(insert_sort);
//	random_test(bubble_sort, "bubble_sort");
//	random_test(merge_sort);
//	random_test(heap_sort);
//	random_test(quicksort);
//	random_test(randomized_quicksort);

//	HUGE_SORT_TEST(insert_sort);
//	HUGE_SORT_TEST(bubble_sort);
//	HUGE_SORT_TEST(merge_sort);
//	HUGE_SORT_TEST(heap_sort);
//	HUGE_SORT_TEST(quicksort);
//	HUGE_SORT_TEST(randomized_quicksort);
	int price[] = {1, 5, 8, 9, 10, 17, 17, 20, 24, 30};
	for(int i = 0; i < 10; ++i)
	{
		//int q = cut_rod(price, i+1);
		int q = bottom_up_cut_rot(price, i+1);
		cout<<"len is :"<<i+1<<" q is : "<<q<<endl;
	}

	return 0;
}

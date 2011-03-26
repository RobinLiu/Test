/*
 * common.h
 *
 *  Created on: 2011-3-23
 *      Author: Robin
 */

#ifndef COMMON_H_
#define COMMON_H_

#include <iostream>
#include <string>

typedef void (*SORT_FUNC)(int* a, int len);

void print_array(int* a, int len);

void test_sort(SORT_FUNC sort_func);

void random_test(SORT_FUNC sort_func, std::string func_name);

void huge_sort_test(SORT_FUNC sort_func, std::string func_name);

//#define print_func_name(func_name) cout<<#func_name<<endl; test_sort(func_name)
#define RANDOM_TEST(sort_func) random_test(sort_func, #sort_func)
#define HUGE_SORT_TEST(sort_func) huge_sort_test(sort_func, #sort_func)
void swap(int* a, int* b);

#endif /* COMMON_H_ */

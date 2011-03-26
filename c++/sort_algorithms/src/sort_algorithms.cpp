/*
 * insert_sort.cpp
 *
 *  Created on: 2011-3-23
 *      Author: Robin
 */
#include "sort_algorithms.h"
#include "common.h"
#include <cstring>
#include <cstdlib>
using namespace std;
void insert_sort(int* a, int len)
{
	int i;
	int key;
	for(int j = 1; j < len; ++j)
	{
		key = a[j];
		i = j - 1;
		while(i >= 0 && a[i] > key)
		{
			a[i + 1] = a[i];
			--i;
		}
		a[i + 1] = key;
	}
}


void bubble_sort(int* a, int len)
{
	for(int i = 0; i < len; ++i)
	{
		for(int j = len; j > 0; --j)
		{
			if (a[j] < a[j-1])
			{
				swap(&a[j], &a[j-1]);
			}
		}
	}
}


void merge(int* a, int p, int q, int r)
{
	int n1 = q - p + 1;
	int n2 = r - q;
//	cout<<"p: "<<p<<" q: "<<q<<" r: "<<r<<endl;
	int* l1 = new int[n1];
	if(NULL == l1)
	{
		std::cout<<"malloc l1 failed"<<endl;
		return;
	}
	int* l2 = new int[n2];
	if(NULL == l2)
	{
		std::cout<<"malloc l2 failed"<<endl;
		delete[] l1;
		return;
	}
	memset(l1, 0, n1*sizeof(int));
	memset(l2, 0, n2*sizeof(int));

	for(int i = p, j = 0; i<= q;)
	{
		l1[j++] = a[i++];
	}
	for(int i = q+1, j = 0; i<= r;)
	{
		l2[j++] = a[i++];
	}

//	cout<<"l1:";
//	print_array(l1, n1);
//	cout<<"l2:";
//	print_array(l2, n2);
	int l1cnt = n1;
	int l2cnt = n2;
	int i = 0, j = 0;
	for(int k = p; k <= r; ++k)
	{
		if(l1cnt == 0)
		{
			a[k] = l2[j++];
			continue;
		}
		if(l2cnt == 0)
		{
			a[k] = l1[i++];
			continue;
		}

		if(l1[i] <= l2[j])
		{
			a[k] = l1[i++];
			l1cnt--;
		}
		else
		{
			a[k] = l2[j++];
			l2cnt--;
		}
	}
	delete[] l1;
	delete[] l2;
}

void _merge_sort(int*a, int p, int r)
{
	if(p < r)
	{
		int q = (p + r)/2;
		_merge_sort(a, p, q);
		_merge_sort(a, q+1, r);
		merge(a, p, q, r);
	}
}

void merge_sort(int* a, int len)
{
	_merge_sort(a, 0, len -1);
}


/***********************************************
 * 关键是搞清楚几个下标：
 * 1.获取父节点，左子树，右子树
 * 2.获取最后一个非叶子节点的下标
 * 3.递归的时候len长度要减一，这样才能收敛
 **********************************************/
int get_parent(int i)
{
	return (i - 1)/2;
}

int get_left(int i)
{
	return 2*i + 1;
}

int get_right(int i)
{
	return (2*i + 2);
}

void max_heapify(int* a, int index, int len)
{
	if(index >= len)
	{
		cout <<"index error"<<endl;
		return;
	}
	int left = get_left(index);
	int right = get_right(index);
	int largest = 0;
	if (left < len && a[left] > a[index])
	{
		largest = left;
	}
	else
	{
		largest = index;
	}
	if(right < len && a[right] > a[largest])
	{
		largest = right;
	}

	if(largest != index)
	{
		swap(&a[index], &a[largest]);
		max_heapify(a, largest, len);
	}
}

void build_max_heap(int* a, int len)
{
	int heap_len = len;
	/*find the last one which is not leaf*/
	for(int index = (heap_len/2 - 1); index >= 0; --index)
	{
		max_heapify(a, index, len);
	}
}

void heap_sort(int* a, int len)
{
	build_max_heap(a, len);
	for(int i = len - 1; i > 0; --i)
	{
		swap(&a[0], &a[i]);
		/*len need minus 1*/
		len--;
		max_heapify(a, 0, len);
	}
}

/*Priority queues
 *
 */

int heap_max(int* a)
{
	return a[0];
}

int heap_extract_max(int* a, int len)
{
//	assert(len >= 1);
	int max = a[0];
	a[0] = a[len - 1];
	len--;
	max_heapify(a, 0, len);
	return max;
}

void heap_increase_key(int* a, int index, int key)
{
	if(key < a[index])
		return;
	a[index] = key;
	for(int i = 0; i>=0 && a[get_parent(i)] < a[i]; i = get_parent(i))
	{
		swap(&a[i], &a[get_parent(i)]);
	}
}

//void max_heap_insert(int* a, int key, int len)
//{
//	len
//}


int partition(int* a, int lindex, int rindex)
{
	int tmp = a[rindex];
	int i = lindex - 1 ;
	for(int j = lindex; j < rindex; ++j)
	{
		if(a[j] <= tmp)
		{
			i++;
			swap(&a[i], &a[j]);
		}
	}
	swap(&a[i+1], &a[rindex]);
	return (i + 1);
}

void _quicksort(int* a, int p, int r)
{
	if(p < r)
	{
		int q = partition(a, p, r);
		_quicksort(a, p, q-1);
		_quicksort(a, q + 1, r);
	}
}

void quicksort(int* a, int len)
{
	_quicksort(a, 0, len -1);
}


int randomized_partition(int* a, int p, int r)
{
	int i = rand();
	i = p + i%(r - p);
	swap(&a[i], &a[r]);
	return partition(a, p, r);

	/*int i = random(p, r);
	 * swap(&a[i], &a[r]);
	 * return partition(a, p, r);
	 * */
}

void _randomized_quicksort(int* a, int p, int r)
{
	if(p < r)
	{
		int q = randomized_partition(a, p, r);
		_randomized_quicksort(a, p, q-1);
		_randomized_quicksort(a, q + 1, r);
	}
}

void randomized_quicksort(int* a, int len)
{
	_randomized_quicksort(a, 0, len - 1);
}

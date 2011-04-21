/*
 * main.cpp
 *
 *  Created on: 2011-4-21
 *      Author: reliu
 */

#include "BST.h"
#include<iostream>

using namespace std;

Node* reserve_node(int key)
{
	Node* node = new Node;
	node->right = NULL;
	node->left = NULL;
	node->parent = NULL;
	node->key = key;
	return node;
}

int main(int argc, char** argv)
{
	cout<<"test"<<endl;
	BST root = NULL;
	tree_insert(&root, reserve_node(10));
	tree_insert(&root, reserve_node(12));
	tree_insert(&root, reserve_node(11));
	tree_insert(&root, reserve_node(7));
	tree_insert(&root, reserve_node(9));
	tree_insert(&root, reserve_node(8));
	tree_insert(&root, reserve_node(13));
	inorder_tree_walk(root);
	Node* node = NULL;
	node = tree_search(root, 9);
	if(NULL != node)
	{
		cout<<"key 9 is "<<node->key<<endl;
	}
	Node* tmp = tree_successor(node);
	if(NULL != node)
	{
		cout<<"successor of 9 is "<<tmp->key<<endl;
	}
	tmp = tree_maximum(root);
	if(NULL != node)
	{
		cout<<"max is "<<tmp->key<<endl;
	}

	tmp = iterative_tree_search(root, 9);
	if(NULL != node)
	{
		cout<<"search 9 is "<<tmp->key<<endl;
	}
	return 0;
}

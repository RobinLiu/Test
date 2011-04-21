/*
 * BST.cpp
 *
 *  Created on: 2011-4-21
 *      Author: reliu
 */
#include "BST.h"
#include <iostream>
using namespace std;

void inorder_tree_walk(BST root)
{
	if(NULL == root)
	{
		return;
	}
	Node* iter_node = root;
	inorder_tree_walk(iter_node->left);
	cout<<iter_node->key<<" ";
	inorder_tree_walk(iter_node->right);
}

Node* tree_search(BST root, int key)
{
	if(NULL == root)
	{
		return NULL;
	}
	Node * iter = root;
	if(key == iter->key)
	{
		return iter;
	}
	else if(key > iter->key)
	{
		return tree_search(iter->right, key);
	}
	else
	{
		return tree_search(iter->left, key);
	}
}

Node* iterative_tree_search(BST root, int key)
{
	if(NULL == root)
	{
		return NULL;
	}
	Node* iter = root;
	while(NULL != iter)
	{
		if(key == iter->key)
		{
			return iter;
		}
		else if(key > iter->key)
		{
			iter = iter->right;
		}
		else
		{
			iter = iter->left;
		}
	}
	return iter;
}

Node* tree_minimum(BST root)
{
	if(NULL == root)
	{
		return NULL;
	}
	Node* iter = root;
	while(NULL != iter->left)
	{
		iter = iter->left;
	}
	return iter;
}

Node* tree_maximum(BST root)
{
	if(NULL == root)
	{
		return NULL;
	}
	Node* iter = root;
	while(NULL != iter->right)
	{
		iter = iter->right;
	}
	return iter;
}

Node* tree_successor(Node* node)
{
	if(NULL == node)
	{
		return NULL;
	}
	if(NULL != node->right)
	{
		return tree_minimum(node->right);
	}
	Node* iter = node;
	Node* parent = node->parent;

	while(NULL != parent && iter == parent->right)
	{
		iter = parent;
		parent = parent->parent;
	}
	return parent;

}

void tree_insert(BST* root, Node* node)
{
	Node* parent = NULL;
	Node* iter = *root;
	while(NULL != iter)
	{
		parent = iter;
		if(node->key < iter->key)
		{
			iter = iter->left;
		}
		else
		{
			iter = iter->right;
		}
	}
	node->parent = parent;
	if(NULL == parent)
	{
		*root = node;
	}
	else if(node->key < parent->key)
	{
		parent->left = node;
	}
	else
	{
		parent->right = node;
	}
}

void delete_tree(BST* root)
{
	if(NULL == root || NULL == *root)
		return;
	Node* &tmp = *root;
	delete_tree(&tmp->right);
	delete_tree(&tmp->left);
	delete tmp;
	tmp = NULL;
//	*root = NULL;
}

void transplant(BST* root, Node* oldnode, Node* newnode)
{
	if(oldnode == NULL)
		return;
	if(NULL == oldnode->parent)
	{
		*root = newnode;
	}
	else if(oldnode == oldnode->parent->left)
		oldnode->parent->left = newnode;
	else
		oldnode->parent->right = newnode;
	if(NULL != newnode)
		newnode->parent = oldnode->parent;
}

void tree_delete(BST* root, Node* z)
{
	if(NULL == z)
		return;
	if(NULL == z->left)
		transplant(root, z, z->right);
	else if (NULL == z->right)
	{
		transplant(root, z, z->left);
	}
	else
	{
		Node* y = tree_minimum(*root);
		if(z != y->parent)
		{
			transplant(root, y, y->right);
			y->right = z->right;
			y->right->parent = y;
		}
		transplant(root, z, y);
		y->left = z->left;
		y->left->parent = y;
	}
	delete z;
	z = NULL;
}

/*
 * BST.h
 *
 *  Created on: 2011-4-21
 *      Author: reliu
 */

#ifndef BST_H_
#define BST_H_

typedef struct Node {
	int	key;
	struct Node* left;
	struct Node* right;
	struct Node* parent;
} Node;

typedef Node* BST;

void inorder_tree_walk(BST root);

Node* tree_search(BST root, int key);

Node* iterative_tree_search(BST root, int key);

Node* tree_minimum(BST root);

Node* tree_maximum(BST root);

Node* tree_successor(Node* node);

void tree_insert(BST* root, Node* node);

void transplant(BST root, Node* u, Node* v);

void tree_delete(BST root, Node* z);

#endif /* BST_H_ */

'''
Created on 2011-4-16

@author: Robin
'''

class Node:
    """
    Tree Node: left and right child + data, which can be any object
    """
    def __init__(self, data):
        """
        Node constructor
        
        @param data node data object
        """
        self.left = None
        self.right = None
        self.data = data
        
    def insert(self, data):
        """
        Insert new node with data
        
        @param data: Node data objec to insert
        """
        if data < self.data:
            if self.left is None:
                self.left = Node(data)
            else:
                self.left.insert(data)
        else:
            if self.right is None:
                self.right = Node(data)
            else:
                self.right.insert(data)
                
    def lookup(self, data, parent=None):
        """
        Lookup node containing data
        
        @param data: Node data object to look up
        @param parent: Node's parent
        @return: node and node's parent if found or None, None
        """
        if data < self.data:
            if self.left is None:
                return None, None
            return self.lookup(data, self)
        elif data > self.data:
            if self.right is None:
                return None, None
            return self.right.lookup(data, self)
        else:
            return self, parent
    
    def delete(self, data):
        """
        Delete node containing data
        
        @param data: node's content to delete
        """
        #get node containing data
        node, parent = self.lookup(data)
        if node is not None:
            children_count = node.children_count()
        
        #if node has no children, just remove it
        if children_count == 0:
            if parent.left is Node:
                parent.left = None
            else:
                parent.right = None
        #if node has only 1 childe, replace node by its child
        elif children_count == 1:
            if node.left:
                node.data = node.left.data
                node.left = None
            else:
                node.data = node.right.data
                node.right = None
        #if node has 2 children find its successor
        else:
            parent = None
            successor = node
            while successor.left:
                parent = successor
                successor = successor.left
            #replace node data by its successor's data
            node.data = successor.data
            #fix successor's parant's child
            if parent.left == successor:
                parent.left = successor.right
            else:
                parent.right = successor.right
                 
    def children_count(self):
        """
        Returns the number of children
        
        @return: number of children: 0, 1, or 2
        """
        cnt = 0
        if self.left:
            cnt += 1
        if self.right:
            cnt += 1
        return cnt 
    
    def print_tree(self):
        """
        Print tree content in order
        """
        if self.left:
            self.left.print_tree()
        print(self.data, end=" ")
        if self.right:
            self.right.print_tree()
            
if __name__ == '__main__':
    root = Node(8)
    root.insert(3)
    root.insert(10)
    root.insert(1)
    root.insert(6)
    root.insert(4)
    root.insert(7)
    root.insert(14)
    root.insert(13)
    root.print_tree()
    
#!/usr/bin/env python3

class Node:
    def __init__(self, key, children=None):
        self.key = key
        self.children = children # children is an array

def search(tree, key):
    if tree.key == key:
        print(key)
        return True
    if tree.children != None:
        for child in tree.children:
            if search(child, key):
                return True
    return False


tree = Node('a', [
        Node('b', [
            Node('d', None),
            Node('e', None),
            Node('f', None)]),
        Node('c', [
            Node('g', [
                Node('h', None)])])])
print(search(tree, 'f'))
print(search(tree, 'z'))

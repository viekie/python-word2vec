#!/usr/bin/env python
# -*- coding: utf8 -*-
# Power by viekie2017-09-03 17:50:24

import numpy as np


class HuffmanNode(object):

    def __init__(self, value, possibility):
        self.possibility = possibility
        self.left = None
        self.right = None
        self.value = value
        self.huffman = ''

    def __str__(self):
        return 'huffman node object, value: {v}, possibility: {p}, \
            huffman: {h}'.format(v=self.value,
                                 p=self.possibility,
                                 h=self.huffman)


class HuffmanTree(object):

    def __init__(self, word_dict, vec_len=15000):
        self.vec_len = vec_len
        self.root = None
        word_dict_list = list(word_dict.values())
        node_list = [HuffmanNode(x['word'], x['possibility'])
                     for x in word_dict_list]
        self.build_tree(node_list)
        self.generate_huffman_code(self.root, word_dict)

    def build_tree(self, node_list):
        while len(node_list) > 1:
            i1 = 0
            i2 = 1

            if node_list[i2].possibility < node_list[i1].possibility:
                [i1, i2] = [i2, i1]

            for i in range(2, len(node_list)):
                if node_list[i].possibility < node_list[i2].possibility:
                    i2 = i
                    if node_list[i].possibility < node_list[i1].possibility:
                        [i1, i2] = [i2, i1]
            top_node = self.merge(node_list[i1], node_list[i2])

            if i1 < i2:
                node_list.pop(i2)
                node_list.pop(i1)
            elif i1 > i2:
                node_list.pop(i1)
                node_list.pop(i2)
            else:
                raise RuntimeError('i1 should be not equal to i2')
            node_list.insert(0, top_node)
        self.root = node_list[0]

    def generate_huffman_code(self, node, word_dict):
        stack = [self.root]
        while(len(stack) > 0):
            node = stack.pop()
            while node.left or node.right:
                code = node.huffman
                node.left.huffman = code + '1'
                node.right.huffman = code + '0'
                stack.append(node.right)
                node = node.left
            word = node.value
            code = node.huffman
            word_dict[word]['huffman'] = code

    def merge(self, node1, node2):
        top_pos = node1.possibility + node2.possibility
        top_node = HuffmanNode(np.zeros([1, self.vec_len]), top_pos)
        if node1.possibility > node2.possibility:
            top_node.left = node1
            top_node.right = node2
        else:
            top_node.left = node2
            top_node.right = node1
        return top_node

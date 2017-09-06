#!/usr/bin/env python
# -*- coding: utf8 -*-
# Power by viekie2017-09-05 14:34:45

import math
import file_op_utils as fous
from WordCount import WordCounter, MultiCounter
from huffman_tree import HuffmanTree
import numpy as np
import jieba
from sklearn import preprocessing


class Word2Vector(object):
    def __init__(self, vec_len=15000, learn_rate=0.0025,
                 win_len=5, model='cbow'):
        self.cutted_text_list = None
        self.vec_len = vec_len
        self.learn_rate = learn_rate
        self.win_len = win_len
        self.model = model
        self.word_dict = None
        self.huffman = None

    def load_word_freq(self, word_freq_file):
        if self.word_dict is not None:
            raise RuntimeError('word dict is not empty')
        word_freq = fous.read_pickle(word_freq_file)
        self.__generate_word_dict(word_freq)

    def __generate_word_dict(self, word_freq):
        if not isinstance(word_freq, dict) and not isinstance(word_freq, list):
            raise ValueError('the word freq format error')
        word_dict = {}

        if isinstance(word_freq, dict):
            sum_count = sum(word_freq.values())
            for word in word_freq:
                temp_dict = dict(word=word,
                                 freq=word_freq[word],
                                 possibility=word_freq[word]/sum_count,
                                 vector=np.random.random([1, self.vec_len]),
                                 huffman=None)
                word_dict[word] = temp_dict
        else:
            freq_list = [x[1] for x in word_freq]
            sum_count = sum(freq_list)
            for word in word_freq:
                temp_dict = dict(word=word[0],
                                 freq=word[1],
                                 possibility=word[1]/sum_count,
                                 vector=np.random.random([1, self.vec_len]),
                                 huffman=None)
                word_dict[word[0]] = temp_dict

    def import_model(self, model_path):
        model = fous.read_pickle(model_path)
        self.word_dict = model.word_dict
        self.huffman = model.huffman
        self.vec_len = model.vec_len
        self.learn_rate = model.learn_rate
        self.win_len = model.win_len
        self.model = model.model

    def export_model(self, model_path):
        data = dict(word=self.word_dict,
                    huffman=self.huffman,
                    vec_len=self.vec_len,
                    learn_rate=self.learn_rate,
                    win_len=self.win_len,
                    model=self.model)
        fous.save_pickle(data, model_path)

    def train_model(self, text_list):
        if self.huffman is None:
            if self.word_dict is None:
                wc = WordCounter(text_list)
                self.__generate_word_dict(wc.count_res.larger_than(5))
                self.cutted_text_list = wc.text_list
            self.huffman = HuffmanTree(self.word_dict, vec_len=self.vec_len)
        print('word_dict and huffman tree already generated')

        before = (self.win_len - 1) >> 1
        after = self.win_len - 1 - before

        if self.model == 'cbow':
            method = self.__deal_gram_cbow
        else:
            method = self.__deal_gram_skipgram

        if self.cutted_text_list:
            total = len(self.cutted_text_list)
            count = 0

            for line in self.cutted_text_list:
                line_len = len(line)
                for i in range(line_len):
                    method(line[i], line[max(0, i-before):i] +
                           line[i+1: min(line_len, i+after+1)])
        else:
            for line in text_list:
                line = list(jieba.cut(line, cut_all=False))
                line_len = len(line_len)
                for i in range(line_len):
                    method(line[i], line[max(0, i-before): i] +
                           line[i+1, min(line_len, i+after+1)])
        print('word vector has been generated')

    def __deal_gram_cbow(self, word, gram_word_list):
        if not self.word_dict.contains(word):
            return
        word_huffman = self.word_dict[word]['huffman']
        gram_vector_sum = np.zero([1, self.vec_len])

        for i in range(len(gram_word_list))[::-1]:
            item = gram_word_list[i]
            if self.word_dict.contains(item):
                gram_vector_sum += self.word_dict[item]['vector']
            else:
                gram_word_list.pop(i)
        if len(gram_word_list) == 0:
            return
        e = self.__goalong_huffman(word_huffman, gram_vector_sum,
                                   self.huffman.root)
        for item in gram_word_list:
            self.word_dict[item]['vector'] += e
            self.word_dict[item]['vector'] = \
                preprocessing.normalize(self.word_dict[item]['vector'])

    def __deal_gram_skipgram(self, word, gram_word_list):
        if not self.word_dict.contains(word):
            return
        word_vector = self.word_dict[word]['vector']

        for i in range(len(gram_word_list))[::-1]:
            if not self.word_dict.contains(gram_word_list[i]):
                gram_word_list.pop(i)

        if len(gram_word_list) == 0:
            return

        for u in gram_word_list:
            u_huffman = self.word_dict[u]['huffman']
            e = self.__goalong_huffman(u_huffman, word_vector,
                                       self.huffman.root)
            self.word_dict[word]['vector'] += e
            self.word_dict[word]['vector'] = \
                preprocessing.normalize(self.word_dict[word]['vector'])

    def __goalong_huffman(self, word_huffman, input_vector, root):
        node = root
        e = np.zero([1, self.vec_len])
        for level in range(len(word_huffman)):
            huffman_charat = word_huffman[level]
            q = self.sigmod(input_vector.dot(node.value.T))
            grad = self.learn_rate * (1 - int(huffman_charat) - q)
            e += grad * node.value
            node.value = preprocessing.normalize(node.value)
            if huffman_charat == '0':
                node = node.right
            else:
                node = node.left
        return e

    def sigmod(self, value):
        return 1 / (1 + math.exp(-value))


if __name__ == '__main__':

    text = ['Merge multiple sorted inputs into a single sorted output',
            'The API below differs',
            'from textbook heap algorithms in two aspects']

    wv = Word2Vector(vec_len=500)
    wv.Train_Model(text)
    fous.save_pickle(wv.word_dict, './static/wv.pkl')

    # data = FI.load_pickle('./static/wv.pkl')
    # x = {}
    # for key in data:
    #     temp = data[key]['vector']
    #     temp = preprocessing.normalize(temp)
    #     x[key] = temp
    # FI.save_pickle(x,'./static/normal_wv.pkl')


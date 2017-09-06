#!/usr/bin/env python
# -*- coding: utf8 -*-
# Power by viekie2017-09-06 11:19:28

import jieba
import codecs
from gensim.models import word2vec


def generate_corpus(corpus_path, word_corpus_path):

    if corpus_path is None or word_corpus_path is None:
        raise ValueError('corpus path is null')

    f1 = codecs.open(corpus_path)
    f2 = codecs.open(word_corpus_path, 'a', encoding='utf-8')

    lines = f1.readlines()
    for line in lines:
        line.replace('\t', '').replace(' ', '').replace('\n', '')
        seg_list = jieba.cut(line, cut_all=False)
        f2.write(' '.join(seg_list))

    f2.close()
    f1.close()


def compute_similar(word_corpus_path, word):
    sentences = word2vec.Text8Corpus(word_corpus_path)
    model = word2vec.Word2Vec(sentences, size=200)

    try:
        y1 = model.similarity(word, u'文人')
    except Exception:
        y1 = 0
    print(u'{0} and {1} similarity:{2}'.format(word, u'文人', y1))

    y2 = model.most_similar(word, topn=20)

    for item in y2:
        text = item[0].encode('unicode-escape').decode('string_escape')
        print(text.decode('utf8'), item[1])


if __name__ == '__main__':
    # generate_corpus('./data.txt', './data_seg.txt')
    compute_similar('./data_seg.txt', u'小说')

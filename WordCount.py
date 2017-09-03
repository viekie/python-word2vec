#!/usr/bin/env python
# -*- coding: utf8 -*-
# Power by viekie2017-09-03 16:40:56

from collections import Counter
from operator import itemgetter as itemgtr
import jieba
import file_op_utils as foutils


class WordCounter():
    def __init__(self, text_list):
        self.text_list = text_list
        self.stop_word = self.Get_Stop_Words()
        self.count_res = None
        self.Word_Count(self.text_list)

    def Get_Stop_Words(self):
        ret = []
        ret = foutils.read_pickle('./static/stop_words.pkl')
        return ret

    def Word_Count(self, text_list, cut_all=False):
        flted_word_list = []
        count = 0

        for line in text_list:
            res = jieba.cut(line, cut_all=cut_all)
            res = list(res)
            text_list[count] = res
            count += 1
            flted_word_list += res

        self.count_res = MultiCounter(flted_word_list)

        for word in flted_word_list:
            try:
                self.count_res.pop(word)
            except Exception:
                pass


class MultiCounter(Counter):
    def __init__(self, element_list):
        super().__init__(element_list)

    def larger_than(self, minvalue, ret='list'):
        temp = sorted(self.items(), key=itemgtr(1), reverse=True)
        low = 0
        high = len(temp)

        while(high - low > 1):
            mid = (low + high) >> 1
            if temp[mid][1] >= minvalue:
                low = mid
            else:
                high = mid

        if temp[low][1] < minvalue:
            if ret == 'dict':
                return {}
            else:
                return []

        if ret == 'dict':
            ret_data = {}
            for ele, count in temp[:high]:
                ret_data[ele] = count
            return ret_data
        else:
            return temp[:high]

    def less_than(self, minvalue, ret='list'):
        temp = sorted(self.items(), key=itemgtr(1))
        low = 0
        high = len(temp)

        while(high - low > 1):
            mid = (high + low) >> 1

            if temp[mid][1] <= minvalue:
                low = mid
            else:
                high = mid

        if temp[low][1] < minvalue:
            if ret == 'dict':
                return {}
            else:
                return []

        if ret == 'dict':
            ret_data = {}
            for ele, count in temp[:high]:
                ret_data[ele] = count
            return ret_data
        else:
            return temp[:high]


if __name__ == '__main__':
    data = ['我是中国人，爱吃中国菜',
            '你是日本人，滚回日本岛']
    wc = WordCounter(data)
    c = wc.count_res
    print(c)
    print(sum(c.values()))

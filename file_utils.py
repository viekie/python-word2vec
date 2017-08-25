#!/usr/bin/env python
# -*- coding: utf8 -*-
# Power by viekie2017-08-25 13:50:37
##
# @file file_utils.py
# @brief
# @author viekiedu@gmail.com
# @version 1.0
# @date 2017-08-25

import csv
import pickle


def read_csv(file):
    with open(file, 'r') as f:
        reader = csv.reader(f)
        data = [row for row in reader]
        return data


def load_pickle(file):
    with open(file, 'rb') as f:
        data = pickle.load(f)
        return data


def save_pickle(data, file):
    with open(file, 'wb') as f:
        pickle.dump(data, f)

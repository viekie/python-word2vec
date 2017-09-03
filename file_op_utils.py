#!/usr/bin/env python
# -*- coding: utf8 -*-
# Power by viekie2017-09-03 16:20:29

import csv
import pickle


def read_csv(f):
    if f is not None:
        with open(f, 'r') as file:
            reader = csv.read(file)
            data = [row for row in reader]
            return data
    else:
        raise ValueError


def read_pickle(f):
    if f is not None:
        with open(f, 'rb') as file:
            reader = pickle.load(file)
            return reader
    else:
        raise ValueError


def save_pickle(f, d):
    if f is not None:
        with open(f, 'wb') as file:
            pickle.save(d, file)
    else:
        raise ValueError


if __name__ == '__main__':
    read_pickle('./static/stop_words.pkl')

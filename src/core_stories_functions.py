from collections import Counter
from itertools import groupby, chain
from math import floor

import spacy


def tokenize(book):
    '''Operates in-place on the book to add
    - chapter body_tokens
    - chapter token_list
    - chapter token_counts
    - top-level (whole book) token_list
    - top-level (whole book) token_counts
    '''
    nlp = spacy.load("en_core_web_lg")

    for chapter in book['chapters']:
        chapter['body_tokens'] = nlp(chapter['body_raw'].replace('---', ' ').replace('--', ' ').replace('\n',' '))
        # could use token.is_sent_start to only lower-case the sentence starts
        # but don't rely on that. we'll lose proper pronouns, but we don't need them
        chapter['token_list'] = [str(token).lower() for token in chapter['body_tokens'] if (not token.is_punct) and (not token.is_space) and (not token.is_quote) and (not token.is_bracket)]
        chapter['token_counts'] = Counter({k: len(list(g)) for k, g in groupby(sorted(chapter['token_list']))})

    book['token_list'] = list(chain.from_iterable([x['token_list'] for x in book['chapters']]))
    # book['token_counts'] = {k: len(list(g)) for k, g in groupby(sorted(book['token_list']))}
    book['token_counts'] = sum([chapter['token_counts'] for chapter in book['chapters']], Counter())


def split_fixed_size(iterable, chunks):
    '''Split into N chunks.'''
    n = len(iterable)
    endpoints = [floor(i*n/chunks) for i in range(chunks+1)]
    return [Counter({k: len(list(g)) for k, g in groupby(sorted(iterable[endpoints[i]:endpoints[i+1]]))}) for i in range(chunks)]


def test_split_fixed_size(moby_dick):
    split_fixed_size(moby_dick['token_list'][:221], 22)
    [sum(x.values()) for x in split_fixed_size(moby_dick['token_list'][:220], 22)]
    [sum(x.values()) for x in split_fixed_size(moby_dick['token_list'][:221], 1)]
    [sum(x.values()) for x in split_fixed_size(moby_dick['token_list'][:223], 2)]
    [sum(x.values()) for x in split_fixed_size(moby_dick['token_list'][:229], 10)]


def split_min_size(iterable, min_size=10000):
    '''Split into as many chunks as possible with min size.'''
    n = len(iterable)
    chunks = floor(n/min_size)
    return split_fixed_size(iterable, chunks)


def test_split_min_size(moby_dick):
    split_min_size(moby_dick['token_list'][:221], min_size=10)
    [sum(x.values()) for x in split_min_size(moby_dick['token_list'][:220], min_size=10)]
    [sum(x.values()) for x in split_min_size(moby_dick['token_list'][:221], min_size=10)]
    [sum(x.values()) for x in split_min_size(moby_dick['token_list'][:223], min_size=10)]
    [sum(x.values()) for x in split_min_size(moby_dick['token_list'][:229], min_size=10)]


def split_sliding(iterable, window=10000, num_points=100):
    n = len(iterable)

    # check for unreasonable arguments:
    if n > ( window * num_points ):
        print("WARNING: windows will be disjoint at window size", window, ". using a equal split into", num_points, "segments instead")
        return split_fixed_size(iterable, num_points)
    elif n <= window:
        print("WARNING: book is smaller than window size", window, "all the points will be the same")

    starts = [floor(i*max((n-window),0)/(num_points-1)) for i in range(num_points)]
    # can check these if you want:
    # endpoints = [(starts[i], starts[i]+window) for i in range(num_points)]
    # could add and remove counters at each step to be more efficient (potentially)
    return [Counter({k: len(list(g)) for k, g in groupby(sorted(iterable[starts[i]:starts[i]+window]))}) for i in range(chunks)]
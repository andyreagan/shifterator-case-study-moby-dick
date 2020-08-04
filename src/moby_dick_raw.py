# coding: utf-8
import requests
import re
from core_stories_functions import tokenize, split_fixed_size
from moby_dick import without_stopwords, with_stopwords


def get_raw_book(uri: str='http://www.gutenberg.org/files/2701/2701.txt') -> list:
    r = requests.get(uri)
    r.raise_for_status()
    raw_text = r.content.decode('utf8')
    lines = raw_text.split('\r\n')
    # print(len(lines))
    return lines


is_chapter = lambda x: re.match('\s*CHAPTER [0-9]+', x) is not None
is_etymology = lambda x: re.match('.*?ETYMOLOGY.*?', x) is not None


def main():
    lines = get_raw_book()
    chapter_lines = [(i, lines[i]) for i in range(len(lines)) if is_chapter(lines[i])]
    chapter_headings = [(i+2, lines[i+2]) for i, line in chapter_lines]
    start = chapter_lines[0]
    end = [(i, lines[i]) for i in range(len(lines)) if is_etymology(lines[i])][0]

    x = chapter_lines + [end]

    chapter_bodies = [('\n'.join(lines[x[i][0]+3:x[i+1][0]])).strip('\n') for i in range(len(chapter_lines))]

    assert len(chapter_bodies) == len(chapter_headings)

    moby_dick = {
        'title': 'Moby Dick',
        'author': 'Herman Melville',
        'chapters': [{
            'title': x[1].strip(),
            'body_raw': y} for x, y in zip(chapter_headings, chapter_bodies)]}

    tokenize(moby_dick)

    # these are the stats on word types, number of tokens reported in methods:
    [(len(x), sum(x.values())) for x in split_fixed_size(moby_dick['token_list'], 1)]
    [(len(x), sum(x.values())) for x in split_fixed_size(moby_dick['token_list'], 2)]
    left, right = split_fixed_size(moby_dick['token_list'], 2)

    without_stopwords(left, right)
    with_stopwords(left, right)



if __name__ == '__main__':
    main()
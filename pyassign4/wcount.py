"""wcount.py: count words from an Internet file.

__author__ = 'Li Hongyu'
__pkuid__ = '1700017785'
__email__ = 'hongyuli@pku.edu.cn'"""

import sys
from urllib.request import urlopen


def wcount(lines, topn=10):
    """count words from lines of text string, then sort by their counts
    in reverse order, output the topn (word count), each in one line."""

    lines = lines.lower()
    new_lines = ''
    times = {}
    for i in range(len(lines)):
        # remove the punctuations, except - and '
        if lines[i] in ',.;:?!"%()[]#@&*$/_0123456789':
            new_lines += ' '
        # remove dash(--) but not connector(-)
        elif lines[i:i + 2] == '--' or lines[i - 1:i + 1] == '--':
            new_lines += ' '
        else:
            new_lines += lines[i]

    words = new_lines.split()
    vocabulary = set(words)
    for word in vocabulary:
        times[word] = words.count(word)
    times = sorted(times.items(), key=lambda t: t[1], reverse=True)
    # after being sorted, now times is a list of tuples
    if topn > len(times):
        topn = len(times)
    for i in range(topn):
        print('{:20s}{}'.format(times[i][0], times[i][1]))


def get_text(url, topn=10):
    """access the url and get the text as str,
    then call the function wcount to analyze it"""

    try:
        with urlopen(url) as url_obj:
            lines = url_obj.read().decode(encoding='utf-8-sig')
    # change the encoding method from 'utf-8' to 'utf-8-sig'
    # to remove the error code '\ufeff'
    except Exception as ex:
        print(ex)
    else:
        wcount(lines, topn)


def main():
    '''check if the calling method is correct,
    then call the function get_text to access the url'''

    if len(sys.argv) == 1:
        print('Usage: {} url [topn]'.format(sys.argv[0]))
        print('  url: URL of the txt file to analyze ')
        print('  topn: how many (words count) to output.' +
              ' If not given, will output top 10 words')
        sys.exit(1)

    elif len(sys.argv) == 2:
        get_text(sys.argv[1])

    elif len(sys.argv) == 3:
        try:
            get_text(sys.argv[1], int(sys.argv[2]))
        except ValueError:
            print('Wrong input:' +
                  'Alternative parameter [topn] must be an integer')

    else:
        print('Usage: {} url [topn]'.format(sys.argv[0]))
        print('  url: URL of the txt file to analyze ')
        print('  topn: how many (words count) to output.' +
              ' If not given, will output top 10 words')
        sys.exit(1)


if __name__ == '__main__':
    main()

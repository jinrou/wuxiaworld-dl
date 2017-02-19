#! /usr/bin/env python
# -*- coding: utf-8 -*-

""" 
Example: python wuxiaworld-dl.py --name=coiling-dragon \
--indexpath="http://www.wuxiaworld.com/cdindex-html/"\
 --outputdir=./out --book=16 --numberofchapters=32
"""

import click
import lxml.html


class Novel:
    """
    Class for operate with novel

    Example:
    n = Novel('coiling-dragon', 'http://www.wuxiaworld.com/cdindex-html/')
    n.download(16, 32)

    """

    def __init__(self, name, index_path, outdir):
        self.name = name
        self.index_path = index_path
        self.outdir = outdir

    def download(self, book, number_of_chapters):
        "download all chapters of book in one file"
        with open(self._book_path(book), 'w') as f:
            for i in xrange(1, number_of_chapters + 1):
                url = self._chapter_url(book, i)
                root = lxml.html.parse(url)
                content = root.xpath('//div[@itemprop="articleBody"]')
                f.write(content[0].text_content().encode("utf-8"))

    def _chapter_url(self, book, chapter):
        "return chapter url"
        return '{}book-{}-chapter-{}/'.format(self.index_path,
                                              book, chapter)

    def _book_path(self, book):
        "return book path"
        return '{}/{}-book-{}.txt'.format(self.outdir, self.name, book)


@click.command()
@click.option('--name', help='novel name; example: --name=coiling-dragon')
@click.option('--indexpath', help='index path for novel; example: --indexpath="http://www.wuxiaworld.com/cdindex-html/"')
@click.option('--outputdir', help='output dir; example: --outputdir=./out')
@click.option('--book', help='book number; example: --book=16')
@click.option('--numberofchapters', help='number of chapters in book; example: --numberofchapters=32')
def main(name, indexpath, outputdir, book, numberofchapters):
    n = Novel(name, indexpath, outputdir)
    n.download(int(book), int(numberofchapters))

if __name__ == '__main__':
    main()

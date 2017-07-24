#! /usr/bin/env python3
"""output contents of DocTree data file to separate documents
"""
import argparse
from doctree.doctree_2print import main


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-f', '--file', dest='fname')
    parser.add_argument('-H', '--html', dest='as_html', action='store_true',
                        help='leave contents as stored instead of parsed into plain text')
    parser.add_argument('-v', '--verbose', dest='to_files', action='store_true',
                        help='echo output instead of sent to file')
    args = parser.parse_args()
    main(args.fname, args.as_html, args.to_files)

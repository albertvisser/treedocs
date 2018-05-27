#! /usr/bin/env python3
"""output contents of DocTree data file to one or more documents
"""
import argparse
from doctree.doctree_2print import main


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__,
                                     epilog="output files are created "
                                     "in the same directory as the input file "
                                     "and end with .out")
    parser.add_argument('fname', help="name of DocTree file")
    parser.add_argument('-H', '--html', dest='as_html', action='store_true',
                        help='leave contents as stored instead of parsed into '
                             'plain text')
    parser.add_argument('-s', '--separate', dest='to_files', action='store_true',
                        help='write output to separate files instead of to a '
                             'single one (filenames are generated)')
    args = parser.parse_args()
    main(args.fname, args.as_html, args.to_files)

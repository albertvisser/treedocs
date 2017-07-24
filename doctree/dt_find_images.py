"""Leesbaar weergeven van een DocTree data file
"""
## import os
import sys
import pickle as pck
import bs4 as bs


def main(fname):
    """
    Als het opgegeven bestand een doctree structuur bevat, geef deze dan weer
    in een leesbare vorm

    uit de html voor in de edit velden wordt de tekst geëxtraheerd tenzij
    een tweede argument opgegeven is
    """

    # try to open the input file, if not present do not create output but fail
    with open(fname, "rb") as f_in, open(fname + '.list', 'w') as _out:

        # get the input from the file
        nt_data = pck.load(f_in)

        # if this is not a list whose first element is a dictionary that contains a specific key
        # then this is definitely not a doctree structure
        try:
            test = nt_data[0]["AskBeforeHide"]
        except (ValueError, KeyError):
            return "{} is not a valid Doctree data file".format(fname)

        for key, value in nt_data[2].items():
            title, data = value
            names = [img['src'] for img in bs.BeautifulSoup(data).find_all('img')]
            for name in names:
                _out.write("{} {} {}\n".format(name, key, title))

if __name__ == '__main__':
    main(sys.argv[1])

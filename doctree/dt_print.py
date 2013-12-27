# -*- coding: utf-8 -*-
import sys
import pprint
import pickle as pck
import bs4 as bs


def filter_html(data):
    """
    behandel de data als een html document en geeft de inhoud van de html body terug
    als een string. Indien niet aanwezig: geef een lege string terug
    """
    soup = bs.BeautifulSoup(data)
    if soup.html:
        body = soup.html.body
        return body.get_text()
    else:
        return ''


def main(fname, donot_filter_html=False):
    """
    Als het opgegeven bestand een doctree structuur bevat, geef deze dan weer
    in een leesbare vorm

    uit de html voor in de edit velden wordt de tekst geëxtraheerd tenzij
    een tweede argument opgegeven is
    """

    # try to open the input file, if not present do not create output but fail
    with open(fname, "rb") as f_in, open(fname + '.out', 'w') as _out:

        # get the input from the file
        nt_data = pck.load(f_in)

        # if this is not a list whose first element is a dictionary that contains a specific key
        # then this is definitely not a doctree structure
        try:
            test = nt_data[0]["AskBeforeHide"]
        except (ValueError, KeyError):
            return "{} is not a valid Doctree data file".format(self.project_file)

        # pprint the first element; a dictionary with settings
        print('options:', file=_out)
        options = nt_data[0]
        if donot_filter_html:
            pass
        else:
            for opt in options:
                if opt == 'RootData': # deze bevat HTML; dus eerst filteren
                    options[opt] = filter_html(options[opt])
        pprint.pprint(options, stream=_out)

        # pprint the second element: the view(s) (lists of lists)
        print('views', file=_out)
        pprint.pprint(nt_data[1], stream=_out)

        # pprint the third element: a dictionary with node titles en texts
        print('itemdict', file=_out)
        if donot_filter_html:
            itemdict = nt_data[2]
        else:
            itemdict = {x: (y[0], filter_html(y[1])) for x, y in nt_data[2].items()}
        pprint.pprint(itemdict, stream=_out)


if __name__ == '__main__':
    # plac is used to parse the command line arguments
    import plac; plac.call(main)

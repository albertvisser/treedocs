"""DocTree utility program to present the data in a viewable form
"""
import os.path
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


def write_file(fname, title, data, as_html):
    """
    schrijf `data` weg als "`title`.html of `title`.out"
    """
    root, base = os.path.split(fname)
    base, _ = os.path.splitext(base)
    ext = '.html' if as_html else '.out'
    outfile = os.path.join(root, '_'.join((base, '_'.join(title.split()))) + ext)
    with open(outfile, 'w') as _out:
        _out.write(data)


def main(fname, *, donot_filter_html=False, to_files=False):
    """Produce readable output from a DocTree document collection

    :param fname: name of DocTree file
    :param donot_filter_html: leave contents as stored instead of parsed into
                              plain text
    :param to_files: write output to separate files instead of to a single one
                    (filenames are generated)

    output files are created in the same directory as the input file and end with
    .out
    """
    ## """
    ## Als het opgegeven bestand een doctree structuur bevat, geef deze dan weer
    ## in een leesbare vorm

    ## uit de html voor in de edit velden wordt de tekst geëxtraheerd tenzij
    ## een tweede argument opgegeven is
    ## """

    print(fname)
    print('donot-filter-html:', donot_filter_html)
    print('to-files:', to_files)
    # try to open the input file, if not present do not create output but fail
    with open(fname, "rb") as f_in, open(fname + '.out', 'w') as _out:

        # get the input from the file
        nt_data = pck.load(f_in)

        # if this is not a list whose first element is a dictionary that contains a specific key
        # then this is definitely not a doctree structure
        try:
            test = nt_data[0]["AskBeforeHide"]
        except (ValueError, KeyError):
            return "{} is not a valid Doctree data file".format(fname)

        # pprint the first element; a dictionary with settings
        options = nt_data[0]
        for opt in options:
            if opt == 'RootData':
                if to_files:
                    if donot_filter_html:
                        pass
                    else:
                        options[opt] = filter_html(options[opt])
                    write_file(fname, opt, options[opt], donot_filter_html)
                else:
                    print('options:', file=_out)
                    pprint.pprint(options, stream=_out)

        # pprint the second element: the view(s) (lists of lists)
        if not to_files:
            print('views', file=_out)
            pprint.pprint(nt_data[1], stream=_out)

        # pprint the third element: a dictionary with node titles en texts
        if donot_filter_html:
            itemdict = nt_data[2]
        else:
            itemdict = {x: (y[0], filter_html(y[1])) for x, y in nt_data[2].items()}
        if to_files:
            for key, value in itemdict.items():
                write_file(fname, " ".join((str(key), value[0])), value[1],
                           donot_filter_html)
        else:
            print('itemdict', file=_out)
            pprint.pprint(itemdict, stream=_out)

"""DocTree utility program to present the data in a viewable form
"""
import pathlib
import tempfile
import zipfile as zpf
import json
import pprint
import bs4 as bs


def main(fname, donot_filter_html=False, to_files=False):
    """Produce readable output from a DocTree document collection

    :param fname: name of DocTree file
    :param donot_filter_html: leave contents as stored instead of parsed into
                              plain text
    :param to_files: write output to separate files instead of to a single one
                    (filenames are generated)

    output files are created in the same directory as the input file and end with
    .out
    """
    # """
    # Als het opgegeven bestand een doctree structuur bevat, geef deze dan weer
    # in een leesbare vorm

    # uit de html voor in de edit velden wordt de tekst geëxtraheerd tenzij
    # een tweede argument opgegeven is
    # """

    infile = pathlib.Path(fname)
    temp_imagepath = pathlib.Path(tempfile.mkdtemp())
    extra = 'as-saved' if donot_filter_html else 'text-only'
    print('donot-filter-html:', donot_filter_html)
    print('to-files:', to_files)
    extracted = extract_json_data(infile, temp_imagepath)
    if not extracted:
        return 'no data portion found in file'
    new = pathlib.Path(fname + f'-{extra}.out')
    new_gen = pathlib.Path(fname + f'-{extra}{"_general" if to_files else ""}.out')
    with extracted.open("rb") as f_in, new_gen.open('w') as _out:

        # get the input from the file
        nt_data = json.load(f_in)

        try:
            _test = nt_data['0']["AskBeforeHide"]
        except (TypeError, KeyError):
            return f"{fname} is not a valid Doctree data file"
        if any(('1' not in nt_data, '2' not in nt_data, '3' not in nt_data)):
            return f"{fname} is not a valid Doctree data file"

        # pprint the first element; a dictionary with settings
        # if donot-filter-html and to_files print the root item separately
        options = nt_data['0']
        if donot_filter_html:
            if to_files:
                write_file(new, title2filename(f'rootitem {options["RootTitle"]}'),
                           options["RootData"], donot_filter_html)
        else:
            options['RootData'] = filter_html(options['RootData'])
        print_plain('options', options, _out)

        # pprint the second element: the view(s) (lists of lists)
        print_plain('views', nt_data['1'], _out)

        # pprint the third element: a dictionary with node titles en texts
        if donot_filter_html:
            itemdict = nt_data['2']
        else:
            itemdict = {x: (y[0], filter_html(y[1])) for x, y in nt_data['2'].items()}
        if to_files:
            for key, value in itemdict.items():
                write_file(new, title2filename(f"{key:>03} {value[0]}"), value[1],
                           donot_filter_html)
        else:
            print_plain('itemdict', itemdict, _out)

        print_plain('text positions', nt_data['3'], _out)
        return 'done.'


def title2filename(title):
    """maak titel geschikt om als filenaam(deel) gebruikt te worden
    """
    return title.replace('/', '-')


def write_file(outfile, title, data, as_html):
    """
    schrijf `data` weg als "`title`.html of `title`.out"
    """
    root = outfile.parent
    base = outfile.stem
    ext = '.html' if as_html else '.out'
    outfile = root / '_'.join((base, '-'.join(title.split()) + ext))
    with outfile.open('w') as _out:
        _out.write(data)


def filter_html(data):
    """
    behandel de data als een html document en geeft de inhoud van de html body terug
    als een string. Indien niet aanwezig: geef een lege string terug
    """
    soup = bs.BeautifulSoup(data, 'lxml')
    if soup.html:
        body = soup.html.body
        return body.get_text()
    return ''


def extract_json_data(infile, temp_imagepath):
    """try to open the input file, if not present do not create output but fail
    """
    with zpf.ZipFile(infile) as zipped:
        imagelist = zipped.namelist()
        for name in imagelist:
            if name.endswith('.json'):
                zipped.extract(name, path=temp_imagepath)
                return temp_imagepath / name


def print_plain(heading, data, _out):
    """pprint part odf the data in a standard way
    """
    print(f'----- {heading}:', file=_out)
    pprint.pprint(data, width=200, stream=_out)

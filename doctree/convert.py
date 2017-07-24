#! /usr/bin/env python
"""
DocTree data file conversion program
usage: [python] convert.py [<filename> [<method>]]

<filename> is a pre-richedit doctree file, can even be a pre-views one.
           If none is given, the name 'MyMan.ini' is used.
<method> can be 'wx' or 'qt', if none is given 'qt' is used.
"""
from __future__ import print_function
import os
import sys
import cPickle as pck
## import pprint

data_list = []
items_list = {}


def unravel(item):
    "recursieve functie voor het opbouwen van de view"
    titel, tekst, subitems = item
    newkey = len(items_list)
    items_list[newkey] = (titel, tekst)
    subitem_list = []
    data_item = (newkey, subitem_list)
    for subitem in subitems:
        subitem_list.append(unravel(subitem))
    return data_item


def convert(data):
    """
    self.nt_data = {
        0: {
            naam instelling: waarde voor instelling
            };
        n: (
            titel,
            tekst,
            subitems
            );
        }
    een dictionary met genummerde keys
        de eerste heeft als waarde een dictionary met instellingen
        de volgende hebben als waarde een tuple bestaande uit de titel, de tekst en
            en list met onderliggende waarden, deze zijn op dezelfde manier opgebouwd

    omzetten naar

    self.nt_data = {
        0: {
            naam instelling: waarde voor instelling, [...]
            };
        1: [
            (verwijzing naar item, lijst met subitems), [...]
            ];
        2: {
            verwijzing: data-item, [...]
            }
        }
    subitem: net zo opgebouwd als item dus als (verwijzing naar item, lijst met subitems)
    data-item: opgebouwd als (titel, tekst)
    """
    try:
        data.strip()
    except AttributeError:
        pass
    else:
        print(data)
        return
    # eerst maar even kijken wat er in zit en in welke volgorde het staat
    ## for key, value in data.items():
        ## if key == 0:
            ## continue
        ## print key, value[0]
    activeitem = data[0]["ActiveItem"]
    for key, value in data.items():
        if key == 0:
            continue
        ## print key, value
        data_list.append(unravel(value))
        data.pop(key)
    data[0]["ActiveItem"] = [activeitem]
    # resultaat samenstellen en opslaan
    data[0]["ActiveView"] = 0
    data[1] = (data_list,)
    data[2] = items_list


def make_richtext(data, methode):
    """
    plain text buffers vervangen door rich text buffers door er wat XML (voor wx versie)
    of HTML (voor qt versie) omheen te zetten
    """
    omzetdict = {'wx': "richtext_wx.xml",
                 'qt': 'richtext_qt.html'}
    try:
        fnaam = omzetdict[methode]
    except KeyError:
        raise
    with open(os.path.join(os.path.dirname(__file__), fnaam)) as f_in:
        template = f_in.read()
    print(data[0]['RootData'])
    data[0]['RootData'] = template.format(
        data[0]['RootData'].replace('\n', '<br/>').encode('utf-8'))
    for key, item in data[2].iteritems():
        titel, tekst = item
        content = template.format(tekst.replace('\n', '<br/>').encode('utf-8'))
        data[2][key] = titel, content
    return data


def main():
    """
    data file laden, unpicklen, converteren, picklen en terugschrijven
    """
    if len(sys.argv) > 1:
        filenaam = sys.argv[1]
        if 'help' in filenaam or '?' in filenaam:
            print(__doc__)
            sys.exit()
    else:
        filenaam = "MyMan.ini"
    if len(sys.argv) > 2:
        methode = sys.argv[2]
    else:
        methode = 'qt'
    with open(filenaam, "rb") as f_in:
        data = pck.load(f_in)
    if len(data) != 3:
        print('converting to multiple view format')
        convert(data)
        with open("_multi".join(os.path.splitext(filenaam)), "wb") as f_out:
            pck.dump(data, f_out)
    print('converting to rich text format')
    data = make_richtext(data, methode)
    ## pprint.pprint(data)
    with open("_{}".format(methode).join(os.path.splitext(filenaam)), "wb") as f_out:
        pck.dump(data, f_out)

if __name__ == "__main__":
    main()

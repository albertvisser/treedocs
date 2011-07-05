#! /usr/bin/env python
# -*- coding: latin-1 -*-

import os
import sys
import cPickle as pck

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
data_list = []
items_list = {}

def read_file(filenaam):
    try:
        file = open(filenaam,"rb")
    except ValueError:
        try:
            file = open(filenaam,"rb")
        except IOError:
            ## raise
            return "couldn't open "+ filenaam
    except IOError:
        ## raise
        return "couldn't open "+ filenaam
    try:
        data = pck.load(file)
    except EOFError:
        return "couldn't load data"
    file.close()
    return data

def unravel(item):
    titel, tekst, subitems = item
    newkey = len(items_list)
    items_list[newkey] = (titel, tekst)
    subitem_list = []
    data_item = (newkey, subitem_list)
    for subitem in subitems:
        subitem_list.append(unravel(subitem))
    return data_item

def convert(filenaam):
    # lezen van de data
    data = read_file(filenaam)
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
    for key, value in data.items():
        if key == 0:
            continue
        if key == data[0]["ActiveItem"]:
            data[0]["ActiveItem"] = (len(items_list),)
        data_list.append(unravel(value))
        data.pop(key)
    # resultaat bekijken
    ## for item in data_list:
        ## print item[0]
    ## for key, value in items_list.items():
        ## print key, value[0]
    # resultaat samenstellen en opslaan
    data[0]["ActiveView"] = 0
    data[1] = (data_list,)
    data[2] = items_list
    print len(data)
    file = open(filenaam + "_new","wb")
    pck.dump(data, file)
    file.close()
    return

if __name__ == "__main__":
    if sys.argv > 1:
        fnaam = sys.argv[1]
    else:
        fnaam = "MyMan.ini"
    convert(fnaam)




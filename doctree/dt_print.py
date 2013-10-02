# -*- coding: utf-8 -*-
import sys
import pprint
import pickle as pck

def main(args):
    fname = args[1]
    with open(fname, "rb") as f_in, open(fname + '.out', 'w') as _out:
        nt_data = pck.load(f_in)
        try:
            test = nt_data[0]["AskBeforeHide"]
        except (ValueError, KeyError):
            return "{} is not a valid Doctree data file".format(self.project_file)
        print('options:', file=_out)
        ## for key, value in nt_data[0].items():
            ## print('\t{}: {}'.format(key, value), file=_out)
        pprint.pprint(nt_data[0], stream=_out)
        print('views', file=_out)
        pprint.pprint(nt_data[1], stream=_out)
        print('itemdict', file=_out)
        pprint.pprint(nt_data[2], stream=_out)

if __name__ == '__main__':
    main(sys.argv)

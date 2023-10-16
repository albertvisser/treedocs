"""DocTree: data access using pickle
"""
import pickle as pck
import shutil
import zipfile as zpf
import bs4 as bs
# from doctree import shared


def read_from_files(this_file, other_file, temp_imagepath):
    "(try to) load the data"
    # determine the name of the file to read and read + unpickle it if possible,
    # otherwise cancel
    infile = other_file or this_file
    if not infile:
        return ['no file name given']
    try:
        f_in = infile.open("rb")
    except IOError:
        return [f"couldn't open {infile}"]
    with f_in:
        try:
            nt_data = pck.load(f_in)
        except (EOFError, pck.UnpicklingError):
            return [f"couldn't load data from {infile}"]

    # read/init/check settings if possible, otherwise cancel
    ## print(nt_data[0])
    try:
        test = nt_data[0].get("Application", None)
        fail = test != 'DocTree'
    except AttributeError:
        fail = True
    if fail:
        return [f"{infile} is not a valid Doctree data file"]

    # read views
    try:
        views = list(nt_data[1])
    except KeyError:
        views = [[]]

    # read itemdict
    try:
        itemdict = nt_data[2]
    except KeyError:
        itemdict = {}

    # read text positions
    try:
        text_positions = nt_data[3]
    except KeyError:
        # initialize screen positions dict
        text_positions = {x: 0 for x in itemdict}

    imagelist = []
    if not other_file:
        try:
            with zpf.ZipFile(str(this_file.with_suffix('.zip'))) as f_in:
                f_in.extractall(path=temp_imagepath)
                imagelist = f_in.namelist()
        except FileNotFoundError:
            pass

    return nt_data[0], views, itemdict, text_positions, imagelist


def verify_imagenames(items_to_move, temp_imagepath, other_file):
    """controleer of namen van te verplaatsen images al in het doelbestand voorkomen
    zo ja, wijzig de naam dan in iets dat nog niet gebruikt is en pas de tekst waarin
    naar het image verwezen wordt ook aan
    """
    zipfile = other_file.with_suffix('.zip')
    with zpf.ZipFile(str(zipfile)) as zipped:
        names_in_target = zipped.namelist()
    highest = int(max(names_in_target).split('.')[0])

    imagelist = []
    for ix, item in enumerate(items_to_move):
        key, data = item
        title, text = data

        text_was_changed = False
        soup = bs.BeautifulSoup(text, 'lxml')
        for img in soup.find_all('img'):
            oldloc = loc = img['src']
            while loc in names_in_target:
                highest += 1
                loc = f'{highest:05}.png'
                img['src'] = loc
                text_was_changed = True
            imagelist.append(loc)
            if loc != oldloc:
                names_in_target.append(loc)
                (temp_imagepath / oldloc).rename(temp_imagepath / loc)
        if text_was_changed:
            items_to_move[ix] = (key, (title, str(soup)))

    return items_to_move, imagelist


def write_to_files(filename, opts, views, itemdict, textpositions, temp_imagepath,
                   extra_images=None, backup=True, save_images=True):
    """settings en tree data in een structuur omzetten en opslaan

    images contained exist in the temp_imagepath directory (not needed for wx)
    """
    zipfile = filename.with_suffix('.zip')
    if backup:
        try:
            shutil.copyfile(str(filename), str(filename) + ".bak")
            shutil.copyfile(str(zipfile), str(zipfile) + ".bak")
        except FileNotFoundError:
            pass
    nt_data = {0: opts, 1: views, 2: itemdict, 3: textpositions}
    with filename.open("wb") as f_out:
        pck.dump(nt_data, f_out)  # , protocol=2)`
    if not save_images:
        return []

    imagelist = []
    if extra_images:
        imagelist = extra_images
        mode = "a"
    else:
        extra_images = []
        # scan de itemdict af op image files en zet ze in een list
        for _, data in nt_data[2].values():
            imagelist.extend([img['src'] for img in bs.BeautifulSoup(data, 'lxml').find_all('img')])
        mode = "w"

    # rebuild zipfile or add extra images to the zipfile
    zipped = []
    with zpf.ZipFile(str(zipfile), mode, compression=zpf.ZIP_DEFLATED) as _out:
        for name in imagelist:
            imagepath = temp_imagepath / name
            if imagepath.exists():
                _out.write(str(imagepath), arcname=name)
                zipped.append(name)
    return zipped

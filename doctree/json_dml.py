"""DocTree: data access using pickle
"""
import os
import contextlib
import json
import shutil
import zipfile as zpf
import bs4 as bs


def read_from_files(this_file, other_file, temp_imagepath):
    "(try to) load the data"
    # pak de hele zipfile uit naar een temp directory, doe de controles en geef de gegevens terug
    # het onderscheid this_file - other_file is eigenlijk niet meer nodig
    # breakpoint()
    infile = other_file or this_file
    if not infile:
        return ['missing filename']
    try:
        with zpf.ZipFile(infile) as zipped:
            imagelist = zipped.namelist()
            zipped.extractall(path=temp_imagepath)
    except (FileNotFoundError, zpf.BadZipFile) as e:
        return [str(e)]
    for name in imagelist:
        if os.path.splitext(name)[1] == '.json':
            datafile = name
            imagelist.remove(name)
            break
    else:
        if not imagelist:
            return [f'{infile} appears to be empty']
        return [f'{infile} does not contain a data portion']

    with open(os.path.join(temp_imagepath, datafile), "r") as f_in:
        try:
            nt_data = json.load(f_in)
        # except UnicodeDecodeError:
        #     return [f"couldn't read {infile}"]
        # except json.JSONDecodeError:
        #     return [f"couldn't load data from {infile}"]
        except (UnicodeDecodeError, json.JSONDecodeError) as e:
            return [str(e)]

    # json turns number dict keys into strings, so turn them back
    nt_data = {int(x): y for (x, y) in nt_data.items()}
    test = nt_data.get(0, {}).get("Application", None)
    if test != 'DocTree':
        return [f"{infile} is not a valid DocTree data file"]

    # read views
    views = nt_data.get(1, [[]])

    # read itemdict
    itemdict = {int(x): y for (x, y) in nt_data.get(2, {}).items()}

    # read text positions
    text_positions = {int(x): y for (x, y) in nt_data.get(3, {}).items()}

    if other_file:
        imagelist = []

    return nt_data[0], views, itemdict, text_positions, imagelist


def verify_imagenames(items_to_move, temp_imagepath, other_file):
    """controleer of namen van te verplaatsen images al in het doelbestand voorkomen
    (voor het gemak vullen we gaten in de nummering niet op)
    zo ja, wijzig de naam dan in iets dat nog niet gebruikt is en pas de tekst waarin
    naar het image verwezen wordt ook aan
    """
    names_in_target, highest = determine_highest_in_zipfile(other_file)

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


def determine_highest_in_zipfile(filename):
    """loop de namen van de imagefiles langs en bepaal het hoogst gebruikte volgnummer
    """
    # in de zipped_imagelist alleen kijken naar bestanden met extensie .png
    # niet nodig omdat het data file nummer 00000 oplevert
    zipfile = filename.with_suffix('.zip')
    with zpf.ZipFile(str(zipfile)) as zipped:
        names_in_target = zipped.namelist()
    highest = int(max(names_in_target).split('.')[0]) if names_in_target else 0
    return names_in_target, highest


def write_to_files(filename, opts, views, itemdict, textpositions, temp_imagepath,
                   # extra_images=None, backup=True, save_images=True):
                   backup=True, save_images=True):
    """settings en tree data in een structuur omzetten en opslaan

    filename is hier een Path, geen string
    images contained exist in the temp_imagepath directory (not needed for wx)
    """
    nt_data = {0: opts, 1: views, 2: itemdict, 3: textpositions}
    with (temp_imagepath / '00000.json').open("w") as f_out:
        json.dump(nt_data, f_out)

    imagelist = []
    # scan de itemdict af op image files en zet ze in een list
    # for _, data in nt_data[2].values():
    if save_images:
        for _, data in itemdict.values():
            imagelist.extend([img['src'] for img in bs.BeautifulSoup(data, 'lxml').find_all('img')])

    if backup:
        with contextlib.suppress(FileNotFoundError):
            shutil.copyfile(str(filename), str(filename) + ".bak")
    # (re)write zipfile - containing json-ed nt_data and image files
    zipped = []
    with zpf.ZipFile(str(filename), "w", compression=zpf.ZIP_DEFLATED) as _out:
        _out.write(str(temp_imagepath / '00000.json'), arcname='00000.json')
        for name in imagelist:
            imagepath = temp_imagepath / name
            if imagepath.exists():
                _out.write(str(imagepath), arcname=name)
                zipped.append(name)
    return zipped

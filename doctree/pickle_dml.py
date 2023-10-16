"""DocTree: data access using pickle
"""
import pickle as pck
import shutil
import zipfile as zpf
from doctree import shared


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


def write_to_files(filename, opts, views, itemdict, textpositions, temp_imagepath,
                   extra_images=None, new_keys=None,
                   backup=True, save_images=True, origin=None):
    """settings en tree data in een structuur omzetten en opslaan

    images contained are saved in a separate zipfile"""
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
    # if toolkit == 'wx':  # wx versie doet niet aan externe images
    #     return ''
    if not save_images:
        return []

    imagelist = []
    if extra_images is None:
        extra_images = []
        # scan de itemdict af op image files en zet ze in een list
        for _, data in nt_data[2].values():
            names = shared.get_imagenames(data)
            imagelist.extend(names)
        ## fname = os.path.basename(filename)
        mode = "w"
    else:
        # bepalen welke namen er nu in het doelbestand zitten, met het oog op mogelijke duplicaten
        names_in_target = zpf.ZipFile(str(zipfile)).namelist()
        highest= int(max(names_in_target).split('.')[0])
        renamed = {}
        for name in extra_images:
            oldname = name
            while name in names_in_target:
                highest += 1
                name = f'{highest:05}.png'
                renamed[oldname] = name
            (temp_imagepath / oldname).rename(temp_imagepath / name)
            names_in_target.append(name)
            imagelist.append(name)
        if renamed:
            for key in new_keys:
                names = shared.get_imagenames(itemdict[key])
                for name in names:
                    if name in renamed:
                        # m.b.v. BeautifulSoup itemdict waarde aanpassen zie conversieprogramma
                        pass
            nt_data = {0: opts, 1: views, 2: itemdict, 3: textpositions}
            with filename.open("wb") as f_out:
                pck.dump(nt_data, f_out)  # , protocol=2)`
        mode = "a"
        # plaatjes uit verplaatste items kopieren indien nodig
        # dankzij apart temporary image path niet meer nodig
        # if origin and origin.parent != filename.parent:
        #     for name in extra_images:  # als dit het doet aparte functie dml.movefiles van maken
        #         src = origin.parent / name
        #         dest = filename.parent / name
        #         shutil.copyfile(str(src), str(dest))

    # rebuild zipfile or add extra images to the zipfile
    zipped = []
    with zpf.ZipFile(str(zipfile), mode, compression=zpf.ZIP_DEFLATED) as _out:
        for name in imagelist:
            # if name.startswith(str(filename)):
            imagepath = temp_imagepath / name
            if imagepath.exists():
                ## _out.write(os.path.join(path, name), arcname=os.path.basename(name))
                # _out.write(str(path / name), arcname=pathlib.Path(name).name)
                _out.write(str(imagepath), arcname=name)
                zipped.append(name)
    # plaatjes uit verplaatste items fysiek verwijderen
    # dankzij apart temporary image path niet meer nodig
    # if origin and origin.parent != filename.parent:
    #     for name in extra_images:
    #         dest = filename.parent / name
    #         dest.unlink()
    return zipped

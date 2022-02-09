"""DocTree: data access using pickle
"""
import pickle as pck
import shutil
import zipfile as zpf
import doctree.shared as shared


def read_from_files(this_file, other_file):
    "(try to) load the data"
    # determine the name of the file to read and read + unpickle it if possible,
    # otherwise cancel
    infile = other_file or this_file
    if not infile:
        return ['no file name given']
    try:
        f_in = infile.open("rb")
    except IOError:
        return ["couldn't open {}".format(str(infile))]
    with f_in:
        try:
            nt_data = pck.load(f_in)
        except EOFError:
            return ["couldn't load data from {}".format(str(infile))]

    # read/init/check settings if possible, otherwise cancel
    ## print(nt_data[0])
    test = nt_data[0].get("Application", None)
    if test and test != 'DocTree':
        return ["{} is not a valid Doctree data file".format(str(infile))]

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
        # if possible, build a list of referred-to image files
        ## path = os.path.dirname((self.project_file))
        path = str(this_file.parent)
        try:
            with zpf.ZipFile(str(this_file.with_suffix('.zip'))) as f_in:
                f_in.extractall(path=path)
                imagelist = f_in.namelist()
        except FileNotFoundError:
            pass

    return nt_data[0], views, itemdict, text_positions, imagelist


def write_to_files(filename, opts, views, itemdict, textpositions, toolkit, extra_images=None,
                   backup=True, save_images=True, origin=None):
    """settings en tree data in een structuur omzetten en opslaan

    images contained are saved in a separate zipfile"""
    nt_data = {0: opts, 1: views, 2: itemdict, 3: textpositions}
    zipfile = filename.with_suffix('.zip')
    if backup:
        try:
            shutil.copyfile(str(filename), str(filename) + ".bak")
            shutil.copyfile(str(zipfile), str(zipfile) + ".bak")
        except FileNotFoundError:
            pass
    with filename.open("wb") as f_out:
        pck.dump(nt_data, f_out)  # , protocol=2)
    if toolkit == 'wx':  # wx versie doet niet aan externe images
        return ''
    if not save_images:
        return ''

    if extra_images is None:
        extra_images = []
        # scan de itemdict af op image files en zet ze in een list
        imagelist = []
        for _, data in nt_data[2].values():
            names = shared.get_imagenames(data)
            imagelist.extend(names)
        ## fname = os.path.basename(filename)
        mode = "w"
    else:
        imagelist = extra_images
        mode = "a"
        # plaatjes uit verplaatste items kopieren indien nodig
        if origin and origin.parent != filename.parent:
            for name in extra_images:  # als dit het doet aparte functie dml.movefiles van maken
                src = origin.parent / name
                dest = filename.parent / name
                shutil.copyfile(str(src), str(dest))

    # rebuild zipfile or add extra images to the zipfile
    path = filename.parent  # eventueel eerst absoluut maken
    zipped = []
    with zpf.ZipFile(str(zipfile), mode) as _out:
        for name in imagelist:
            # if name.startswith(str(filename)):
            imagepath = path / name
            if imagepath.exists():
                ## _out.write(os.path.join(path, name), arcname=os.path.basename(name))
                # _out.write(str(path / name), arcname=pathlib.Path(name).name)
                _out.write(str(imagepath), arcname=name)
                zipped.append(name)
    # plaatjes uit verplaatste items fysiek verwijderen
    if origin and origin.parent != filename.parent:
        for name in extra_images:
            dest = filename.parent / name
            dest.unlink()
    return zipped

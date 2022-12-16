"""Data processing routines for MongoDB version
"""
# import datetime
# import shutil
# import pathlib
from pymongo import MongoClient
# from pymongo.collection import Collection
cl = MongoClient()
db = cl.doctree_database
# support for older pymongo versions
# try:
#     test = Collection.update_one
# except AttributeError:
#     ## Collection.insert_one = Collection.insert
#     Collection.update_one = Collection.update
#     Collection.replace_one = Collection.update
#     ## # Collection.find_one_and_delete = Collection.remove
#     Collection.delete_many = Collection.remove


def _add_doc(filename, doc):
    """create new document in the dtree document
    """
    # try:
    id_ = db[filename].insert_one(doc).inserted_id
    # except TypeError:
    #     id_ = db[filename].insert(doc)
    return id_


def _update_doc(filename, docid, doc):
    """change a document in the dtree document
    """
    db[filename].update_one({'_id': docid}, doc)


def list_dtrees():
    """list all dtrees (collections) registered in the database
    """
    return db.list_collection_names()


def create_new_dtree(filename):
    """set up a new dtree/  """
    if db[filename].find_one({'type': 'settings'}):
        raise FileExistsError
    db[filename].insert_one({'type': 'settings'})
    # db[filename].insert_one({'type': 'textpos'})
    db[filename].insert_one({'type': 'imagelist'})


def clear_dtree(filename, recreate=False):
    """remove (all data from) a dtree/collection
    """
    if not db[filename].find_one({'type': 'settings'}):
        raise FileNotFoundError
    db[filename].drop()
    if recreate:
        create_new_dtree(filename)


def read_dtree(filename, readable=False):
    """read and return all data from a dtree/collection
    """
    if not readable:
        return db[filename].find()
    views, itemdict, textpos = [], {}, {}
    for item in read_dtree(filename):
        if item['type'] == 'settings':
            opts = item['data']
        elif item['type'] == 'view':
            views.append(item['data'])
        elif item['type'] == 'textitem':
            itemdict[item['textid']] = item['data']
            textpos[item['textid']] = item['textpos']
    # imagelist = []  # db[filename].find_one({'type': 'imagelist'})['data']
    return opts, views, itemdict, textpos  # , imagelist


def rename_dtree(filename, newname):
    """change the dtree/collection's name if possible
    """
    if db[newname].find_one({'type': 'settings'}) is not None:
        raise FileExistsError('new_name_taken')
    db[filename].rename(newname)


# ----------- deze routines komen uit main - ombouwen voor mongodb
def read_from_files(this_file, other_file=''):
    "(try to) load the data"
    filename = other_file or this_file
    if not filename:
        return ['no file name given']

    # read/init/check settings if possible, otherwise cancel
    opts = db[filename].find_one({'type': 'settings'})['data']
    if opts.get('Application', '') != 'DocTree':
        return [f"{filename} is not a valid Doctree data file"]  # is dit een Path?

    # read views
    views_from_db = db[filename].find({'type': 'view'})
    views = [x['data'] for x in sorted(views_from_db, key=lambda x: x['viewno'])]

    # read itemdict
    # read text positions
    data_from_db = list(db[filename].find({'type': 'textitem'}))
    itemdict = {x['textid']: x['data'] for x in data_from_db}
    text_positions = {x['textid']: x['textpos'] for x in data_from_db}

    # als ik geen datafile aanmaak wil ik eigenlijk ook geen zipfile hebben
    # hoe dan wel de plaatjes opslaan?
    # imagelist = []  # db[filename].find_one({'type': 'imagelist'})['data']
    # if not other_file:
    #     # if possible, build a list of referred-to image files
    #     ## path = os.path.dirname((self.project_file))
    #     path = str(this_file.parent)
    #     try:
    #         with zpf.ZipFile(str(this_file.with_suffix('.zip'))) as f_in:
    #             f_in.extractall(path=path)
    #             imagelist = f_in.namelist()
    #     except FileNotFoundError:
    #         pass

    return opts, views, itemdict, text_positions  # , imagelist


def write_to_files(filename, opts, views, itemdict, textpositions, extra_images=None,
                   backup=True, save_images=True, origin=None):
    """settings en tree data in een structuur omzetten en opslaan

    images contained are saved in a separate zipfile (not needed for wx)
    """
    # nt_data = {0: opts, 1: views, 2: itemdict, 3: textpositions}
    # zipfile = filename.with_suffix('.zip')
    # if backup:
    #     try:
    #         shutil.copyfile(str(filename), str(filename) + ".bak")
    #         shutil.copyfile(str(zipfile), str(zipfile) + ".bak")
    #     except FileNotFoundError:
    #         pass
    # with filename.open("wb") as f_out:
    #     pck.dump(nt_data, f_out, protocol=2)

    # nt_data = {'settings': opts, 'views': views, 'docdata': itemdict, 'textpos': textpositions}
    db[filename].update_one({'type': 'settings'}, {'$set': {'data': opts}})
    for seq, view in enumerate(views):
        print(seq, view)
        result = db[filename].update_one({'type': 'view', 'viewno': seq},
                                         {'$set': {'data': view}}, upsert=True)
        print(result.raw_result)
    # kan dit met updatemany? Nou zo in elk geval niet:
    # db[filename].update_many({'type': 'view', 'viewno': seq}, {'$set': {'data': view}},
    #                          upsert=True) for (seq, view) in enumerate(views)
    for docid, doc in itemdict.items():
        pos = textpositions[docid]
        db[filename].update_one({'type': 'textitem', 'textid': docid},
                                {'$set': {'data': doc, 'textpos': pos}}, upsert=True)
    # db[filename].update_many({'type': 'textitem', 'textid': docid},
    #                          {'$set': {'data': doc, 'textpos': textpositions[docid]}},
    #                          upsert = True) for (docid, doc) in itemdict.items()

    # TODO: bedenken hoe ik images ga doen (en dus ook hoe ik ze moet kopiëren)
    # db[filename].update_one({'type': 'imagelist'}, {'$set': {'data': []}})
    # if not save_images:
    #    return

    # if extra_images is None:
    #     # scan de itemdict af op image files en zet ze in een list
    #     imagelist = []
    #     for _, data in nt_data[2].values():
    #         names = [img['src'] for img in bs.BeautifulSoup(data, 'lxml').find_all('img')]
    #         imagelist.extend(names)
    #     ## fname = os.path.basename(filename)
    #     mode = "w"
    # else:
    #     imagelist = extra_images
    #     mode = "a"
    # # rebuild zipfile or add extra images to the zipfile
    # # FIXME: als er niks veranderd is hoeft het zipfile ook niet aangemaakt te worden?
    # #        kun je daarvoor imagelist vergelijken met self.imagelist?
    # path = filename.parent  # eventueel eerst absoluut maken
    # zipped = []
    # with zpf.ZipFile(str(zipfile), mode) as _out:
    #     for name in imagelist:
    #         # if name.startswith(str(filename)):
    #         imagepath = path / name
    #         if imagepath.exists():
    #             ## _out.write(os.path.join(path, name), arcname=os.path.basename(name))
    #             # _out.write(str(path / name), arcname=pathlib.Path(name).name)
    #             _out.write(str(imagepath), arcname=name)
    #             zipped.append(name)
    # return zipped
# misschien werkt het afhandelen van images als ik het als volgt doe:
# - een plaatje is opgeslagen als dtree001.png en wordt ook zo geïdentificeerd in de html
# - maak er een bytestream van door het te openen met PIL -> io
#   img = PIL.Image.open('dtree001.png')
#   img_bytes = io.BytesIO()
#   img.save(img_bytes, format='PNG') # dit lijkt een ingewikkelde methode om dit hierin te krijgen
#   zou het niet gewoon kunnen met
#   img_bytes = open('dtree001.png', 'rb')
# de manier om dit mongodb in te krijgen lijkt in elk geval
#   db[filename].insert_one({'type': 'image', 'name': 'dtree001.png', data: img_bytes})
#   of misschien moet je dit nog omzetten met bson.Binary(img_bytes)

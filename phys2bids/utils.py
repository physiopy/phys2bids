# -*- coding: utf-8 -*-

import json
import logging
import os
import sys
from csv import writer
from pathlib import Path

LGR = logging.getLogger(__name__)

SUPPORTED_FTYPES = ('acq', 'txt')  # 'mat', ...


def check_input_dir(indir):
    """
    Checks that the given indir doesn't have a trailing `/`
    Possibly useless if better way to handle this in Python.

    Parameters
    ----------
    indir: str or path
        A string or path that might (or not) end with a `/`

    Returns
    -------
    indir: str or path
        Same as input, but surely without trailing `/`
    """
    if indir.endswith('/'):
        indir = indir[:-1]

    return indir


def check_input_ext(filename, ext):
    """
    Checks that the given file has the given extension.
    It also treats composite extensions such as `.tsv.gz`,
    common in BIDS formats.

    Parameters
    ----------
    filename: str or path
        A string representing a file name or a fullpath
        to a file
    ext: str
        Desired file name extension. Doesn't matter if preceded by `.`

    Returns
    -------
    Path(filename).with_suffix(ext): path
        Path representing the input filename, but with corrected extension.
    """
    if filename.endswith('.gz'):
        filename = filename[:-3]

    if not ext.startswith('.'):
        ext = '.' + ext

    return Path(filename).with_suffix(ext)


def check_input_type(filename, indir):
    """
    Check which supported type is the filename.
    Alternatively, raise an error if file not found or type not supported.

    Parameters
    ----------
    filename: str or path
        A string representing a file name or a fullpath
        to a file
    indir: str or path
        A string representing a folder in which the file is,
        or a fullpath to such folder

    Returns
    -------
    fname: str or path, same as input `filename`
        Complete file name, might be the same or with an extension between
        the supported ones
    ftype: str
        Extension of the file, if the extension is supported
        and the file exists

    Raises
    ------
    Exception
        If the file doesn't exists or the extension is not supported,
        it interrupts the program and return the issue.
    """
    fftype_found = False
    for ftype in SUPPORTED_FTYPES:
        fname = check_input_ext(filename, ftype)
        if os.path.isfile(os.path.join(indir, fname)):
            fftype_found = True
            break

    if fftype_found:
        LGR.info(f'File extension is .{ftype}')
        LGR.warning('If both acq and txt files exist in the path, acq will be selected.')
        return fname, ftype
    else:
        raise Exception(f'The file {filename} wasn\'t found in {indir}'
                        f' or {ftype} is not supported yet.\n'
                        f'phys2bids currently supports:'
                        f' {", ".join(SUPPORTED_FTYPES)}')


def path_exists_or_make_it(fldr):
    """
    Check if folder exists, if not make it

    Parameters
    ----------
    fldr: str or path
        A string representing a folder,
        or a fullpath to such folder

    Notes
    -----
    Outcome:
    fldr:
        Creates the fullpath to `fldr` if it doesn't exists.
    """
    if not os.path.isdir(fldr):
        os.makedirs(fldr)


def check_file_exists(filename):
    """
    Check if file exists.

    Parameters
    ----------
    filename: str or path
        A string representing a file name or a fullpath
        to a file

    Raises
    ------
    FileNotFoundError
        If the file doesn't exists.
    """
    if not os.path.isfile(filename) and filename is not None:
        raise FileNotFoundError(f'The file {filename} does not exist!')


def move_file(oldpath, newpath, ext=''):
    """
    Moves file from oldpath to newpath.
    If file already exists, removes it first.

    Parameters
    ----------
    oldpath: str or path
        A string or a fullpath to a file that has to be moved
    newpath: str or path
        A string or a fullpath to the new destination of the file
    ext: str
        Possible extension to add to the oldpath and newpath. Not necessary.

    Notes
    -----
    Outcome:
    newpath + ext:
        Moves file to new destination
    """
    check_file_exists(oldpath + ext)

    if os.path.isfile(newpath + ext):
        os.remove(newpath + ext)

    os.rename(oldpath + ext, newpath + ext)


def copy_file(oldpath, newpath, ext=''):
    """
    Copy file from oldpath to newpath.
    If file already exists, remove it first.

    Parameters
    ----------
    oldpath: str or path
        A string or a fullpath to a file that has to be copied
    newpath: str or path
        A string or a fullpath to the new destination of the file
    ext: str
        Possible extension to add to the oldpath and newpath. Not necessary.

    Notes
    -----
    Outcome:
    newpath + ext:
        Copies file to new destination
    """
    from shutil import copy as cp

    check_file_exists(oldpath + ext)

    if os.path.isfile(newpath + ext):
        os.remove(newpath + ext)

    cp(oldpath + ext, newpath + ext)


def writefile(filename, ext, text):
    """
    Produces a textfile of the specified extension `ext`,
    containing the given content `text`.

    Parameters
    ----------
    filename: str or path
        A string representing a file name or a fullpath
        to a file
    ext: str
        Possible extension to add to the oldpath and newpath. Not necessary.
    text: str
        Text that has to be printed in `filename`

    Notes
    -----
    Outcome:
    filename + ext:
        Creates new file `filename.ext`.
    """
    with open(filename + ext, 'w') as text_file:
        print(text, file=text_file)


def writejson(filename, data, **kwargs):
    """
    Outputs a json file with the given data inside.

    Parameters
    ----------
    filename: str or path
        A string representing a file name or a fullpath
        to a file
    data: dict
        dictionary containing data to be printed in json.

    Notes
    -----
    Outcome:
    filename:
        Creates new file `filename.json`.
    """
    if not filename.endswith('.json'):
        filename += '.json'
    with open(filename, 'w') as out:
        json.dump(data, out, **kwargs)


def load_heuristic(heuristic):
    """ Loads `heuristic`, returning a callable Python module

    References
    ----------
    Copied from [nipy/heudiconv](https://github.com/nipy/heudiconv)
    Copyright [2014-2019] [Heudiconv developers], Apache 2 license.
    """
    if os.path.lexists(heuristic):
        heuristic_file = os.path.realpath(heuristic)
        path, fname = os.path.split(heuristic_file)
        try:
            old_syspath = sys.path[:]
            sys.path.append(path)
            mod = __import__(fname.split('.')[0])
            mod.filename = heuristic_file
        finally:
            sys.path = old_syspath
    else:
        from importlib import import_module
        try:
            mod = import_module(f'phys2bids.heuristics.{heuristic}')
            # remove c or o from pyc/pyo
            mod.filename = mod.__file__.rstrip('co')
        except Exception as exc:
            raise ImportError(f'Failed to import heuristic {heuristic}: {exc}')
    return mod


def append_list_as_row(file_name, list_of_elem):
    # Open file in append mode
    with open(file_name, 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        csv_writer = writer(write_obj, delimiter='\t')
        # Add contents of list as last row in the csv file
        csv_writer.writerow(list_of_elem)

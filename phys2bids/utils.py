# -*- coding: utf-8 -*-

import os
import sys


def check_input_dir(indir):
    if indir[-1:] == '/':
        indir = indir[-1:]

    return indir


def check_input_ext(file, ext):
    if file[-len(ext):] != ext:
        file = file + ext

    return file


def path_exists_or_make_it(fldr):
    """
    Check if folder exists, if not make it
    """
    if not os.path.isdir(fldr):
        os.makedirs(fldr)


def check_file_exists(file, hardexit=True):
    """
    Check if file exists.
    """
    if not os.path.isfile(file) and file is not None:
        raise FileNotFoundError('The file ' + file + ' does not exist!')


def move_file(oldpath, newpath, ext=''):
    """
    Moves file from oldpath to newpath.
    If file already exists, remove it first.
    """
    check_file_exists(oldpath + ext)

    if os.path.isfile(newpath + ext):
        os.remove(newpath + ext)

    os.rename(oldpath + ext, newpath + ext)


def copy_file(oldpath, newpath, ext=''):
    """
    Copy file from oldpath to newpath.
    If file already exists, remove it first.
    """
    from shutil import copy as cp

    check_file_exists(oldpath + ext)

    if os.path.isfile(newpath + ext):
        os.remove(newpath + ext)

    cp(oldpath + ext, newpath + ext)


def writefile(filename, ext, text):
    with open(filename + ext, 'w') as text_file:
        print(text, file=text_file)


def load_heuristic(heuristic):
    """ Loads `heuristic`, returning a callable Python module

    References
    ----------
    Copied from nipy/heudiconv
    """
    if os.path.sep in heuristic or os.path.lexists(heuristic):
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
            mod.filename = mod.__file__.rstrip('co')  # remove c or o from pyc/pyo
        except Exception as exc:
            raise ImportError(f'Failed to import heuristic {heuristic}: {exc}')
    return mod

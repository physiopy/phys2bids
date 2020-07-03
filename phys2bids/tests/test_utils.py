"""
    Runs unit tests on utils.py
"""

import json
import os
from csv import reader
from phys2bids import utils


# Tests check_input_dir
def test_check_input_dir():
    test_path = '/home/mrmeeseeks/blue/'
    assert utils.check_input_dir(test_path) == test_path[:-1]
    assert utils.check_input_dir(test_path[:-1]) == test_path[:-1]


# Tests check_input_ext
def test_check_input_ext():
    test_filename = 'help'
    ext = 'py'
    out_filename = utils.check_input_ext(test_filename, ext)
    assert str(out_filename) == f'{test_filename}.{ext}'

    test_filename = 'help.txt.gz'
    assert str(utils.check_input_ext(test_filename, ext)) == 'help.py'


# Tests check_input_type
def test_check_input_type(testpath, samefreq_full_acq_file):
    assert utils.check_input_type(samefreq_full_acq_file, testpath)


# Tests path_exists_or_make_it
def test_path_exists_or_make_it(tmpdir):
    # test_folder = '/home/travis/build/physiopy/phys2bids/tests/foo'
    test_folder = tmpdir.mkdir('foo')
    utils.path_exists_or_make_it(test_folder)
    os.path.isdir(test_folder)

    # Checking again with already existing folder
    utils.path_exists_or_make_it(test_folder)
    os.rmdir(test_folder)  # Removes the created folder


# Tests check_file_exists
def test_check_file_exists(samefreq_full_acq_file):
    utils.check_file_exists(samefreq_full_acq_file)


# Tests move_file
def test_move_file(tmpdir):
    ext = '.txt'
    test_old_path = tmpdir.join('foo.txt')
    with open(test_old_path, 'a'):
        pass
    test_old_path = str(test_old_path)[:-4]
    test_new_path = tmpdir.join('mrmeeseeks')
    utils.move_file(test_old_path, test_new_path, ext)


# Tests copy_file
def test_copy_file(tmpdir):
    ext = '.txt'
    test_old_path = tmpdir.join('foo.txt')
    test_new_path = tmpdir.join('mrmeeseeks')
    open(f'{test_old_path}.txt', 'a').close()
    utils.copy_file(test_old_path, test_new_path, ext)


# Tests writefile
def test_writefile(tmpdir):
    ext = '.txt'
    test_old_path = tmpdir.join('foo.txt')
    test_text = 'Wubba lubba dub dub!'
    utils.writefile(test_old_path, ext, test_text)


# Tests writejson
def test_writejson(tmpdir):
    test_json_filename = tmpdir.join('foo')
    test_json_data = dict(SamplingFrequency=42,
                          StartTime='00:00 ET',
                          Columns='Rick')
    utils.writejson(str(test_json_filename), test_json_data, indent=4, sort_keys=False)
    test_json_filename += '.json'
    assert os.path.isfile(test_json_filename)
    with open(test_json_filename, 'r') as src:
        loaded_data = json.load(src)
    assert test_json_data == loaded_data


# Tests load_heuristics
def test_load_heuristics():
    test_heuristic = 'heur_test_acq'
    heuristic_output_filename = utils.load_heuristic(test_heuristic).filename
    assert test_heuristic in heuristic_output_filename


# Test writing rows util
def test_append_list_as_row():
    file_name = 'test_row.tsv'
    list_of_elem = ["01", "32", 'some_info', "132.98", 'M']
    utils.append_list_as_row(file_name, list_of_elem)
    with open(file_name, mode='r') as tsv:
        tsv_read = reader(tsv, delimiter="\t")
        for row in tsv_read:
            assert row == list_of_elem

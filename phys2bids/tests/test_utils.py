"""
    Runs unit tests on utils.py
"""

import json
import os
from csv import reader
from pytest import raises

from phys2bids import utils


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

    with raises(Exception) as errorinfo:
        utils.check_input_type('nobel_prize.win', testpath)
    assert "wasn't found" in str(errorinfo.value)


# Tests check_file_exists
def test_check_file_exists(samefreq_full_acq_file):
    utils.check_file_exists(samefreq_full_acq_file)

    with raises(Exception) as errorinfo:
        utils.check_file_exists('')
    assert 'does not exist' in str(errorinfo.value)


# Tests copy_file
def test_copy_file(tmpdir):
    ext = '.txt'
    test_old_path = tmpdir.join('foo.txt')
    test_new_path = tmpdir.join('mrmeeseeks')
    open(f'{test_old_path}.txt', 'a').close()
    utils.copy_file(test_old_path, test_new_path, ext)


# Tests write_file
def test_write_file(tmpdir):
    ext = '.txt'
    test_old_path = tmpdir.join('foo.txt')
    test_text = 'Wubba lubba dub dub!'
    utils.write_file(test_old_path, ext, test_text)


# Tests write_json
def test_write_json(tmpdir):
    test_json_filename = tmpdir.join('foo')
    test_json_data = dict(SamplingFrequency=42,
                          StartTime='00:00 ET',
                          Columns='Rick')
    utils.write_json(str(test_json_filename), test_json_data, indent=4, sort_keys=False)
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

    with raises(Exception) as errorinfo:
        utils.load_heuristic('')
    assert 'Failed to import heuristic' in str(errorinfo.value)


# Test writing rows util
def test_append_list_as_row(tmpdir):
    file_name = tmpdir.join('test_row.tsv')
    list_of_elem = ["01", "32", 'some_info', "132.98", 'M']
    utils.append_list_as_row(file_name, list_of_elem)
    with open(file_name, mode='r') as tsv:
        tsv_read = reader(tsv, delimiter="\t")
        for row in tsv_read:
            assert row == list_of_elem

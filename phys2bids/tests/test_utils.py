"""
    Runs unit tests on utils.py
"""

import numpy as np
import os
from phys2bids import utils


# Tests check_input_dir
test_path = '/home/mrmeeseeks/blue/'
path_corrected = utils.check_input_dir(test_path)
assert path_corrected == test_path[:-1]

# Tests check_input_ext
test_filename = 'help'
ext = 'py'
out_filename = utils.check_input_ext(test_filename, ext)
assert str(out_filename) == f'{test_filename}.{ext}'

# Tests check_input_type
test_filename = 'Test_belt_pulse_samefreq.acq'
test_path = 'phys2bids/tests/data'
assert utils.check_input_type(test_filename, test_path)

# Tests path_exists_or_make_it
test_folder = 'phys2bids/tests/foo'
utils.path_exists_or_make_it(test_folder)
os.path.isdir(test_folder)
os.rmdir(test_folder) # Removes the created folder

# Tests check_file_exists
test_full_path = os.path.join(test_path, test_filename)
utils.check_file_exists(test_full_path)

# Tests move_file
ext = '.txt'
test_old_path = os.path.join(test_path, 'foo.txt')
open(test_old_path, 'a').close()
test_old_path = test_old_path[:-4]
test_new_path = os.path.join(test_path, 'mrmeeseeks')
utils.move_file(test_old_path, test_new_path, ext)
os.remove(f'{test_new_path}.txt')

# Tests copy_file
open(f'{test_old_path}.txt', 'a').close()
utils.copy_file(test_old_path, test_new_path, ext)
os.remove(f'{test_old_path}.txt')
os.remove(f'{test_new_path}.txt')

# Tests writefile
test_text = 'Wubba lubba dub dub!'
utils.writefile(test_old_path, ext, test_text)
os.remove(f'{test_old_path}.txt')

# Tests writejson
test_json_filename = os.path.join(test_path, 'foo')
test_json_data = dict(SamplingFrequency=42,
                      StartTime='00:00 ET',
                      Columns='Rick')
utils.writejson(test_json_filename, test_json_data, indent=4, sort_keys=False)
os.remove(f'{test_json_filename}.json')


# Tests load_heuristics
heuristic_file = 'heur_test_acq.py'
test_heuristic = os.path.join('phys2bids/heuristics', heuristic_file)
heuristic_output_filename = utils.load_heuristic(test_heuristic).filename
assert test_heuristic in heuristic_output_filename

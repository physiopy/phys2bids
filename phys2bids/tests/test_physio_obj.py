"""
Tests physio_obj.py
"""

import numpy as np
from phys2bids import physio_obj as po


# Tests is_valid
def test_is_valid():
    test_list = [0, 1, 1, 2, 3, 5, 8, 13]
    valid_output = po.is_valid(test_list, list, int)
    assert valid_output == test_list

# Tests has_size
def test_has_size():
    test_list = [0, 1, 1, 2, 3, 5, 8, 13]
    test_length = 10
    size_output = po.has_size(test_list, test_length, 0)
    assert len(size_output) == test_length

# Tests BlueprintInput
def test_BlueprintInput():
    test_time = np.array([0, 1, 1, 2, 3, 5, 8, 13])
    test_trigger = np.array([0, 1, 0, 0, 0, 0, 0, 0])
    test_timeseries = [test_time, test_trigger]
    test_freq = [42.0, 3.14]
    test_chn_name = ['Time', 'Trigger']
    test_units = ['s', 's']

    blueprint_in = po.BlueprintInput(test_timeseries, test_freq, test_chn_name, test_units)
    new_names = ['trigger', 'chocolate']
    blueprint_in.rename_channels(new_names=new_names)

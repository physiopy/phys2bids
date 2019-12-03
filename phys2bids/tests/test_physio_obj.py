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
    test_chocolate = np.array([1, 0, 0, 1, 0, 0, 1, 0])
    test_timeseries = [test_time, test_trigger, test_chocolate]
    test_freq = [42.0, 3.14, 20.0]
    test_chn_name = ['time', 'trigger', 'chocolate']
    test_units = ['s', 's', 'sweetness']
    num_channnels = len(test_timeseries)

    blueprint_in = po.BlueprintInput(test_timeseries, test_freq, test_chn_name, test_units)

    # Tests rename_channels
    new_names = ['trigger', 'time', 'lindt']
    blueprint_in.rename_channels(new_names.copy())
    assert blueprint_in.ch_name == ['time', 'trigger', 'lindt']

    # Tests return_index
    test_index = blueprint_in.return_index(1)
    assert (test_index[0] == test_trigger).all()
    assert test_index[1] == len(test_timeseries)
    assert test_index[2] == test_freq[1]
    assert test_index[3] == test_chn_name[1]
    assert test_index[4] == test_units[1]

    # Tests delete_at_index
    blueprint_in.delete_at_index(2)
    assert blueprint_in.ch_amount == num_channnels - 1

    # Tests check_trigger_amount
    blueprint_in.check_trigger_amount(thr=0.9, num_timepoints_expected=1)
    assert blueprint_in.num_timepoints_found == 1

def test_BlueprintOutput():
    test_time = np.array([0, 1, 1, 2, 3, 5, 8, 13])
    test_trigger = np.array([0, 1, 0, 0, 0, 0, 0, 0])
    test_chocolate = np.array([1, 0, 0, 1, 0, 0, 1, 0])
    test_timeseries = [test_time, test_trigger, test_chocolate]
    test_freq = [42.0, 3.14, 20.0]
    test_chn_name = ['trigger', 'time', 'chocolate']
    test_units = ['s', 's', 'sweetness']
    num_channnels = len(test_timeseries)

    blueprint_in = po.BlueprintInput(test_timeseries, test_freq, test_chn_name, test_units)

    # Tests init_from_blueprint
    blueprint_out = po.BlueprintOutput.init_from_blueprint(blueprint_in)

    # Tests return_index
    test_index = blueprint_out.return_index(1)
    assert (test_index[0] == test_trigger).all()
    assert test_index[1] == len(test_timeseries)
    assert test_index[2] == test_freq[1]
    assert test_index[3] == test_chn_name[1]
    assert test_index[4] == test_units[1]

    # Tests delete_at_index
    blueprint_out.delete_at_index(2)
    assert blueprint_out.ch_amount == num_channnels - 1


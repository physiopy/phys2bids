"""Test physio_obj.py ."""

import numpy as np
from pytest import raises

from phys2bids import physio_obj as po


# Tests is_valid
def test_is_valid():
    test_list = [0, 1, 1, 2, 3, 5, 8, 13]
    valid_output = po.is_valid(test_list, list, int)
    assert valid_output == test_list

    test_array = np.array([0, 1, 1, 2, 3, 5, 8, 13])
    valid_output = po.is_valid(test_array, np.ndarray)
    assert (valid_output == test_array).all()

    test_list = [test_array, test_array]
    valid_output = po.is_valid(test_list, list, np.ndarray)
    assert valid_output == test_list

    with raises(AttributeError) as errorinfo:
        valid_output = po.is_valid(test_array, int)
    assert "The given variable is not a" in str(errorinfo.value)


# Tests has_size
def test_has_size():
    # Check padding is correct
    test_list = [0, 1, 1, 2, 3, 5, 8, 13]
    test_length = 10
    list_check = [0, 1, 1, 2, 3, 5, 8, 13, 0, 0]
    size_output = po.has_size(test_list, test_length, 0)
    assert len(size_output) == test_length
    assert size_output == list_check

    # Check output is correct when size is the same
    test_length = 8
    size_output = po.has_size(test_list, test_length, 0)
    assert len(size_output) == test_length
    assert size_output == test_list


def test_are_equal():
    """Test are_equal ."""
    test_string = "So Long, and Thanks for All the Fish"
    test_time = np.array([0, 1, 1, 2, 3, 5, 8, 13])
    test_trigger = np.array([0, 1, 0, 0, 0, 0, 0, 0])

    class C(object):
        c = "c"

    c1 = C()
    c1.ts = [test_time, test_trigger]

    c2 = C()
    c2.ts = [test_time]

    test_half = np.array([0, 1, 2])
    test_twice = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    test_timeseries = [test_time, test_trigger, test_half, test_twice]
    test_freq = [1, 1, 0.5, 2]
    test_chn_name = ["time", "trigger", "half", "twice"]
    test_units = ["s", "V", "V", "V"]
    test_chtrig = 1

    phys_in = po.BlueprintInput(test_timeseries, test_freq, test_chn_name, test_units, test_chtrig)
    phys_out = po.BlueprintInput(
        [test_trigger, test_half, test_twice], test_freq, test_chn_name, test_units, test_chtrig
    )

    assert po.are_equal(test_string, test_string)
    assert po.are_equal(c1, c1)
    assert po.are_equal(phys_in, phys_in)
    assert po.are_equal(c1, c1.__dict__)
    assert po.are_equal(c1.__dict__, c1)
    assert not po.are_equal(c1, c2)
    assert not po.are_equal(c1, phys_in)
    assert not po.are_equal(phys_out, phys_in)
    assert not po.are_equal(phys_in, c2)
    assert not po.are_equal(c1, c2.__dict__)
    assert not po.are_equal(test_string, c1)


# Tests BlueprintInput
def test_BlueprintInput():
    test_time = np.array([0, 1, 1, 2, 3, 5, 8, 13])
    test_trigger = np.array([0, 1, 0, 0, 0, 0, 0, 0])
    test_chocolate = np.array([1, 0, 0, 1, 0, 0, 1, 0])
    test_timeseries = [test_time, test_trigger, test_chocolate]
    test_freq = [42.0, 3.14, 20.0]
    test_chn_name = ["time", "trigger", "chocolate"]
    test_units = ["s", "s", "sweetness"]
    test_chtrig = 1
    num_channnels = len(test_timeseries)

    blueprint_in = po.BlueprintInput(
        test_timeseries, test_freq, test_chn_name, test_units, test_chtrig
    )

    # Tests rename_channels
    new_names = ["trigger", "time", "lindt"]
    blueprint_in.rename_channels(new_names)
    assert blueprint_in.ch_name == ["time", "trigger", "lindt"]

    # Tests return_index
    test_index = blueprint_in.return_index(1)
    assert test_index[0] is not test_trigger
    assert (test_index[0] == test_trigger).all()
    assert test_index[1] == len(test_timeseries)
    assert test_index[2] == test_freq[1]
    assert test_index[3] == test_chn_name[1]
    assert test_index[4] == test_units[1]

    # Tests delete_at_index
    blueprint_in.delete_at_index(2)
    assert blueprint_in.ch_amount == num_channnels - 1

    # Tests check_trigger_amount
    blueprint_in.check_trigger_amount(thr=0.9, num_timepoints_expected=1)
    assert blueprint_in.num_timepoints_found == 1
    assert blueprint_in.time_offset == 1
    test_offset_time = test_time - 1
    assert np.array_equal(blueprint_in.timeseries[0], test_offset_time)

    # Tests delete_at_index with trigger channel
    blueprint_in.delete_at_index(test_chtrig)
    assert blueprint_in.ch_amount == num_channnels - 2
    assert blueprint_in.trigger_idx == 0

    # Test __eq__
    assert blueprint_in == blueprint_in

    with raises(IndexError) as errorinfo:
        blueprint_in.__getitem__(1000)
    assert "out of bounds" in str(errorinfo.value)


def test_cta_time_interp():
    """Test BlueprintInput.check_trigger_amount with time resampling."""
    test_time = np.array([0, 7])
    test_trigger = np.array([0, 1, 0, 0, 0, 0, 0, 0])
    test_timeseries = [test_time, test_trigger]
    test_freq = [42.0, 3.14]
    test_chn_name = ["time", "trigger"]
    test_units = ["s", "s"]
    test_chtrig = 1

    blueprint_in = po.BlueprintInput(
        test_timeseries, test_freq, test_chn_name, test_units, test_chtrig
    )
    # Test check_trigger_amount with time resampling
    blueprint_in.check_trigger_amount(thr=0.9, num_timepoints_expected=1)
    assert blueprint_in.num_timepoints_found == 1
    assert blueprint_in.time_offset == 1
    test_offset_time = test_time - 1
    assert np.array_equal(blueprint_in.timeseries[0], test_offset_time)


def test_BlueprintInput_slice():
    """Test BlueprintInput_slice.__getitem__ ."""
    test_time = np.array([0, 1, 2, 3, 4])
    test_trigger = np.array([0, 1, 2, 3, 4])
    test_half = np.array([0, 1, 2])
    test_twice = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    test_timeseries = [test_time, test_trigger, test_half, test_twice]
    test_freq = [1, 1, 0.5, 2]
    test_chn_name = ["time", "trigger", "half", "twice"]
    test_units = ["s", "V", "V", "V"]
    test_chtrig = 1

    phys_in = po.BlueprintInput(test_timeseries, test_freq, test_chn_name, test_units, test_chtrig)

    phys_d = po.BlueprintInput(
        test_timeseries, test_freq, ["time", "trigger", "half", "twice"], ["s", "V", "V", "V"], 1
    )

    phys_d.num_timepoints_found = None
    phys_d.thr = None
    phys_d.time_offset = 0
    phys_d._time_resampled_to_trigger = None

    # Test all-comprehensive slice
    assert phys_in[0 : len(test_trigger)] == phys_d

    # Test instantaneous slice first and last
    phys_d.timeseries = [
        np.array([test_time[0]]),
        np.array([test_trigger[0]]),
        np.array([test_half[0]]),
        np.array([test_twice[0]]),
    ]
    assert phys_in[0] == phys_d

    phys_d.timeseries = [
        np.array([test_time[-1]]),
        np.array([test_trigger[-1]]),
        np.array([test_half[-1]]),
        np.array([test_twice[-2]]),
    ]
    assert phys_in[-1] == phys_d

    # Test slice in the middle
    phys_d.timeseries = [
        np.array(test_time[2:4]),
        np.array(test_trigger[2:4]),
        np.array(test_half[1:2]),
        np.array(test_twice[4:8]),
    ]
    assert phys_in[2:4] == phys_d

    # Test slice in the middle with steps
    phys_d.timeseries = [
        np.array(test_time[1:4:2]),
        np.array(test_trigger[1:4:2]),
        np.array(test_half[0:2:1]),
        np.array(test_twice[4:8:4]),
    ]
    assert phys_in[1:4:2] == phys_d


def test_BlueprintOutput():
    test_time = np.array([0, 1, 1, 2, 3, 5, 8, 13])
    test_trigger = np.array([0, 1, 0, 0, 0, 0, 0, 0])
    test_chocolate = np.array([1, 0, 0, 1, 0, 0, 1, 0])
    test_timeseries = [test_time, test_trigger, test_chocolate]
    test_freq = [42.0, 3.14, 20.0]
    test_chn_name = ["trigger", "time", "chocolate"]
    test_units = ["s", "s", "sweetness"]
    test_chtrig = 1
    num_channnels = len(test_timeseries)

    blueprint_in = po.BlueprintInput(
        test_timeseries, test_freq, test_chn_name, test_units, test_chtrig
    )

    # Tests init_from_blueprint
    blueprint_out = po.BlueprintOutput.init_from_blueprint(blueprint_in)
    start_time = blueprint_out.start_time
    assert (blueprint_out.timeseries == np.asarray(test_timeseries).T).all()
    assert blueprint_out.freq == test_freq[0]
    assert blueprint_out.ch_name == test_chn_name
    assert blueprint_out.units == test_units
    assert blueprint_out.start_time == 0

    # Tests return_index
    test_timeseries = np.array(
        [[0, 1, 1, 2, 3, 5, 8, 13], [0, 1, 0, 0, 0, 0, 0, 0], [1, 0, 0, 1, 0, 0, 1, 0]]
    ).T
    test_freq = 42.0
    test_chn_name = ["trigger", "time", "chocolate"]
    test_units = ["s", "s", "sweetness"]
    num_channnels = test_timeseries.shape[1]
    blueprint_out = po.BlueprintOutput(
        test_timeseries, test_freq, test_chn_name, test_units, start_time
    )
    test_index = blueprint_out.return_index(1)
    assert (test_index[0] == test_trigger).all()
    assert test_index[1] == test_timeseries.shape[1]
    assert test_index[3] == test_chn_name[1]
    assert test_index[4] == test_units[1]

    # Tests delete_at_index
    blueprint_out.delete_at_index(1)
    assert len(blueprint_out.ch_name) == num_channnels - 1
    assert len(blueprint_out.units) == num_channnels - 1
    assert blueprint_out.timeseries.shape[1] == num_channnels - 1
    assert blueprint_out.ch_amount == num_channnels - 1

    # Test __eq__
    assert blueprint_out == blueprint_out


def test_auto_trigger_selection_text(caplog):
    """Test auto_trigger_selection."""
    test_time = np.array([0, 1, 2, 3, 4])
    test_trigger = np.array([0, 1, 2, 3, 4])
    test_half = np.array([0, 1, 2])
    test_twice = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    test_timeseries = [test_time, test_trigger, test_half, test_twice, test_twice, test_twice]
    test_freq = [1, 1, 0.5, 2, 2, 2]
    test_chn_name = ["time", "trigger", "half", "CO2", "CO 2", "strigose"]
    test_units = ["s", "V", "V", "V", "V", "V"]

    # test when trigger is not the name of the channel
    test_chtrig = 2
    phys_in = po.BlueprintInput(test_timeseries, test_freq, test_chn_name, test_units, test_chtrig)
    assert "Trigger channel name is not" in caplog.text

    # test when trigger is 0 and that the trigger channel is recognized by name:
    test_chtrig = 0
    phys_in = po.BlueprintInput(test_timeseries, test_freq, test_chn_name, test_units, test_chtrig)
    assert phys_in.trigger_idx == 1
    # test when no trigger is found
    test_chn_name = ["time", "trigger", "TRIGGER", "CO2", "CO 2", "strigose"]
    with raises(Exception) as errorinfo:
        phys_in = po.BlueprintInput(
            test_timeseries, test_freq, test_chn_name, test_units, test_chtrig
        )
        assert "More than one possible trigger channel" in str(errorinfo.value)


def test_auto_trigger_selection_time():
    """Test auto_trigger_selection in time domain."""
    # Simulate 10 s of a trigger, O2 and ECG
    T = 10
    nSamp = 100
    fs = nSamp / T
    test_time = np.linspace(0, T, nSamp)
    test_freq = [fs, fs, fs, fs]

    # O2 as a sinusoidal of 0.5 Hz
    test_O2 = np.sin(2 * np.pi * 0.5 * test_time)
    # ECG as a sinusoidal with 1.5 Hz
    test_ecg = np.sin(2 * np.pi * 1.5 * test_time)
    # Trigger as a binary signal
    test_trigger = np.zeros(nSamp)
    test_trigger[1:nSamp:4] = 1

    test_timeseries = [test_time, test_O2, test_ecg, test_trigger]
    test_chn_name = ["time", "O2", "ecg", "tiger"]
    test_units = ["s", "V", "V", "V"]

    # test when chtrig is 0 and the trigger is not recognized by text matching:
    test_chtrig = 0
    phys_in = po.BlueprintInput(test_timeseries, test_freq, test_chn_name, test_units, test_chtrig)
    assert phys_in.trigger_idx == 3

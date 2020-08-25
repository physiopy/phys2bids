from phys2bids.interfaces.mat import populate_phys_input


def test_populate_phys_input(matlab_file):
    # Read data to test
    chtrig = 1
    phys_obj = populate_phys_input(matlab_file, chtrig)

    # Check channel names are the same.
    orig_channels = ['time', 'Trigger', 'CO2', 'O2', 'Pulse']
    assert phys_obj.ch_name == orig_channels

    # Check frequencies are the same.
    orig_freq = [1000.0, 1000.0, 1000.0, 1000.0, 1000.0]
    assert phys_obj.freq == orig_freq

    # Check units are the same
    orig_units = ['s', 'V', 'mmHg', 'mmHg', 'V']
    assert phys_obj.units == orig_units


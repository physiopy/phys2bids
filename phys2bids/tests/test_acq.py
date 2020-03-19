from bioread import read_file

from phys2bids.interfaces.acq import populate_phys_input


def test_populate_phys_input(samefreq_full_acq_file):
    # Read data to test
    chtrig = 3
    phys_obj = populate_phys_input(samefreq_full_acq_file, chtrig)

    # checks that the outputs make sense
    assert phys_obj.ch_name[0] == 'time'
    assert phys_obj.freq[0] == 10000.0
    assert phys_obj.units[0] == 's'

    # checks that the trigger is in the right channel
    assert phys_obj.ch_name[chtrig] == 'MR TRIGGER - Custom, HLT100C - A 5'
    assert phys_obj.freq[chtrig] == 10000.0
    assert phys_obj.units[chtrig] == 'Volts'


def test_read_file(samefreq_full_acq_file):
    # Makes sure that the read_file method from bioread works
    data = read_file(samefreq_full_acq_file).channels
    assert data[0].units == 'Volts'

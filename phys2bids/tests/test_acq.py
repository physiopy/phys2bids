import os
import wget
from pkg_resources import resource_filename
from bioread import read_file
from phys2bids.interfaces.acq import populate_phys_input


def test_populate_phys_input():
    # Read data to test
    # url to Test_belt_pulse_samefreq.acq
    url = 'https://osf.io/pn7vt/download'
    test_path = resource_filename('phys2bids', 'tests/data')
    test_filename = 'Test_belt_pulse_samefreq.txt'
    test_full_path = os.path.join(test_path, test_filename)
    wget.download(url, test_full_path)
    chtrig = 2
    phys_obj = populate_phys_input(test_full_path, chtrig)
    assert phys_obj.ch_name[0] == 'time'
    assert phys_obj.freq[0] == 10000.0
    assert phys_obj.units[0] == 's'
    # checkts that the trigger is in the given channel
    assert phys_obj.ch_name[chtrig - 1] == 'trigger'
    assert phys_obj.freq[chtrig - 1] == 10000.0
    assert phys_obj.units[chtrig - 1] == 'Volts'


def test_read_file():
    # Makes sure that the read_file method from bioread works
    # Read data to test
    # url to Test_belt_pulse_samefreq.acq
    url = 'https://osf.io/pn7vt/download'
    test_path = resource_filename('phys2bids', 'tests/data')
    test_filename = 'Test_belt_pulse_samefreq.txt'
    test_full_path = os.path.join(test_path, test_filename)
    wget.download(url, test_full_path)
    data = read_file(test_full_path).channels
    assert data[0].units == 'Volts'

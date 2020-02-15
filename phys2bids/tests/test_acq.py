from phys2bids.interfaces.acq import populate_phys_input
from pkg_resources import resource_filename
import os
import wget


def test_populate_phys_input():
    # Read data to test
    # url to Test_belt_pulse_samefreq.acq
    url = 'https://osf.io/pn7vt//download'
    test_path = resource_filename('phys2bids', 'tests/data')
    test_filename = 'Test_belt_pulse_samefreq.txt'
    test_full_path = os.path.join(test_path, test_filename)
    wget.download(url, test_full_path)
    chtrig = 2
    phys_obj = populate_phys_input(test_full_path, chtrig)

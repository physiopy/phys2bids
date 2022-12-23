import os

import pytest

from phys2bids import io
from phys2bids import viz


def test_plot_all(samefreq_full_acq_file):
    chtrig = 3
    test_path, test_filename = os.path.split(samefreq_full_acq_file)
    phys_obj = io.load_acq(samefreq_full_acq_file, chtrig)
    viz.plot_all(phys_obj.ch_name, phys_obj.timeseries, phys_obj.units,
                 phys_obj.freq, test_filename, outfile=test_path)
    assert os.path.isfile(os.path.join(test_path,
                          os.path.splitext(os.path.basename(test_filename))[0] + '.png'))


# Expected to fail due to trigger plot issue
@pytest.mark.xfail
def test_plot_trigger(samefreq_full_acq_file):
    chtrig = 3
    test_path, test_filename = os.path.split(samefreq_full_acq_file)
    out = os.path.join(test_path, 'Test_belt_pulse_samefreq')
    phys_obj = io.load_acq(samefreq_full_acq_file, chtrig)
    viz.plot_trigger(phys_obj.timeseries[0], phys_obj.timeseries[chtrig],
                     out, 1.5, 1.6, 60, test_filename)
    assert os.path.isfile(out + '_trigger_time.png')

import os

from phys2bids.interfaces import acq
from phys2bids import viz


def test_plot_all(samefreq_full_acq_file):
    chtrig = 3
    test_path, test_filename = os.path.split(samefreq_full_acq_file)
    phys_obj = acq.populate_phys_input(samefreq_full_acq_file, chtrig)
    out = os.path.join(test_path, 'Test_belt_pulse_samefreq.png')
    viz.plot_all(phys_obj.ch_name, phys_obj.timeseries, phys_obj.units,
                 phys_obj.freq, test_filename, outfile=out)
    assert os.path.isfile(out)


def test_plot_trigger(samefreq_full_acq_file):
    chtrig = 3
    test_path, test_filename = os.path.split(samefreq_full_acq_file)
    out = os.path.join(test_path, 'Test_belt_pulse_samefreq')
    phys_obj = acq.populate_phys_input(samefreq_full_acq_file, chtrig)
    viz.plot_trigger(phys_obj.timeseries[0], phys_obj.timeseries[chtrig],
                     out, 1.5, 2.5, 0, test_filename)
    assert os.path.isfile(out + '_trigger_time.png')

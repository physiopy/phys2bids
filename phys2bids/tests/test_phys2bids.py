"""
Tests phys2bids.py
"""

import json
import os
from pytest import raises

from phys2bids import phys2bids


def test_print_summary(tmpdir):
    test_filename = 'input.txt'
    test_ntp_expected = [10, ]
    test_ntp_found = 5
    test_samp_freq = 0.2
    test_time_offset = 0.8
    test_outfile = tmpdir.join('summary')
    test_outfile_log = tmpdir.join('summary.log')

    phys2bids.print_summary(test_filename, test_ntp_expected, test_ntp_found,
                            test_samp_freq, test_time_offset, str(test_outfile))

    assert os.path.isfile(str(test_outfile_log))


def test_print_json(tmpdir):
    test_outfile = tmpdir.join('json_test')
    test_outfile_json = tmpdir.join('json_test.json')
    test_samp_freq = 0.1
    test_time_offset = -0.5
    test_ch_name = 'foo'

    phys2bids.print_json(str(test_outfile), test_samp_freq, test_time_offset, test_ch_name)

    assert os.path.isfile(test_outfile_json)

    test_json_data = dict(SamplingFrequency=0.1,
                          StartTime=0.5,
                          Columns='foo')
    with open(test_outfile_json, 'r') as src:
        loaded_data = json.load(src)

    assert test_json_data == loaded_data


def test_raise_exception(samefreq_full_acq_file):
    test_path, test_filename = os.path.split(samefreq_full_acq_file)
    with raises(Exception) as errorinfo:
        phys2bids.phys2bids(filename=test_filename, indir=test_path, outdir=test_path, chtrig=0)
    assert 'Wrong trigger' in str(errorinfo.value)

    with raises(Exception) as errorinfo:
        phys2bids.phys2bids(filename=test_filename, num_timepoints_expected=[70], tr=[1.3, 2],
                            indir=test_path, outdir=test_path)
    assert "doesn't match" in str(errorinfo.value)

    with raises(Exception) as errorinfo:
        phys2bids.phys2bids(filename=test_filename, num_timepoints_expected=[20, 300], chtrig=3,
                            tr=1.5, indir=test_path, outdir=test_path)
    assert 'stop now' in str(errorinfo.value)

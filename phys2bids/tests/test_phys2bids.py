"""
Tests phys2bids.py
"""

import os
import json
from phys2bids import phys2bids
from pkg_resources import resource_filename


def test_print_summary(tmpdir):
    test_filename = 'input.txt'
    test_ntp_expected = 10
    test_ntp_found = 5
    test_samp_freq = 0.2
    test_time_offset = 0.8
    test_outfile = tmpdir.join('summary')
    test_outfile_log = tmpdir.join('summary.log')

    phys2bids.print_summary(test_filename, test_ntp_expected, test_ntp_found,
                            test_samp_freq, test_time_offset, str(test_outfile))

    assert os.path.isfile(str(test_outfile_log))

    os.remove(str(test_outfile_log))


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

    os.remove(str(test_outfile_json))


def test_use_heuristic(tmpdir):
    test_heur_path = resource_filename('phys2bids', 'heuristics')
    test_heur_file = 'heur_test_acq.py'
    test_full_heur_path = os.path.join(test_heur_path, test_heur_file)
    test_sub = 'SBJ01'
    test_ses = 'S05'
    test_input_path = resource_filename('phys2bids', 'tests/data')
    test_input_file = 'Test_belt_pulse_samefreq.acq'
    test_full_input_path = os.path.join(test_input_path, test_input_file)
    test_outdir = tmpdir
    test_record_label = 'test'

    heur_path = phys2bids.use_heuristic(test_full_heur_path, test_sub, test_ses,
                                        test_full_input_path, test_outdir, test_record_label)

    test_result = ('/sub-SBJ01/ses-S05/func/sub-SBJ01_ses-S05_task-test_rec'
                   '-biopac_run-00_recording-test_physio')
    test_result = str(tmpdir) + test_result

    assert test_result == str(heur_path)

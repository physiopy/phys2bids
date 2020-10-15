import glob
import json
import math
import re
import shutil
import subprocess
from os import remove
from os.path import isfile, join, split
from pkg_resources import resource_filename

import pytest

from phys2bids._version import get_versions
from phys2bids.phys2bids import phys2bids


def check_string(str_container, str_to_find, str_expected, is_num=True):
    idx = [log_idx for log_idx, log_str in enumerate(
                      str_container) if str_to_find in log_str]
    str_found = str_container[idx[0]]
    if is_num:
        num_found = re.findall(r"[-+]?\d*\.\d+|\d+", str_found)
        return str_expected in num_found
    else:
        return str_expected in str_found


def test_integration_acq(skip_integration, samefreq_full_acq_file):
    """
    Does the integration test for an acq file
    """

    if skip_integration:
        pytest.skip('Skipping integration test')

    test_path, test_filename = split(samefreq_full_acq_file)
    test_chtrig = 3
    conversion_path = join(test_path, 'code', 'conversion')

    phys2bids(filename=test_filename, indir=test_path, outdir=test_path,
              chtrig=test_chtrig, num_timepoints_expected=60, tr=1.5)

    # Check that files are generated
    for suffix in ['.json', '.tsv.gz']:
        assert isfile(join(test_path, 'Test_belt_pulse_samefreq' + suffix))

    # Check files in extra are generated
    for suffix in ['.log']:
        assert isfile(join(conversion_path, 'Test_belt_pulse_samefreq' + suffix))

    # Read log file (note that this file is not the logger file)
    with open(join(conversion_path, 'Test_belt_pulse_samefreq.log')) as log_info:
        log_info = log_info.readlines()

    # Check timepoints expected
    assert check_string(log_info, 'Timepoints expected', '60')
    # Check timepoints found
    assert check_string(log_info, 'Timepoints found', '60')
    # Check sampling frequency
    assert check_string(log_info, 'Sampling Frequency', '10000.0')
    # Check sampling started
    assert check_string(log_info, 'Sampling started', '10.4251')
    # Check start time
    assert check_string(log_info, 'first trigger', 'Time 0', is_num=False)

    # Checks json file
    with open(join(test_path, 'Test_belt_pulse_samefreq.json')) as json_file:
        json_data = json.load(json_file)

    # Compares values in json file with ground truth
    assert math.isclose(json_data['SamplingFrequency'], 10000.0)
    assert math.isclose(json_data['StartTime'], 10.4251)
    assert json_data['Columns'] == ['time', 'RESP - RSP100C', 'PULSE - Custom, DA100C',
                                    'MR TRIGGER - Custom, HLT100C - A 5', 'PPG100C', 'CO2', 'O2']

    # Remove generated files
    for filename in glob.glob(join(conversion_path, 'phys2bids*')):
        remove(filename)
    for filename in glob.glob(join(test_path, 'Test_belt_pulse_samefreq*')):
        remove(filename)
    shutil.rmtree(conversion_path)


def test_integration_heuristic(skip_integration, multifreq_lab_file):
    """
    Does integration test of tutorial file with heurositics
    """

    if skip_integration:
        pytest.skip('Skipping integration test')

    test_path, test_filename = split(multifreq_lab_file)
    test_full_path = join(test_path, test_filename)
    test_chtrig = 1
    test_outdir = test_path
    conversion_path = join(test_path, 'code', 'conversion')
    test_ntp = 30
    test_tr = 1.2
    test_thr = 0.735
    heur_path = resource_filename('phys2bids', 'heuristics')
    test_heur = join(heur_path, 'heur_test_multifreq.py')

    # Move into folder
    subprocess.run(f'cd {test_path}', shell=True, check=True)
    # Phys2bids call through terminal
    command_str = (f'phys2bids -in {test_full_path} ',
                   f'-chtrig {test_chtrig} -outdir {test_outdir} ',
                   f'-tr {test_tr} -ntp {test_ntp} -thr {test_thr} ',
                   f'-sub 006 -ses 01 -heur {test_heur}')
    command_str = ''.join(command_str)
    subprocess.run(command_str, shell=True, check=True)

    # Check that call.sh is generated
    assert isfile(join(conversion_path, 'call.sh'))

    # Read logger file
    logger_file = glob.glob(join(conversion_path, '*phys2bids*'))[0]
    with open(logger_file) as logger_info:
        logger_info = logger_info.readlines()

    # Get version info
    current_version = get_versions()
    assert check_string(logger_info, 'phys2bids version', current_version['version'], is_num=False)

    assert check_string(logger_info, '01. Trigger; sampled at', '1000.0')
    assert check_string(logger_info, '04. Belt; sampled at', '500.0')

    # Check that files are generated in conversion path
    for freq in ['40', '100', '500', '1000']:
        assert isfile(join(conversion_path,
                           'sub-006_ses-01_task-test_rec-biopac_run-01_'
                           f'recording-{freq}Hz_physio.log'))
    # assert isfile(join(conversion_path,
    #                    'Test1_multifreq_onescan_sub-006_ses-01_trigger_time.png'))
    assert isfile(join(conversion_path, 'Test1_multifreq_onescan.png'))
    assert isfile(join(conversion_path, 'heur_test_multifreq.py'))
    test_path_output = join(test_path, 'sub-006/ses-01/func')

    # Check that files are generated
    base_filename = 'sub-006_ses-01_task-test_rec-biopac_run-01_recording-'
    for suffix in ['.json', '.tsv.gz']:
        for freq in ['40', '100', '500', '1000']:
            assert isfile(join(test_path_output,
                               f'{base_filename}{freq}Hz_physio{suffix}'))

    # ##### Checks for 40 Hz files
    # Read log file (note that this file is not the logger file)
    log_filename = 'sub-006_ses-01_task-test_rec-biopac_run-01_recording-40Hz_physio.log'
    with open(join(conversion_path, log_filename)) as log_info:
        log_info = log_info.readlines()

    # Check timepoints expected
    assert check_string(log_info, 'Timepoints expected', '30')
    # Check timepoints found
    assert check_string(log_info, 'Timepoints found', '30')
    # Check sampling frequency
    assert check_string(log_info, 'Sampling Frequency', '40.0')
    # Check sampling started
    assert check_string(log_info, 'Sampling started', '3.6960')
    # Check first trigger
    assert check_string(log_info, 'first trigger', 'Time 0', is_num=False)

    # Checks json file
    json_filename = 'sub-006_ses-01_task-test_rec-biopac_run-01_recording-40Hz_physio.json'
    with open(join(test_path_output, json_filename)) as json_file:
        json_data = json.load(json_file)

    # Compares values in json file with ground truth
    assert math.isclose(json_data['SamplingFrequency'], 40.0,)
    assert math.isclose(json_data['StartTime'], 3.6960,)
    assert json_data['Columns'] == ['time', 'Trigger', 'O2']

    # ##### Checks for 100 Hz files
    # Read log file (note that this file is not the logger file)
    log_filename = 'sub-006_ses-01_task-test_rec-biopac_run-01_recording-100Hz_physio.log'
    with open(join(conversion_path, log_filename)) as log_info:
        log_info = log_info.readlines()

    # Check timepoints expected
    assert check_string(log_info, 'Timepoints expected', '30')
    # Check timepoints found
    assert check_string(log_info, 'Timepoints found', '30')
    # Check sampling frequency
    assert check_string(log_info, 'Sampling Frequency', '100.0')
    # Check sampling started
    assert check_string(log_info, 'Sampling started', '3.6960')
    # Check first trigger
    assert check_string(log_info, 'first trigger', 'Time 0', is_num=False)

    # Checks json file
    json_filename = 'sub-006_ses-01_task-test_rec-biopac_run-01_recording-100Hz_physio.json'
    with open(join(test_path_output, json_filename)) as json_file:
        json_data = json.load(json_file)

    # Compares values in json file with ground truth
    assert math.isclose(json_data['SamplingFrequency'], 100.0,)
    assert math.isclose(json_data['StartTime'], 3.6960,)
    assert json_data['Columns'] == ['time', 'Trigger', 'CO2']

    # Remove generated files
    shutil.rmtree(test_path_output)
    shutil.rmtree(conversion_path)
    for filename in glob.glob(join(test_path, 'Test1_multifreq_onescan*')):
        remove(filename)


def test_integration_multirun(skip_integration, multi_run_file):

    if skip_integration:
        pytest.skip('Skipping integration test')

    test_path, test_filename = split(multi_run_file)
    test_chtrig = 1
    conversion_path = join(test_path, 'code', 'conversion')

    phys2bids(filename=test_filename, indir=test_path, outdir=test_path,
              chtrig=test_chtrig, num_timepoints_expected=[534, 513], tr=[1.2, 1.2])

    # Check that files are generated in outdir
    base_filename = 'Test2_samefreq_TWOscans_'
    for suffix in ['.json', '.tsv.gz']:
        for run in ['01', '02']:
            assert isfile(join(test_path, f'{base_filename}{run}{suffix}'))

    assert isfile(join(test_path, 'Test2_samefreq_TWOscans.txt'))

    # Check that files are generated in conversion_path
    for run in ['01', '02']:
        assert isfile(join(conversion_path, f'Test2_samefreq_TWOscans_{run}.log'))

    # Check that plots are generated in conversion_path
    # base_filename = 'Test2_samefreq_TWOscans_'
    # for run in ['1', '2']:
    #     assert isfile(join(conversion_path, f'Test2_samefreq_TWOscans_{run}_trigger_time.png'))
    assert isfile(join(conversion_path, 'Test2_samefreq_TWOscans.png'))

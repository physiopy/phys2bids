import glob
import json
import math
import os
from pkg_resources import resource_filename
import re
import subprocess

from phys2bids.phys2bids import phys2bids
from phys2bids._version import get_versions


def check_string(str_container, str_to_find, str_expected, is_num=True):
    idx = [log_idx for log_idx, log_str in enumerate(
                      str_container) if str_to_find in log_str]
    str_found = str_container[idx[0]]
    if is_num:
        num_found = re.findall(r"[-+]?\d*\.\d+|\d+", str_found)
        return str_expected in num_found
    else:
        return str_expected in str_found


def test_logger():
    """
    Tests the logger
    """

    # Move into folder
    test_path = resource_filename('phys2bids', 'tests/data')
    subprocess.run(f'cd {test_path}', shell=True, check=True)

    # Input arguments
    test_filename = 'tutorial_file.txt'
    test_chtrig = 1
    test_outdir = test_path

    # Phys2bids call through terminal
    subprocess.run(f'phys2bids -in {test_filename} -indir {test_path} '
                   f'-chtrig {test_chtrig} -outdir {test_outdir}', shell=True, check=True)

    # Read logger file
    logger_file = glob.glob(os.path.join(test_path, '*phys2bids*'))[0]
    with open(logger_file) as logger_info:
        logger_info = logger_info.readlines()

    # Get version info
    current_version = get_versions()
    assert check_string(logger_info, 'phys2bids version', current_version['version'], is_num=False)

    # Removes generated files
    os.remove(os.path.join(test_path, logger_file))


def test_integration_tutorial():
    """
    Does an integration test with the tutorial file
    """
    test_path = resource_filename('phys2bids', 'tests/data')
    test_filename = 'tutorial_file.txt'
    test_full_path = os.path.join(test_path, test_filename)
    test_chtrig = 1
    test_outdir = test_path
    test_ntp = 158
    test_tr = 1.2
    test_thr = 0.735
    phys2bids(filename=test_full_path, chtrig=test_chtrig, outdir=test_outdir,
              num_timepoints_expected=test_ntp, tr=test_tr, thr=test_thr)

    # Check that files are generated
    for suffix in ['.log', '.json', '.tsv.gz', '_trigger_time.png']:
        assert os.path.isfile(os.path.join(test_path, 'tutorial_file' + suffix))

    # Read log file (note that this file is not the logger file)
    with open(os.path.join(test_path, 'tutorial_file.log')) as log_info:
        log_info = log_info.readlines()

    # Check timepoints expected
    assert check_string(log_info, 'Timepoints expected', '158')
    # Check timepoints found
    assert check_string(log_info, 'Timepoints found', '158')
    # Check sampling frequency
    assert check_string(log_info, 'Sampling Frequency', '1000.0')
    # Check sampling frequency
    assert check_string(log_info, 'Sampling started', '0.24499999999989086')
    # Check start time
    assert check_string(log_info, 'first trigger', 'Time 0', is_num=False)

    # Checks json file
    with open(os.path.join(test_path, 'tutorial_file.json')) as json_file:
        json_data = json.load(json_file)

    # Compares values in json file with ground truth
    assert math.isclose(json_data['SamplingFrequency'], 1000.0)
    assert math.isclose(json_data['StartTime'], 0.245)
    assert json_data['Columns'] == ['time', 'Trigger', 'CO2', 'O2', 'Pulse']

    # Remove generated files
    for filename in glob.glob(os.path.join(test_path, 'phys2bids*')):
        os.remove(filename)


def test_integration_acq(samefreq_full_acq_file):
    """
    Does the integration test for an acq file
    """

    test_path, test_filename = os.path.split(samefreq_full_acq_file)
    test_chtrig = 3

    phys2bids(filename=test_filename, indir=test_path, outdir=test_path,
              chtrig=test_chtrig, num_timepoints_expected=1)

    # Check that files are generated
    for suffix in ['.log', '.json', '.tsv.gz', '_trigger_time.png']:
        assert os.path.isfile(os.path.join(test_path, 'Test_belt_pulse_samefreq' + suffix))

    # Read log file (note that this file is not the logger file)
    with open(os.path.join(test_path, 'Test_belt_pulse_samefreq.log')) as log_info:
        log_info = log_info.readlines()

    # Check timepoints expected
    assert check_string(log_info, 'Timepoints expected', '1')
    # Check timepoints found
    assert check_string(log_info, 'Timepoints found', '60')
    # Check sampling frequency
    assert check_string(log_info, 'Sampling Frequency', '10000.0')
    # Check sampling started
    assert check_string(log_info, 'Sampling started', '10.425107798467103')
    # Check start time
    assert check_string(log_info, 'first trigger', 'Time 0', is_num=False)

    # Checks json file
    with open(os.path.join(test_path, 'Test_belt_pulse_samefreq.json')) as json_file:
        json_data = json.load(json_file)

    # Compares values in json file with ground truth
    assert math.isclose(json_data['SamplingFrequency'], 10000.0)
    assert math.isclose(json_data['StartTime'], 10.425107798467103)
    assert json_data['Columns'] == ['time', 'RESP - RSP100C', 'PULSE - Custom, DA100C',
                                    'MR TRIGGER - Custom, HLT100C - A 5', 'PPG100C', 'CO2', 'O2']

    # Remove generated files
    for filename in glob.glob(os.path.join(test_path, 'phys2bids*')):
        os.remove(filename)
    for filename in glob.glob(os.path.join(test_path, 'Test_belt_pulse_samefreq*')):
        os.remove(filename)


def test_integration_multifreq(multifreq_acq_file):
    """
    Does the integration test for a multi-frequency file
    """

    test_path, test_filename = os.path.split(multifreq_acq_file)
    test_chtrig = 3

    phys2bids(filename=test_filename, indir=test_path, outdir=test_path,
              chtrig=test_chtrig, num_timepoints_expected=1)

    # Check that files are generated
    for suffix in ['.log', '.json', '.tsv.gz']:
        assert os.path.isfile(os.path.join(test_path,
                                           'Test_belt_pulse_multifreq_625.0' + suffix))
    for suffix in ['.log', '.json', '.tsv.gz']:
        assert os.path.isfile(os.path.join(test_path,
                                           'Test_belt_pulse_multifreq_10000.0' + suffix))
    assert os.path.isfile(os.path.join(test_path, 'Test_belt_pulse_multifreq_trigger_time.png'))

    """
    Checks 625 Hz output
    """
    # Read log file of frequency 625 (note that this file is not the logger file)
    with open(os.path.join(test_path, 'Test_belt_pulse_multifreq_625.0.log')) as log_info:
        log_info = log_info.readlines()

    # Check timepoints expected
    assert check_string(log_info, 'Timepoints expected', '1')
    # Check timepoints found
    assert check_string(log_info, 'Timepoints found', '60')
    # Check sampling frequency
    assert check_string(log_info, 'Sampling Frequency', '625.0')
    # Check sampling frequency
    assert check_string(log_info, 'Sampling started', '0.29052734375')
    # Check start time
    assert check_string(log_info, 'first trigger', 'Time 0', is_num=False)

    # Checks json file
    with open(os.path.join(test_path, 'Test_belt_pulse_multifreq_625.0.json')) as json_file:
        json_data = json.load(json_file)

    # Compares values in json file with ground truth
    assert math.isclose(json_data['SamplingFrequency'], 625.0)
    assert math.isclose(json_data['StartTime'], 0.29052734375)
    assert json_data['Columns'] == ['PULSE - Custom, DA100C']

    """
    Checks 10000 Hz output
    """
    # Read log file of frequency 625 (note that this file is not the logger file)
    with open(os.path.join(test_path, 'Test_belt_pulse_multifreq_10000.0.log')) as log_info:
        log_info = log_info.readlines()

    # Check timepoints expected
    assert check_string(log_info, 'Timepoints expected', '1')
    # Check timepoints found
    assert check_string(log_info, 'Timepoints found', '60')
    # Check sampling frequency
    assert check_string(log_info, 'Sampling Frequency', '10000.0')
    # Check sampling started
    assert check_string(log_info, 'Sampling started', '10.425107798467103')
    # Check start time
    assert check_string(log_info, 'first trigger', 'Time 0', is_num=False)

    # Checks json file
    with open(os.path.join(test_path, 'Test_belt_pulse_multifreq_10000.0.json')) as json_file:
        json_data = json.load(json_file)

    # Compares values in json file with ground truth
    assert math.isclose(json_data['SamplingFrequency'], 10000.0)
    assert math.isclose(json_data['StartTime'], 10.425107798467103)
    assert json_data['Columns'] == ['time', 'RESP - RSP100C',
                                    'MR TRIGGER - Custom, HLT100C - A 5', 'PPG100C', 'CO2', 'O2']

    # Remove generated files
    for filename in glob.glob(os.path.join(test_path, 'phys2bids*')):
        os.remove(filename)
    for filename in glob.glob(os.path.join(test_path, 'Test_belt_pulse_multifreq*')):
        os.remove(filename)


def test_integration_heuristic():
    """
    Does integration test of tutorial file with heurositics
    """
    test_path = resource_filename('phys2bids', 'tests/data')
    test_filename = 'tutorial_file.txt'
    test_full_path = os.path.join(test_path, test_filename)
    test_chtrig = 1
    test_outdir = test_path
    test_ntp = 158
    test_tr = 1.2
    test_thr = 0.735
    heur_path = resource_filename('phys2bids', 'heuristics')
    test_heur = os.path.join(heur_path, 'heur_tutorial.py')
    phys2bids(filename=test_full_path, chtrig=test_chtrig, outdir=test_outdir,
              num_timepoints_expected=test_ntp, tr=test_tr, thr=test_thr, sub='006',
              ses='01', heur_file=test_heur)

    test_path_output = os.path.join(test_path, 'sub-006/ses-01/func')

    # Check that files are generated
    base_filename = 'sub-006_ses-01_task-test_rec-labchart_run-00_physio'
    for suffix in ['.log', '.json', '.tsv.gz']:
        assert os.path.isfile(os.path.join(test_path_output, base_filename + suffix))

    # Read log file (note that this file is not the logger file)
    log_filename = 'sub-006_ses-01_task-test_rec-labchart_run-00_physio.log'
    with open(os.path.join(test_path_output, log_filename)) as log_info:
        log_info = log_info.readlines()

    # Check timepoints expected
    assert check_string(log_info, 'Timepoints expected', '158')
    # Check timepoints found
    assert check_string(log_info, 'Timepoints found', '158')
    # Check sampling frequency
    assert check_string(log_info, 'Sampling Frequency', '1000.0')
    # Check sampling started
    assert check_string(log_info, 'Sampling started', '0.24499999999989086')
    # Check start time
    assert check_string(log_info, 'first trigger', 'Time 0', is_num=False)

    # Checks json file
    json_filename = 'sub-006_ses-01_task-test_rec-labchart_run-00_physio.json'
    with open(os.path.join(test_path_output, json_filename)) as json_file:
        json_data = json.load(json_file)

    # Compares values in json file with ground truth
    assert math.isclose(json_data['SamplingFrequency'], 1000.0)
    assert math.isclose(json_data['StartTime'], 0.24499999999989086)
    assert json_data['Columns'] == ['time', 'Trigger', 'CO2', 'O2', 'Pulse']

    # Remove generated files
    for filename in glob.glob(os.path.join(test_path, 'phys2bids*')):
        os.remove(filename)
    for filename in glob.glob(os.path.join(test_path, 'Test_belt_pulse_samefreq*')):
        os.remove(filename)
    for filename in glob.glob(os.path.join(test_path_output, '*')):
        os.remove(filename)


def test_integration_info():
    """
    Tests the info option
    """
    test_path = resource_filename('phys2bids', 'tests/data')
    test_filename = 'tutorial_file.txt'
    test_chtrig = 1
    test_outdir = test_path
    test_ntp = 158
    test_tr = 1.2
    test_thr = 0.735

    # Move into folder
    subprocess.run(f'cd {test_path}', shell=True, check=True)
    # Phys2bids call through terminal
    command_str = (f'phys2bids -in {test_filename} -indir {test_path} ',
                   f'-chtrig {test_chtrig} -outdir {test_outdir} ',
                   f'-tr {test_tr} -ntp {test_ntp} -thr {test_thr} ',
                   f'-info')
    command_str = ''.join(command_str)
    subprocess.run(command_str, shell=True, check=True)

    # Check that plot all file is generated
    assert os.path.isfile('tutorial_file.png')

    # Read logger file
    logger_file = glob.glob(os.path.join(test_path, '*phys2bids*'))[0]
    with open(logger_file) as logger_info:
        logger_info = logger_info.readlines()

    # Get trigger info
    assert check_string(logger_info, 'Trigger; sampled at', '1000.0')
    # Get CO2 info
    assert check_string(logger_info, 'CO2; sampled at', '1000.0')
    # Get O2 info
    assert check_string(logger_info, 'O2; sampled at', '1000.0')
    # Get pulse info
    assert check_string(logger_info, 'Pulse; sampled at', '1000.0')

    # Remove generated files
    for filename in glob.glob(os.path.join(test_path, 'phys2bids*')):
        os.remove(filename)

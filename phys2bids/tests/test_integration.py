import glob
import json
import math
import os
import re
import shutil
import subprocess
from csv import reader
from pkg_resources import resource_filename

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


def test_integration_multifreq(multifreq_lab_file):
    """
    Does the integration test for a multi-frequency file
    """

    test_path, test_filename = os.path.split(multifreq_lab_file)
    test_chtrig = 3
    conversion_path = os.path.join(test_path, 'code/conversion')

    phys2bids(filename=test_filename, indir=test_path, outdir=test_path,
              chtrig=test_chtrig, num_timepoints_expected=1)

    # Check that files are generated
    for suffix in ['.json', '.tsv.gz']:
        assert os.path.isfile(os.path.join(test_path,
                                           'Test1_multifreq_onescan_40.0' + suffix))
    for suffix in ['.json', '.tsv.gz']:
        assert os.path.isfile(os.path.join(test_path,
                                           'Test1_multifreq_onescan_100.0' + suffix))
    for suffix in ['.json', '.tsv.gz']:
        assert os.path.isfile(os.path.join(test_path,
                                           'Test1_multifreq_onescan_500.0' + suffix))
    for suffix in ['.json', '.tsv.gz']:
        assert os.path.isfile(os.path.join(test_path,
                                           'Test1_multifreq_onescan_1000.0' + suffix))
    for freq in ['40', '100', '500', '1000']:
        assert os.path.isfile(os.path.join(conversion_path,
                                           'Test1_multifreq_onescan_' + freq + '.log'))
    assert os.path.isfile(os.path.join(conversion_path,
                          'Test1_multifreq_onescan_trigger_time.png'))

    """
    Checks 40 Hz output
    """
    # Read log file of frequency 625 (note that this file is not the logger file)
    with open(os.path.join(conversion_path, 'Test1_multifreq_onescan_40.log')) as log_info:
        log_info = log_info.readlines()

    # Check timepoints expected
    assert check_string(log_info, 'Timepoints expected', '1')
    # Check timepoints found
    assert check_string(log_info, 'Timepoints found', '0')
    # Check sampling frequency
    assert check_string(log_info, 'Sampling Frequency', '40.0')
    # Check sampling frequency
    assert check_string(log_info, 'Sampling started', '-157.8535')
    # Check start time
    assert check_string(log_info, 'first trigger', 'Time 0', is_num=False)

    # Checks json file
    with open(os.path.join(test_path, 'Test1_multifreq_onescan_40.0.json')) as json_file:
        json_data = json.load(json_file)

    # Compares values in json file with ground truth
    assert math.isclose(json_data['SamplingFrequency'], 40.0)
    assert math.isclose(json_data['StartTime'], -157.8535)
    assert json_data['Columns'] == ['O2']

    """
    Checks 100 Hz output
    """
    # Read log file of frequency 625 (note that this file is not the logger file)
    with open(os.path.join(conversion_path, 'Test1_multifreq_onescan_100.log')) as log_info:
        log_info = log_info.readlines()

    # Check timepoints expected
    assert check_string(log_info, 'Timepoints expected', '1')
    # Check timepoints found
    assert check_string(log_info, 'Timepoints found', '0')
    # Check sampling frequency
    assert check_string(log_info, 'Sampling Frequency', '100.0')
    # Check sampling started
    assert check_string(log_info, 'Sampling started', '-0.3057')
    # Check start time
    assert check_string(log_info, 'first trigger', 'Time 0', is_num=False)

    # Checks json file
    with open(os.path.join(test_path, 'Test1_multifreq_onescan_100.0.json')) as json_file:
        json_data = json.load(json_file)

    # Compares values in json file with ground truth
    assert math.isclose(json_data['SamplingFrequency'], 100.0)
    assert math.isclose(json_data['StartTime'], -0.3057)
    assert json_data['Columns'] == ['CO2']

    """
    Checks 500 Hz output
    """
    # Read log file of frequency 625 (note that this file is not the logger file)
    with open(os.path.join(conversion_path, 'Test1_multifreq_onescan_500.log')) as log_info:
        log_info = log_info.readlines()

    # Check timepoints expected
    assert check_string(log_info, 'Timepoints expected', '1')
    # Check timepoints found
    assert check_string(log_info, 'Timepoints found', '0')
    # Check sampling frequency
    assert check_string(log_info, 'Sampling Frequency', '500.0')
    # Check sampling started
    assert check_string(log_info, 'Sampling started', '-4.2019')
    # Check start time
    assert check_string(log_info, 'first trigger', 'Time 0', is_num=False)

    # Checks json file
    with open(os.path.join(test_path, 'Test1_multifreq_onescan_500.0.json')) as json_file:
        json_data = json.load(json_file)

    # Compares values in json file with ground truth
    assert math.isclose(json_data['SamplingFrequency'], 500.0)
    assert math.isclose(json_data['StartTime'], -4.2019)
    assert json_data['Columns'] == ['Belt']

    """
    Checks 1000 Hz output
    """
    # Read log file of frequency 625 (note that this file is not the logger file)
    with open(os.path.join(conversion_path, 'Test1_multifreq_onescan_1000.log')) as log_info:
        log_info = log_info.readlines()

    # Check timepoints expected
    assert check_string(log_info, 'Timepoints expected', '1')
    # Check timepoints found
    assert check_string(log_info, 'Timepoints found', '0')
    # Check sampling frequency
    assert check_string(log_info, 'Sampling Frequency', '1000.0')
    # Check sampling started
    assert check_string(log_info, 'Sampling started', '-1.0000')
    # Check start time
    assert check_string(log_info, 'first trigger', 'Time 0', is_num=False)

    # Checks json file
    with open(os.path.join(test_path, 'Test1_multifreq_onescan_1000.0.json')) as json_file:
        json_data = json.load(json_file)

    # Compares values in json file with ground truth
    assert math.isclose(json_data['SamplingFrequency'], 1000.0)
    assert math.isclose(json_data['StartTime'], -1.0000)
    assert json_data['Columns'] == ['time', 'Trigger']

    # Remove generated files
    for filename in glob.glob(os.path.join(conversion_path, 'phys2bids*')):
        os.remove(filename)
    for filename in glob.glob(os.path.join(test_path, 'Test_belt_pulse_multifreq*')):
        os.remove(filename)
    shutil.rmtree(conversion_path)


def test_integration_heuristic(samefreq_short_txt_file):
    """
    Does integration test of tutorial file with heurositics
    """

    test_path, test_filename = os.path.split(samefreq_short_txt_file)
    test_full_path = os.path.join(test_path, test_filename)
    test_chtrig = 1
    test_outdir = test_path
    conversion_path = os.path.join(test_path, 'code/conversion')
    test_ntp = 158
    test_tr = 1.2
    test_thr = 0.735
    heur_path = resource_filename('phys2bids', 'heuristics')
    test_heur = os.path.join(heur_path, 'heur_test_acq.py')
    phys2bids(filename=test_full_path, chtrig=test_chtrig, outdir=test_outdir,
              num_timepoints_expected=test_ntp, tr=test_tr, thr=test_thr, sub='006',
              ses='01', heur_file=test_heur)

    test_path_output = os.path.join(test_path, 'sub-006/ses-01/func')

    # Check that files are generated
    base_filename = 'sub-006_ses-01_task-test_rec-biopac_run-01_physio'
    for suffix in ['.json', '.tsv.gz']:
        assert os.path.isfile(os.path.join(test_path_output, base_filename + suffix))
    assert os.path.isfile(os.path.join(conversion_path, base_filename + '.log'))
    # Read log file (note that this file is not the logger file)
    log_filename = 'sub-006_ses-01_task-test_rec-biopac_run-01_physio.log'
    with open(os.path.join(conversion_path, log_filename)) as log_info:
        log_info = log_info.readlines()

    # Check timepoints expected
    assert check_string(log_info, 'Timepoints expected', '158')
    # Check timepoints found
    assert check_string(log_info, 'Timepoints found', '0')
    # Check sampling frequency
    assert check_string(log_info, 'Sampling Frequency', '10000.0')
    # Check sampling started
    assert check_string(log_info, 'Sampling started', '-189.6000')
    # Check first trigger
    assert check_string(log_info, 'first trigger', 'Time 0', is_num=False)

    # Checks json file
    json_filename = 'sub-006_ses-01_task-test_rec-biopac_run-01_physio.json'
    with open(os.path.join(test_path_output, json_filename)) as json_file:
        json_data = json.load(json_file)

    # Compares values in json file with ground truth
    assert math.isclose(json_data['SamplingFrequency'], 10000.0,)
    assert math.isclose(json_data['StartTime'], -189.6,)
    assert json_data['Columns'] == ['time', 'RESP - RSP100C', 'MR TRIGGER - Custom, HLT100C - A 5']

    # Check that participant.tsv gets updated
    phys2bids(filename=test_full_path, chtrig=test_chtrig, outdir=test_outdir,
              num_timepoints_expected=test_ntp, tr=test_tr, thr=test_thr, sub='002',
              ses='01', heur_file=test_heur)

    counter = 0
    subject_list = ['participant_id', '006', '002']
    with open(os.path.join(test_path, 'participants.tsv')) as pf:
        tsvreader = reader(pf, delimiter="\t")
        for line in tsvreader:
            assert subject_list[counter] in line[0]
            counter += 1

    # Remove generated files
    for filename in glob.glob(os.path.join(conversion_path, 'phys2bids*')):
        os.remove(filename)
    for filename in glob.glob(os.path.join(test_path, 'Test_belt_pulse_samefreq*')):
        os.remove(filename)
    for filename in glob.glob(os.path.join(test_path_output, '*')):
        os.remove(filename)
    shutil.rmtree(conversion_path)


def test_integration_info(samefreq_short_txt_file):
    """
    Tests the info option
    """

    test_path, test_filename = os.path.split(samefreq_short_txt_file)
    test_chtrig = 1
    test_outdir = test_path
    test_ntp = 158
    test_tr = 1.2
    test_thr = 0.735
    conversion_path = os.path.join(test_path, 'code/conversion')
    # Move into folder
    subprocess.run(f'cd {test_path}', shell=True, check=True)
    # Phys2bids call through terminal
    command_str = (f'phys2bids -in {test_filename} -indir {test_path} ',
                   f'-chtrig {test_chtrig} -outdir {test_outdir} ',
                   f'-tr {test_tr} -ntp {test_ntp} -thr {test_thr} ',
                   f'-info')
    command_str = ''.join(command_str)
    subprocess.run(command_str, shell=True, check=True)

    # Check that call.sh is generated
    assert os.path.isfile(os.path.join(conversion_path, 'call.sh'))

    # Check that plot all file is generated
    assert os.path.isfile(os.path.join(conversion_path,
                                       'Test_belt_pulse_samefreq_short.png'))

    # Read logger file
    logger_file = glob.glob(os.path.join(conversion_path, '*phys2bids*'))[0]
    with open(logger_file) as logger_info:
        logger_info = logger_info.readlines()

    assert check_string(logger_info, '01. RESP - RSP100C; sampled at', '10000.0')
    assert check_string(logger_info,
                        '02. MR TRIGGER - Custom, HLT100C - A 5; sampled at', '10000.0')

    # Remove generated files
    for filename in glob.glob(os.path.join(conversion_path, 'phys2bids*')):
        os.remove(filename)
    shutil.rmtree(conversion_path)

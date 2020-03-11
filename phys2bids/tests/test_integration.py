import os
import wget
import glob
import json
import subprocess

from pkg_resources import resource_filename

from phys2bids.phys2bids import phys2bids
from phys2bids._version import get_versions


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
    files = os.listdir(test_path)
    logger_idx = [log_idx for log_idx, log_str in enumerate(
                      files) if 'phys2bids' in log_str]
    logger_file = files[logger_idx[0]]

    with open(os.path.join(test_path, logger_file)) as logger_info:
        logger_info = logger_info.readlines()

    # Get version info
    version_idx = [log_idx for log_idx, log_str in enumerate(
                      logger_info) if 'phys2bids version' in log_str]
    version_found = logger_info[version_idx[0]]
    current_version = get_versions()

    # Checks logger version is the current version
    assert current_version['version'] in version_found

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
    assert os.path.isfile(os.path.join(test_path, 'tutorial_file.log'))
    assert os.path.isfile(os.path.join(test_path, 'tutorial_file.json'))
    assert os.path.isfile(os.path.join(test_path, 'tutorial_file.tsv.gz'))
    assert os.path.isfile(os.path.join(test_path, 'tutorial_file_trigger_time.png'))

    # Read log file (note that this file is not the logger file)
    with open(os.path.join(test_path, 'tutorial_file.log')) as log_info:
        log_info = log_info.readlines()

    # Check timepoints expected
    expected_idx = [log_idx for log_idx, log_str in enumerate(
                      log_info) if 'Timepoints expected' in log_str]
    expected_found = log_info[expected_idx[0]]
    assert '158' in expected_found

    # Check timepoints found
    timepoints_idx = [log_idx for log_idx, log_str in enumerate(
                      log_info) if 'Timepoints expected' in log_str]
    timepoints_found = log_info[timepoints_idx[0]]
    assert '158' in timepoints_found

    # Check sampling frequency
    sampling_idx = [log_idx for log_idx, log_str in enumerate(
                      log_info) if 'Sampling Frequency' in log_str]
    sampling_found = log_info[sampling_idx[0]]
    assert '1000.0' in sampling_found

    # Check sampling frequency
    started_idx = [log_idx for log_idx, log_str in enumerate(
                      log_info) if 'Sampling started' in log_str]
    started_found = log_info[started_idx[0]]
    assert '0.24499999999989086' in started_found

    # Check start time
    start_idx = [log_idx for log_idx, log_str in enumerate(
                      log_info) if 'first trigger' in log_str]
    start_found = log_info[start_idx[0]]
    assert 'Time 0' in start_found

    # Checks json file
    # json_data = json.load(os.path.join(test_path, 'tutorial_file.json'))
    with open(os.path.join(test_path, 'tutorial_file.json')) as json_file:
        json_data = json.load(json_file)

    # Compares values in json file with ground truth
    assert json_data['SamplingFrequency'] == 1000.0
    assert json_data['StartTime'] == 0.24499999999989086
    assert json_data['Columns'] == ['time', 'Trigger', 'CO2', 'O2', 'Pulse']

    # Remove generated files
    for filename in glob.glob(os.path.join(test_path, 'phys2bids*')):
        os.remove(filename)
    # for filename in glob.glob(os.path.join(test_path, 'tutorial*')):
    #     os.remove(filename)


def test_integration_acq():
    """
    Does the integration test for an acq file
    """

    url = 'https://osf.io/27gqb/download'
    test_path = resource_filename('phys2bids', 'tests/data')
    test_filename = 'Test_belt_pulse_samefreq.acq'
    test_full_path = os.path.join(test_path, test_filename)
    wget.download(url, test_full_path)
    test_chtrig = 3

    phys2bids(filename=test_filename, indir=test_path, outdir=test_path,
              chtrig=test_chtrig, num_timepoints_expected=1)

    # Check that files are generated
    assert os.path.isfile(os.path.join(test_path, 'Test_belt_pulse_samefreq.log'))
    assert os.path.isfile(os.path.join(test_path, 'Test_belt_pulse_samefreq.json'))
    assert os.path.isfile(os.path.join(test_path, 'Test_belt_pulse_samefreq.tsv.gz'))
    assert os.path.isfile(os.path.join(test_path, 'Test_belt_pulse_samefreq_trigger_time.png'))

    # Read log file (note that this file is not the logger file)
    with open(os.path.join(test_path, 'Test_belt_pulse_samefreq.log')) as log_info:
        log_info = log_info.readlines()

    # Check timepoints expected
    expected_idx = [log_idx for log_idx, log_str in enumerate(
                      log_info) if 'Timepoints expected' in log_str]
    expected_found = log_info[expected_idx[0]]
    assert '1' in expected_found

    # Check timepoints found
    timepoints_idx = [log_idx for log_idx, log_str in enumerate(
                      log_info) if 'Timepoints found' in log_str]
    timepoints_found = log_info[timepoints_idx[0]]
    assert '60' in timepoints_found

    # Check sampling frequency
    sampling_idx = [log_idx for log_idx, log_str in enumerate(
                      log_info) if 'Sampling Frequency' in log_str]
    sampling_found = log_info[sampling_idx[0]]
    assert '10000.0' in sampling_found

    # Check sampling frequency
    started_idx = [log_idx for log_idx, log_str in enumerate(
                      log_info) if 'Sampling started' in log_str]
    started_found = log_info[started_idx[0]]
    assert '10.425007798392297' in started_found

    # Check start time
    start_idx = [log_idx for log_idx, log_str in enumerate(
                      log_info) if 'first trigger' in log_str]
    start_found = log_info[start_idx[0]]
    assert 'Time 0' in start_found

    # Checks json file
    with open(os.path.join(test_path, 'Test_belt_pulse_samefreq.json')) as json_file:
        json_data = json.load(json_file)

    # Compares values in json file with ground truth
    assert json_data['SamplingFrequency'] == 10000.0
    assert json_data['StartTime'] == 10.425007798392297
    assert json_data['Columns'] == ['time', 'RESP - RSP100C', 'PULSE - Custom, DA100C',
                                    'MR TRIGGER - Custom, HLT100C - A 5', 'PPG100C', 'CO2', 'O2']

    # Remove generated files
    for filename in glob.glob(os.path.join(test_path, 'phys2bids*')):
        os.remove(filename)
    for filename in glob.glob(os.path.join(test_path, 'Test_belt_pulse_samefreq*')):
        os.remove(filename)


def test_integration_multifreq():
    """
    Does the integration test for a multi-frequency file
    """

    url = 'https://osf.io/9a7yv/download'
    test_path = resource_filename('phys2bids', 'tests/data')
    test_filename = 'Test_belt_pulse_multifreq.acq'
    test_full_path = os.path.join(test_path, test_filename)
    wget.download(url, test_full_path)
    test_chtrig = 3

    phys2bids(filename=test_filename, indir=test_path, outdir=test_path,
              chtrig=test_chtrig, num_timepoints_expected=1)

    # Check that files are generated
    assert os.path.isfile(os.path.join(test_path, 'Test_belt_pulse_multifreq_625.0.log'))
    assert os.path.isfile(os.path.join(test_path, 'Test_belt_pulse_multifreq_625.0.json'))
    assert os.path.isfile(os.path.join(test_path, 'Test_belt_pulse_multifreq_625.0.tsv.gz'))
    assert os.path.isfile(os.path.join(test_path, 'Test_belt_pulse_multifreq_trigger_time.png'))
    assert os.path.isfile(os.path.join(test_path, 'Test_belt_pulse_multifreq_10000.0.log'))
    assert os.path.isfile(os.path.join(test_path, 'Test_belt_pulse_multifreq_10000.0.json'))
    assert os.path.isfile(os.path.join(test_path, 'Test_belt_pulse_multifreq_10000.0.tsv.gz'))

    """
    Checks 625 Hz output
    """
    # Read log file of frequency 625 (note that this file is not the logger file)
    with open(os.path.join(test_path, 'Test_belt_pulse_multifreq_625.0.log')) as log_info:
        log_info = log_info.readlines()

    # Check timepoints expected
    expected_idx = [log_idx for log_idx, log_str in enumerate(
                      log_info) if 'Timepoints expected' in log_str]
    expected_found = log_info[expected_idx[0]]
    assert '1' in expected_found

    # Check timepoints found
    timepoints_idx = [log_idx for log_idx, log_str in enumerate(
                      log_info) if 'Timepoints found' in log_str]
    timepoints_found = log_info[timepoints_idx[0]]
    assert '60' in timepoints_found

    # Check sampling frequency
    sampling_idx = [log_idx for log_idx, log_str in enumerate(
                      log_info) if 'Sampling Frequency' in log_str]
    sampling_found = log_info[sampling_idx[0]]
    assert '625.0' in sampling_found

    # Check sampling frequency
    started_idx = [log_idx for log_idx, log_str in enumerate(
                      log_info) if 'Sampling started' in log_str]
    started_found = log_info[started_idx[0]]
    assert '0.29052734375' in started_found

    # Check start time
    start_idx = [log_idx for log_idx, log_str in enumerate(
                      log_info) if 'first trigger' in log_str]
    start_found = log_info[start_idx[0]]
    assert 'Time 0' in start_found

    # Checks json file
    with open(os.path.join(test_path, 'Test_belt_pulse_multifreq_625.0.json')) as json_file:
        json_data = json.load(json_file)

    # Compares values in json file with ground truth
    assert json_data['SamplingFrequency'] == 625.0
    assert json_data['StartTime'] == 0.29052734375
    assert json_data['Columns'] == ['PULSE - Custom, DA100C']

    """
    Checks 10000 Hz output
    """
    # Read log file of frequency 625 (note that this file is not the logger file)
    with open(os.path.join(test_path, 'Test_belt_pulse_multifreq_10000.0.log')) as log_info:
        log_info = log_info.readlines()

    # Check timepoints expected
    expected_idx = [log_idx for log_idx, log_str in enumerate(
                      log_info) if 'Timepoints expected' in log_str]
    expected_found = log_info[expected_idx[0]]
    assert '1' in expected_found

    # Check timepoints found
    timepoints_idx = [log_idx for log_idx, log_str in enumerate(
                      log_info) if 'Timepoints found' in log_str]
    timepoints_found = log_info[timepoints_idx[0]]
    assert '60' in timepoints_found

    # Check sampling frequency
    sampling_idx = [log_idx for log_idx, log_str in enumerate(
                      log_info) if 'Sampling Frequency' in log_str]
    sampling_found = log_info[sampling_idx[0]]
    assert '10000.0' in sampling_found

    # Check sampling frequency
    started_idx = [log_idx for log_idx, log_str in enumerate(
                      log_info) if 'Sampling started' in log_str]
    started_found = log_info[started_idx[0]]
    assert '10.425007798392297' in started_found

    # Check start time
    start_idx = [log_idx for log_idx, log_str in enumerate(
                      log_info) if 'first trigger' in log_str]
    start_found = log_info[start_idx[0]]
    assert 'Time 0' in start_found

    # Checks json file
    with open(os.path.join(test_path, 'Test_belt_pulse_multifreq_10000.0.json')) as json_file:
        json_data = json.load(json_file)

    # Compares values in json file with ground truth
    assert json_data['SamplingFrequency'] == 10000.0
    assert json_data['StartTime'] == 10.425007798392297
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
    assert os.path.isfile(os.path.join(test_path_output, ('sub-006_ses-01_task-test_rec-'
                                                          'labchart_run-00_physio.json')))
    assert os.path.isfile(os.path.join(test_path_output, ('sub-006_ses-01_task-test_rec-'
                                                          'labchart_run-00_physio.log')))
    assert os.path.isfile(os.path.join(test_path_output, ('sub-006_ses-01_task-test_rec-'
                                                          'labchart_run-00_physio.tsv.gz')))

    # Read log file (note that this file is not the logger file)
    log_filename = 'sub-006_ses-01_task-test_rec-labchart_run-00_physio.log'
    with open(os.path.join(test_path_output, log_filename)) as log_info:
        log_info = log_info.readlines()

    # Check timepoints expected
    expected_idx = [log_idx for log_idx, log_str in enumerate(
                      log_info) if 'Timepoints expected' in log_str]
    expected_found = log_info[expected_idx[0]]
    assert '158' in expected_found

    # Check timepoints found
    timepoints_idx = [log_idx for log_idx, log_str in enumerate(
                      log_info) if 'Timepoints expected' in log_str]
    timepoints_found = log_info[timepoints_idx[0]]
    assert '158' in timepoints_found

    # Check sampling frequency
    sampling_idx = [log_idx for log_idx, log_str in enumerate(
                      log_info) if 'Sampling Frequency' in log_str]
    sampling_found = log_info[sampling_idx[0]]
    assert '1000.0' in sampling_found

    # Check sampling frequency
    started_idx = [log_idx for log_idx, log_str in enumerate(
                      log_info) if 'Sampling started' in log_str]
    started_found = log_info[started_idx[0]]
    assert '0.24499999999989086' in started_found

    # Check start time
    start_idx = [log_idx for log_idx, log_str in enumerate(
                      log_info) if 'first trigger' in log_str]
    start_found = log_info[start_idx[0]]
    assert 'Time 0' in start_found

    # Checks json file
    json_filename = 'sub-006_ses-01_task-test_rec-labchart_run-00_physio.json'
    with open(os.path.join(test_path_output, json_filename)) as json_file:
        json_data = json.load(json_file)

    # Compares values in json file with ground truth
    assert json_data['SamplingFrequency'] == 1000.0
    assert json_data['StartTime'] == 0.24499999999989086
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
    command_str = (f'phys2bids -in {test_filename} -indir {test_path} '
                   f'-chtrig {test_chtrig} -outdir {test_outdir} ',
                   f'-tr {test_tr} -ntp {test_ntp} -thr {test_thr} ',
                   f'-info')
    subprocess.run(command_str, shell=True, check=True)

    breakpoint()

    # Check that plot all file is generated
    assert os.path.isfile(os.path.join(test_path, 'tutorial_file.png'))

    # Read logger file
    files = os.listdir(test_path)
    logger_idx = [log_idx for log_idx, log_str in enumerate(
                      files) if 'phys2bids' in log_str]
    logger_file = files[logger_idx[0]]

    # Check files were correctly read
    with open(os.path.join(test_path, logger_file)) as logger_info:
        logger_info = logger_info.readlines()

    # Get trigger info
    trigger_idx = [log_idx for log_idx, log_str in enumerate(
                      logger_info) if 'Trigger; sampled at' in log_str]
    trigger_found = logger_info[trigger_idx[0]]
    assert '1000.0' in trigger_found

    # Get CO2 info
    co2_idx = [log_idx for log_idx, log_str in enumerate(
                      logger_info) if 'CO2; sampled at' in log_str]
    co2_found = logger_info[co2_idx[0]]
    assert '1000.0' in co2_found

    # Get O2 info
    o2_idx = [log_idx for log_idx, log_str in enumerate(
                      logger_info) if 'O2; sampled at' in log_str]
    o2_found = logger_info[o2_idx[0]]
    assert '1000.0' in o2_found

    # Get pulse info
    pulse_idx = [log_idx for log_idx, log_str in enumerate(
                      logger_info) if 'Pulse; sampled at' in log_str]
    pulse_found = logger_info[pulse_idx[0]]
    assert '1000.0' in pulse_found

    # Remove generated files
    for filename in glob.glob(os.path.join(test_path, 'phys2bids*')):
        os.remove(filename)

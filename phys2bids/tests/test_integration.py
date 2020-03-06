import os
import wget
import glob
import json

from pkg_resources import resource_filename

from phys2bids.phys2bids import phys2bids
from phys2bids._version import get_versions


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
    assert '0.2449' in started_found

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


def test_logger():

    # Move into folder
    test_path = resource_filename('phys2bids', 'tests/data')
    os.system(f'cd {test_path}')

    # Input arguments
    test_filename = 'tutorial_file.txt'
    test_chtrig = 1
    test_outdir = test_path

    # Phys2bids call through terminal
    os.system(f'phys2bids -in {test_filename} -indir {test_path} -chtrig {test_chtrig} -outdir {test_outdir}')

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

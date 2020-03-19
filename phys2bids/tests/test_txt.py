import os
from pkg_resources import resource_filename
from phys2bids.interfaces import txt
from pytest import raises
import wget
import pytest


@pytest.fixture
def samefreq_acq_file():
    url = 'https://osf.io/4yudk/download'  # url to Test_belt_pulse_samefreq.txt
    test_path = resource_filename('phys2bids', 'tests/data')
    test_filename = 'Test_belt_pulse_samefreq_short.txt'
    test_full_path1 = os.path.join(test_path, test_filename)
    if not os.path.isfile(test_full_path1):
        wget.download(url, test_full_path1)
    # chtrig = 2
    return test_full_path1


@pytest.fixture
def multi_lab_file():
    url = 'https://osf.io/q4x2f/download'
    # url to Test_2minRest_trig_multifreq_header_comment.txt
    test_filename = 'Test_2minRest_trig_multifreq_header_comment.txt'
    test_path = resource_filename('phys2bids', 'tests/data')
    test_full_path2 = os.path.join(test_path, test_filename)
    if not os.path.isfile(test_full_path2):
        wget.download(url, test_full_path2)
    # chtrig = 1
    return test_full_path2


@pytest.fixture
def no_time_file():
    # use file without time column
    # # url to the file Test2_trigger_CO2_O2_pulse_1000Hz_534TRs_no_time.txt
    url = 'https://osf.io/u5dq8/download'
    test_filename = 'Test2_trigger_CO2_O2_pulse_1000Hz_534TRs_no_time.txt'
    test_path = resource_filename('phys2bids', 'tests/data')
    test_full_path3 = os.path.join(test_path, test_filename)
    if not os.path.isfile(test_full_path3):
        wget.download(url, test_full_path3)
    # chtrig = 0
    return test_full_path3
# header_T2ntime, channels_T2ntime = txt.read_header_and_channels(test_full_path3, chtrig)


@pytest.fixture
def test_read_header_and_channels(samefreq_acq_file, multi_lab_file):
    header_acq, channels_acq = txt.read_header_and_channels(samefreq_acq_file, 2)
    header_lab, channels_lab = txt.read_header_and_channels(multi_lab_file, 1)
    assert len(header_acq) == 8  # check proper header lenght
    assert len(channels_acq) == 1048560  # check proper number of timepoints
    assert len(header_acq[-1]) == 2  # check extra line is deleted
    # load file with comment
    # url to Test_2minRest_trig_multifreq_header_comment.txt
    assert len(channels_lab[152109 - 9]) == 6  # check the comment has been eliminated
    return header_acq, channels_acq, header_lab, channels_lab


def test_populate_phys_input(samefreq_acq_file, multi_lab_file, test_read_header_and_channels):
    # testing for AcqKnoledge files
    chtrig = 2
    header_acq = test_read_header_and_channels[0]
    assert 'acq' in header_acq[0][0]
    txt.populate_phys_input(samefreq_acq_file, chtrig)
    # testing for labchart files
    # check the printing output according to each format
    header_lab = test_read_header_and_channels[2]
    assert 'Interval=' in header_lab[0]
    chtrig = 1
    txt.populate_phys_input(multi_lab_file, chtrig)


def test_process_labchart(test_read_header_and_channels, no_time_file):
    chtrig = 1
    header_time = test_read_header_and_channels[2]
    channels_time = test_read_header_and_channels[3]
    header_no_time, channels_no_time = txt.read_header_and_channels(no_time_file, 0)
    # test file with header and seconds as unit:
    phys_obj = txt.process_labchart(channels_time, chtrig, header_time)
    assert phys_obj.freq[0] == 1000
    # test when units are min:
    header_time[0][1] = '0.001 min'
    phys_obj = txt.process_labchart(channels_time, chtrig, header_time)
    assert phys_obj.freq[0] == 16.666666666666668
    # test when units are hr:
    header_time[0][1] = '0.001 hr'
    phys_obj = txt.process_labchart(channels_time, chtrig, header_time)
    assert phys_obj.freq[0] == 0.2777777777777778
    # test when units are ms:
    header_time[0][1] = '1 ms'
    phys_obj = txt.process_labchart(channels_time, chtrig, header_time)
    assert phys_obj.freq[0] == 1000
    # test when units are µs:
    header_time[0][1] = '1000 µs'
    phys_obj = txt.process_labchart(channels_time, chtrig, header_time)
    assert phys_obj.freq[0] == 1000
    chtrig = 0
    phys_obj = txt.process_labchart(channels_no_time, chtrig, header_no_time)
    assert len(phys_obj.timeseries) == len(channels_no_time[0]) + 1


def test_process_acq(test_read_header_and_channels):
    header = test_read_header_and_channels[0]
    channels = test_read_header_and_channels[1]
    chtrig = 2
    # test file without header
    with raises(AttributeError) as errorinfo:
        txt.process_acq(channels, chtrig)
    assert 'not supported' in str(errorinfo.value)
    # test when units are msec:
    phys_obj = txt.process_acq(channels, chtrig, header)
    assert phys_obj.freq[0] == 10000
    # test when units are msec:
    header[1][0] = '0.01 sec/sample'
    phys_obj = txt.process_acq(channels, chtrig, header)
    assert phys_obj.freq[0] == 100
    # test when units are in µsec:
    header[1][0] = '1 µsec/sample'
    phys_obj = txt.process_acq(channels, chtrig, header)
    assert phys_obj.freq[0] == 1000000.0
    # test when units are in Hz:
    header[1][0] = '100 Hz'
    phys_obj = txt.process_acq(channels, chtrig, header)
    assert phys_obj.freq[0] == 100
    # test when units are in kHz:
    header[1][0] = '1 kHz'
    phys_obj = txt.process_acq(channels, chtrig, header)
    assert phys_obj.freq[0] == 1000
    # test when units are in MHz:
    header[1][0] = '1 MHz'
    phys_obj = txt.process_acq(channels, chtrig, header)
    assert phys_obj.freq[0] == 1000000
    # test when units are not valid:
    header[1][0] = '1 GHz'
    with raises(AttributeError) as errorinfo:
        phys_obj = txt.process_acq(channels, chtrig, header)
    assert 'not in a valid AcqKnowledge' in str(errorinfo.value)


def test_raises(test_read_header_and_channels):
    # testing error for files without header for populate_phys_input
    # url to the file Test_belt_pulse_samefreq_no_header.txt
    url = 'https://osf.io/sre3h/download'
    test_filename = 'Test_belt_pulse_samefreq_no_header.txt'
    test_path = resource_filename('phys2bids', 'tests/data')
    test_full_path = os.path.join(test_path, test_filename)
    if not os.path.isfile(test_full_path):
        wget.download(url, test_full_path)
    chtrig = 2
    with raises(AttributeError) as errorinfo:
        txt.populate_phys_input(test_full_path, chtrig)
    assert 'not supported' in str(errorinfo.value)
    # test file without header for process_acq
    header, channels = txt.read_header_and_channels(test_full_path, chtrig)
    with raises(AttributeError) as errorinfo:
        txt.process_acq(channels, chtrig)
    assert 'not supported' in str(errorinfo.value)
    os.remove(test_full_path)
    # now for labchart read
    # testing file already downloaded in the other tests
    header = test_read_header_and_channels[2]
    channels = test_read_header_and_channels[3]
    chtrig = 1
    with raises(AttributeError) as errorinfo:
        txt.process_labchart(test_full_path, chtrig)
    assert 'not supported' in str(errorinfo.value)
    # test when units are not valid for process_labchart
    header[0][1] = ' 1 gHz'
    with raises(AttributeError) as errorinfo:
        txt.process_labchart(channels, chtrig, header)
    assert 'not in a valid LabChart' in str(errorinfo.value)


def test_multifreq(test_read_header_and_channels):
    header = test_read_header_and_channels[2]
    channels = test_read_header_and_channels[3]
    chtrig = 1
    phys_obj = txt.process_labchart(channels, chtrig, header)
    new_freq = txt.check_multifreq(phys_obj.timeseries, [phys_obj.freq[0]] * len(phys_obj.freq))
    assert new_freq[-3] == 40
    assert new_freq[-2] == 500
    assert new_freq[-4] == 100

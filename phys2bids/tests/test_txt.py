import os
from pkg_resources import resource_filename
from phys2bids.interfaces import txt
from pytest import raises
import wget
import pytest
url = 'https://osf.io/sdz4n/download'  # url to Test_belt_pulse_samefreq.txt
test_path = resource_filename('phys2bids', 'tests/data')
test_filename = 'Test_belt_pulse_samefreq.txt'
test_full_path1 = os.path.join(test_path, test_filename)
wget.download(url, test_full_path1)
chtrig = 2
header_TBSF, channels_TBSF = txt.read_header_and_channels(test_full_path1, chtrig)
# load file with comment
url = 'https://osf.io/q4x2f/download'
# url to Test_2minRest_trig_multifreq_header_comment.txt
test_filename = 'Test_2minRest_trig_multifreq_header_comment.txt'
test_path = resource_filename('phys2bids', 'tests/data')
test_full_path2 = os.path.join(test_path, test_filename)
wget.download(url, test_full_path2)
chtrig = 1
header_T2MF, channels_T2MF = txt.read_header_and_channels(test_full_path2, chtrig)
# use file without time column
# # url to the file Test2_trigger_CO2_O2_pulse_1000Hz_534TRs_no_time.txt
url = 'https://osf.io/u5dq8/download'
test_filename = 'Test2_trigger_CO2_O2_pulse_1000Hz_534TRs_no_time.txt'
test_path = resource_filename('phys2bids', 'tests/data')
test_full_path3 = os.path.join(test_path, test_filename)
wget.download(url, test_full_path3)
chtrig = 0
header_T2ntime, channels_T2ntime = txt.read_header_and_channels(test_full_path3, chtrig)


testdata = [(header_TBSF, channels_TBSF, header_T2MF, channels_T2MF)]
@pytest.mark.parametrize("header_acq, channels_acq, header_lab, channels_lab", testdata)
def test_read_header_and_channels(header_acq, channels_acq, header_lab, channels_lab):
    assert len(header_acq) == 16  # check proper header lenght
    assert len(channels_acq) == 1336816  # check proper number of timepoints
    assert len(header_acq[-1]) == 6  # check extra line is deleted
    # load file with comment
    # url to Test_2minRest_trig_multifreq_header_comment.txt
    assert len(channels_lab[152109 - 9]) == 6  # check the comment has been eliminated


testdata = [(header_TBSF, header_T2MF)]
@pytest.mark.parametrize("header_acq,header_lab", testdata)
def test_populate_phys_input(header_acq, header_lab):
    # testing for AcqKnoledge files
    test_filename = 'Test_belt_pulse_samefreq.txt'
    test_path = resource_filename('phys2bids', 'tests/data')
    test_full_path = os.path.join(test_path, test_filename)
    chtrig = 1
    assert 'acq' in header_acq[0][0]
    txt.populate_phys_input(test_full_path, chtrig)
    # testing for labchart files
    test_filename = 'Test_2minRest_trig_multifreq_header_comment.txt'
    test_full_path = os.path.join(test_path, test_filename)
    chtrig = 1
    # check the printing output according to each format
    assert 'Interval=' in header_lab[0]
    txt.populate_phys_input(test_full_path, chtrig)


testdata = [(header_T2MF, channels_T2MF, header_T2ntime, channels_T2ntime)]
@pytest.mark.parametrize("header_time, channels_time, header_no_time, channels_no_time", testdata)
def test_process_labchart(header_time, channels_time, header_no_time, channels_no_time):
    chtrig = 1
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
    phys_obj = txt.process_labchart(channels_no_time, chtrig, header_no_time)
    assert len(phys_obj.timeseries) == len(channels_no_time[0]) + 1


testdata = [(header_TBSF, channels_TBSF)]
@pytest.mark.parametrize("header,channels", testdata)
def test_process_acq(header, channels):
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


def test_raises():
    # testing error for files without header for populate_phys_input
    # url to the file Test_belt_pulse_samefreq_no_header.txt
    url = 'https://osf.io/sre3h/download'
    test_filename = 'Test_belt_pulse_samefreq_no_header.txt'
    test_path = resource_filename('phys2bids', 'tests/data')
    test_full_path = os.path.join(test_path, test_filename)
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
    test_path = resource_filename('phys2bids', 'tests/data')
    test_filename = 'Test_2minRest_trig_multifreq_header_comment.txt'
    test_full_path = os.path.join(test_path, test_filename)
    chtrig = 1
    header, channels = txt.read_header_and_channels(test_full_path, chtrig)
    with raises(AttributeError) as errorinfo:
        txt.process_labchart(test_full_path, chtrig)
    assert 'not supported' in str(errorinfo.value)
    # test when units are not valid for process_labchart
    header[0][1] = ' 1 gHz'
    with raises(AttributeError) as errorinfo:
        txt.process_labchart(channels, chtrig, header)
    assert 'not in a valid LabChart' in str(errorinfo.value)


testdata = [(header_T2MF, channels_T2MF)]
@pytest.mark.parametrize("header,channels", testdata)
def test_multifreq(header, channels):
    chtrig = 1
    phys_obj = txt.process_labchart(channels, chtrig, header)
    new_freq = txt.check_multifreq(phys_obj.timeseries, [phys_obj.freq[0]] * len(phys_obj.freq))
    assert new_freq[-3] == 40


testdata = [(test_full_path1, test_full_path2, test_full_path3)]
@pytest.mark.parametrize("file1,file2,file3", testdata)
def eliminate_files(file1, file2, file3):
    os.remove(file1)
    os.remove(file2)
    os.remove(file3)

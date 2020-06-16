import math

import pytest
from pytest import raises

from phys2bids.interfaces import txt


@pytest.fixture(scope='function')
def loaded_acq_file(samefreq_short_txt_file):
    chtrig = 2
    header_acq, channels_acq = txt.read_header_and_channels(samefreq_short_txt_file, chtrig)

    # just a few quick checks to make sure the data loaded correctly
    assert len(header_acq) == 8  # check proper header lenght
    assert len(channels_acq) == 1048560  # check proper number of timepoints
    assert len(header_acq[-1]) == 2  # check extra line is deleted
    assert 'acq' in header_acq[0][0]

    return header_acq, channels_acq, chtrig


@pytest.fixture(scope='function')
def loaded_lab_file(multifreq_lab_file):
    chtrig = 1
    header_lab, channels_lab = txt.read_header_and_channels(multifreq_lab_file, chtrig)

    # just a few quick checks to make sure the data loaded correctly
    assert len(channels_lab[0]) == 5
    assert 'Interval=' in header_lab[0]

    return header_lab, channels_lab, chtrig


def test_populate_phys_input(samefreq_short_txt_file, multifreq_lab_file):
    # testing for AcqKnowledge files
    txt.populate_phys_input(samefreq_short_txt_file, chtrig=2)
    # testing for LabChart files
    txt.populate_phys_input(multifreq_lab_file, chtrig=1)


@pytest.mark.parametrize('units, expected', [
    ('0.001 s', 1000),
    ('0.001 min', 16.666666666666668),
    ('0.001 hr', 0.2777777777777778),
    ('1 ms', 1000),
    ('1000 µs', 1000)
])
def test_process_labchart(loaded_lab_file, units, expected):
    header, channels, chtrig = loaded_lab_file
    header[0][1] = units
    phys_obj = txt.process_labchart(channels, chtrig=chtrig, header=header)
    assert math.isclose(phys_obj.freq[0], expected)


def test_process_labchart_notime(notime_lab_file):
    chtrig = 0
    header, channels = txt.read_header_and_channels(notime_lab_file, chtrig)
    phys_obj = txt.process_labchart(channels, chtrig=chtrig, header=header)
    assert len(phys_obj.timeseries) == len(channels[0]) + 1


def test_process_labchart_errors(loaded_lab_file):
    header, channels, chtrig = loaded_lab_file

    # test file without header
    with raises(AttributeError) as errorinfo:
        txt.process_labchart(channels, chtrig=chtrig)
    assert 'not supported' in str(errorinfo.value)

    # test when units are not valid for process_labchart
    header[0][1] = ' 1 gHz'
    with raises(AttributeError) as errorinfo:
        txt.process_labchart(channels, chtrig=chtrig, header=header)
    assert 'not in a valid LabChart' in str(errorinfo.value)


@pytest.mark.parametrize('units, expected', [
    ('1 µsec/sample', 1000000),
    ('1 msec/sample', 1000),
    ('0.01 sec/sample', 100),
    ('0.001 min/sample', 100 / 6),
    ('100 Hz', 100),
    ('1 kHz', 1000),
    ('1 MHz', 1000000)
])
def test_process_acq(loaded_acq_file, units, expected):
    header, channels, chtrig = loaded_acq_file

    # set units to test that expected frequency is generated correctly
    header[1][0] = units
    phys_obj = txt.process_acq(channels, chtrig=chtrig, header=header)
    assert math.isclose(phys_obj.freq[0], expected)


def test_process_acq_errors(loaded_acq_file):
    header, channels, chtrig = loaded_acq_file

    # test file without header
    with raises(AttributeError) as errorinfo:
        txt.process_acq(channels, chtrig=chtrig)
    assert 'not supported' in str(errorinfo.value)

    # test when units are not valid:
    header[1][0] = '1 GHz'
    with raises(AttributeError) as errorinfo:
        txt.process_acq(channels, chtrig=chtrig, header=header)
    assert 'not in a valid AcqKnowledge' in str(errorinfo.value)


def test_noheader_acq_error(samefreq_noheader_txt_file):
    chtrig = 2
    with raises(AttributeError) as errorinfo:
        txt.populate_phys_input(samefreq_noheader_txt_file, chtrig=chtrig)
    assert 'not supported' in str(errorinfo.value)

    # test file without header for process_acq
    header, channels = txt.read_header_and_channels(samefreq_noheader_txt_file, chtrig)
    with raises(AttributeError) as errorinfo:
        txt.process_acq(channels, chtrig=chtrig)
    assert 'not supported' in str(errorinfo.value)


def test_multifreq(loaded_lab_file):
    header, channels, chtrig = loaded_lab_file
    phys_obj = txt.process_labchart(channels, chtrig=chtrig, header=header)
    new_freq = txt.check_multifreq(phys_obj.timeseries, [phys_obj.freq[0]] * len(phys_obj.freq))
    assert new_freq[-3:] == [100, 40, 500]

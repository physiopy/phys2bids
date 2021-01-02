import os
import ssl
from urllib.request import urlretrieve

import pytest


def pytest_addoption(parser):
    parser.addoption('--skipintegration', action='store_true',
                     default=False, help='Skip integration tests.')


@pytest.fixture
def skip_integration(request):
    return request.config.getoption('--skipintegration')


def fetch_file(osf_id, path, filename):
    """
    Fetches file located on OSF and downloads to `path`/`filename`1

    Parameters
    ----------
    osf_id : str
        Unique OSF ID for file to be downloaded. Will be inserted into relevant
        location in URL: https://osf.io/{osf_id}/download
    path : str
        Path to which `filename` should be downloaded. Ideally a temporary
        directory
    filename : str
        Name of file to be downloaded (does not necessarily have to match name
        of file on OSF)

    Returns
    -------
    full_path : str
        Full path to downloaded `filename`
    """
    # This restores the same behavior as before.
    # this three lines make tests dowloads work in windows
    if os.name == 'nt':
        orig_sslsocket_init = ssl.SSLSocket.__init__
        ssl.SSLSocket.__init__ = lambda *args, cert_reqs=ssl.CERT_NONE, **kwargs: orig_sslsocket_init(*args, cert_reqs=ssl.CERT_NONE, **kwargs)
        ssl._create_default_https_context = ssl._create_unverified_context
    url = 'https://osf.io/{}/download'.format(osf_id)
    full_path = os.path.join(path, filename)
    if not os.path.isfile(full_path):
        urlretrieve(url, full_path)
    return full_path


@pytest.fixture(scope='session')
def testpath(tmp_path_factory):
    """ Test path that will be used to download all files """
    return tmp_path_factory.getbasetemp()


@pytest.fixture
def samefreq_full_acq_file(testpath):
    return fetch_file('27gqb', testpath,
                      'Test_belt_pulse_samefreq.acq')


@pytest.fixture
def samefreq_short_txt_file(testpath):
    return fetch_file('4yudk', testpath,
                      'Test_belt_pulse_samefreq_short.txt')


@pytest.fixture
def samefreq_noheader_txt_file(testpath):
    return fetch_file('xbwq9', testpath,
                      'Test_belt_pulse_samefreq_no_header.txt')


@pytest.fixture
def multifreq_acq_file(testpath):
    return fetch_file('9a7yv', testpath,
                      'Test_belt_pulse_multifreq.acq')


@pytest.fixture
def multifreq_lab_file(testpath):
    return fetch_file('7se4t', testpath,
                      'Test1_multifreq_onescan.txt')


@pytest.fixture
def notime_lab_file(testpath):
    return fetch_file('cv5zr', testpath,
                      'Test2_samefreq_onescan_notime.txt')


@pytest.fixture
def multi_run_file(testpath):
    return fetch_file('gvy84', testpath,
                      'Test2_samefreq_TWOscans.txt')

@pytest.fixture
def matlab_file_labchart(testpath):
    return fetch_file('2j43t', testpath,
                      'test_2minRest.mat')


@pytest.fixture
def matlab_file_acq(testpath):
    return fetch_file('mc96w', testpath,
                      'Test_belt_pulse_multifreq.mat')

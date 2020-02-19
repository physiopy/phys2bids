import wget
import os
from pkg_resources import resource_filename
import csv
from phys2bids import _version


def test_run():
    # testing integration for acq file in txt format
    url = 'https://osf.io/sdz4n/download'  # url to Test_belt_pulse_samefreq.txt
    test_path = resource_filename('phys2bids', 'tests/data')
    test_filename = 'Test_belt_pulse_samefreq.txt'
    test_full_path = os.path.join(test_path, test_filename)
    wget.download(url, test_full_path)
    chtrig = 2
    os.system('mkdir $HOME/test_run')
    os.system('phys2bids -in ' + test_full_path + ' -info -indir '
              + test_path + ' -chtrig ' + str(chtrig) + ' -outdir $HOME/test_run '
              + '-chplot $HOME/test_run/plot.png')
    os.system('phys2bids -in ' + test_full_path + ' -indir '
              + test_path + ' -chtrig ' + str(chtrig) + ' -outdir $HOME/test_run '
              + '-chplot $HOME/test_run/plot.png')
    home = os.path.expanduser('~')
    os.chdir(home + '/test_run')
    out_dir = os.listdir()
    tsv_files = [item for item in out_dir if item.endswith('.tsv')]
    assert len(tsv_files) == 2
    for log_f in tsv_files:
        log = []
        with open(log_f) as fd:
            rd = csv.reader(fd, delimiter="\t", quotechar='"')
            for row in rd:
                log.append(row)
        assert _version.get_versions()['version'] in log[0][3]
    return

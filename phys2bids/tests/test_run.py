import wget
import os
from pkg_resources import resource_filename


def test_run():
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
    return

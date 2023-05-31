from phys2bids import physio_obj as po
from phys2bids import slice4phys as slice
import importlib
import numpy as np
import neurokit2 as nk

importlib.reload(slice)

sub_idx=27
path_raw = 'D:\\data\\final_experiment\\physio\\%s\\sub-%02d' %('raw', sub_idx)
data_exp = nk.read_acqknowledge(path_raw + '\\sub-%02d.acq' %(sub_idx), sampling_rate=500, resample_method='interpolation', impute_missing=True)
data_exp=data_exp[0]


def test_split_signal_to_runs(path_data, data_exp):
    # test_time = np.array([0, 1, 1, 2, 3, 5, 8, 13])
    # test_trigger = np.array([0, 1, 0, 0, 0, 0, 0, 0])
    # test_chocolate = np.array([1, 0, 0, 1, 0, 0, 1, 0])
    # test_timeseries = [test_time, test_trigger, test_chocolate]
    test_timeseries =[data_exp.trig_1.to_numpy(), data_exp.trig_8.to_numpy()]
    test_freq = [200, 500]
    test_chn_name = ['channel_1', 'trigger']
    test_units = ['s', 's']
    test_chtrig = 1
    num_channnels = len(test_timeseries)

    blueprint_in = po.BlueprintInput(test_timeseries, test_freq, test_chn_name,
                                     test_units, test_chtrig)

    importlib.reload(slice)
    run_onset_raw, run_offset_raw = slice.split_signal_to_runs(blueprint_in, sensitivity=30, manual_check=True, padding=9)
import numpy as np
import pandas as pd

import phys2bids.physio_obj as po
import phys2bids.slice4phys as slice


def test_slice_signal_to_runs(path_data):
    # read in data
    data_exp = pd.read_csv(path_data, sep="\t")

    # create blueprintinput
    test_chocolate = np.array(data_exp.EDA)
    test_trigger = np.array(data_exp.trig_8)
    test_timeseries = [test_trigger, test_chocolate]
    test_freq = [500, 100]
    test_chn_name = ["trigger", "chocolate"]
    test_units = ["s", "sweetness"]
    test_chtrig = 0
    num_channnels = len(test_timeseries)

    phys_in = po.BlueprintInput(test_timeseries, test_freq, test_chn_name, test_units, test_chtrig)

    # slice phys input into runs
    run_data, onsets_start, onsets_end = slice.split_signal_to_runs(
        phys_in, manual_check=True, sensitivity=20, padding=9
    )

    assert len(run_data) == len(onsets_start) == len(onsets_end)

"""
1. Extract segments from physio file.
    - Each segment must be named according to the onset time if there are
      multiple segments. If there is only one segment, then there is no need
      for a timestamp.
2. Extract trigger periods from physio segments.
    - Onset
3. Extract scan times
    - Name
    - Onset with subsecond resolution as close to trigger pulse as possible
    - Duration (from TR * data dimension)
4. Calculate difference in time between each scan and each physio trigger.
5. Use differences to identify similar values across as many physio/scan pairs as possible.
    - Physio may be missing if trigger failed.
    - Physio may be delayed if task was manually trigger after scan began
      (sometimes happens with resting-state scans where the task itself isn't
      very important).
    - Scan may be missing if it wasn't converted (e.g., a scan stopped early
      and re-run).
6. Assign scan names to trigger period, infer times for other scan times
   in cases where trigger failed, and ignore trigger periods associated with
   scans that weren't kept in the BIDS dataset.
"""
from bids import BIDSLayout
import pandas as pd
import numpy as np


def extract_physio_onsets(f):
    """
    TODO: Stitch segments together before extracting onsets.
    """
    import bioread
    from operator import itemgetter
    from itertools import groupby
    d = bioread.read_file(f)
    c = d.channels[-1]
    samplerate = 1. / c.samples_per_second
    data = c.data
    scan_idx = np.where(data > 0)[0]
    # Get groups of consecutive numbers in index
    groups = []
    for k, g in groupby(enumerate(scan_idx), lambda x: x[0] - x[1]):
        groups.append(list(map(itemgetter(1), g)))

    # Extract onsets
    onsets = np.array([g[0] for g in groups])
    onsets_in_sec = onsets * samplerate
    df = pd.DataFrame(
        columns=['onset'],
        data=onsets_in_sec,
    )
    df['index'] = onsets
    return df


def synchronize_onsets(phys_df, scan_df):
    """There can be fewer physios than scans (task failed to trigger physio)
    or fewer scans than physios (aborted scans are not retained in BIDS dataset).

    Both phys_df and scan_df should be sorted in chronological order (i.e.,
    ascending by "onset").
    Onsets are in seconds. The baseline doesn't matter.
    """
    # Get difference between each scan onset and each physio trigger onset
    diffs = np.zeros((scan_df.shape[0], phys_df.shape[0]))
    for i, i_row in scan_df.iterrows():
        for j, j_row in phys_df.iterrows():
            onset_diff = i_row['onset'] - j_row['onset']
            diffs[i, j] = onset_diff

    # Find a scan onset for each physio onset where the time difference
    # roughly matches up across as many physio onsets as possible
    # Not necessarily *all* physio onsets, since sometimes scans are stopped
    # early or re-run, and may not end up in the final BIDS dataset.
    sel_rows = []
    for i_scan in range(diffs.shape[0]):
        # difference between onset of scan and first physio
        # if the scan corresponds to the physio, then this difference
        # should be roughly equal for all corresponding scan/physio pairs
        # TODO: Loop through physio onsets and combine findings across to
        # account for dropped scans.
        val = diffs[i_scan, 5]  # if scan was dropped, this won't work.

        # find one row for each column
        diffs_from_phys_onset = diffs - val
        np.set_printoptions(suppress=True)
        print(np.min(np.abs(diffs_from_phys_onset), axis=0))
        # Here we see one row (i_scan) with very low values (0-1) across many
        # columns, indicating that that scan onset corresponds to the physio
        # onset indexed in "val"

        diff_thresh = 5  # threshold for variability
        idx = np.where(np.abs(diffs - val) < diff_thresh)[1]
        print(idx)
        if np.array_equal(idx, np.arange(diffs.shape[1])):
            print('GOT IT: {} (row {})'.format(val, i_scan))
            sel_rows.append(i_row)
    if len(sel_rows) != 1:
        # We hope for one solution: one time-shift applied to the scan onsets
        # to synchronize them with the physio onsets.
        raise Exception('Bad sel_rows: {}'.format(len(sel_rows)))
    sel_row = sel_rows[0]
    clock_diff = scan_df.loc[sel_row, 'onset'] - phys_df.loc[0, 'onset']
    print('Scan onsets must be shifted {}s to match physio onsets'.format(clock_diff))

    # Get onset of each scan in terms of the physio time series
    scan_df['phys_onset'] = scan_df['onset'] - clock_diff
    samplerate = ((phys_df.loc[1, 'index'] - phys_df.loc[0, 'index']) /
                  (phys_df.loc[1, 'onset'] - phys_df.loc[0, 'onset']))
    scan_df['phys_index'] = (scan_df['phys_onset'] * samplerate).astype(int)
    return scan_df


def stitch_segments(physio_data):
    """Merge segments in BioPac physio file. The segments must be named with
    timestamps, so that the actual time difference can be calculated and zeros
    can be inserted in the gaps.

    Timestamps have second-level resolution, so stitching them together adds
    uncertainty to timing, which should be accounted for in the onset
    synchronization.
    """
    pass


def split_physio(scan_df, physio_file):
    """Extract timeseries associated with each scan.
    Key in dict is scan name or physio filename and value is physio data in
    some format.
    Uses the onsets, durations, and filenames from scan_df, and the time series
    data from physio_file.
    """
    pass


def save_physio(physio_data_dict):
    """Save split physio data to BIDS dataset.
    """
    pass


def determine_scan_durations(scan_df):
    """Extract scan durations by loading fMRI files/metadata and
    multiplying TR by number of volumes. This can be used to determine the
    endpoints for the physio files.
    """
    pass


def workflow(dset, physio_file, sub, ses=None):
    layout = BIDSLayout(dset)
    scans_file = layout.get(extension='tsv', suffix='scans', sub=sub, ses=ses)
    scan_df = pd.read_table(scans_file)
    scan_df = determine_scan_durations(scan_df)
    physio_df = extract_physio_onsets(physio_file)
    scan_df = synchronize_onsets(physio_df, scan_df)
    # Extract timeseries associated with each scan. Key in dict is scan name or
    # physio filename and key is physio data in some format.
    physio_data_dict = split_physio(scan_df, physio_file)
    save_physio(layout, physio_data_dict)

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
    # Get difference between each physio trigger onset and each scan onset
    diffs = np.zeros((scan_df.shape[0], phys_df.shape[0]))
    for i, i_scan in scan_df.iterrows():
        for j, j_phys in phys_df.iterrows():
            onset_diff = j_phys['onset'] - i_scan['onset']
            diffs[i, j] = onset_diff

    # Find the delay that gives the smallest difference between scan onsets
    # and physio onsets
    sel_rows = []
    selected = (None, None)
    thresh = 1000
    for i_scan in range(diffs.shape[0]):
        for j_phys in range(diffs.shape[1]):
            test_offset = diffs[i_scan, j_phys]
            diffs_from_phys_onset = diffs - test_offset
            diffs_from_abs = np.abs(diffs_from_phys_onset)
            min_diff_row_idx = np.argmin(diffs_from_abs, axis=0)
            min_diff_col_idx = np.arange(len(min_diff_row_idx))
            min_diffs = diffs_from_abs[min_diff_row_idx, min_diff_col_idx]
            min_diff_sum = np.sum(min_diffs)
            if min_diff_sum < thresh:
                selected = (i_scan, j_phys)
                thresh = min_diff_sum
    print('Selected solution: {}'.format(selected))
    offset = diffs[selected[0], selected[1]]

    # Isolate close, but negative relative onsets, to ensure scan onsets are
    # always before or at physio triggers.
    close_thresh = 2  # threshold for "close" onsets
    diffs_from_phys_onset = diffs - offset
    min_diff_row_idx = np.argmin(np.abs(diffs_from_phys_onset), axis=0)
    min_diff_col_idx = np.arange(len(min_diff_row_idx))
    min_diffs = diffs_from_phys_onset[min_diff_row_idx, min_diff_col_idx]
    min_diffs_tmp = min_diffs[abs(min_diffs) <= close_thresh]
    min_val = min(min_diffs_tmp)
    min_diffs += min_val
    offset += min_val
    print('Scan DF should be adjusted forward by {} seconds'.format(offset))

    # Get onset of each scan in terms of the physio time series
    scan_df['phys_onset'] = scan_df['onset'] + offset
    samplerate = ((phys_df.loc[1, 'index'] - phys_df.loc[0, 'index']) /
                  (phys_df.loc[1, 'onset'] - phys_df.loc[0, 'onset']))
    scan_df['phys_index'] = (scan_df['phys_onset'] * samplerate).astype(int)
    return scan_df


def stitch_segments(physio_file):
    """Merge segments in BioPac physio file. The segments must be named with
    timestamps, so that the actual time difference can be calculated and zeros
    can be inserted in the gaps.

    Timestamps have second-level resolution, so stitching them together adds
    uncertainty to timing, which should be accounted for in the onset
    synchronization.
    """
    import bioread
    d = bioread.read_file(physio_file)
    em_df = pd.DataFrame()
    c = 0
    for em in d.event_markers:
        print('{}: {}'.format(em.text, em.sample_index))
        try:
            em_dt = datetime.strptime(em.text, '%a %b %d %Y %H:%M:%S')
        except:
            continue
        em_df.loc[c, 'segment'] = em.text
        em_df.loc[c, 'start_idx'] = em.sample_index
        em_df.loc[c, 'onset_time'] = em_dt
        c += 1

    # segment timestamp resolution is one second
    # we need to incorporate possible variability into that
    idx_diff = em_df['start_idx'].diff()
    time_diff = em_df['onset_time'].diff().dt.total_seconds()

    for i in range(em_df.shape[0] - 1):
        time_pair_diff = time_diff.iloc[i+1]
        idx_pair_diff = idx_diff.iloc[i+1] / d.samples_per_second
        if abs(idx_pair_diff - time_pair_diff) > 2:
            diff_diff_sec = time_pair_diff - idx_pair_diff
            diff_diff_idx = diff_diff_sec * d.samples_per_second
            # Now we have the sizes, we can load the data and insert zeros.


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

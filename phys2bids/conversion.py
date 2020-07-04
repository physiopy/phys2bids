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
import os.path as op
from operator import itemgetter
from itertools import groupby
import logging

from bids import BIDSLayout
import pandas as pd
import numpy as np
import nibabel as nib

from .slice4phys import update_name, slice_phys
from .utils import drop_bids_multicontrast_keys
from .physio_obj import BlueprintOutput

LGR = logging.getLogger(__name__)


def load_scan_data(layout, sub, ses=None):
    """
    Extract subject- and session-specific scan onsets and durations from BIDSLayout.

    Parameters
    ----------
    layout : BIDSLayout
    sub : str
    ses : str or None, optional

    Returns
    -------
    df : pandas.DataFrame
        DataFrame with the following columns: 'filename', 'original_filename',
        'acq_time', 'duration', 'onset'.
        'filename' is the name of the BIDS file minus within-acquisition entities.
        'original_filename' is the actual, existing BIDS file.
        'acq_time' is the acquisition time in datetime format.
        'duration' is the scan duration in seconds.
        'onset' is the scan onset in seconds, starting with zero at the first scan.
    """
    # This is the strategy we'll use in the future. Commented out for now.
    # scans_file = layout.get(extension='.tsv', suffix='scans', subject=sub, session=ses)
    # df = pd.read_table(scans_file)

    # Collect acquisition times
    # NOTE: Will be replaced with scans file when heudiconv makes the change
    img_files = layout.get(datatype='func', suffix='bold',
                           extension=['.nii.gz', '.nii'],
                           subject=sub, session=ses)
    df = pd.DataFrame(
        columns=['original_filename', 'acq_time'],
    )
    for i, img_file in enumerate(img_files):
        df.loc[i, 'original_filename'] = img_file.path
        df.loc[i, 'acq_time'] = img_file.get_metadata()['AcquisitionTime']

    # Get generic filenames (without within-acquisition entities like echo)
    df['filename'] = df['original_filename'].apply(drop_bids_multicontrast_keys)

    # Get "first" scan from multi-file acquisitions
    df['acq_time'] = pd.to_datetime(df['acq_time'])
    df = df.sort_values(by='acq_time')
    df = df.drop_duplicates(subset='filename', keep='first', ignore_index=True)

    # Now back to general-purpose code
    df = determine_scan_durations(layout, df, sub=sub, ses=ses)
    df = df.dropna(subset=['duration'])  # limit to relevant scans

    # Convert scan times to relative onsets (first scan is at 0 seconds)
    df['onset'] = (df['acq_time'] - df['acq_time'].min())
    df['onset'] = df['onset'].dt.total_seconds()
    return df


def determine_scan_durations(layout, scan_df, sub, ses=None):
    """
    Extract scan durations by loading fMRI files/metadata and
    multiplying TR by number of volumes. This can be used to determine the
    endpoints for the physio files.

    Parameters
    ----------
    layout : bids.layout.BIDSLayout
        Dataset layout. Used to identify functional scans and load them to
        determine scan durations.
    scan_df : pandas.DataFrame
        Scans DataFrame containing functional scan filenames and onset times.
    sub : str
        Subject ID.
    ses : str or None, optional
        Session ID. If None, then no session.

    Returns
    -------
    scan_df : pandas.DataFrame
        Updated DataFrame with new "duration" column. Calculated durations are
        in seconds.
    """
    # TODO: parse entities in func files for searches instead of larger search.
    func_files = layout.get(datatype='func', suffix='bold',
                            extension=['.nii.gz', '.nii'],
                            subject=sub, session=ses)
    scan_df['duration'] = None
    for func_file in func_files:
        filename = func_file.path
        if filename in scan_df['original_filename'].values:
            n_vols = nib.load(filename).shape[3]
            tr = func_file.get_metadata()['RepetitionTime']
            duration = n_vols * tr
            scan_df.loc[scan_df['original_filename'] == filename, 'duration'] = duration
        else:
            LGR.info('Skipping {}'.format(op.basename(filename)))
    return scan_df


def extract_physio_onsets(trigger_timeseries, freq, threshold=0.5):
    """
    Collect onsets from physio file, both in terms of seconds and time series
    indices.

    Parameters
    ----------
    trigger_timeseries : 1D numpy.ndarray
        Trigger time series.
    freq : float
        Frequency of trigger time series, in Hertz.
    threshold : float, optional
        Threshold to apply to binarize trigger time series.

    Returns
    -------
    df : pandas.DataFrame
        DataFrame with one row for each trigger period and three columns:
        onset (in seconds), index (onsets in index of time series array),
        and duration (in seconds).
    """
    samplerate = 1. / freq
    scan_idx = np.where(trigger_timeseries > 0)[0]
    # Get groups of consecutive numbers in index
    groups = []
    for k, g in groupby(enumerate(scan_idx), lambda x: x[0] - x[1]):
        groups.append(list(map(itemgetter(1), g)))

    # Extract onsets
    onsets = np.array([g[0] for g in groups])
    onsets_in_sec = onsets * samplerate
    durations = np.array([g[-1] - g[0] for g in groups])
    durations_in_sec = durations * samplerate
    df = pd.DataFrame(
        columns=['onset'],
        data=onsets_in_sec,
    )
    df['index'] = onsets
    df['duration'] = durations_in_sec
    return df


def synchronize_onsets(phys_df, scan_df):
    """
    Find matching scans and physio trigger periods from separate DataFrames,
    using time differences within each DataFrame.

    There can be fewer physios than scans (task failed to trigger physio)
    or fewer scans than physios (aborted scans are not retained in BIDS dataset).

    Onsets are in seconds. The baseline (i.e., absolute timing) doesn't matter.
    Relative timing is all that matters.

    Parameters
    ----------
    phys_df : pandas.DataFrame
        DataFrame with onsets of physio trigger periods, in seconds. The
        baseline does not matter, so it is reasonable for the onsets to start
        with zero. The following columns are required: 'onset', 'index'.
    scan_df : pandas.DataFrame
        DataFrame with onsets and names of functional scans from BIDS dataset,
        in seconds. The baseline does not matter, so it is reasonable for the
        onsets to start with zero. The following columns are required: 'onset',
        'duration'.

    Returns
    -------
    scan_df : pandas.DataFrame
        Updated scan DataFrame, now with columns for predicted physio onsets in
        seconds and in indices of the physio trigger channel, as well as scan
        duration in units of the physio trigger channel.
    """
    phys_df = phys_df.sort_values(by=['onset'])
    scan_df = scan_df.sort_values(by=['onset'])

    # Get difference between each physio trigger onset and each scan onset
    onset_diffs = np.zeros((scan_df.shape[0], phys_df.shape[0]))
    for i, i_scan in scan_df.iterrows():
        for j, j_phys in phys_df.iterrows():
            onset_diff = j_phys['onset'] - i_scan['onset']
            onset_diffs[i, j] = onset_diff

    # Find the delay that gives the smallest difference between scan onsets
    # and physio onsets
    selected = (None, None)
    thresh = 1000
    for i_scan in range(onset_diffs.shape[0]):
        for j_phys in range(onset_diffs.shape[1]):
            test_offset = onset_diffs[i_scan, j_phys]
            diffs_from_phys_onset = onset_diffs - test_offset
            diffs_from_abs = np.abs(diffs_from_phys_onset)
            min_diff_row_idx = np.argmin(diffs_from_abs, axis=0)
            min_diff_col_idx = np.arange(len(min_diff_row_idx))
            min_diffs = diffs_from_abs[min_diff_row_idx, min_diff_col_idx]
            min_diff_sum = np.sum(min_diffs)
            if min_diff_sum < thresh:
                selected = (i_scan, j_phys)
                thresh = min_diff_sum

    offset = onset_diffs[selected[0], selected[1]]

    # Isolate close, but negative relative onsets, to ensure scan onsets are
    # always before or at physio triggers.
    close_thresh = 2  # threshold for "close" onsets, in seconds
    diffs_from_phys_onset = onset_diffs - offset
    min_diff_row_idx = np.argmin(np.abs(diffs_from_phys_onset), axis=0)
    min_diff_col_idx = np.arange(len(min_diff_row_idx))
    min_diffs = diffs_from_phys_onset[min_diff_row_idx, min_diff_col_idx]
    min_diffs_tmp = min_diffs[abs(min_diffs) <= close_thresh]
    min_val = min(min_diffs_tmp)
    min_diffs += min_val
    offset += min_val
    LGR.info('Scan onsets should be adjusted forward by {} seconds to best '
             'match physio onsets.'.format(offset))

    # Get onset of each scan in terms of the physio time series
    scan_df['phys_onset'] = scan_df['onset'] + offset
    rise = (phys_df.loc[1, 'index'] - phys_df.loc[0, 'index'])
    run = (phys_df.loc[1, 'onset'] - phys_df.loc[0, 'onset'])
    samplerate = rise / run
    scan_df['index_onset'] = (scan_df['phys_onset'] * samplerate).astype(int)
    scan_df['index_duration'] = (scan_df['duration'] * samplerate).astype(int)
    scan_df['index_offset'] = scan_df['index_onset'] + scan_df['index_duration']
    return scan_df


def plot_sync(scan_df, physio_df):
    """
    Plot unsynchronized and synchonized scan and physio onsets and durations.
    """
    fig, axes = plt.subplots(nrows=2, figsize=(20, 6), sharex=True)

    # get max value rounded to nearest 1000
    max_ = int(1000 * np.ceil(max((
        physio_df['onset'].max(),
        scan_df['onset'].max(),
        scan_df['phys_onset'].max())) / 1000))
    scalar = 10
    x = np.linspace(0, max_, (max_*scalar)+1)

    # first the raw version
    physio_timeseries = np.zeros(x.shape)
    func_timeseries = np.zeros(x.shape)
    for i, row in scan_df.iterrows():
        func_timeseries[
            int(row['onset'] * scalar):int((row['onset'] + row['duration']) * scalar)
        ] = 1

    for i, row in physio_df.iterrows():
        physio_timeseries[
            int(row['onset'] * scalar):int((row['onset'] + row['duration']) * scalar)
        ] = 0.5

    axes[0].fill_between(x, func_timeseries, where=func_timeseries >= 0,
                         interpolate=True, color='red', alpha=0.3,
                         label='Functional scans')
    axes[0].fill_between(x, physio_timeseries, where=physio_timeseries >= 0,
                         interpolate=True, color='blue', alpha=0.3,
                         label='Physio triggers')

    # now the adjusted version
    physio_timeseries = np.zeros(x.shape)
    func_timeseries = np.zeros(x.shape)
    for i, row in scan_df.iterrows():
        func_timeseries[
            int(row['phys_onset'] * scalar):int((row['phys_onset'] + row['duration']) * scalar)
        ] = 1

    for i, row in physio_df.iterrows():
        physio_timeseries[
            int(row['onset'] * scalar):int((row['onset'] + row['duration']) * scalar)
        ] = 0.5

    axes[1].fill_between(x, func_timeseries, where=func_timeseries >= 0,
                         interpolate=True, color='red', alpha=0.3,
                         label='Functional scans')
    axes[1].fill_between(x, physio_timeseries, where=physio_timeseries >= 0,
                         interpolate=True, color='blue', alpha=0.3,
                         label='Physio triggers')

    axes[0].set_xlim((min(x), max(x)))
    axes[0].set_ylim((0, None))
    axes[1].set_xlabel('Time (s)')
    axes[0].legend()
    return fig, axes


def workflow(physio, bids_dir, sub, ses=None):
    """
    A potential workflow for running physio/scan onset synchronization and
    BIDSification. This workflow writes out physio files to a BIDS dataset.

    Parameters
    ----------
    physio : BlueprintInput
        Object *must* contain multiple physio trigger periods associated with scans.
    bids_dir : str
        Path to BIDS dataset
    sub : str
        Subject ID. Used to search the BIDS dataset for relevant scans.
    ses : str or None, optional
        Session ID. Used to search the BIDS dataset for relevant scans in
        longitudinal studies. Default is None.

    Returns
    -------
    out : list of BlueprintOutput
    """
    layout = BIDSLayout(bids_dir)
    scan_df = load_scan_data(layout, sub=sub, ses=ses)

    trigger_timeseries = physio.timeseries[physio.trigger_idx + 1]
    freq = physio.freq[physio.trigger_idx + 1]
    physio_df = extract_physio_onsets(trigger_timeseries, freq=freq)
    scan_df = synchronize_onsets(physio_df, scan_df)

    # we should do something better with this figure, but it's nice to have for QC
    fig, axes = plot_sync(scan_df, physio_df)
    fig.savefig('synchronization_results.png')

    run_dict = {}
    # could probably be replaced with apply() followed by to_dict()
    for _, row in scan_df.iterrows():
        base_fname = update_name(row['filename'], suffix='physio', extension='')
        split_times = (row['index_onset'], row['index_offset'])
        run_dict[base_fname] = split_times
    phys_dict = slice_phys(physio, run_dict, time_before=6)
    outputs = []
    for k, v in phys_dict.items():
        output = BlueprintOutput.init_from_blueprint(v)
        output.filename = k
        outputs.append(output)
        # Let's not actually save files until we're more confident.
        # output.save()
    return outputs

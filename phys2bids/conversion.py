"""
1. Extract segments from physio file.
    - Each segment must be named according to the onset time.
2. Extract trigger periods from physio segments.
    - Onset
    - Duration (low priority)
3. Scrape dicom directory
    - Name
    - Onset
    - Duration
4. Calculate time between onsets of each pair of trigger periods.
5. Calculate time between onsets of each pair of scans.
6. Compare these time differences to maximize similarity between structures.
7. Assign scan names to trigger period, and infer times for other scan times
   in cases where trigger failed.
"""

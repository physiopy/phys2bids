# Segment recordings by runs

#36

## 1. Parser
Create argument parser for new command ; based on `run.py`

  in : `cli/split.py`
  arg : `-ntp` and `-tr`

### 1.1. Copy elements from main parser
`run.py` to `split.py`
Integrate arguments : -in, -info, -indir, -outdir, -thr, -v
***Do we need anything else ?***

### 1.2. Adapt
We have to adapt types for : `-ntp`  (int --> list) and `-tr` (float --> list)
NOTES: if the TR parameter of a sequence is the same in different runs, just pad it with the same value

```
if list_tr.size[0] = 1:
  list_tr = list_tr * np.ones(list_ntp.size)
```

## 2. split2phys function
Create new file for the splitting utility and integrate `physio_obj` functions

  in : `/phys2bids/split2phys.py`

### 2.1. Verify num_timepoints_found and sum(ntp_list) are equivalent
Pad tr list so that it's equivalent to the number of runs contained in ntp_list

**To consider eventually**: maybe, the user doesn't know how many runs are contained in the file but knows (1) the usual length of a single run, (2) the sessions has only 1 sequence type, i.e. the same TR. So both `list_ntp.size[0]`and `list_tr.size[0]` could be `1` eventhough the file has multiple runs.

  from : `/phys_obj.py`, `BlueprintInput()`
  fn : `num_timepoints_found` and `check_trigger_amount`

```
BlueprintInput.check_trigger_amount(sum(list_ntp), tr=1)
```
### 2.2. Find start-end indexes for each run in list
Initialize dictionaries from which to define start and end indexes of timeseries. Call phys2bids

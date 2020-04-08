# Segment recordings by runs

#36
Ideas for name : split4phys, split4runs, obj2split,  split4bids, rec2run, phys2runs, ses2run, 4run2split

**Ways to integrate PR**
1. Another Repo : create a physiopy repo that is dedicated to splitting physiological recordings concurrent to neuroimaging ; least interesting option, aim is too specific.
2. Integrate phys2bids in [name of fn]: workflow on its own that calls phys2bids at the end of script for each segments
3. Independant utility : function gets called by phys2bids if list are detected as phys2bids arguments, no parser.
4. Integrate [name of fn] in phys2bids: keep the parser, have parallel workflows for different outcomes - less easy to integrate but more convenient for users

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
Initialize dictionaries from which to define start and end indexes of timeseries.

```
init dictionary for BlueprintInputs (dict)

  for i, elem in list_ntp:
    BlueprintInput.check_trigger_amount(ntp=elem, tr=list_tr[i])
    start_index = 0
    end_index = {index of spike 0} + {index of elem*list_tr[i]}
    dict[‘0’] = BlueprintInput.timeseries[0:end_index+padding, :]
    if i == len(list_ntp):
        end_index+padding <= number of indexes
        if it’s not:       padding= number of indexes-end_index
     BlueprintInput = BlueprintInput.timeseries[end_index+padding; , :]

make dict exportable
```
## 3. Call phys2bids
Call phys2bids for each of them

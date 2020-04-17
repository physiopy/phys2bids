# Segment recordings by runs

#36
Ideas for name : split4phys, split4runs, obj2split,  split4bids, rec2run, phys2runs, ses2run, 4run2split

# The option we settled for :
Integrate the splitting function with phys2bids.

# What we need to do
## 1.Adapt phys2bids parser arguments, in `run.py`
-[] ntp type, from int to list
-[] tr type, from float to list
-[] (uncertain) either add argument to specify the file is multi-run, or detect if list contains multiple item.

```
if multiple item (in ntp or in tr):
  -run is True.

If run is True:
  redirect to part of code that splits the file
```

## 2.Ascertain lists length before running main workflow, after loading file (in `phys2bids.py, line 241`)
-[ ] Raise appropriate errors (e.g. ntp list has 1 item but `-run` is True, ntp has more than 1 item and tr has more) - in `split2phys.py line 75 to 90`
-[ ] add padding to non-equivalent list (in `split2phys.py line 92`)
## 3.Check that sum(ntp_list) gives the right amount of trigger tps
-[ ] adapt check_trigger_amount section in `phys2bids.py, line 265`, with `split2phys.py, line 118`
-[ ] find the right value to give to `tr` parameter when running `phys_in.check_trigger_amount()` (no hard-coded value)
## 4.***Code the thing*** (that I really need help with)
-[ ] Figure out where to insert the loop (developped in `split2phys.py line 130`). Probably somewhere around line 294
-[ ] Insert If... else statement to redirect.
-[ ] Adapt `phys_out` to deal with multi-run, and eventually, multi-freq files.

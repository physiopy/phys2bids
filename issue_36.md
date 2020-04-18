# Segment recordings by runs

#36
Ideas for name : split4phys, split4runs, obj2split,  split4bids, rec2run, phys2runs, ses2run, 4run2split

# The option we settled for :
Integrate the splitting function with phys2bids.

# What we need to do
## 1.Adapt phys2bids parser arguments, in `run.py`
-   [x] tr type, from float to list
-   [x] ntp type, from int to list
-   [ ] add a check for those lists in a different issue
-   [ ] (uncertain) either add argument to specify the file is multi-run, or detect if list contains multiple item.
## 2.In phys2bids, ascertain lists length
-   [x] Raise appropriate errors (e.g. ntp list has 1 item but `-run` is True, ntp has more than 1 item and tr has more)
-   [x] add padding of ones to tr when non-equivalent list
-   [x] Insert If... else statements to redirect.
-   [x] check that sum(ntp_list) gives the right amount of trigger tps
-   [x] Figure out where to call split2phys
## 3.In split2phys,
-   [x] adapt check_trigger_amount section
-   [ ] Create dictionary with start, end index
-   [ ] Adapt `phys_out` to deal with multi-run,
-   [ ] and eventually, multi-freq files (in a different issue).

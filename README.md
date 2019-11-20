[![DOI](https://zenodo.org/badge/208861898.svg)](https://zenodo.org/badge/latestdoi/208861898)


phys2bids
=========
Phys2bids is a python3 library meant to format physiological files in BIDS.
It was born for Acqknowledge files (BIOPAC), and at the moment it supports
``.acq`` files as well as ``.txt`` files obtained by labchart
(ADInstruments).
It doesn't support physiological files recorded with the MRI, as you can find a software for it [here](https://github.com/tarrlab/physio2bids).

It requires python 3.6 or above, as well as the modules:
- `numpy >= 1.9.3`
- `pandas >= 0.10`
- `matplotlib >= 3.1.1`

In order to process ``.acq`` files, it needs [`bioread`](https://github.com/uwmadison-chm/bioread), an excellent module
that can be found at [this link](https://github.com/uwmadison-chm/bioread).
Linux and mac installation:
Donwload the package as zip from github and uncompress or if you have ``git`` use the command:
`` git clone https://github.com/smoia/phys2bids.git``
open a terminal in the phy2bids folder and execute the command:
``sudo python3 setup.py install``
type the command:
``phys2bids``
if your output is:
``usage: phys2bids [-h] -in FILENAME [-info] [-indir INDIR] [-outdir OUTDIR]
                 [-heur HEUR_FILE] [-sub SUB] [-ses SES] [-chtrig CHTRIG]
                 [-chsel [CHSEL [CHSEL ...]]] [-ntp NUM_TPS_EXPECTED] [-tr TR]
                 [-thr THR] [-tbhd [TABLE_HEADER [TABLE_HEADER ...]]] [-v]
phys2bids: error: the following arguments are required: -in/--input-file``
it should mean that phys2bids is ready to be use

**The project is currently under development**.
Any suggestion/bug report is welcome! Feel free to open an issue.

At the very moment, it assumes all the extracted channels from a file
have the same sampling freq.

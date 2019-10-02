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

In order to process ``.acq`` files, it needs `bioread`, an excellent module
that can be found at [`this link`](https://github.com/uwmadison-chm/bioread).

The project is currently under development.
Any suggestion/bug report is welcome! Feel free to open an issue.

At the very moment, it assumes all the extracted channels from a file
have the same sampling freq.

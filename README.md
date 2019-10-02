[![DOI](https://zenodo.org/badge/208861898.svg)](https://zenodo.org/badge/latestdoi/208861898)


phys2bids
=========
Phys2bids is a python3 library meant to set physiological files in BIDS
standard.
It was born for Acqknowledge files (BIOPAC), and at the moment it supports
``.acq`` files and ``.txt`` files obtained by labchart
(ADInstruments) and Respiract.

It requires python 3.6 or above, as well as the modules:
- `numpy`
- `pandas`
- `matplotlib >= 3.1.1`

In order to process ``.acq`` files, it needs `bioread`, an excellent module
that can be found at `this link`_

The project is under development.

At the very moment, it assumes all the extracted channels from a file
have the same sampling freq.

.. _this link:
   https://github.com/uwmadison-chm/bioread

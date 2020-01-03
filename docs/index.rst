=========
phys2bids
=========

<img alt="Phys2BIDS" src="https://github.com/physiopy/phys2bids/blob/master/docs/phys2bids_logo1280×640.png" height="150">

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3586045.svg)](https://doi.org/10.5281/zenodo.3586045)
[![Join the chat at https://gitter.im/phys2bids/community](https://badges.gitter.im/phys2bids/community.svg)](https://gitter.im/phys2bids/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

Phys2bids is a python3 library meant to format physiological files in BIDS.
It was born for AcqKnowledge files (BIOPAC), and at the moment it supports
``.acq`` files as well as ``.txt`` files obtained by labchart
(ADInstruments).
It doesn't support physiological files recorded with the MRI, as you can find a software for it [here](https://github.com/tarrlab/physio2bids).

**The project is currently under development**.
Any suggestion/bug report is welcome! Feel free to open an issue.

Contents
--------

.. toctree::
   :maxdepth: 1

   installation
   howto
   heuristic
   bestpractice
   cli
   contributing
   license
   api
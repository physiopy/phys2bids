=========
phys2bids
=========

.. image:: _static/phys2bids_logo1280×640.png
   :alt: phys2bids logo
   :align: center

.. image:: https://zenodo.org/badge/DOI/10.5281/zenodo.3586045.svg
   :target: https://doi.org/10.5281/zenodo.3586045

.. image:: https://badges.gitter.im/phys2bids/community.svg
   :target: https://badges.gitter.im/phys2bids/community.svg)](https://gitter.im/phys2bids/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge

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
   contributorfile
   conduct
   license
   api
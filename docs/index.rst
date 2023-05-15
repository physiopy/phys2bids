=========
phys2bids
=========

.. image:: _static/phys2bids_logo1280×640.png
    :alt: phys2bids logo
    :align: center

.. image:: https://img.shields.io/pypi/v/phys2bids
    :alt: Latest version
    :target: https://pypi.org/project/phys2bids/
.. image:: https://zenodo.org/badge/DOI/10.5281/zenodo.3470091.svg
    :alt: DOI
    :target: https://doi.org/10.5281/zenodo.3470091
.. image:: https://img.shields.io/github/license/physiopy/phys2bids
    :alt: Licensed Apache 2.0
    :target: https://github.com/physiopy/phys2bids/blob/master/LICENSE

.. image:: https://codecov.io/gh/physiopy/phys2bids/branch/master/graph/badge.svg
    :alt: codecov
    :target: https://codecov.io/gh/physiopy/phys2bids
.. image:: https://circleci.com/gh/physiopy/phys2bids.svg?branch=master&style=shield
    :alt: CircleCI
    :target: https://circleci.com/gh/physiopy/phys2bids
.. image:: https://dev.azure.com/physiopy/phys2bids/_apis/build/status/physiopy.phys2bids?branchName=master
    :alt: Build Status. Windows
    :target: https://dev.azure.com/physiopy/phys2bids/_build/latest?definitionId=1&branchName=master
.. image:: https://readthedocs.org/projects/phys2bids/badge/?version=latest
    :alt: See the documentation at: https://phys2bids.readthedocs.io
    :target: https://phys2bids.readthedocs.io/en/latest/?badge=latest

.. image:: https://badges.gitter.im/physiopy/phys2bids.svg
    :alt: Join the chat at Gitter: https://gitter.im/physiopy/phys2bids
    :target: https://gitter.im/physiopy/phys2bids?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=body_badge
.. image:: https://img.shields.io/badge/release-auto.svg?colorA=888888&colorB=9B065A&label=auto
    :alt: Auto Release
    :target: https://github.com/intuit/auto
.. image:: https://img.shields.io/pypi/pyversions/phys2bids
    :alt: Supports python version
    :target: https://pypi.org/project/phys2bids/
.. image:: https://requires.io/github/physiopy/phys2bids/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/physiopy/phys2bids/requirements/?branch=master



``phys2bids`` is a python3 library meant to format physiological files in BIDS.
At the moment, it supports:

   * .acq, .txt, and .mat AcqKnowledge format (BIOPAC)
   * .txt and .mat LabChart format (ADInstruments)
   * .smr Spike2 format (CED)
   * GE MRI file format (GE).

We want to offer as much support as possible! If you have a file format that you want to see added, open an issue about it!

While we aim at supporting all MRI proprietary physiological file formats, at the moment we only supports GE MRI scanners. You can find software that will work with files from other MRI scanner types `here <https://github.com/tarrlab/physio2bids>`_.

**We're looking for code contributors,** and any suggestion/bug report is welcome! Feel free to open issues!

This project follows the `all contributors <https://github.com/all-contributors/all-contributors>`_ specification. Contributions of any kind welcome!


Citing ``phys2bids``
--------------------

If you use ``phys2bids``, please cite it using the Zenodo DOI that you can find here:

    https://doi.org/10.5281/zenodo.3470091

We also support gathering all relevant citations via `DueCredit <http://duecredit.org>`_.


Contents
--------

.. toctree::
   :maxdepth: 1

   installation
   howto
   heuristic
   bestpractice
   bids
   cli
   contributing
   contributorfile
   conduct
   license
   api

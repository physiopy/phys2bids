.. _installation:

============
Installation
============

Requirements
------------

``phys2bids`` requires python 3.6 or above, as well as the modules:

- ``numpy >= 1.9.3``
- ``matplotlib >= 3.1.1``

Depending on the processed files, it might require the **manual installation** of extra modules.
At the moment, those modules are:

- |bioread|_, for AcqKnowledge (``.acq``) files.

.. _bioread: https://github.com/uwmadison-chm/bioread

.. |bioread| replace:: ``bioread``

Linux and mac installation
--------------------------

Install with ``pip``
^^^^^^^^^^^^^^^^^^^^

.. note::
	The following instructions are provided assuming that python 3 is **not** your default version of python.
	If it is, remember to use ``pip`` instead of ``pip3``.
	If you want to check, type ``python --version`` in a terminal.

Install main program
~~~~~~~~~~~~~~~~~~~~

Pypi has the latest stable release of ``phys2bids`` as a package. Just run::

	pip3 install phys2bids

If you want the latest development version of the program, download the package from `github <https://github.com/physiopy/phys2bids>`_ and uncompress it.
Alternatively, if you have ``git``, use the command::

    git clone https://github.com/physiopy/phys2bids.git

Open a terminal in the ``phy2bids`` folder and execute the command::

    pip3 install .

Install extra modules
~~~~~~~~~~~~~~~~~~~~~

If you are planning to use file formats other than plain ``txt``, you need to install extra modules to have the right interface.
Extra modules installation can be done with the sintax::

	pip3 install <package>[<extra>]

Where ``<package>>`` is either ``phys2bids`` or ``.``, depending on how you installed it, and ``<extra>`` is one of the following:

	- ``acq``: if you plan to use native AcqKnowledge files (``.acq`` extension)
	- ``interfaces``: for all the interfaces above.

For instance, if you plan to install phys2bids and use all the interfaces, run::

    pip3 install phys2bids[interfaces]

Install without ``pip``
^^^^^^^^^^^^^^^^^^^^^^^

Download the latest package release from `github <https://github.com/physiopy/phys2bids>`_ and uncompress it.
Alternatively, if you have ``git`` installed, use the command::

    git clone https://github.com/physiopy/phys2bids.git

Open a terminal in the ``phy2bids`` folder and execute the command::

    python3 setup.py

You might still need to install extra dependencies listed at the beginning of the page.

.. note::
	If python 3 is already your default, you might use ``python`` rather than ``python3``

Check your installation!
^^^^^^^^^^^^^^^^^^^^^^^^

Type the command::

    phys2bids -v

If your output is: ``phys2bids 1.3.0-beta`` or similar, ``phys2bids`` is ready to be used.

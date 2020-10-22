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
    If it is, you might need to use ``pip`` instead of ``pip3``, although some OSs do adopt ``pip3`` anyway.
    If you want to check, type ``python --version`` in a terminal.

Install ``phys2bids`` alone
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Pypi has the latest stable release of ``phys2bids`` as a package. Just run::

    pip3 install phys2bids

If you want the latest development version of the program, download the package from `github <https://github.com/physiopy/phys2bids>`_ and uncompress it.
Alternatively, if you have ``git``, use the command::

    git clone https://github.com/physiopy/phys2bids.git

Open a terminal in the ``phys2bids`` folder and execute the command::

    pip3 install .

Install extra modules
~~~~~~~~~~~~~~~~~~~~~

If you are planning to use file formats other than plain ``txt``, you need to install extra modules to have the right interface.
Extra modules installation can be done with the syntax::

    pip3 install <package>[<extra>]

Where ``<package>>`` is either ``phys2bids`` or ``.``, depending on whether you want to use ``pip`` or ``git`` for the installation, and ``<extra>`` is one of the following:

    - ``acq``: if you plan to use native AcqKnowledge files (``.acq`` extension)
    - ``interfaces``: for all the interfaces above.

For instance, if you plan to install ``phys2bids`` and use all the interfaces, run::

    pip3 install phys2bids[interfaces]

.. note::
    If you "missed" or skipped this trick when you installed ``phys2bids`` the first time, don't worry!
    You can do it any time - this will update ``phys2bids`` and install all the extra modules you want. 


Install without ``pip``
^^^^^^^^^^^^^^^^^^^^^^^

Download the latest package release from `github <https://github.com/physiopy/phys2bids>`_ and uncompress it.
Alternatively, if you have ``git`` installed, use the command::

    git clone https://github.com/physiopy/phys2bids.git

Open a terminal in the ``phys2bids`` folder and execute the command::

    python3 setup.py

You might still need to install extra dependencies listed at the beginning of the page.

.. note::
    If python 3 is already your default, you might use ``python`` rather than ``python3``

Check your installation!
^^^^^^^^^^^^^^^^^^^^^^^^

Type the command::

    phys2bids -v

If your output is: ``phys2bids 1.3.0-beta`` or similar, ``phys2bids`` is ready to be used.

Windows installation
--------------------------

First of all let's check you have python installed. Open a windows power shell window in ADMIN MODE and type::

    python --version

In case you don't have it, either install it from this link https://www.microsoft.com/en-us/p/python-38/9mssztt1n39l?activetab=pivot:overviewtab or type the command::

    python

It will redirect you to the windows store python install (in the creation of this tutorial the newest version of python was 3.8).

Once python is installed, you can either install phys2bids directly with pip::

    pip install phys2bids

If you want the latest development version of the program, download the package from `github <https://github.com/physiopy/phys2bids>`_ and uncompress it.
Alternatively, if you have ``git``, use the command::

    git clone https://github.com/physiopy/phys2bids.git

Open a terminal in the ``phys2bids`` folder in ADMIN MODE and execute the command::

    pip install .
    # or if you want all the extra dependencies installed:
    pip install .[all]

Check your installation!
^^^^^^^^^^^^^^^^^^^^^^^^

Type the command::

    phys2bids -v

.. _installation:

============
Installation
============

Requirements
------------

``phys2bids`` requires python 3.6 or above, as well as the modules:

.. literalinclude:: ../setup.cfg
   :lines: 28-30
   :dedent: 4

If you are planning to use file formats other than plain ``txt``, you will need to install additional **extra modules** to have the right interface.
At the moment, those modules are:

- |bioread|_, for AcqKnowledge (``.acq``) files.

.. _bioread: https://github.com/uwmadison-chm/bioread

.. |bioread| replace:: ``bioread``

Linux and mac installation
--------------------------
The most convenient option is to use ``pip``, as it allows you to automatically download and install the package from PyPI repository and facilitates upgrading or uninstalling it. Since we use ``auto`` to publish the latest features as soon as they are ready, PyPI will always have the latest stable release of ``phys2bids`` as a package.

Alternatively, you can get the package directly from GitHub but all download, installation and package handling steps will need to be done manually.

Install with ``pip``
^^^^^^^^^^^^^^^^^^^^

.. note::
    The following instructions are provided assuming that python 3 is **not** your default version of python.
    If it is, you might need to use ``pip`` instead of ``pip3``, although some OSs do adopt ``pip3`` anyway.
    If you want to check, type ``python --version`` in a terminal.

If you don't need any of the extra modules listed at the beginning of this page go to **Install phys2bids alone**. Otherwise, follow the instructions under **Install phys2bids with extra modules**.

Install ``phys2bids`` alone
~~~~~~~~~~~~~~~~~~~~~~~~~~~

To install ``phys2bids`` along with the basic required modules just run::

    pip3 install phys2bids
    
You can now proceed to check your installation and start using ``phys2bids``!

Install ``phys2bids`` with extra modules
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The installation of ``phys2bids`` along with extra modules can be done with the syntax::

    pip3 install phys2bids[<extra>]

Where ``<extra>`` is one of the following:

    - ``acq``: if you plan to use native AcqKnowledge files (``.acq`` extension)
    - ``interfaces``: for all the interfaces above.

For instance, if you plan to install ``phys2bids`` and use all of the interfaces, run::

    pip3 install phys2bids[interfaces]

You can now proceed to check your installation and start using ``phys2bids``!

.. note::
    If you "missed" or skipped this trick when you installed ``phys2bids`` the first time, don't worry!
    You can do it any time - this will update ``phys2bids`` and install all extra modules you want. 


Install without ``pip``
^^^^^^^^^^^^^^^^^^^^^^^

Download the latest package release from `github <https://github.com/physiopy/phys2bids>`_ and uncompress it.
Alternatively, if you have ``git`` installed, use the command::

    git clone https://github.com/physiopy/phys2bids.git

Open a terminal in the ``phys2bids`` folder and execute the command::

    python3 setup.py install

This should have installed ``phys2bids`` along with the basic required modules. If you need any of the extra modules listed at the beginning of the page you might need to install them manually. Otherwise, you can proceed to check your installation and start using ``phys2bids``. 

.. note::
    If python 3 is already your default, you might use ``python`` rather than ``python3``

Check your installation!
^^^^^^^^^^^^^^^^^^^^^^^^

Type the command::

    phys2bids -v

If your output is: ``phys2bids 2.2.2`` or similar, ``phys2bids`` is ready to be used.

Windows installation
--------------------

First of all let's check you have python installed. Open a windows power shell window in **admin mode** and type::

    python --version

In case you don't have it, either install it from `here <https://www.microsoft.com/en-us/p/python-38/9mssztt1n39l?activetab=pivot:overviewtab>`_ or type the command::

    python

It will redirect you to the windows store python install (in the creation of this tutorial the newest version of python was 3.8).

.. warning::
    ``phys2bids`` supports Python 3.6 and later versions. We can't guarantee it will work if you use python 2.

Once python is installed, you can follow the instructions to install ``phys2bids`` reported `above <#install-with-pip>`_

.. note::
    Remember to open a terminal in **admin mode** to install libraries!

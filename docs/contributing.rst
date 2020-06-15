.. _contributing:

=============================
Contributing to ``physiopy``
=============================

First of all: thank you!

Contributions can be made in different ways, not only code!
As we follow the `all-contributors`_ specification, any contribution will be recognised accordingly.

Follow these steps to get started:

1. Have a look at the `contributor guide <contributorfile.html>`_ page as well as the `code of conduct <conduct.html>`_.
2. Make sure that you have a GitHub account. You can set up a `free GitHub account <https://github.com/>`_; here are some `instructions <https://help.github.com/articles/signing-up-for-a-new-github-account>`_.
3. If you intend to contribute code and/or use the ``physiopy`` packages in any way, check that you have ``git`` and ``pip`` installed on your system. Then install ``phys2bids`` as a developer. This will let you run the program with the latest modification, without requiring to re-install it every time.

.. _`all-contributors`: https://github.com/all-contributors/all-contributors

.. note::
    The following instructions are provided assuming that python 3 is **not** your default version of python.
    If it is, you might need to use ``pip`` instead of ``pip3``, although some OSs do adopt ``pip3`` anyway.
    If you want to check, type ``python --version`` in a terminal.

Linux and mac developer installation
------------------------------------

Be sure to have ``git`` and ``pip`` installed, then open a terminal and run::

	git clone https://github.com/physiopy/phys2bids.git

Basic installation
^^^^^^^^^^^^^^^^^^

If you use python frequently, or you are a python developer, chances are that all the necessary dependencies
are already installed in your system.

Move into the ``phys2bids`` folder and execute the command::

	pip3 install -e .

Full developer installation
^^^^^^^^^^^^^^^^^^^^^^^^^^^

If it's your first experience as a python developer, or you just want to be sure that you have everything you need
to collaborate with us, you can install ``phys2bids`` with all the other packages that we frequently use during development in one step!

Move into the ``phys2bids`` folder and execute the command::

	pip3 install -e .[all]

This will install:

	- ``phys2bids`` as an editable package, which means that you can modify the program and run it without having to reinstall it every time!
	- All the ``phys2bids`` dependencies.
	- All the **interface** modules, that deal with the interfaces for all the file formats.
	- All the **style** modules, such as ``flake8``, to help you linter the code!
	- All the **documentation** modules, like ``sphinx``, so that you can build the docs locally before submitting them.
	- All the **test** modules, like ``pytest``, in order for you to test your code locally before committing it!

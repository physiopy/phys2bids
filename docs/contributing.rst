.. _contributing:

=============================
Contributing to ``physiopy``
=============================

First of all: thank you!

Contributions can be made in different ways, not only code!
As we follow the `all-contributors`_ specification, any contribution will be recognised accordingly.

The first thing you might want to do, is having a look at the `contributor guide <contributorfile.html>`_ page as well as the `code of conduct <conduct.html>`_.

The second thing is to be sure you have ``git`` and ``pip`` installed in your system.

The third thing is to install ``phys2bids`` as a developer.
This will let you run the program with the latest modification, without requiring to re-install it every time.

.. _`all-contributors`: https://github.com/all-contributors/all-contributors


Linux and mac developer installation
------------------------------------

Be sure to have git installed, then open a terminal and run::

	``git clone https://github.com/physiopy/phys2bids.git``

Basic installation
^^^^^^^^^^^^^^^^^^

If you use python frequently, or you are a python developer, chances are that all the necessary dependencies
are already installed in your system.

Move in the ``phy2bids`` folder and execute the command::

	``pip3 install -e .``

If python 3 is already your default, you might use instead::

	``pip install -e .``

Full developer installation
^^^^^^^^^^^^^^^^^^^^^^^^^^^

If it's your first experience as a python developer, or you just want to be sure that you have everything you need
to collaborate with us, you can install ``phy2bids`` and all the other packages that we frequently use during development
in one step.

Move in the ``phy2bids`` folder and execute the command::

	``pip3 install -e .[all]``

This will install:

	- ``phys2bids`` as an editable package, which means that you can modify the program and run it without having to reinstall it every time!
	- All the ``phys2bids`` dependencies.
	- All the **interface** modules, that deal with the interfaces for all the file formats.
	- All the **style** modules, such as ``flake8``, to help you linter the code!
	- All the **documentation** modules, like ``sphinx``, so that you can build the docs locally before submitting them.
	- All the **test** modules, like ``pytest``, in order for you to test your code locally before committing it!
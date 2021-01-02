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
3. If you intend to contribute code and/or use the ``physiopy`` packages in any way, check that you have ``git`` and ``pip`` installed on your system. Then install ``phys2bids`` as a developer. This will let you run the program with the latest modifications, without requiring to re-install it every time.

.. _`all-contributors`: https://github.com/all-contributors/all-contributors

.. note::
    The following instructions are provided assuming that python 3 is **not** your default version of python.
    If it is, you might need to use ``pip`` instead of ``pip3``, although some OSs do adopt ``pip3`` anyway.
    If you want to check, type ``python --version`` in a terminal.


Linux, Mac, and Windows developer installation
----------------------------------------------

Be sure to have ``git`` and ``pip`` installed. Fork the phys2bids repository in GitHub, then open a terminal and run the following code to clone the forked repository and set it as your `origin`::

    git clone https://github.com/{username}/phys2bids.git
    # or in case you prefer to use ssh:
    git clone git@github.com:{username}/phys2bids.git

We also recommend to set up the physiopy/phys2bids repository as `upstream`.
In this way you can always keep your main branch up to date with the command `git pull upstream master`::

    cd phys2bids
    git remote add upstream https://github.com/physiopy/phys2bids.git
    git pull upstream master 


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
    - All ``phys2bids`` dependencies.
    - All **interface** modules, that deal with the interfaces for all the file formats.
    - All **style** modules, such as ``flake8``, to help you linter the code!
    - All **documentation** modules, like ``sphinx``, so that you can build the docs locally before submitting them.
    - All **test** modules, like ``pytest``, in order for you to test your code locally before committing it!

Check your installation!
^^^^^^^^^^^^^^^^^^^^^^^^

Type the commands::

    cd phys2bids/tests
    pytest

This will execute the tests locally and check that your phys2bids installation works properly.

.. code-block:: shell

    pytest
    =================================== test session starts ===================================
    platform win32 -- Python 3.8.6, pytest-6.1.1, py-1.9.0, pluggy-0.13.1
    rootdir: C:\Users\sento\phys2bids, configfile: setup.cfg
    plugins: cov-2.10.1
    collected 61 items

    test_acq.py .                                                                        [  1%]
    test_bids.py ................                                                        [ 27%]
    test_integration.py ...                                                              [ 32%]
    test_phys2bids.py ...                                                                [ 37%]
    test_physio_obj.py .......                                                           [ 49%]
    test_txt.py ..................                                                       [ 78%]
    test_utils.py ...........                                                            [ 96%]
    test_viz.py .x                                                                       [100%]

    ================================= short test summary info =================================
    XFAIL test_viz.py::test_plot_trigger
    ======================== 60 passed, 1 xfailed in 142.58s (0:02:22) ========================

Do **not** worry if there is a xfail error in the log. This happens when we know that a test will fail for known reasons, and we are probably working to fix it (see `here <https://docs.pytest.org/en/latest/skipping.html#xfail-mark-test-functions-as-expected-to-fail>`_. However, if you do encounter any other error, check that you have all the extra dependencies installed and their version meets ``phys2bids`` requirements. Contact us on `gitter <https://gitter.im/physiopy/community>`_ if you need help!

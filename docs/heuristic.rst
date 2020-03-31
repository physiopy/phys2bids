.. _heuristic:

==============================
How to set up a heuristic file
==============================

This tutorial prepares an heuristic file to process general ``phys2bids`` inputs.

Anatomy of a heuristic file
---------------------------

Let's have a look under the hood of the heuristic files used in the `tutorial <howto.html>`_.
It's the file ``heur_tutorial.py`` in ``phys2bids/phy2bids/heuristics/``:

.. literalinclude:: ../phys2bids/heuristics/heur_tutorial.py
   :linenos:

We can split this file into three parts: the initialisation, the dictionaries, and the functional code.

Initialisation
^^^^^^^^^^^^^^

.. literalinclude:: ../phys2bids/heuristics/heur_tutorial.py
   :linenos:
   :lines: 1-4

It's important **not to modify this part of the file**. Instead, you can copy and paste it into your own heuristic file.

This file looks like a python function, initialised by two mandatory parameters:
-``physinfo`` is the information used to label your file. **At the moment, it corresponds to the name of the input file itself**. This is what you need to build your heuristic.
-``name`` is an argument passed by the main script that contains part of the name of the file. Don't worry about this.

The file also has another bunch of optional arguments that are empty by default. These are the labels you can add to your dictionaries, in order to construct the BIDsified name of your files.

The scripts imports ``fnmatch``, a nice python module that lets you use bash-like wildcards.

Dictionaries
^^^^^^^^^^^^

.. literalinclude:: ../phys2bids/heuristics/heur_tutorial.py
   :linenos:
   :lines: 5-29
   :lineno-start: 5
   :dedent: 4

This is the core of the function, and the part that should be adapted to process your files. In practice, it's the beginning of a |statement|_.
| You need an ``if`` or ``elif`` statement for each file that you want to process, that will test if the ``physinfo`` is similar to a string (first case) or exactly matches a string (second case). The content of the statement is a set of `variable initialisations as a string <https://www.w3schools.com/python/python_strings.asp>`_.
| The list of possible variables is in the comment above, and corresponds to the list of possible entities of the `BIDs specification <https://bids-specification.readthedocs.io/en/stable/04-modality-specific-files/06-physiological-and-other-continuous-recordings.html>`_:

- ``task`` stands for the name of the task. **It's the only required entity**, and it should match the task of the neuroimaging file associated to the physiological data.
- ``run`` is the optional entity for the `index of the scan in a group of same modalities <https://bids-specification.readthedocs.io/en/stable/04-modality-specific-files/01-magnetic-resonance-imaging-data.html#the-run-entity>`_ (e.g. 2 resting states).
- ``rec`` is the optional entity for the `reconstruction algorithm <https://bids-specification.readthedocs.io/en/stable/04-modality-specific-files/01-magnetic-resonance-imaging-data.html#the-rec-entity>`_.
- ``acq`` is the optional entity for the `set of acquisition parameters <https://bids-specification.readthedocs.io/en/stable/04-modality-specific-files/01-magnetic-resonance-imaging-data.html#the-acq-entity>`_.
- ``direct`` is the equivalent of the ``dic`` entity, an optional entity for the phase encoding direction (see `here <https://bids-specification.readthedocs.io/en/stable/04-modality-specific-files/01-magnetic-resonance-imaging-data.html#task-including-resting-state-imaging-data>`_).

Note that one mandatory BIDs entity is missing: the **``sub`` entity**, correspondent to the subject label. This is because it has to be specified while calling ``phys2bids``, as it's explained in the tutorial section `"generating-outputs-in-bids-format" <howto.html#generating-outputs-in-bids-format>`_. The **session entity** can be specified in the same way. Moreover, if you have a **multifrequency file** there will be another entity, ``recording`` automatically added to those specified here, and containing the sample frequency of the different outputs.

Let's try to read the first statement in the example:

	*"If the name of the file (``physinfo``) contains the string ``'*tutorial*'``, then assign the entity ``task`` with value ``test``, the ``run`` as number ``00``, and the reconstruction used as ``labchart``"*

Note that we used only a subset of possible entities.

.. _statement: https://www.w3resource.com/python/python-if-else-statements.php

.. |statement| replace:: ``if .. elif .. else`` statement.

Functional code
^^^^^^^^^^^^^^^

.. literalinclude:: ../phys2bids/heuristics/heur_tutorial.py
   :linenos:
   :lines: 27-
   :lineno-start: 27
   :dedent: 4

This part contains some code that composes the heuristic function output.
It's important **not to modify this part of the file**. Instead, you can copy and paste it into your own heuristic file.
There's a warning that will raise if the file wasn't able to process the input file, and an error that will raise if the mandatory ``task`` entity is still empty after the dictionary attribution.

Using the heuristic file
------------------------

Once you modified your heuristic file or created a new one, you can save it anywhere you want, as a python script (``somename.py``). Check that the file is **executable**! Then, you will have to call ``phys2bids`` using the ``-heur``, the ``-sub``, and optionally the ``-ses``, arguments:

.. code-block:: shell

    phys2bids -in tutorial_file.txt -indir /home/arthurdent/git/phys2bids/phys2bids/tests/data/ -chtrig 1 -ntp 158 -tr 1.2 -outdir /home/arthurdent/physio -heur /home/arthurdent/git/phys2bids/phys2bids/heuristics/heur_tutorial.py -sub 006 -ses 01

Remember to **specify the full path** to the heuristic file. A copy of the heuristic file will be saved in the site folder.

You can find more information in the `relevant tutorial section <howto.html#generating-outputs-in-bids-format>`_.

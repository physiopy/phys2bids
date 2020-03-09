.. _howto:

========================
How to use ``phys2bids``
========================

This tutorial uses a text file exported from LabChart software. The principles of this tutorial apply for other inputs that ``phys2bids`` currently supports (AcqKnowledge native files and text files). However, future tutorials will go into the specifics of processing different inputs, as well as inputs which contain different sampling frequencies across data columns and inputs with multiple scans within one file.

This tutorial will:

1. Run ``phys2bids`` with the ``-info`` option, to show how to retrieve information about your input file.
2. Run ``phys2bids`` and explain the output files (png, json, tsv) that are generated.
3. Run ``phys2bids`` with a heuristic file, showing how the input file can be outputted in BIDS format.

Setup
#####

In order to follow the tutorial, you need a very quick setup: download or clone the `github repository <https://github.com/physiopy/phys2bids>`_ and install either the latest stable or development release as described `here <installation.html#install-with-pip>`_.

**Note**: for the tutorial, we will assume the repository was downloaded in ``/home/arthurdent/git``. Let's get there right now:

.. code-block:: shell

    cd /home/arthurdent/git/

What is in the tutorial text file?
##################################

The file can be found in ``phys2bids/phys2bids/tests/data/tutorial_file.txt``. This file has header information (first 9 lines) which phys2bids will use to process this file, alongside information directly inputted by the user. Following this header information, the data in the file is stored in a column format. In this example, we have time (column 1), MRI trigger pulse (column 2), CO2 (column 3), O2 (column 4) and pulse (column 5). Each column was sampled at 1000Hz (Interval = 0.001 s).

.. literalinclude:: ../phys2bids/tests/data/tutorial_file.txt
   :linenos:
   :lines: 1-15

**Note**: time is not a "real" channel recorded by LabChart or AcqKnowledge. For this reason, ``phys2bids`` treats it as a hidden channel, always in position 0. Channel 1 will be the first channel recorded in either software.

Using the -info option
######################

First, we can see what information ``phys2bids`` reads from the file, and make sure this is correct before processing the file.

The simplest way of calling ``phys2bids`` is moving to the folder containing the physiological file and typing:

.. code-block:: shell

    cd phys2bids/phys2bids/tests/data/
    phys2bids -in tutorial_file

``phys2bids`` will try to get the extension for you. 
However, we’ll use one more argument to have a sneak peak into the content of the file:

.. code-block:: shell

    phys2bids -in tutorial_file.txt -info

This ``-info`` argument means ``phy2bids`` does not process the file, but only outputs information it reads from the file, by printing to the terminal and outputting a png plot of the data in the current directory:

.. code-block:: shell

    INFO:phys2bids.phys2bids:Currently running phys2bids version v1.3.0-beta+149.ge4a3c87
    INFO:phys2bids.phys2bids:Input file is tutorial_file.txt
    INFO:phys2bids.utils:File extension is .txt
    WARNING:phys2bids.utils:If both acq and txt files exist in the path, acq will be selected.
    INFO:phys2bids.phys2bids:Reading the file ./tutorial_file.txt
    INFO:phys2bids.interfaces.txt:phys2bids detected that your file is in Labchart format
    INFO:phys2bids.phys2bids:Reading infos
    INFO:phys2bids.physio_obj:
    ------------------------------------------------
    File tutorial_file.txt contains:
    01. Trigger; sampled at 1000.0 Hz
    02. CO2; sampled at 1000.0 Hz
    03. O2; sampled at 1000.0 Hz
    04. Pulse; sampled at 1000.0 Hz
    ------------------------------------------------

    INFO:phys2bids.viz:saving channel plot to tutorial_file.png

.. image:: _static/tutorial_file.png
   :alt: tutorial_file_channels
   :align: center
    
Great! Now we know that the our file contains four channels, sampled at the same frequency, and that the trigger is in the first column. All this information will become useful.

Generating outputs
##################

Specifying paths and names
^^^^^^^^^^^^^^^^^^^^^^^^^^

Now we'll call ``phys2bids`` without the ``-info`` option. We'll use the same inputs as above, as well as adding ``-indir``, ``-outdir``, and ``-chplot``. If you use ``-indir`` you can specify a path to your input file i.e. it does not have to be in the current directory, as is the default. Using the ``-chplot`` argument allows you to specify the name (and full path) for the png channel plot. The ``-indir`` and ``-chplot`` arguments can be used alongside the ``-info`` argument. When calling ``phys2bids`` without the ``-info`` argument, it will generate files; if you use the ``-outdir`` argument this is where ``phys2bids`` will save these files - if the folder doesn't exist, it will be created.

Unless specified with ``-chsel``, ``phys2bids`` will process and output all channels. Unless specified with ``-chnames``, ``phys2bids`` will read the channel names from the header information in the file.

.. code-block:: shell

    phys2bids -in tutorial_file.txt -indir /home/arthurdent/git/phys2bids/phys2bids/tests/data/ -chtrig 1 -outdir /home/arthurdent/physio

This is outputted to the terminal:

.. code-block:: shell

    INFO:phys2bids.phys2bids:Currently running phys2bids version v1.3.0-beta+149.ge4a3c87.dirty
    INFO:phys2bids.phys2bids:Input file is tutorial_file.txt
    INFO:phys2bids.utils:File extension is .txt
    WARNING:phys2bids.utils:If both acq and txt files exist in the path, acq will be selected.
    INFO:phys2bids.phys2bids:Reading the file /home/arthurdent/git/phys2bids/phys2bids/tests/data/tutorial_file.txt
    INFO:phys2bids.interfaces.txt:phys2bids detected that your file is in Labchart format
    INFO:phys2bids.phys2bids:Reading infos
    INFO:phys2bids.physio_obj:
    ------------------------------------------------
    File tutorial_file.txt contains:
    01. Trigger; sampled at 1000.0 Hz
    02. CO2; sampled at 1000.0 Hz
    03. O2; sampled at 1000.0 Hz
    04. Pulse; sampled at 1000.0 Hz
    ------------------------------------------------

    INFO:phys2bids.viz:saving channel plot to tutorial_file.png
    INFO:phys2bids.physio_obj:Counting trigger points
    WARNING:phys2bids.physio_obj:The necessary options to find the amount of timepoints were not provided.
    INFO:phys2bids.phys2bids:Plot trigger
    INFO:phys2bids.phys2bids:Preparing 1 output files.
    INFO:phys2bids.phys2bids:Exporting files for freq 1000.0
    INFO:phys2bids.phys2bids:
    ------------------------------------------------
    Filename:            tutorial_file.txt

    Timepoints expected: 0
    Timepoints found:    0
    Sampling Frequency:  1000.0 Hz
    Sampling started at: -0.0 s
    Tip: Time 0 is the time of first trigger
    ------------------------------------------------

Five files have been generated in the output directory:

- **tutorial_file.log**
    The same information outputted to the terminal at the end of the call. 
- **tutorial_file.tsv.gz**
    Compressed file in ``tsv`` format containing your data without header information.
- **tutorial_file.json**
    As phys2bids is designed to be BIDs compatible, this is one of the two necessary BIDs files. It describes the content of your ``tsv.gz`` file.
- **tutorial_file_trigger_time.png**
    This file will become important later, but in a nutshell it shows the trigger channel from your file, as well as an indication of when the "0" time (corresponding to the first TR) should be.
    If you're just transforming files into ``tsv.gz``, **you can ignore this**
- **phys2bids_yyyy-mm-ddThh:mm:ss.tsv**
    This is the logger file. It contains the full terminal output of your ``phys2bids`` call.

Finding the "start time"
^^^^^^^^^^^^^^^^^^^^^^^^

If you recorded the trigger of your **(f)MRI**, ``phys2bids`` can use it to detect the moment in which you started sampling your neuroimaging data, and set the "0" time to be that point.  

First, we need to tell ``phys2bids`` where our trigger channel is, and we can use the argument ``-chtrig``. ``-chtrig`` has a default of 0, which means that if there is no input given ``phys2bids`` will assume the trigger information is in the hidden time channel.
For the text file used in this example, the trigger information is the second column of the raw file; the first recorded channel.

The last command line output said "Counting trigger points" and "The necessary options to find the amount of timepoints were not provided", so we need to give ``phys2bids`` some more information for it to correctly read the trigger information in the data. In this tutorial file, there are 158 triggers and the TR is 1.2 seconds. Using these arguments, we can call ``phys2bids`` again:

.. code-block:: shell

    phys2bids -in tutorial_file -chtrig 1 -outdir /home/arthurdent/physio -ntp 158 -tr 1.2

The output still warns us about something:

.. code-block:: shell

    WARNING:phys2bids.physio_obj:Found 158 timepoints less than expected!
    WARNING:phys2bids.physio_obj:Correcting time offset, assuming missing timepoints are at the beginning (try again with a more liberal thr)

How come?!? We know there are exactly 158 timepoints! Don't Panic. In order to find the triggers, ``phys2bids`` gets the first derivative of the trigger channel, and uses a threshold (default 2.5) to get the peaks of the derivative, corresponding to the trigger event. If the threshold is too strict or is too liberal for the recorded trigger, it won't get all the trigger points.
``phys2bids`` was created to deal with little sampling errors - such as distracted researchers that started sampling a bit too late than expected. For this reason, if it finds less timepoints than the amount specified, it will assume that the error was caused by a *distracted researcher*. 

Therefore, we need to change the ``-thr`` input until ``phys2bids`` finds the correct number of timepoints. Looking at the tutorial_file_trigger_time.png file can help determine what threshold is most appropriate. For this tutorial file, a threshold of 0.735 finds the right number of time points.

.. code-block:: shell

    phys2bids -in tutorial_file -chtrig 1 -outdir /home/arthurdent/physio -ntp 158 -tr 1.2 -thr 0.735

    INFO:phys2bids.phys2bids:Currently running phys2bids version v1.3.0-beta+152.g1f98d16.dirty
    INFO:phys2bids.phys2bids:Input file is tutorial_file.txt
    INFO:phys2bids.utils:File extension is .txt
    WARNING:phys2bids.utils:If both acq and txt files exist in the path, acq will be selected.
    INFO:phys2bids.phys2bids:Reading the file ./tutorial_file.txt
    INFO:phys2bids.interfaces.txt:phys2bids detected that your file is in Labchart format
    INFO:phys2bids.phys2bids:Reading infos
    INFO:phys2bids.physio_obj:
    ------------------------------------------------
    File tutorial_file.txt contains:
    01. Trigger; sampled at 1000.0 Hz
    02. CO2; sampled at 1000.0 Hz
    03. O2; sampled at 1000.0 Hz
    04. Pulse; sampled at 1000.0 Hz
    ------------------------------------------------

    INFO:phys2bids.viz:saving channel plot to tutorial_file.png
    INFO:phys2bids.physio_obj:Counting trigger points
    INFO:phys2bids.physio_obj:Checking number of timepoints
    INFO:phys2bids.physio_obj:Found just the right amount of timepoints!
    INFO:phys2bids.phys2bids:Plot trigger
    INFO:phys2bids.phys2bids:Preparing 1 output files.
    INFO:phys2bids.phys2bids:Exporting files for freq 1000.0
    INFO:phys2bids.phys2bids:
    ------------------------------------------------
    Filename:            tutorial_file.txt

    Timepoints expected: 158
    Timepoints found:    158
    Sampling Frequency:  1000.0 Hz
    Sampling started at: 0.24499999999989086 s
    Tip: Time 0 is the time of first trigger
    ------------------------------------------------

.. image:: _static/tutorial_file_trigger_time.png
   :alt: tutorial_file_trigger_time
   :align: center
    

Alright! Now we have some outputs that make sense.
The main difference from the previous call is in **tutorial_file.log** and **tutorial_file_trigger_time.png**.
The first one now reports 158 timepoints expected (as input) and found (as correctly estimated) and it also tells us that the sampling of the neuroimaging files started around 0.25 seconds later than the physiological sampling.
The second file now contains an orange trace that intersect the 0 x-axis and y-axis in correspondence with the first trigger.
In the first row, there's the whole trigger channel. In the second row, we see the first and last trigger (or expected first and last).

**Note**: It is *very* important to calibrate the threshold in a couple of files. This still *won't* necessarily mean that it's the right threshold for all the files, but there's a chance that it's ok(ish) for most of them.


Generating outputs in BIDs format
#################################

Alright, now the really interesting part! This section will explain how to use the ``-heur``, ``-sub``, and ``-ses`` arguments, to save the files in BIDs format. After all, that's probably why you're here.

``phys2bids`` uses heuristic rules *à la* `heudiconv <https://github.com/nipy/heudiconv>`_. At the moment, it can only use the name of the file to understand what should be done with it but we're working on making it *smarter*. There is a complete heuristic file for the tutorial, in the ``heuristics`` folder. Inside it looks more or less like this:

.. literalinclude:: ../phys2bids/heuristics/heur_tutorial.py
   :linenos:
   :lines: 4-22
   :lineno-start: 4

The heuristic file has to be written accordingly, with a set of rules that could work for all the files in your dataset. You can learn more about it if you check the `guide on how to set it up <heuristic.html>`_.
In this case, our heuristic file looks for a file that contains the name ``tutorial``. It corresponds to the task ``test`` and run ``00``. Note that **only the task is required**, all the other fields are optional - look them up in the BIDs documentation and see if you need them.

As there might not be a link between the physiological file and the subject (and session) that it relates to, ``phys2bids`` requires such information to be given from the user. In order for the *BIDsification* to happen, ``phys2bids`` needs the **full path** to the heuristic file, as well as the subject label. The session label is optional. The ``-outdir`` option will become the root folder for your BIDs files - i.e. your *site folder*:

.. code-block:: shell

    phys2bids -in tutorial_file.txt -chtrig 1 -outdir /home/arthurdent/physio_bids -ntp 158 -tr 1.2 -thr 0.735 -heur /home/arthurdent/git/phys2bids/phys2bids/heuristics/heur_tutorial.py -sub 006 -ses 01

The terminal output is as follows:

.. code-block:: shell

    INFO:phys2bids.phys2bids:Currently running phys2bids version v1.3.0-beta+152.g1f98d16.dirty
    INFO:phys2bids.phys2bids:Input file is tutorial_file.txt
    INFO:phys2bids.utils:File extension is .txt
    WARNING:phys2bids.utils:If both acq and txt files exist in the path, acq will be selected.
    INFO:phys2bids.phys2bids:Reading the file ./tutorial_file.txt
    INFO:phys2bids.interfaces.txt:phys2bids detected that your file is in Labchart format
    INFO:phys2bids.phys2bids:Reading infos
    INFO:phys2bids.physio_obj:
    ------------------------------------------------
    File tutorial_file.txt contains:
    01. Trigger; sampled at 1000.0 Hz
    02. CO2; sampled at 1000.0 Hz
    03. O2; sampled at 1000.0 Hz
    04. Pulse; sampled at 1000.0 Hz
    ------------------------------------------------

    INFO:phys2bids.viz:saving channel plot to tutorial_file.png
    INFO:phys2bids.physio_obj:Counting trigger points
    INFO:phys2bids.physio_obj:Checking number of timepoints
    INFO:phys2bids.physio_obj:Found just the right amount of timepoints!
    INFO:phys2bids.phys2bids:Plot trigger
    INFO:phys2bids.phys2bids:Preparing 1 output files.
    INFO:phys2bids.phys2bids:Preparing BIDS output using /home/arthurdent/git/phys2bids/phys2bids/heuristics/heur_tutorial.py
    INFO:phys2bids.phys2bids:Exporting files for freq 1000.0
    INFO:phys2bids.phys2bids:
    ------------------------------------------------
    Filename:            tutorial_file.txt

    Timepoints expected: 158
    Timepoints found:    158
    Sampling Frequency:  1000.0 Hz
    Sampling started at: 0.24499999999989086 s
    Tip: Time 0 is the time of first trigger
    ------------------------------------------------

It seems very similar to the last call - let's check the output folder.
It now contains the logger file, the trigger_time plot, and a folder for the specified subject, that (optionally) contains a folder for the session, containing a folder for the functional data, containing the log file and the required BIDs files with the right name!

.. code-block:: none

    - /home/arthurdent/physio_bids /
        - tutorial_file_sub-006_sub-01_trigger_time.png                              
        - phys2bids_yyyy-mm-ddThh:mm:ss.tsv                                          
        - sub-006 /
            - ses-01 /
                - func /
                    - sub-006_ses-01_task-test_rec-labchart_run-00_physio.json
                    - sub-006_ses-01_task-test_rec-labchart_run-00_physio.tsv.gz
                    - sub-006_ses-01_task-test_rec-labchart_run-00_physio.log        

**Note**: The main idea is that ``phys2bids`` should be called through a loop that can process all the files of your dataset. It's still a bit cranky, but we're looking to implement *smarter* solutions.

**Important**: Do not edit the heuristic file under where it says 'Don't modify below this!'.

One last thing left to do: take these files, remove the logs, and share them in public platforms!

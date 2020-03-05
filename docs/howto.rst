.. _howto:

========================
How to use ``phys2bids``
========================

This tutorial uses a text file exported from LabChart software. The principles of this tutorial apply for other inputs that ``phys2bids`` currently supports (AcqKnowledge native files and text files). However, future tutorials will go into the specifics of processing different inputs, as well as inputs which contain different sampling frequencies across data columns and inputs with multiple scans within one file.

This tutorial will:

1. Run ``phys2bids`` with the "-info" option, to show how to retrieve information about your input file.
2. Run ``phys2bids`` and explain the output files (png, json, tsv) that are generated.
3. Run ``phys2bids`` with a heuristic file, showing how the input file can be outputted in BIDS format.

Setup
#####

In order to follow the tutorial, you need a very quick setup: download or clone the `github repository <https://github.com/physiopy/phys2bids>`_ and install either the latest stable or development release as described `here <installation.html#install-with-pip>`_.

**Note**: for the tutorial, we will assume the repository was downloaded in ``/home/arthurdent/git``. Let's get there right now::

    cd /home/arthurdent/git/

What is in the tutorial text file?
##################################

The file can be found in ``phys2bids/phys2bids/tests/data/tutorial_file.txt``. This file has header information (first 9 lines) which phys2bids will use to process this file, alongside information directly inputted by the user. Following this header information, the data in the file is stored in a column format. In this example, we have time (column 1), MRI trigger pulse (column 2), CO2 (column 3), O2 (column 4) and pulse (column 5). Each column was sampled at 1000Hz (Interval = 0.001 s). ::

    Interval=	0.001 s
    ExcelDateTime=	4.3749464322749809e+04	10/11/19 11:08:37.485584
    TimeFormat=	StartOfBlock
    DateFormat=
    ChannelTitle=	Trigger	CO2	O2	Pulse
    Range=	2.000 V	50.0 mmHg	180.0 mmHg	10.000 V
    UnitName=	*	mmHg	mmHg	*
    TopValue=	*	56.44	180.80	*
    BottomValue=	*	-0.09	-0.96	*
    432.000 0.5810 0.7649 157.8775 0.0163
    432.001 0.5809 0.7621 157.8775 0.0213
    432.002 0.5810 0.7621 157.8295 0.0313
    432.003 0.5810 0.7621 157.8295 0.0319
    432.004 0.5810 0.7621 157.9255 0.0275
    432.005 0.5809 0.7595 157.8775 0.0288

**Note**: time is not a "real" channel recorded by LabChart or AcqKnowledge. For this reason, ``phys2bids`` treats it as hidden channel, always in position 0 - channel 1 will be the first channel recorded in either software.

Using the -info option
######################

First, we can see what information ``phys2bids`` reads from the file, and make sure this is correct before processing the file.

The simplest way of calling ``phys2bids`` is moving to the folder containing the physiological file and call: ::

    cd phys2bids/phys2bids/tests/data/
    phys2bids -in tutorial_file

``pys2bids`` will try to get the extension for you. 
However, we’ll use one more argument to have a sneak peak of the content of the file: ::

    phys2bids -in tutorial_file.txt -info

This ``-info`` argument means ``phy2bids`` does not process the file, but only outputs information it reads from the file, by printing to the terminal and outputting a png plot of the data in the current directory. ::

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

** [Correct channel plot here] **
    
Great! Now we know that the our file contains four channels, sampled at the same frequency, and that the trigger is in the first position. All this information will become useful.

Generating outputs
##################

Specifying paths and names
^^^^^^^^^^^^^^^^^^^^^^^^^^

Now we'll call ``phys2bids`` without the ``-info`` option. We'll use the same inputs as above, as well as adding ``-indir``, ``-outdir``, and ``-chplot``. If you use ``-indir`` you can specify a path to your input file i.e. it does not have to be in the current directory, as is the default. Using the ``-chplot`` argument allows you to specify the name (and full path) for the png channel plot. The ``-indir`` and ``-chplot`` arguments can be used alongside the ``-info`` argument. When calling ``phys2bids`` without the ``-info`` argument, it will generate files; if you use the ``-outdir`` argument this is where ``phys2bids`` will save these files.

Unless specified with ``-chsel`` ``phys2bids`` will process and output all channels. Unless specified with ``-chnames`` ``phys2bids`` will read the channel names from the header information in the file.  ::

    phys2bids -in tutorial_file.txt -indir /home/arthurdent/git/phys2bids/phys2bids/tests/data/ -chtrig 1 -outdir /home/arthurdent/physio

This is outputted to the terminal: ::

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
- **tutorial_file.json**
    As phys2bids is thought to be bids compatible, this is one of the two necessary bids files. It describes the content of your ``tsv.gz`` file.
- **tutorial_file.tsv.gz**
    Compressed file in ``tsv`` format containing your data without header information.
- **tutorial_file_trigger_time.png**
    This file will become important later, but in a nutshell it shows the trigger channel of your file, as well as an indication on when the "0" time (corresponding to the first tr) should be.
    If you're just transforming files into ``tsv.gz``, **you can ignore this**
- **phys2bids_yyyy-mm-ddThh:mm:ss.tsv**
    This is the logger file. It contains the full terminal output of your ``phys2bids`` call.

Finding the "start time"
^^^^^^^^^^^^^^^^^^^^^^^^

If you recorded the trigger of your **(f)MRI**, ``phys2bids`` can use it to detect the moment in which you started sampling your neuroimaging data, and set the "0" time to that point.  

First, we need to tell ``phys2bids`` what is our trigger channel, and we can use the argument ``-chtrig``. ``-chtrig`` has a default of 0, which means that if there is no input given ``phys2bids`` will assume the trigger information is in the hidden time channel.
For the text file used in this example, the trigger information is the second column of the raw file, and first recorded channel.

The last command line output said "Counting trigger points" and "The necessary options to find the amount of timepoints were not provided", so we need to give ``phys2bids`` some more information for it to correctly read the trigger information in the data. In this tutorial file, there are 534 triggers and the TR is 1.2 seconds. Using these arguments, we can call ``phys2bids`` again: ::

    phys2bids -in tutorial_file -chtrig 1 -chplot tutorial_file.png -outdir /home/arthurdent/physio -ntp 534 -tr 1.2

The output still warns us about something: ::

    WARNING:phys2bids.physio_obj:Found 534 timepoints less than expected!
    WARNING:phys2bids.physio_obj:Correcting time offset, assuming missing timepoints are at the beginning (try again with a more liberal thr)


tells us "Found 534 timepoints less than expected! Correcting time offset, assuming missing timepoints are at the beginning (try again with a more liberal thr)." Therefore, we need to change the "-thr" input until ``phys2bids`` finds the correct number of timepoints. Looking at the tutorial_file_trigger_time.png file can help your determine what threshold is more appropriate. For this tutorial file, a threshold of 0.735 finds the right number of time points. ::

    phys2bids -in tutorial_file -indir /home/my_phys_data/ -chtrig 1 -chplot /home/my_phys_outputs/tutorial_file.png -outdir /home/my_phys_outputs/ -ntp 534 -tr 1.2 -thr 0.735

    File extension is .txt
    Reading the file
    phys2bids detected that your file is in Labchart format
    Reading infos
    File tutorial_file.txt contains:

    00. CO2; sampled at 1000.0 Hz
    01. O2; sampled at 1000.0 Hz
    02. Pulse; sampled at 1000.0 Hz
    saving channels plot at plot at /home/my_phys_outputs/tutorial_file.png
    Counting trigger points
    Checking number of timepoints
    Found just the right amount of timepoints!
    Checking that the output folder exists
    Plot trigger
    Preparing 1 output files.
    Exporting files for freq 1000.0
    ------------------------------------------------
    Filename:            tutorial_file.txt

    Timepoints expected: 534
    Timepoints found:    534
    Sampling Frequency:  1000.0 Hz
    Sampling started at: 48.625999999999976 s
    Tip: Time 0 is the time of first trigger
    ------------------------------------------------

** [trigger_time.png here] **

** [explain how the 4 files above have changed] **

Generating outputs in BIDs format
#################################

This section will explain how to use the "-heur", "-sub" and "-ses" arguments, to save the file with BIDS naming.  

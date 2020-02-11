.. _howto:

====================
How to use phys2bids
====================

This tutorial uses a text file exported from LabChart software. The principles of this tutorial should still apply for other inputs that phys2bids currently supports (AcqKnowledge native files and text files). However, future tutorials will go into the specifics of processing different inputs, as well as inputs which contain different sampling frequencies across data columns and inputs with multiple scans within one file.

This tutorial will:

1. Run phys2bids with the "-info" option, to show how to retrieve information about your input file.
2. Run phys2bids and explain the output files (png, json, tsv) that are generated.
3. Run phys2bids with a heuristic file, showing how the input file can be outputted in BIDS format.

What is in the tutorial text file?
#################################

The file can be found in *tests/data/tutorial_file.txt*. This file has header information (first 9 lines) which phys2bids will use to process this file, alongside information directly inputted by the user. Following this header information, the data in the file is stored in a column format. In this example, we have time (column 1), MRI trigger pulse (column 2), CO2 (column 3), O2 (column 4) and pulse (column 5). Each column was sampled at 1000Hz (Interval = 0.001 s). ::

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

Using the -info option
######################

First, we can see what information phys2bids reads from the file, and make sure this is correct before processing the file.

The simplest way of calling phy2bids is: ::

    phys2bids -in tutorial_file

However, we’ll use one more argument: ::

    phys2bids -in tutorial_file -info

This "-info" argument means phy2bids does not process the file, but only outputs information it reads from the file, by printing to the terminal and outputting a png plot of the data in the current directory. ::

    File extension is .txt
    Reading the file
    phys2bids detected that your file is in Labchart format
    Reading infos
    File tutorial_file.txt contains:

    00. Trigger; sampled at 1000.0 Hz
    01. CO2; sampled at 1000.0 Hz
    02. O2; sampled at 1000.0 Hz
    saving channels plot at tutorial_file.png
    
** [Wrong channel plot here] **

Some of this information is right, but notice  the output does not mention a 'pulse' column, which we know is in the file. Therefore, if any of the information outputted from using the '-info' option is not correct, we need to give phys2bids more inputs.

Looking through the optional arguments of the phys2bids command (https://phys2bids.readthedocs.io/en/latest/cli.html) we will first ensure that all the channels we want processed are read and plotted correctly. The argument "-chtrig" has a default of 0, which means if there is no input given phys2bids will assume the trigger information is in the first channel. For the text file used in this example, the trigger information is the second column, therefore we need to write: ::

    phys2bids -in tutorial_file -info -chtrig 1

** [Correct channel plot here] **

Generating outputs
##################

Now we'll call phys2bids without the "-info" option. We'll use the same inputs as above, as well as adding "-indir", "outdir", and "-chplot". If you use "-indir" you can specify a path to your input file i.e. it does not have to be in the current directory, as is the default. Using the "-chplot" argument allows you to specify the name (and full path) for the png channel plot. The "-input" and "-chplot" arguments can be used alongside the "-info" argument. When calling phys2bids without the "-info" argument, it will generate files; if you use the "-outdir" argument this is where phys2bids will save these files.

Unless specified with "-chsel" phys2bids will process and output all channels. Unless specified with "-chnames" phys2bids will read the channel names from the header information in the file.  ::

    phys2bids -in tutorial_file -indir /home/my_phys_data/ -chtrig 1 -chplot /home/my_phys_outputs/tutorial_file.png -outdir /home/my_phys_outputs/

This is outputted to the terminal: ::

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
    Cannot check the number of timepoints
    Checking that the output folder exists
    Plot trigger
    Preparing 1 output files.
    Exporting files for freq 1000.0
    ------------------------------------------------
    Filename:            tutorial_file.txt

    Timepoints expected: 0
    Timepoints found:    0
    Sampling Frequency:  1000.0 Hz
    Sampling started at: -0.0 s
    Tip: Time 0 is the time of first trigger
    ------------------------------------------------

Four files have been generated in the output directory:

**tutorial_file.log**
The same information outputted to the terminal. 

**tutorial_file.json**
** [not sure how best to explain this one - "Column header information read from your file"] **

**tutorial_file.tsv.gz**
Compressed file containing your data without header information. 

**tutorial_file_trigger_time.png**
** [not sure how best to explain this one] **

The last command line output said "Cannot check the number of timepoints", so we need to give phys2bids some more information in order so it can correctly read the trigger information in the data. In this tutorial file, there are 534 triggers and the TR is 1.2 seconds. Using these arguments, we can call phys2bids again: ::

    phys2bids -in tutorial_file -indir /home/my_phys_data/ -chtrig 1 -chplot /home/my_phys_outputs/tutorial_file.png -outdir /home/my_phys_outputs/ -ntp 534 -tr 1.2

The output tells us "Found 534 timepoints less than expected! Correcting time offset, assuming missing timepoints are at the beginning (try again with a more liberal thr)." Therefore, we need to change the "-thr" input until phys2bids finds the correct number of timepoints. Looking at the tutorial_file_trigger_time.png file can help your determine what threshold is more appropriate. For this tutorial file, a threshold of 0.735 finds the right number of time points. ::

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

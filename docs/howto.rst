.. _howto:

====================
How to use phys2bids
====================

This tutorial uses a text file exported from LabChart software. The principles of this tutorial should still apply for other inputs that phys2bids currently supports (AcqKnowledge native files and text files). However, future tutorials will go into the specifics of processing different inputs, as well as inputs which contain different sampling frequencies across data columns and inputs with multiple scans within one file.

This tutorial will:

1. Run phys2bids with the "-info" option, to show how to retrieve information about your input file.
2. Run phys2bids and explain the output files (png, json, tsv) that are generated.
3. Run phys2bids with a heuristic file, showing how the input file can be outputted in BIDS format.

What is in the example text file?
#################################

The text file can be found in **location**. This text file has header information (first 9 lines) which phys2bids will use to process this file, alongside information directly inputted by the user. Following this header information, the data in the file is stored in a column format. In this example, we have time (column 1), MRI trigger pulse (column 2), CO2 (column 3), O2 (column 4) and pulse (column 5). Each column was sampled at 1000Hz (Interval = 0.001 s).::

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

First, we can see what information phys2bids can read from the file, and make sure this is correct before processing the file.

The simplest way of calling phy2bids is: ::

    phys2bids -in textfile

However, we’ll add one more input: ::

    phys2bids -in textfile -info

This "-info" option means phy2bids does not process the file, but only outputs information it reads from the file, by printing to the terminal and outputting a png plot of the data in the current directory. ::

    File extension is .txt
    Reading the file
    phys2bids detected that your file is in Labchart format
    Reading infos
    File Test2_time_trigger_CO2_O2_pulse_1000Hz_534TRs.txt contains:

    00. Trigger; sampled at 1000.0 Hz
    01. CO2; sampled at 1000.0 Hz
    02. O2; sampled at 1000.0 Hz
    saving channels plot at plot at Test2_time_trigger_CO2_O2_pulse_1000Hz_534TRs.png

**[Wrong channel plot here]**

Some of this information is right, but notice  the output does not mention a 'pulse' column, which we know is in the file. Therefore, if any of the information outputted from using the '-info' option is not correct, we need to give phys2bids more options.

Looking through the optional arguments of the phys2bids command (**Link here to the command-line usage page**) we will first ensure that all the channels we want processed are read and plotted correctly. 

**explain here how and why you might want to change -indir, -chtrig, -chplot**

**[Correct channel plot here]**

Generating outputs
##################

**first run the same as above but without -info**

**look at outputs it generates**

**then explain the -outdir, -chsel, -ntp, -tr, -thr, -chnames options**

Generating outputs in BIDs format
#################################
 
**explain heuristics file and the -sub and -ses inputs**

.. _howto:

====================
How to use phys2bids
====================

This tutorial uses a text file exported from LabChart software.
The principles of this tutorial should still apply for other inputs that phys2bids currently supports (AcqKnowledge native files and text files).
However, future tutorials will go into the specifics of processing different inputs, as well as inputs which contain different sampling frequencies across data columns and inputs with multiple scans within one file.

This tutorial will:
Show you how to retrieve information about your input file (with the "-info" option), ensuring phys2bids has the correct information about your file.
Explain the output files (png, json, tsv) phys2bids generates.
Explain how phys2bids can return the input file in BIDS format.

What is in the example text file?

This text file has header information (first 9 lines) which the phys2bids software will use, alongside information directly inputted by the user. Following this header information, the data is stored in a column format. In this example, we have time (column 1), MRI trigger pulse (column 2), CO2 (column 3), O2 (column 4) and pulse (column 5). Each column was sampled at 1000Hz (Interval = 0.001 s).

Interval=	0.001 s
ExcelDateTime=	4.3749464322749809e+04	10/11/19 11:08:37.485584
TimeFormat=	StartOfBlock
DateFormat=
ChannelTitle=	Trigger	CO2	O2	Pulse
Range=	2.000 V	50.0 mmHg	180.0 mmHg	10.000 V
UnitName=	*	mmHg	mmHg	*
TopValue=	*	56.44	180.80	*
BottomValue=	*	-0.09	-0.96	*
432	            0.581	            0.7648337	157.8775	0.01625
432.001	0.5809375	0.7621496	157.8775	0.02125
432.002	0.581	            0.7621496	157.8295	0.03125
432.003	0.581	            0.7621496	157.8295	0.031875
432.004	0.581	            0.7621496	157.9255	0.0275
432.005	0.5809375	0.7594637	157.8775	0.02875
432.006	0.5809375	0.7594637	157.9015	0.0378125
432.007	0.5809375	0.7567795	157.9255	0.0340625
432.008	0.581	            0.7567795	157.9255	0.0353125
432.009	0.5809375	0.7540936	157.8775	0.04125
432.01	            0.5809375	0.7540936	157.9494	0.0415625
…

Using the -info option


First, we can see what information phys2bids can read from the file.

The simplest way of calling phy2bids is:

phys2bids -in textfile

However, we’ll add one more input:

phys2bids -in textfile -info

This ‘info’ option means phy2bids does not process the file, but only outputs information about the file, by printing to the terminal and outputting a .png file, which is a plot of the data.

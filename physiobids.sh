#!/bin/bash

#### TODO
# channel names -> get array
# get rid of AFNI
# get rid of csvtool
# better trigger

ver=2.0.0

# Check locale
oldnum=${LC_NUMERIC}
LC_NUMERIC=en_IN

displayhelp() {
echo ""
echo "physiobids version ${ver}"
echo "Script to convert AcqKnowledge files into .tsv.gz files"
echo "It outputs a .tsv.gz and a .json file with the same name of input,"
echo ""
echo "unless heuristics are used (see usage)"
echo ""
echo "If option -ntp and -tr are specified, the program check if the first trigger"
echo "detected is the first trigger, and correct starting time for it."
echo ""
echo "Dependances:"
echo "   -AFNI"
echo "   -csvtool (deb) OR ocaml-csv (rpm)"
echo "   -acq2txt"
echo ""
echo "Usage:"
echo "   physiobids.sh -in infile -chtrig trigger -chsel c,h,a,n -ntp num -tr secs"
echo ""
echo "   -in filename:   The name of the acq file, with or without extension."
echo "Input:"
echo "                      Must be an .acq file!"
echo "   -indir pth/to:  Folder containing input."
echo "   -odir pth/to:  Folder where output should be placed. If \"-heur\" is used, "
echo "                      Default: ."
echo "                      It'll become the site folder."
echo "   -heur pth/fl:   File containing heuristic, with or without extension."
echo "                      Default: ."
echo "                      Specify path to it if necessary. Optional."
echo "                      Needs \"-sub\", and it's possible to specify \"-ses\""
echo "                      Default: heur.sh  (in script folder)"
echo "   -sub subnum:    To be specified with \"-heur\". Number of subject to process."
echo "   -info:          Only output info about file, no transformation."
echo "   -ses sesnum:    Can be specified with \"-heur\". Number of session to process."
echo "   -chtrig num:    The number corresponding to the trigger channel."
echo "                      Channels start with zero!"
echo "                      Default: 1"
echo "   -chsel n,m,o:   If specified, it extracts only the specified channels."
echo "                      Channels start with zero!"
echo "                      Channels have to be specified one by one with commas."
echo "   -ntp num:       Number of expected timepoints. Optional."
echo "   -tr sec:        TR of sequence in seconds.  Optional."
echo "   -thr num:       Threshold used for trigger detection."
echo "                      Default: 3"
echo "   -tbhd \"a b c\":  Columns header (for json file). Optional."
echo "                      Default: \"time respiratory_chest trigger cardiac ..."
echo "                              ... respiratory_CO2 respiratory_O2\""
echo ""
echo "   -h:             Display this help."
echo "   -v:             Display version."
echo ""
echo ""

exit 1
} 

# Check if there is input
if [[ ( $# -eq 0 ) ]]
	then
	displayhelp
fi

scriptdir=$( which physiobids )
# Preparing the default values for optional variables
chtrig=1
thr=3
tbhd=$( echo "time respiratory_chest trigger cardiac respiratory_CO2 respiratory_O2" )
indir=.
odir=.
heur=${scriptdir::-10}heur
#colname=$( echo "[\"time\", \"respiratory chest\", \"trigger\", \"cardiac\", \"respiratory CO2\", \"respiratory O2\"]" )


while [[ ! -z "$1" ]]
do
	case "$1" in
		# required variables
		-in)     in=$2;shift;;
		# optional var with default
		-chtrig) chtrig=$2;shift;;
		-thr)    thr=$2;shift;;
		-tbhd)   tbhd=$2;shift;;
		-indir)  indir=$2;shift;;
		-odir)   odir=$2;shift;;
		-heur)   heur=$2;shift;;
		# optional var empty
		-info)   info=1;;
		-chsel)  chsel=$2;shift;;
		-ntp)    ntp=$2;shift;;
		-tr)     tr=$2;shift;;
		# bids
		-sub)    sub=$2;shift;;
		-ses)    ses=$2;shift;;
		# other
		-h)  displayhelp;;
		-v)  echo "Version ${ver}";exit 0;;
		*)   echo "Wrong flag: $1";displayhelp;;
	esac
	shift
done

# in=BH4
# chtrig=1
# chsel=0,1,2,3,4
# ntp=240
# tr=2
# Check if paths have last / and create outdir if non-existent

if [ ${indir: -1} != "/" ]
then
	indir=${indir}/
fi
if [ ${odir: -1} != "/" ]
then
	odir=${odir}/
fi
if [ ! -d ${odir::-1} ]
then
	mkdir ${odir::-1}
fi

# Check if the extension is right
if [ ${in:-4} != ".acq" ]
then
	in=${in}.acq
fi

inmsg=${in}
out=${odir}${in::-4}
in=${indir}${in}

# Check if the file exists
if [ ! -e ${in} ]
then
	printf "File %s doesn't exists\n\n" "${in}"
	displayhelp
fi

# Output channel names and sample time
printf "\nFile %s has:\n" "${inmsg}"
acq_info ${in} | grep -vP "\t"

printf "\n\n-----------------------------------------------------------\n\n"

if [ "${info}" ]
then
	exit
fi

# Transform the file
if [ "${chsel}" ]
then
	echo "Selected channels ${chsel}"
	chsel=--channel-indexes=${chsel}
fi

echo "Extracting info from acq"
acq2txt "${chsel}" -o rm.transform.tsv ${in}

# Remove first line
csvtool -t TAB -u TAB drop 1 rm.transform.tsv > rm.drop.tsv

# Get time and trigger in separate files (correcting trigger offset)
echo "Separating time and trigger (channel ${chtrig})"
csvtool -t TAB col 1 rm.drop.tsv > rm.time.1D
# csvtool -t TAB col 2 rm.trigger.tsv > rm.trigger.1D
let chtrig+=2
csvtool -t TAB col ${chtrig} rm.drop.tsv > rm.trigger.1D

# Derive trigger to check number of tp in file, then threshold and count number of tp.
echo "Counting trigger points"
1d_tool.py -infile rm.trigger.1D -derivative -write rm.trigger_deriv.1D -overwrite
1deval -a rm.trigger_deriv.1D -b=${thr} -expr 'ispositive(a-b)' > rm.trigger_thr.1D

ntpf=$( awk '{s+=$1} END {printf "%.0f", s}' rm.trigger_thr.1D )

# Find time of first timepoint above 0.5: the first trigger
echo "Extracting other info for json file"
evawk="awk '\$${chtrig}>${thr}{print; exit}' rm.drop.tsv"
tza=( $( eval "${evawk}" ) )

if [ "${ntp}" ]
then
	# Correct starting time by number of missing tp, if any.
	echo "Checking if any TPs are missing"
	tz=$( echo " ${tza[0]} - ( ( ${ntp} - ${ntpf} ) * ${tr} ) " | bc )
else
	# Just extract tza
	echo "Skipping TPs check"
	tz=${tza[0]}
fi

# Find Sampling Frequency
sta=( $( acq_info ${in} | grep "Sample time" ) )
sf=$( echo "1 / ${sta[2]}" | bc )

# Correct time column by starting time and replace it in file
echo "Correcting time in file"
1deval -a rm.time.1D -b=${tz} -expr 'a-b' > rm.newtime.1D

csvtool -t TAB -u TAB transpose rm.drop.tsv | csvtool -t TAB -u TAB drop 1 - > rm.drop_t.tsv
csvtool -t TAB -u TAB paste rm.newtime.1D rm.drop.tsv > ${out}.tsv
csvtool -t TAB -u TAB transpose rm.drop_t.tsv > rm.drop.tsv

echo "Preparing output and cleaning up the mess"
# remove all intermediate steps
rm rm.*

gzip -f ${out}.tsv
# gzip tsv

# Print json
tz=$( echo "${tz} * (-1)" | bc )
printf "{\n\t\"SamplingFrequency\": %.3f,\n\t\"StartTime\": %.3f,\n\t\"Columns\": [\"%s\"]\n}" "${sf}" "${tz}" $(echo "${tbhd}" | sed 's: :", ":g' ) > ${out}.json


# Print summary on screen
echo "Filename:            ${out}"
printf "\n\n-----------------------------------------------------------\n\n"
echo ""
echo "Timepoints expected: ${ntp}"
echo "Timepoints found:    ${ntpf}"
echo "Sampling Frequency:  ${sf} Hz" # Check
echo "Sampling started at: ${tz} s"
echo "Tip: Time 0 is the time of first trigger"
printf "\n\n-----------------------------------------------------------\n\n"

# Print summary in file
echo "Filename:            ${out}" > ${out}.log
printf "\n\n-----------------------------------------------------------\n\n" >> ${out}.log
echo "" >> ${out}.log
echo "Timepoints expected: ${ntp}" >> ${out}.log
echo "Timepoints found:    ${ntpf}" >> ${out}.log
echo "Sampling Frequency:  ${sf} Hz" >> ${out}.log # Check
echo "Sampling started at: ${tz} s" >> ${out}.log
echo "Tip: Time 0 is the time of first trigger" >> ${out}.log
printf "\n\n-----------------------------------------------------------\n\n" >> ${out}.log


LC_NUMERIC=${oldnum}
#############################
### Here goes "heuristic" ###
#############################
if [ ! -e ${heur} ]
then
	heur=${heur}.sh
fi
if [ -e ${heur} ] && [ ${sub} ]
then
	${heur} ${inmsg::-4} ${odir} ${sub} ${ses}
else
	echo "Skipping heuristics"
fi

echo "All done!"
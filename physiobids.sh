#!/bin/bash

#### TODO
# flagged input
# channel names -> get array
# get rid of AFNI
# get rid of csvtool
# better trigger

# Check if there is input

if [[ ( $# -eq 0 ) ]]
	then
	displayhelp
fi

# Preparing the default values for optional variables
chtrig=1

colname=$( echo "[\"time\", \"respiratory chest\", \"trigger\", \"cardiac\", \"respiratory CO2\", \"respiratory O2\"]" )

while [[ ! -z "$1" ]]
do
	case "$1" in
		# required variables
		-in)     in=$2;shift;;
		-chtrig) chtrig=$2;shift;;
		-chsel)  chsel=$2;shift;;
		-ntp)    ntp=$2;shift;;
		-tr)     tr=$2;shift;;
		# other
		-h)  displayhelp;;
		-v)  echo "Version 1.0.0";exit 0;;
		*)   echo "Wrong flag: $1";displayhelp;;
	esac
	shift
done


# in=BH4
# chtrig=1
# chsel=0,1,2,3,4
# ntp=240
# tr=2

# Output channel names and sample time
echo ""
echo "File ${in}.acq has:"
acq_info ${in}.acq | grep -vP "\t"

printf "\n\n-----------------------------------------------------------\n\n"

# # Extract the trigger channel, get rid of header
# echo "Extracting channel ${chtrig} for trigger"
# acq2txt --channel-indexes=${chtrig} -o rm.trigger2txt.tsv ${in}.acq
# csvtool -t TAB -u TAB drop 1 rm.trigger2txt.tsv > rm.trigger.tsv

# Transform the file
if [ "${chsel}" ]
then
	echo "Selected channels ${chsel}"
	chsel=--channel-indexes=${chsel}
fi

echo "Extracting info from acq"
acq2txt ${chsel} -o rm.transform.tsv ${in}.acq

# Remove first line
csvtool -t TAB -u TAB drop 1 rm.transform.tsv > rm.drop.tsv

# Get time and trigger in separate files (correcting trigger offset)
echo "Separating time and trigger (channel ${chtrig})"
csvtool -t TAB col 1 rm.drop.tsv > rm.time.1D
# csvtool -t TAB col 2 rm.trigger.tsv > rm.trigger.1D
let chtrig+=2
csvtool -t TAB col ${chtrig} rm.drop.tsv > rm.trigger.1D

# Derive trigger to check number of tp in file, then threshold
echo "Counting trigger points"
1d_tool.py -infile rm.trigger.1D -derivative -write rm.trigger_deriv.1D -overwrite
1deval -a rm.trigger_deriv.1D -b=0.5 -expr 'ispositive(a-b)' > rm.trigger_thr.1D

# Find time of first timepoint above 0.5: the first trigger
echo "Extracting other info for json file"
evawk="awk '\$${chtrig}>0.5{print; exit}' rm.drop.tsv"
tza=( $( eval ${evawk} ) )


#if [ "${ntp}" && ${ntr} ]
# Count number of tp in file, then correct starting time by number of missing tp.
ntpf=$( awk '{s+=$1} END {printf "%.0f", s}' rm.trigger_thr.1D )
tz=$( echo " ${tza[0]} - ( ( ${ntp} - ${ntpf} ) * ${tr} ) " | bc )

# Find Sampling Frequency
sta=( $( acq_info ${in}.acq | grep "Sample time" ) )
sf=$( echo "1 / ${sta[2]}" | bc )

# Correct time column by starting time and replace it in file
echo "Correcting time in file"
1deval -a rm.time.1D -b=${tz} -expr 'a-b' > rm.newtime.1D

csvtool -t TAB -u TAB transpose rm.drop.tsv | csvtool -t TAB -u TAB drop 1 - > rm.drop_t.tsv
csvtool -t TAB -u TAB transpose rm.drop_t.tsv > rm.drop.tsv
csvtool -t TAB -u TAB paste rm.newtime.1D rm.drop.tsv > ${in}.tsv

# remove all intermediate steps
echo "Preparing output and cleaning up the mess"
rm rm.*

# gzip tsv
gzip -f ${in}.tsv

# Print json
tz=$( echo "${tz} * (-1)" | bc )

# Check locale
oldnum=${LC_NUMERIC}
LC_NUMERIC=en_IN

printf "{\n\t\"SamplingFrequency\": %.3f,\n\t\"StartTime\": %.3f,\n\t\"Columns\": %s\n}" "${sf}" "${tz}" "${colname}" > ${in}.json

# Print summary on screen
printf "\n\n-----------------------------------------------------------\n\n"
echo "Filename:            ${in}.acq"
echo ""
echo "Timepoints expected: ${ntp}"
echo "Timepoints found:    ${ntpf}"
echo "Sampling Frequency:  ${sf} Hz" # Check
echo "Sampling started at: ${tz} s"
echo "Tip: Time 0 is the time of first trigger"
printf "\n\n-----------------------------------------------------------\n\n"

LC_NUMERIC=${oldnum}
#############################
### Here goes "heuristic" ###
#############################
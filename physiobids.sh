#!/bin/bash

in=$1
chtrig=$2
chsel=$3

acq2txt --channel-indexes=${chtrig} -o rm.trigger.tsv ${in}.acq

if [ "${chsel}" ]
then
	chsel=--channel-indexes=${chsel}
fi

acq2txt ${chsel} -o ${in}.tsv ${in}.acq




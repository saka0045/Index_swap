#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 10:29:13 2018

@author: m006703
"""

import gzip

# open files
vcfFile = gzip.open('/dlmp/sandbox/runs/WESPP/NGS26-WESPP_F137035_NS0001_NS0001_H2YF5DMXX/samples/WESPP-NA12878-CTRL/ggps_results/OUTPUT/PI/exome/WESPP-NA12878-CTRL/variants/variants.vcf.gz.bior_annotate.vcf.gz', 'rb')
#vcfFile = open('/Users/m006703/Index_Swap/files/practice.vcf', 'r')

# Go to the header line
for line in vcfFile:
    if line.startswith('#CHROM'):
        firstline = line.split('\t')
        sampleName = firstline[9].rstrip()
	break
        
outFile = open('/dlmp/sandbox/cgslIS/Yuta/Index_Swap/files/' + sampleName + '_gnomAD.vcf', 'w')
        
# Start collecting data after the header line           
chrom = []
pos = []
snpid = []
ref = []
alt = []
qual = []
qualfilter = []
info = []
resultformat = []

# Collect data that only has value for non-population specific gnomAD frequency
for line in vcfFile:
    result = line.split('\t')
    infoline = result[7]
    if 'gnomAD_r201_GRCh37.INFO.AF=' in infoline:
        splitinfoline = infoline.split(';')
        for item in splitinfoline:
            if item.startswith('gnomAD_r201_GRCh37.INFO.AF='):
                gnomADInfo = float(item.split('=')[1])
                if 0 < gnomADInfo <= 0.001: # Adjust this to change cutoff
                    chrom.append(result[0])
                    pos.append(result[1])
                    snpid.append(result[2])
                    ref.append(result[3])
                    alt.append(result[4])
                    qual.append(result[5])
                    qualfilter.append(result[6])
                    info.append(gnomADInfo)
                    resultformat.append(result[8])
                   
outFile.write('CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tgnomADINFO\n')

for index in range(len(chrom)):
    resultList = []
    resultList = [chrom[index], pos[index], ref[index], alt[index], qual[index], qualfilter[index], str(info[index])]
    outFile.write('\t'.join(resultList) + '\n')

vcfFile.close()
outFile.close()

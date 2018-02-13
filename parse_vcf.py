#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 10:29:13 2018

@author: m006703
"""

# open files
vcfFile = open('practice.vcf', 'r')
outFile = open('gnomAD.vcf', 'w')

# Go to the header line
for line in vcfFile:
    if line.startswith('#CHROM'):
                       break
        
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

for line in vcfFile:
    result = line.split('\t')
    chrom.append(result[0])
    pos.append(result[1])
    snpid.append(result[2])
    ref.append(result[3])
    alt.append(result[4])
    qual.append(result[5])
    qualfilter.append(result[6])
    info.append(result[7])
    resultformat.append(result[8])

# Replace item in info list with only gnomAD results    
index = 0    
while (index < (len(info))):
    gnomADList = []
    if 'gnomAD' in info[index]:
        eachinfoList = info[index].split(';')
        for item in eachinfoList:
            if item.startswith('gnomAD'):
                gnomADList.append(item)
    else:
        gnomADList = ['NA']
    info[index] = gnomADList
    index += 1
                   
outFile.write('CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n')

index = 0
while (index < (len(chrom))):
    resultList = []
    resultList = [chrom[index], pos[index], ref[index], alt[index], qual[index], qualfilter[index], ';'.join(info[index])]
    outFile.write('\t'.join(resultList) + '\n')
    index += 1

vcfFile.close()
outFile.close()
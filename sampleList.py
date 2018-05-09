#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  4 07:50:59 2018

@author: m006703

Parses the samples in snp_analysis.txt and creates a list of unique samples
"""

# Open the snp_analysis.txt file and read through the header line
snpAnalysisFile = open('/Users/m006703/Index_Swap/files/result/snp_analysis.txt', 'r')
snpAnalysisFile.readline()

uniqueSampleList = []

for line in snpAnalysisFile:
    line = line.rstrip()
    lineList = line.split('\t')
    sampleNames = lineList[6]
    sampleNameList = sampleNames.split(',')
    for sample in sampleNameList:
        if sample not in uniqueSampleList:
            uniqueSampleList.append(sample)
            
snpAnalysisFile.close()

# Write out results
sampleNameFile = open('/Users/m006703/Index_Swap/files/result/snpNameFile.txt', 'w')

for uniqueSample in uniqueSampleList:
    sampleNameFile.write(uniqueSample + '\n')
    
sampleNameFile.close()
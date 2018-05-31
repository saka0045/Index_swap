#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 18 09:30:57 2018

@author: m006703
"""

import os

# Open all of the files created by parse_vcf.py
basedir = '/Users/m006703/Index_Swap/files/' #Replace this with your own directory
fileList = os.listdir(basedir)

# Create snp dictionary for all files in the filePath
snpDict = {}
sampleList = []
for file in fileList:
    filePath = basedir + file
    sampleName = file.split('_')[0]
    # Short name is the unique family ID
    shortName = sampleName.split('-')[0]
    # Only open if it is a file and not a directory
    if os.path.isfile(filePath):
        sampleList.append(sampleName)
        openFile = open(filePath, 'r')
        print("Processing file: " + filePath)
        # Ignore the header
        openFile.readline()
        for line in openFile:
            line = line.rstrip()
            lineList = line.split('\t')
            chrom = lineList[0]
            pos = lineList[1]
            ref = lineList[3]
            alt = lineList[4]
            gnomadFreq = lineList[7]
            # Get the ref allele count from Format column
            alleleInfo = lineList[9]
            alleleInfoList = alleleInfo.split(':')
            alleleCount = alleleInfoList[1].split(',')
            refAlleleCount = alleleCount[1] # This is the ref allele count
            coverage = lineList[10]
            # Calculate the ref allele frequency
            try:
                refAlleleFrequency = ("%.2f" % (float(refAlleleCount) / float(coverage)))
            except ZeroDivisionError:
                refAlleleFrequency = '0'
            # Gather snps with GnomAD frequency less than 0.01%
            if float(gnomadFreq) <= 0.0001:
                # Create a new key if the position is not in the dictionary
               if pos not in snpDict:
                   coverageList = []
                   coverageList.append(coverage)
                   sampleNameList = []
                   sampleNameList.append(sampleName)
                   shortNameList = []
                   shortNameList.append(shortName)
                   frequencyList = []
                   frequencyList.append(refAlleleFrequency)
                   snpDict[pos] = [sampleNameList, coverageList, chrom, ref, alt, gnomadFreq, shortNameList, frequencyList]
               else:
                   snpDict[pos][0].append(sampleName)
                   snpDict[pos][1].append(coverage)
                   snpDict[pos][6].append(shortName)
                   snpDict[pos][7].append(refAlleleFrequency)
        openFile.close()
        
# Create result directory inside basedir if it doesn't exist
if not os.path.exists(basedir + 'result/'):
    print("result directory does not exist in " + basedir + ", creating directory...")
    os.makedirs(basedir + 'result/')

# Make files with sample names in column headers and variant location in row header
# with variant frequencies and coverage for those variants    
freqFile = open(basedir + 'result/sharedVariantFreq.txt', 'w')
coverageFile = open(basedir+ 'result/sharedVariantCoverage.txt', 'w')
freqFile.write("Variant_Position\t" + '\t'.join(sampleList) + '\n')
coverageFile.write("Variant_Position\t" + '\t'.join(sampleList) + '\n')

# Iterate through all the variants and record the respective values for the samples if it exists
for (key, val) in snpDict.items():
    freqFile.write("chr" + snpDict[key][2] + ":" + key + '\t')
    coverageFile.write("chr" + snpDict[key][2] + ":" + key + '\t')
    for sample in sampleList:
        if sample in snpDict[key][0]:
            sampleIndex = snpDict[key][0].index(sample)
            freqFile.write(snpDict[key][7][sampleIndex] + '\t')
            coverageFile.write(snpDict[key][1][sampleIndex] + '\t')
        else:
            freqFile.write("0\t")
            coverageFile.write("0\t")
    freqFile.write('\n')
    coverageFile.write('\n')
    
freqFile.close()
coverageFile.close()

print("Script is done running")
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 26 21:16:31 2018

@author: m006703

This script takes all of the filtered VCF files from parse_vcf.py and
compile the variants that are seen accross multiple samples that are not
related to one another.
"""

import os

# Open all of the files created by parse_vcf.py
basedir = '/Users/m006703/Index_Swap/files/' #Replace this with your own directory
fileList = os.listdir(basedir)

# Create snp dictionary for all files in the filePath
snpDict = {}
for file in fileList:
    filePath = basedir + file
    sampleName = file.split('_')[0]
    # Short name is the unique family ID
    shortName = sampleName.split('-')[0]
    # Only open if it is a file and not a directory
    if os.path.isfile(filePath):
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

# Write out results
resultFile = open(basedir + 'result/snp_analysis.txt', 'w')
resultFile.write("CHROM\tPOS\tREF\tALT\tgnomADFrequency\tCoverage\tFrequency\tSample\n")

# File to report out the coverage and associated frequency of an unfiltered variant for the sample
coverageAndFrequency = open(basedir + 'result/coverage_and_frequency.txt', 'w')
coverageAndFrequency.write("Coverage\tFrequency\n")

reportedCoverage = []
reportedFrequency = []

for (key,val) in snpDict.items():
    if len(snpDict[key][0]) > 1:
        # Only report out variants that are shared across multiple unique family IDs
        if not all(x == snpDict[key][6][0] for x in snpDict[key][6]):
            # At least one sample need to have coverage greater than or equal to 30 and allele frequency greater than or equal to 0.2
            if (max(map(int, snpDict[key][1])) >= 30 and max(map(float, snpDict[key][7])) >= 0.2):
                resultFile.write(snpDict[key][2] + '\t' + key + '\t' + snpDict[key][3] + '\t' + snpDict[key][4]\
                             + '\t' + snpDict[key][5] + '\t' + ','.join(snpDict[key][1]) + '\t'\
                             + ','.join(snpDict[key][7]) + '\t' + ','.join(snpDict[key][0]) + '\n')
                for reportCov in snpDict[key][1]:
                    reportedCoverage.append(reportCov)
                for reportFreq in snpDict[key][7]:
                    reportedFrequency.append(reportFreq)
                    
for index in range(len(reportedCoverage)):
    coverageAndFrequency.write(reportedFrequency[index] + "\t" + reportedCoverage[index] + "\n")
        
resultFile.close()
coverageAndFrequency.close()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 18 09:30:57 2018

@author: m006703
"""

import os

# Open all of the files created by parse_vcf.py
basedir = '/Users/m006703/Index_Swap/files/Probands_Only/' #Replace this with your own directory
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
            # Only collect SNVs
            if (len(ref) == 1 and len(alt)) == 1:
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
freqFile.write("Variant_Position\tgnomAD_Freq\tRef\tAlt\tSamples_with_Frequency\t" \
               + '\t'.join(sampleList) + '\n')
coverageFile.write("Variant_Position\tgnomAD_Freq\tRef\tAlt\tSamples_with_Coverage")
for sample in sampleList:
    coverageFile.write("\t" + sample + "_cov\t" + sample + "_RCF")
coverageFile.write("\tNum0.2RCF")
coverageFile.write("\n")

# Iterate through all the variants and record the respective values for the samples if it exists
for (key, val) in snpDict.items():
    numberOfSamplesWithFrequency = 0
    numberOfSamplesWithCoverage = 0
    numberOfSamplesPoint2RCF = 0
    maxCoverage = max(map(int, snpDict[key][1]))
    for values in snpDict[key][7]:
        if float(values) > 0:
            numberOfSamplesWithFrequency += 1
    # Calculate the number of samples with coverage
    for item in snpDict[key][1]:
        if int(item) > 0:
            numberOfSamplesWithCoverage += 1
    freqFile.write("chr" + snpDict[key][2] + ":" + key + '\t' + snpDict[key][5] + '\t' + snpDict[key][3] + '\t' \
                   + snpDict[key][4] + '\t' + str(numberOfSamplesWithFrequency) + '\t')
    coverageFile.write("chr" + snpDict[key][2] + ":" + key + '\t' + snpDict[key][5] + '\t' + snpDict[key][3] + '\t' \
                   + snpDict[key][4] + '\t' + str(numberOfSamplesWithCoverage) + '\t')
    # Pulls out the frequency or coverage for the specified sample and list them in the order it has in sampleList
    for sample in sampleList:
        if sample in snpDict[key][0]:
            sampleIndex = snpDict[key][0].index(sample)
            freqFile.write(snpDict[key][7][sampleIndex] + '\t')
            relativeCoverageFrequency = ("%.2f" % (int(snpDict[key][1][sampleIndex]) / maxCoverage))
            # Keep count of samples with relative coverage frequency greater than 0.2
            if (0.2 < float(relativeCoverageFrequency)):
                numberOfSamplesPoint2RCF += 1
            coverageFile.write(snpDict[key][1][sampleIndex] + '\t' + \
                               str(relativeCoverageFrequency) + '\t')
        else:
            freqFile.write("0\t")
            coverageFile.write("0\t0\t")
    freqFile.write('\n')
    coverageFile.write(str(numberOfSamplesPoint2RCF) + '\n')
    
freqFile.close()
coverageFile.close()

print("Script is done running")
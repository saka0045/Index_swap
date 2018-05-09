#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  7 07:46:18 2018

@author: m006703

Takes the positions from snp_analysis.txt and compares the positions to set of VCF files
"""

import os
import gzip

snpAnalysisFile = open('/Users/m006703/Index_Swap/files/result/snp_analysis.txt', 'r')
snpAnalysisFile.readline()

positionList = []

for line in snpAnalysisFile:
    line = line.rstrip()
    lineList = line.split('\t')
    chrom = lineList[0]
    position = lineList[1]
    if chrom != 'X':
        positionList.append(position)
        
snpAnalysisFile.close()
 
basedir = '/Users/m006703/Index_Swap/files/'
fileList = os.listdir(basedir)
       
checkDict = {}

for file in fileList:
    filePositionList = []
    fileCheckList = []
    filePath = basedir + file
    sampleName = file.split('_')[0]
    if os.path.isfile(filePath):
        #openFile = gzip.open(filePath, 'rb')
        openFile = open(filePath, 'r')
        print("Processing file: " + filePath)
        # Go to the header line of the VCF results
        #for fileLine in openFile:
            #if fileLine.startswith(b'#CHROM'):
            #if fileLine.startswith('#CHROM'):
                                   #break
        openFile.readline()
        # Collect all the positions in vcf file
        for fileLine in openFile:                            
            fileLine = fileLine.rstrip()
            fileLineList = fileLine.split('\t')
            filePosition = fileLineList[1]
            filePositionList.append(filePosition)
        # Check to see if the positions found in NovaSeq vcfs are in the original vcfs
        for position in positionList:
            if position in filePositionList:
                fileCheckList.append('1')
            else:
                fileCheckList.append('0')
        checkDict[sampleName] = fileCheckList
        openFile.close()

# Create a result directory if it doesn't exist
if not os.path.exists(basedir + 'result/'):
    print("result directory does not exist in " + basedir + ", creating directory...")
    os.makedirs(basedir + 'result/')  
    
checkResultFile = open(basedir + 'result/Position_Check.txt', 'w')
checkResultFile.write('Position')

# Write out the sampne name accross the header
for key in checkDict.keys():
    checkResultFile.write('\t' + key)
checkResultFile.write('\n')

# Write out the contents of each sample's fileCheckList
for index in range(len(positionList)):
    checkResultFile.write(positionList[index])
    for key in checkDict.keys():
        checkResultFile.write('\t' + checkDict[key][index])
    checkResultFile.write('\n')

checkResultFile.close()
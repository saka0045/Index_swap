#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 26 21:16:31 2018

@author: m006703
"""

import os

# Open all of the files created by parse_vcf.py
basedir = '/Users/m006703/Index_Swap/files/'
fileList = os.listdir(basedir)

snpDict = {}
for file in fileList:
    filePath = basedir + file
    sampleName = file.split('_')[0]
    if os.path.isfile(filePath):
        openFile = open(filePath, 'r')
        print("Processing file: " + filePath)
        openFile.readline()
        for line in openFile:
            line = line.rstrip()
            lineList = line.split('\t')
            chrom = lineList[0]
            pos = lineList[1]
            ref = lineList[3]
            alt = lineList[4]
            gnomadFreq = lineList[7]
            coverage = lineList[10]
            if float(gnomadFreq) <= 0.0001:
               if pos not in snpDict:
                   coverageList = []
                   coverageList.append(coverage)
                   sampleNameList = []
                   sampleNameList.append(sampleName)
                   snpDict[pos] = [sampleNameList, coverageList, chrom, ref, alt, gnomadFreq]
               else:
                   snpDict[pos][0].append(sampleName)
                   snpDict[pos][1].append(coverage)
        openFile.close()
        
resultFile = open(basedir + 'result/snp_analysis.txt', 'w')
resultFile.write("CHROM\tPOS\tREF\tALT\tgnomADFrequency\tCoverage\tSample\n")

for (key,val) in snpDict.items():
    if len(snpDict[key][0]) > 1:
        resultFile.write(snpDict[key][2] + '\t' + key + '\t' + snpDict[key][3] + '\t' + snpDict[key][4]\
                         + '\t' + snpDict[key][5] + '\t' + ','.join(snpDict[key][1]) + '\t'\
                         + ','.join(snpDict[key][0]) + '\n')
        
resultFile.close()
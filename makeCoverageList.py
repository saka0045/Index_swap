#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 21 21:12:39 2018

@author: m006703
"""
'''
Script to parse out frequency and coverage created by parse_vcf.py script
Will create 3 files depending on the frequency: 5%, 1% and 0.1%
Assumes that parse_vcf.py fequency cutoff is set at 5%
'''

import os

# Open all of the files created by parse_vcf.py
basedir = '/Users/m006703/Index_Swap/files/'
fileList = os.listdir(basedir)

frequencyList = []
coverageList = []

# Parse out frequency and coverage information from all files
for file in fileList:
    filePath = basedir + file
    print("Processing file: " + filePath)
    openFile = open(filePath, 'r')
    openFile.readline()
    for line in openFile:
        line = line.rstrip()
        frequency = line.split('\t')[7]
        coverage = line.split('\t')[10]
        frequencyList.append(frequency)
        coverageList.append(coverage)
    openFile.close()
        

# Create result directory inside basedir if it doesn't exist
if not os.path.exists(basedir + 'result/'):
    print("result directory does not exist in " + basedir + ", creating directory...")
    os.makedirs(basedir + 'result/')    

# Creating empty files based on the frequency cutoff    
FivePercentCoverageList = open(basedir + 'result/5PercentCoverageList.txt' , 'w')
OnePercentCoverageList = open(basedir + 'result/1PercentCoverageList.txt', 'w')
OneTenthPercentCoverageList = open(basedir + 'result/0.1PercentCoverageList.txt', 'w')
SNPCounter = open(basedir + 'result/SNPCounter.txt', 'w')

# Counting SNPS with certain coverage
FivePercentCounter = 0
OnePercentCounter = 0
OneTenthPercentCounter = 0

for index in range(len(frequencyList)):
    if int(coverageList[index]) >= 100:
        FivePercentCounter += 1
    FivePercentCoverageList.write(frequencyList[index] + '\t' + coverageList[index] + '\n')
    if float(frequencyList[index]) <= 1.0:
        if int(coverageList[index]) >= 100:
            OnePercentCounter += 1
        OnePercentCoverageList.write(frequencyList[index] + '\t' + coverageList[index] + '\n')
        if float(frequencyList[index]) <= 0.1:
            if int(coverageList[index]) >= 100:
                OneTenthPercentCounter += 1
            OneTenthPercentCoverageList.write(frequencyList[index] + '\t' + coverageList[index] + '\n')

SNPCounter.write('SNPs with frequency greater than 5% and coverage greater than 100: ' + str(FivePercentCounter) + '\n'\
                 'SNPs with frequency greater than 1% and coverage greater than 100: ' + str(OnePercentCounter) + '\n'\
                 'SNPs with frequency greater than 0.1% and cverage greater than 100: ' + str(OneTenthPercentCounter) + '\n')

FivePercentCoverageList.close()
OnePercentCoverageList.close()
OneTenthPercentCoverageList.close()
SNPCounter.close()
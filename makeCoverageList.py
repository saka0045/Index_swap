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

basedir = '/Users/m006703/Index_Swap/files/'
fileList = os.listdir(basedir)

frequencyList = []
coverageList = []

for file in fileList:
    filePath = basedir + file
    openFile = open(filePath, 'r')
    openFile.readline()
    for line in openFile:
        line = line.rstrip()
        frequency = line.split('\t')[7]
        coverage = line.split('\t')[10]
        frequencyList.append(frequency)
        coverageList.append(coverage)
    openFile.close()
        
FivePercentCoverageList = open(basedir + '5PercentCoverageList' , 'w')
OnePercentCoverageList = open(basedir + '1PercentCoverageList', 'w')
OneTenthPercentCoverageList = open(basedir + '0.1PercentCoverageList', 'w')

for index in range(len(frequencyList)):
    FivePercentCoverageList.write(frequencyList[index] + '\t' + coverageList[index] + '\n')
    if float(frequencyList[index]) <= 1.0:
        OnePercentCoverageList.write(frequencyList[index] + '\t' + coverageList[index] + '\n')
        if float(frequencyList[index]) <= 0.1:
            OneTenthPercentCoverageList.write(frequencyList[index] + '\t' + coverageList[index] + '\n')
            
FivePercentCoverageList.close()
OnePercentCoverageList.close()
OneTenthPercentCoverageList.close()
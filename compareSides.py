#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 16 10:17:44 2018

@author: m006703
"""


# Change these for other runs
baseFileDir = '/Users/m006703/Index_Swap/HiSeq4000/HNCN5BBXX/result/filtered_sharedVariantCoverage.txt'
compareFileDir = '/Users/m006703/Index_Swap/HiSeq4000/HNFC3BBXX/result/sharedVariantCoverage.txt'

# Open base file and read through the header line
baseFile = open(baseFileDir, 'r')
baseFile.readline()

basePosition = []
baseFreq = []
baseRef = []
baseAlt = []
baseSampleWithCoverage = []
baseSample1Cov = []
baseSample1RCF = []
baseSample2Cov = []
baseSample2RCF = []
baseSample3Cov = []
baseSample3RCF = []
baseSample4Cov = []
baseSample4RCF = []
baseSample5Cov = []
baseSample5RCF = []
baseSample6Cov = []
baseSample6RCF = []

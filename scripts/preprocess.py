#encoding: utf-8
import codecs
import re
import os.path
from indic_transliteration.sanscript import transliterate
import pyexcel as p
from vernacular import vernacular
import datetime
import time
import pandas as pd

def stringify(text):
	return str(text)

def removeAbnormalOrthography(data):
	data = data.replace('फ़', 'फ')
	data = data.replace('ड़', 'ड')
	data = data.replace('देवष्यॉचार्यतर्पण', 'देवर्ष्याचार्यतर्पण') # Sr No 0425
	data = data.replace('निझॅरणव्रतकथा', 'निर्झरणव्रतकथा') # 785
	data = data.replace('पञ्चाशद्वणॅसंचय', 'पञ्चाशद्वर्णसंचय') # 788
	return data


if __name__=="__main__":
	#convertToTsv('../catalogueXlsx/catalogue1v001.xlsx', '../derivedFiles/catalogue1v000.tsv')
	print('Step 1. Converting from xlsx to tsv.')
	data_xls = pd.read_excel('../catalogueXlsx/catalogue1v001.xlsx', 'Sheet1', index_col=None, skiprows=1)
	data_xls.to_csv('../derivedFiles/catalogue1v001.tsv', encoding='utf-8', sep='\t', index=False)
	data_xls = pd.read_excel('../catalogueXlsx/catalogue2v001.xlsx', 'Sheet1', index_col=None, skiprows=1)
	data_xls.to_csv('../derivedFiles/catalogue2v001.tsv', encoding='utf-8', sep='\t', index=False)
	
	print('Step 2. Merging two catalogue files into one')
	# https://stackoverflow.com/questions/13613336/python-concatenate-text-files
	filenames = ['../derivedFiles/catalogue1v001.tsv', '../derivedFiles/catalogue2v001.tsv']
	with codecs.open('../derivedFiles/cataloguev001.tsv', 'w', 'utf-8') as outfile:
		for fname in filenames:
			with codecs.open(fname, 'r', 'utf-8') as infile:
				for line in infile:
					outfile.write(line)
	
	print('Step 3. Remove Abnormal Orthography.')
	data = codecs.open('../derivedFiles/cataloguev001.tsv', 'r', 'utf-8').read()
	data = removeAbnormalOrthography(data)
	data = data.replace('पेपर', 'Paper')
	with codecs.open('../derivedFiles/cataloguev002.tsv', 'w', 'utf-8') as outfile:
		outfile.write(data)
	
	
	with codecs.open('../derivedFiles/cataloguev002.tsv', 'r', 'utf-8') as infile:
		for line in infile:
			print(transliterate(line, 'devanagari', 'slp1'))

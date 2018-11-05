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
import json

def stringify(text):
	return str(text)

def removeAbnormalOrthography(data):
	data = data.replace('फ़', 'फ')
	data = data.replace('ड़', 'ड')
	data = data.replace('देवष्यॉचार्यतर्पण', 'देवर्ष्याचार्यतर्पण') # Sr No 0425
	data = data.replace('निझॅरणव्रतकथा', 'निर्झरणव्रतकथा') # 785
	data = data.replace('पञ्चाशद्वणॅसंचय', 'पञ्चाशद्वर्णसंचय') # 788
	return data


def correctFolioSize(data):
	data = data.replace('´', 'x')
	data = re.sub("[']+", '"', data)
	data = re.sub('["]+', '"', data)
	data = re.sub('[ ]*x[ ]*', 'x', data)
	data = data.lstrip('"')
	return data

def correctCondition(data):
	data = data.replace('उत्तमस्तरीय:', 'Good')
	data = data.replace('उत्तमस्तरीयः', 'Good')
	data = data.replace('उत्तम स्तरीय:', 'Good')
	data = data.replace('उत्तम स्तरीयः', 'Good')
	data = data.replace('मध्यमस्तरीय:', 'Fair')
	data = data.replace('मध्यम स्तरीय:', 'Fair')
	data = data.replace('मध्यमस्तरीयः', 'Fair')
	data = data.replace('मध्यम स्तरीयः', 'Fair')
	data = data.replace('सामान्यस्तरीय:', 'Poor')
	data = data.replace('सामान्य स्तरीय:', 'Poor')
	data = data.replace('सामान्यस्तरीयः', 'Poor')
	data = data.replace('सामान्य स्तरीयः', 'Poor')
	data = data.replace('सामन्यस्तरीयः', 'Poor')
	data = data.replace('अतिPoor', 'Very poor')
	data = data.replace('अति Poor', 'Very poor')
	data = data.replace('अनुचित', 'Not good')
	data = data.replace('Poor क्षतिग्रस्त:', 'Poor, damaged')
	data = data.replace('क्षति ग्रस्त:', 'Good') # There is only one such occurrence 1326, and it is wrongly shown as kshatigrasta.
	data = data.replace('माध्यमस्तरीय:', 'Fair')
	
	return data

def removeH(data):
	data = data.replace(':', '')
	data = data.replace('ः', '')
	return data

def changeSamvat(data):
	data = transliterate(data, 'devanagari', 'itrans')
	data = data.replace('vi.saM.', 'V.S.')
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
	
	
	print('Step 4. Correct the folio size issue.')
	outfile = codecs.open('../derivedFiles/cataloguev003.tsv', 'w', 'utf-8')
	for line in codecs.open('../derivedFiles/cataloguev002.tsv', 'r', 'utf-8'):
		row = line.rstrip().split('\t')
		row1 = row[:7]
		row1.append(correctFolioSize(transliterate(row[7], 'devanagari', 'slp1')))
		row1.append(correctFolioSize(transliterate(row[8], 'devanagari', 'slp1')))
		row1 = row1 + row[9:]
		line = '\t'.join(row1)
		outfile.write(line + '\n')
	outfile.close()
	
	print('Step 4. Change manuscript condition data to English.')
	data = codecs.open('../derivedFiles/cataloguev003.tsv', 'r', 'utf-8').read()
	data = correctCondition(data)
	with codecs.open('../derivedFiles/cataloguev004.tsv', 'w', 'utf-8') as outfile:
		outfile.write(data)
	for line in codecs.open('../derivedFiles/cataloguev004.tsv', 'r', 'utf-8'):
		row = line.split('\t')

	print('Step 5. Remove unnecessary H and : from Title, Author, Commentator, Scribe columns')
	print('Step 6. Convert Sr. No. and Accession No. to Roman alphanumeric')
	print('Step 7. Convert Vikrama Samvat and Shaka samvat.')
	print('Step 8. Convert _ to --')
	outfile = codecs.open('../derivedFiles/cataloguev005.tsv', 'w', 'utf-8')
	for line in codecs.open('../derivedFiles/cataloguev004.tsv', 'r', 'utf-8'):
		row = line.rstrip().split('\t')
		row2 = []
		row2.append(transliterate(row[0], 'devanagari', 'slp1'))
		row2.append(transliterate(row[1], 'devanagari', 'slp1'))
		row2.append(row[2])
		row2.append(removeH(row[3]))
		row2.append(removeH(row[4]))
		row2 = row2 + row[5:12]
		row2.append(removeH(row[12]))
		row2.append(row[13])
		row2.append(changeSamvat(row[14]))
		row2 = row2 + row[15:]
		line = '\t'.join(row2)
		line = line.replace('_', '--')
		outfile.write(line + '\n')
	outfile.close()

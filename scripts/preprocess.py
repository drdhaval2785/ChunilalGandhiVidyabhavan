#encoding: utf-8
import codecs
import re
import os.path
from indic_transliteration.sanscript import transliterate
import pyexcel as p
from vernacular import vernacular
import datetime
import time

def stringify(text):
	return str(text)

def convertToTsv(excelfile, tsvfile):
	rows = p.get_array(file_name=excelfile, start_row=1)
	fout = codecs.open(tsvfile, 'w', 'utf-8')
	for row in rows:
		row1 = [str(item) for item in row]
		fout.write('\t'.join(row1)+'\n')
		"""
		print(row1)
		eng = transliterate(input, 'devanagari', 'optitrans')
		if re.match('[0-9]{4}', eng):
			print(eng)
		else:
			print('ignoring '+eng)
		"""
	fout.close()

if __name__=="__main__":
	# convertToTsv('../catalogueXlsx/catalogue1v003.xlsx', '../derivedFiles/catalogue1v000.tsv')
	
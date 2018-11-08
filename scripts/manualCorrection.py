#encoding: utf-8
import codecs
import re
from indic_transliteration.sanscript import transliterate
from collections import Counter


def repl(matchobject):
	data = transliterate(matchobject.group(0), 'devanagari', 'slp1')
	data = re.sub('M([kKgG])', 'N\g<1>', data)
	data = re.sub('M([cCjJ])', 'Y\g<1>', data)
	data = re.sub('M([wWqQ])', 'R\g<1>', data)
	data = re.sub('M([tTdD])', 'n\g<1>', data)
	data = re.sub('M([pPbB])', 'm\g<1>', data)
	data = transliterate(data, 'slp1', 'devanagari')
	return data
	
def panchama(data):
	result = re.sub('([^\x00-\x7F]+)', repl, data)
	return result
	
	
def correctCommonErrors(data):
	data = panchama(data)
	data = data.replace('वागिश', 'वागीश')
	data = data.replace('न्याय a work on', 'न्यायग्रन्थ')
	data = data.replace('saMvata', 'V.S.')
	return data

	
def prepareDuplicate(filein, fileout):
	fin = codecs.open(filein, 'r', 'utf-8')
	fout = codecs.open(fileout, 'w', 'utf-8')
	for line in fin:
		fout.write(';'+line)
		output = correctCommonErrors(line)
		
		fout.write(correctCommonErrors(line))
	fin.close()
	fout.close()

def findNoChangeLines(filein):
	fin = codecs.open(filein, 'r', 'utf-8')
	inpt = ''
	outpt = ''
	for line in fin:
		if line.startswith(';'):
			inpt = line.lstrip(';')
		else:
			outpt = line
			if inpt == outpt:
				print(inpt.split('\t')[0])
	fin.close()

def findAnusvara(filein):
	fin = codecs.open(filein, 'r', 'utf-8')
	for line in fin:
		if re.search('ं[कखगघचछजझटठडढतथदधपफबभ]', line):
			print(line.split('\t')[0])
	fin.close()

def find_abnormal_accession_no(filein):
	base = [str(item) for item in range(0,1600)]
	accessionList = []
	fin = codecs.open(filein, 'r', 'utf-8')
	for line in fin:
		accessionList.append(line.split('\t')[1])
	print(Counter(accessionList).most_common(50))
	fin.close()
	
if __name__=="__main__":
	input = []
	output = []
	for line in codecs.open('../derivedFiles/manualByLine.txt', 'r', 'utf-8'):
		if line.startswith(';'):
			input.append(line.rstrip().lstrip(';'))
		else:
			output.append(line.rstrip())
	print(len(input))
	print(len(output))

	wholedata = codecs.open('../derivedFiles/cataloguev005.tsv', 'r', 'utf-8').read()

	for x in range(len(input)):
		wholedata = wholedata.replace(input[x], output[x])

	with codecs.open('../derivedFiles/cataloguev006.tsv', 'w', 'utf-8') as fout:
		fout.write(wholedata)

	#prepareDuplicate('../derivedFiles/cataloguev005.tsv','../derivedFiles/manua.txt')
	#print('Duplicate lines in ../derivedFiles/manualByLine.txt')
	#findNoChangeLines('../derivedFiles/manualByLine.txt')


	# The next lines of code are for identifying potential errors in the dataset. Not directly releated to manual correction per se.
	# Find out lines which still have anusvara instead of vargapanchama.
	# findAnusvara('../derivedFiles/cataloguev006.tsv')
	find_abnormal_accession_no('../derivedFiles/cataloguev006.tsv')

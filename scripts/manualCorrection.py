#encoding: utf-8
import codecs
import re


def prepareDuplicate(filein, fileout):
	fin = codecs.open(filein, 'r', 'utf-8')
	fout = codecs.open(fileout, 'w', 'utf-8')
	for line in fin:
		fout.write(';'+line)
		fout.write(line)
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

	# prepareDuplicate('../derivedFiles/cataloguev005.tsv','../derivedFiles/manua.txt')
	findNoChangeLines('../derivedFiles/manualByLine.txt')
	
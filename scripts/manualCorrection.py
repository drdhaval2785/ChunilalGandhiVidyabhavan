#encoding: utf-8
import codecs
import re

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

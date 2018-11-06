from indic_transliteration.sanscript import transliterate
import sys

def vernacular(text):
	text = text.replace('M','n')
	text = text.replace('RRi','ri')
	text = text.replace('LLi','lri')
	text = text.replace('~N','n')
	text = text.replace('j~n','gy')
	text = text.replace('~n','n')
	text = text.replace('x', 'ksh')
	text = text.lower()
	return text

if __name__=="__main__":
	input = sys.argv[1]
	itrans = transliterate(input, 'slp1', 'itrans')
	verna = vernacular(itrans)
	print(itrans)
	print(verna)
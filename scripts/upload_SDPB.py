#encoding: utf-8
import codecs
import re
import os.path
from indic_transliteration import sanscript
from indic_transliteration.sanscript import SchemeMap, SCHEMES, transliterate
from vernacular import vernacular
from internetarchive import get_item, upload, modify_metadata
import datetime
import time
import json
import glob
import sys

	
# Convert the text into various transliteration schemes.
def trans(text, inputScheme=sanscript.DEVANAGARI):
	hk = transliterate(text, inputScheme, sanscript.HK)
	slp1 = transliterate(text, inputScheme, sanscript.SLP1)
	itrans = transliterate(text, inputScheme, sanscript.ITRANS)
	iast = transliterate(text, inputScheme, sanscript.IAST)
	kolkata = transliterate(text, inputScheme, sanscript.KOLKATA)
	velthuis = transliterate(text, inputScheme, sanscript.VELTHUIS)
	bengali = transliterate(text, inputScheme, sanscript.BENGALI)
	devanagari = transliterate(text, inputScheme, sanscript.DEVANAGARI)
	gujarati = transliterate(text, inputScheme, sanscript.GUJARATI)
	gurmukhi = transliterate(text, inputScheme, sanscript.GURMUKHI)
	kannada = transliterate(text, inputScheme, sanscript.KANNADA)
	malayalam = transliterate(text, inputScheme, sanscript.MALAYALAM)
	oriya = transliterate(text, inputScheme, sanscript.ORIYA)
	tamil = transliterate(text, inputScheme, sanscript.TAMIL)
	telugu = transliterate(text, inputScheme, sanscript.TELUGU)
	optitrans = transliterate(text, inputScheme, sanscript.OPTITRANS)
	keyword = vernacular(itrans)
	
	return {'devanagari':devanagari, 'hk':hk, 'slp1':slp1, 'itrans':itrans, 'iast':iast, 'kolkata':kolkata, 'velthuis':velthuis, 'optitrans':optitrans,
	'bengali':bengali, 'gujarati':gujarati, 'kannada':kannada, 'malayalam':malayalam, 'oriya':oriya, 'tamil':tamil, 'telugu':telugu, 'keyword':keyword}

# Createa a metadata dict from each line of Catalogue. Catalogue has total 16 fields. They are read into dict details, and further processed. 68 entries produced to upload to archive.org.
def find_metadata1(line):
	details = line.rstrip('\r\n').split('\t')
	metadata = {}
	if not len(details) == 15:
		print(details[0] + ' does not have 15 fields. Please check.')
	# Get metadata from CSV
	metadata['Accession_No'] = details[0]
	metadata['Subject'] = details[1]
	# Convert title to various transliterations
	for (key, item) in trans(details[2]).items():
		metadata['Title_'+key] = item
	# Convert author to various transliterations
	for (key, item) in trans(details[3]).items():
		metadata['Author_'+key] = item
	# Convert scribe to various transliterations
	for (key, item) in trans(details[4]).items():
		metadata['Scribe_'+key] = item
	metadata['Date_of_work'] = details[5]
	metadata['Date_of_MS'] = details[6]
	metadata['Place_of_work'] = details[7]
	metadata['Place_of_MS'] = details[8]
	metadata['Size'] = details[9]
	metadata['Folios'] = details[10]
	metadata['Script'] = details[12]
	metadata['Additional_remarks'] = details[13]
	metadata['Observations'] = details[14]
	
	# Prepare mandatory metadata for Archive.org.
	titlekey = str(metadata['Title_keyword'])
	titlekey = re.sub('[^a-zA-Z0-9_. -]', ' ', titlekey) # See issue 12.
	titlekey = re.sub('[ ]+', '_', titlekey)
	titlekey = re.sub('^[_.-]+', '', titlekey) # See issue 13.
	acc = metadata['Accession_No']
	acc = re.sub('^SDPB', '', acc)
	identifier = titlekey+'-CGV-SDPB-'+acc
	identifier = re.sub('[^a-zA-Z0-9_. -]', '_', identifier)
	metadata['identifier'] = identifier
	metadata['mediatype'] = 'texts'
	metadata['collection'] = 'opensource'
	metadata['creator'] = 'Chunilal Gandhi Vidyabhavan Surat'
	metadata['description'] = 'Shastri Dinamanishankara Pustaka Bhandara (SDPB) collection of manuscripts of Chunilal Gandhi Vidyabhavan, Surat.'
	metadata['language'] = 'san'
	metadata['email'] = 'cgvidyabhavan@gmail.com'
	return metadata


def uploadToArchive1(metadata):
	identifier = metadata['identifier']
	flog = codecs.open('../logs/uploadLog1.txt', 'a', 'utf-8')
	if len(identifier) > 100:
		print('File name too long: ' + identifier)
		flog.write('File name too long: ' + identifier + '\n----------\n')
	else:
		accession = metadata['Accession_No']
		acc = re.sub('^SDPB', '', accession)
		acc = re.sub('([ABCDEFGHI])$', '-\g<1>', acc)
		startMessage = accession+'#'+identifier+'\n'+'Started at '+str(datetime.datetime.now())
		print(startMessage)
		flog.write(startMessage+'\n')
		r = upload(identifier, {identifier+'.pdf': '../../ChunilalGandhiMSS/compressedPdfFiles/S.D.P.B._NO.'+acc+'.pdf'}, metadata=metadata)
		endMessage=str(r[0].status_code)+'\n'+'Ended at '+str(datetime.datetime.now())+'\n----------\n'
		print(endMessage)
		flog.write(endMessage)
		flog.close()
	
def createMetadataJson1():
	fin = codecs.open('../derivedFiles/SDPBv001.tsv', 'r', 'utf-8')
	#fin = codecs.open('../derivedFiles/new4.tsv', 'r', 'utf-8')
	ferror = codecs.open('../logs/error1.txt', 'a', 'utf-8')
	print('Files not found')
	for line in fin:
		metadata = find_metadata1(line)
		identifier = metadata['identifier']
		accession = metadata['Accession_No']
		accession = re.sub('([ABCDEFGHI])$','-\g<1>',accession)
		fullaccession = accession.replace('SDPB','S.D.P.B._No.')
		if not os.path.isfile('../../ChunilalGandhiMSS/compressedPdfFiles/'+fullaccession+'.pdf'):
			ferror.write('File Not Found:'+accession+'\n')
			print(fullaccession)
		else:
			with codecs.open('../metadataJson/'+accession+'.json', 'w', 'utf-8') as fjson:
				json.dump(metadata, fjson)
				#print('Metadata generated for:'+accession)

	fin.close()
	ferror.close()


if __name__=="__main__":
	if len(sys.argv) > 1:
		createMetadataJson1()

	accessionsToBeUploaded = '../derivedFiles/uploadstack1.txt'
	for line in codecs.open(accessionsToBeUploaded, 'r', 'utf-8'):
		accession = line.rstrip()
		accession = re.sub('([ABCDEFGHI])$','-\g<1>',accession)
		if os.path.isfile('../metadataJson/'+accession+'.json'):
			metadata = json.load(codecs.open('../metadataJson/'+accession+'.json', 'r', 'utf-8'))
			uploadToArchive1(metadata)
		else:
			print('FILE NOT FOUND: '+accession)

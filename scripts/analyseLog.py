import codecs
import os

class EntryRack(object):
	def __init__(self, line):
		line = line.rstrip()
		items = line.split('\t')
		self.SrNo = items[0]
		self.accNo = items[1]

def findAbnormal(uploadLog):
	flog = codecs.open(uploadLog, 'r', 'utf-8')
	logdata = flog.read()
	logSectors = logdata.split('\n----------\n')
	for sector in logSectors:
		parts = sector.split('\n')
		print(len(parts))
	flog.close()

def prepareCheckList(catalogueTsv, uploadLog):
	fcat = codecs.open(catalogueTsv, 'r', 'utf-8')
	lines = fcat.readlines()
	entries = [EntryRack(line) for line in lines]
	flog = codecs.open(uploadLog, 'r', 'utf-8')
	

def scanToPdfLoss(scannedFolder, pdfFolder):
	scanList = os.listdir(scannedFolder)
	#print(scanList)
	pdfList = os.listdir(pdfFolder)
	pdfList = [item.rstrip('.pdf') for item in pdfList]
	pdfSet = set(pdfList)
	for scanFile in scanList:
		if scanFile not in pdfSet:
			print(scanFile)
	
if __name__=="__main__":
	#findAbnormal('../logs/uploadlog.txt')
	scanToPdfLoss('../../ChunilalGandhiMSS/scannedBooks','../../ChunilalGandhiMSS/compressedPdfFiles')
	
import codecs

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
	
	
if __name__=="__main__":
	findAbnormal('../logs/uploadlog.txt')
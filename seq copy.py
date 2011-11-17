"""
A set of functions for finding, analyzing and saving sequenctial dependencies
given a 2d column oriented array or list.
"""

def seq(data,col=None,header=True):
	"""
	Given a column oriented 2d array or list, with or without a header,
	and an named or enumerated sequence column, this script re-sorts 
	the data based on first and second order sequential effects.  
	
	Excepting 'col', data in all columns is maintained, if that is not desirable filter 
	the data prior to use.  

	Returns:
		- 'seqDict', a dictionary keyed on the sequences, values are a 2d array; 
			each row is an entry.  The incoming data's header is in header.
			If there wasn't a header there is now.	
	"""

	import numpy as np

	data = np.asarray(data)
	seqDict = dict()

	if header:
		seqDict['header'] = data[0,].tolist()
		n_1 = data[1,]
		n_2 = data[2,]
		seq = data[3:,head.index(col)]
	else:
		seqDict['header'] = np.arange(data.shape[1])
			# create a simple index as the header
		n_1 = data[0,]
		n_2 = data[1,]
		seq = data[2:,col]


	for ii, n in enumerate(seq):
		row = data[ii,]
		oneBack = n_1 + '_' + n
		twoBack = n_2 + '_' + n_1 + '_' + n

		## Add to bottom of keyed array if key
		## exists, otherwise init w/ row
		if seqDict.has_key(oneBack):
			seqDict[oneBack] = np.vstack(seqDict[oneBack],row) 
		else
			seqDict[oneBack] = row 

		if seqDict.has_key(twoBack):
			seqDict[twoBack] = np.vstack(seqDict[twoBack],row)
		else
			seqDict[twoBack] = row

	return seqDict



def seqStats(seqDict,cols=None):
	"""
	For each key in seqDict (created with seq(), above) this script 
	calculates statistics for each of the specified cols.  
	
	Cols can be numbers or names. Counterintuitivly, if cols is None 
	all columns are used.
	
	The calculated stats are (in order):
		N, mean, sd

	Returns:
		- A 2d char array, rows are stats as described above,
		except column 1 is the key and column 2 if a statistics label
	"""
	import numpy as np
	
	head = seqDict['header']
	colsIndex = []
	[colsIndex.append(head.index(ele)) for ele in cols]  # filter head
	stats = array(('stat','seq',head[colsIndex]))
		# init stats with the filtered header

	for key in seqDict:
		if key is 'header': 
			continue
		
		data = seqDict[key]
		data = data[1:,]
		filtered = data[,colsIndex]

		## calc stats
		N = np.hstack((key,'N',array(filtered.shape[0] * filtered.shape[1])))
		mean = np.hstack((key,'mean',filtered.mean(0)))
		std = np.hstack((key,'std',filtered.std(0)))
		stats = np.vstack(stats,N,mean,std)

	return stats

def writeSeqDict(seqDict,name=''):
	"""
	Writes the contents of seqDict to a tsv text file;
	row data is the values of seqDict, except column 1 is the sequence
	label.

	'name' is the name of the file to be written; silently
	overwrites existing files.
	"""
	import numpy as np
	import string as sr

	f = open(name, mode='w')
	
	## write the header first
	head = seqDict['header']
	head.astype('c')
	head.tolist()
	head.insert(0,'seq')
	head = sr.join(head,sep="\t")
	f.write(head)

	## now the data
	for key in seqDict:
		data = seqDict[key]
		data = np.hstack(np.array([key]*data.shape(0)),data)
			## Add a seq label column
		data.tofile(f,sep="\t",format="%s")

	f.close()

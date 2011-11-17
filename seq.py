"""
A set of functions for finding, analyzing and saving sequenctial dependencies
given a 2d column oriented array or list.
"""

def seq(data,sequence_col_num=1,header=True):
	"""
	The data in data, a 2d column oriented array, is resorted 
	based on the sequential dependencies found in sequence_col_num.  
	When true the header is dropped. 

	A dict, whose values are 2d arrays, keyed on underscore joined names 
	of the conditions found in sequence_col_num is returned.
	"""
	import numpy as np
	from string import join
	from collections import defaultdict

	data = np.array(data)
	if header:
		data = data[1:,...]
			# Drop the header

	## For each row in data, setup the names 
	## for this iteration,
	## then append the current row to each.
	seq_dict = defaultdict(list)
	for ii in range(2,data.shape[1]):
		n = data[ii,sequence_col_num]
		n_minus_1 = data[ii-1,sequence_col_num]
		n_minus_2 = data[ii-2,sequence_col_num]
		
		seq_dict[n].append(data[ii,:])
		seq_dict[join((n_minus_1,n),'_')].append(data[ii,:])
		seq_dict[join((n_minus_2,n_minus_1,n),'_')].append(data[ii,:])

	## Convert from lists to arrays
	for key in seq_dict:
		seq_dict[key] = np.array(seq_dict[key])

	return seq_dict


def seq_descriptive_stats(seq_dict,col_numbers):
	"""
	Returns a dict containing the N, M, SD for each key whose
	value (a 2d array) matches [col_numbers].
	"""
	import numpy as np
	
	stat_dict = {}
	for key,data in seq_dict.items():
		stat_dict['N_'+key] = data.shape(0)
		stat_dict['M_'+key] = data.mean(0)[col_numbers]
		stat_dict['SD_'+key] = data.std(0)[col_numbers]
		
	return stat_dict


def write_seq_dict(seq_dict,col_numbers,f_name=''):
	"""
	Write out the contents of seq_dict into a column oriented tsv table.
	Column 0 is the repeated key (now a factor).  Formating is desgined
	for maximized compatibility with R-style data.frames.
	"""
	import numpy as np
	import string as sr

	f = open(name, mode='w+')
	
	for key in seq_dict:
		data = seq_dict[key]
		data = np.hstack(
				np.array([key,]*data.shape(0)),data[:,col_numbers])
					# Add a seq label column
		data.tofile(f,sep="\t",format="%s")

	f.close()

#!/usr/bin/python
"""
This code is a collaborative effort with Sevtap Duman Northeastern University, systems security lab.
"""
import os
import pandas as pd
import sys
import collections
from Bio import AlignIO
import Bio.Align
dir = os.path.dirname(__file__)
print os.getcwd()
print dir

alndata = []
#sys.argv[1] -> Alignment File
#sys.argv[2] -> type of virus

if len(sys.argv) < 3:
	print "Please provide required arguments in proper order:"
	print "MSA_parser_cleaner.py AlignmentFile TypeOfEBV [RepeatFilter]"
	sys.exit(1)

Ref=''
#Make sure that repeat files are in the same directory
if sys.argv[2] == '1':
	Ref='NC_007605'
	Repeat_inputFile = '%(directory)s/../resources/Annotation/Type1/NC_007605_miropeat_default_run_repeats.bed' %{"directory":dir}

else:
	Ref='NC_009334'
	Repeat_inputFile = '%(directory)s/../resources/Annotation/Type2/NC_009334_miropeat_default_run_repeats.bed' %{"directory":dir}

if sys.argv[3] == "RepeatFilter":

#Find the genomic locations fall into miropeats repeat regions
	RepeatList = []
	with open(Repeat_inputFile) as repeatFile:
		for line in repeatFile:
			repstart = int(line.strip().split("\t")[1])
			repend = int(line.strip().split("\t")[2])
			for i in range(repstart,repend):
				RepeatList.append(i)
	RepeatList = set(RepeatList)
	print len(set(RepeatList))
else:
	RepeatList = []
	pass


compare = lambda x, y: collections.Counter(x) == collections.Counter(y)

alignment = AlignIO.read(open(sys.argv[1]), "fasta")
print("Alignment length %i" % alignment.get_alignment_length())
for record in alignment :
#    print(record.seq + " " + record.id)
    print(record.id), record.seq.count('-'), record.seq.count('n')

#good alignment positions = gap
gap = []
#bad alignment positions = bap
bap = []

edited = alignment[:,1:2]
print edited


Ref_pos = 0
for record in alignment:
	if record.id == Ref:
		for i in range(len(record.seq)):
			if record.seq[i] == '-':
				Ref_pos = Ref_pos
			else:
				Ref_pos = Ref_pos + 1
			if Ref_pos not in RepeatList:
				gap.append(i)
			else:
				bap.append(i)
print "GAP:", len(gap), "BAP:", len(bap)

for i in range(alignment.get_alignment_length()):

	#alignment Position Base Composition = apbc
	apbc = []

	for record in alignment:
		apbc.append(record.seq[i])

	if compare(set(apbc), set(['-','n']) ) or compare(set(apbc), set(['-']) ) or compare(set(apbc), set(['n']) ) or (i in set(bap)):
#		print record.seq[i], record.id, set(apbc)
		pass
	else:
		edited = edited + alignment[:,i:i+1]


edited = edited[:,1:]
print edited

#>>> align.add_sequence("Gamma", "ACTGCTAGATAG")

AlignIO.write(edited, "my_edited_"+sys.argv[1], "fasta")

print len(bap)
print len(gap)
#outfile1 = open(sys.argv[1]+sys.argv[2]+"_Mismatch_error_positions.bed","w")
#outfile2 = open(sys.argv[1]+sys.argv[2]+"_Mismatch_error_rates.txt","w")





#outfile1.close()
#outfile2.close()

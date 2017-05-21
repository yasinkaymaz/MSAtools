#!/usr/bin/python

import os
import pandas  as pd
import sys

alndata = []

#sys.argv[1] -> sample 1
#sys.argv[2] -> sample 2
#sys.argv[3] -> type of virus

Ref=''

if sys.argv[3] == '1':
	Ref='NC_007605'
else:
	Ref='NC_009334'

#Find the genomic locations fall into miropeats repeat regions
RepeatList = []
with open("/home/yasinkaymaz/EBV/NC_007605_miropeat_default_run_repeats.bed") as repeatFile:
	for line in repeatFile:
		repstart = int(line.strip().split("\t")[1])
		repend = int(line.strip().split("\t")[2])
		for i in range(repstart,repend):
			RepeatList.append(i)
print len(set(RepeatList))



with open("AmplificationTest.aln", "r") as alnfile:
    df = pd.read_csv(alnfile,sep="\t",header=None)

    dfseq = []
    # take the names of sequences to index 
    index = df[0]
    
    str_seq1 = df.ix[1][1]
    print "len : " +  str(len(str_seq1))
    # create an empty list of length of sequence letters 
    columns = list(range(len(str_seq1)))

    #new data frame 
    new_df = pd.DataFrame(index=index, columns= columns)
    #print new_df

    #create new dataframe
    for i in range(len(df)):
        # change a string of sequence to a list of sequence
        dfseq = list(df.ix[i][1])
        # You can edit a subset of a dataframe by using loc:
        # df.loc[<row selection>, <column selection>]
        
        # place the list of sequence to the row that it belongs to in the new data frame
        new_df.loc[i:,:] = dfseq

    # for each row: 
    Ref_pos =0
    MatchCount=0
    for i in range(len(str_seq1)):
        # place the the sequence in a position to a set
        set_seq = set(new_df.loc[:,i])

	if new_df.loc[Ref,i] != '-':
		Ref_pos = Ref_pos +1
	else:
		pass

	set_pair = set(new_df.loc[ [sys.argv[1],sys.argv[2] ],i  ])



        if 'n' in set_pair or '-' in set_pair:
		pass
	elif len(set_pair)>1 and Ref_pos not in RepeatList:
		print set_pair, Ref_pos
	elif len(set_pair) == 1 and Ref_pos not in RepeatList:
		MatchCount = MatchCount +1

print "Match Count:", MatchCount


        # if the set has n or - pass it
#        if 'n' in set_seq or '-' in set_seq:
#            pass
        
#        else:
            # if the set has more than 1 letters than learn which row has which one
 #           if(len(set_seq) > 1):
  #              print new_df.loc[:,i], NC_1_pos, NC_2_pos


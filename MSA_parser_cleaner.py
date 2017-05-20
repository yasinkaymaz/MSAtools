/usr/bin/python

import os
import pandas  as pd

alndata = []

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
    for i in range(len(str_seq1)):
        # place the the sequence in a position to a set
        set_seq = set(new_df.loc[:,i])
        # if the set has n or - pass it
        if 'n' in set_seq or '-' in set_seq:
            pass
        
        else:
            # if the set has more than 2 letters than learn which row has which one
            if(len(set_seq) > 1):
                print new_df.loc[:,i]





                                #dfseq= df[1]
                                #df[1] = df[1].to_string()
                                #print df[1]


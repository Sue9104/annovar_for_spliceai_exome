import pandas as pd
import re
import os
import argparse
parser = argparse.ArgumentParser( description='Convert SpliceAI VCF to ANNOVAR DB File')
parser.add_argument( 'infile', type=str, help='input  file')
parser.add_argument( 'outfile', type=str, help='output file')
args = parser.parse_args()


spliceai_columns = [
    "SYMBOL", "STRAND", "TYPE", "DIST",
    "DS_AG", "DS_AL", "DS_DG", "DS_DL",
    "DP_AG", "DP_AL", "DP_DG", "DP_DL"
]

# deal in chunk for big data
columns = ["#Chr","Start","Ref","Alt","INFO"]
data_chunks = pd.read_table(
    args.infile, comment="#", chunksize=1000000,
    usecols=[0,1,3,4,7], names=columns
)

# since writing mode is a, delete outfile first if exists
if os.path.exists(args.outfile):
    os.remove(args.outfile)
# deal with big file in chunk
header = True
for chunk in data_chunks:
    chunk["End"] = chunk["Start"]
    for column in spliceai_columns:
        chunk[column] = chunk["INFO"].apply(
            lambda x: re.search(
                '{}=(?P<text>.*?)(;|$)'.format(column),
                x
            ).group('text')
        )
    chunk.drop( columns = ["INFO"], inplace = True)
    chunk = chunk[ ["#Chr","Start","End","Ref","Alt"] + spliceai_columns ]
    chunk.rename(
        columns = { column: 'SpliceAI_' + column for column in spliceai_columns},
        inplace = True
    )
    chunk.to_csv(
        args.outfile, sep = '\t', 
        index = False, header = header, mode = 'a'
    )
    header = False



import re
from glob import glob
import os

#DESCRIPTION: This File reads the cacm.query.txt file and cleans it the way it
#             cleaned corpus and produces the output in cacm.query.clean.txt


#Global Constants
inpfile = "cacm.query.txt"
outfile = "cacm.query.clean.txt"
#:-
def clean_query():
        f1 = open(inpfile, 'r')
        of = open(outfile, 'w')
        items= f1.read()
        items = items.split("</DOC>")
        count=0
        for i in items:
            items[count] =i [i.find("<DOC>")+len("<DOC>") :]
            count+=1

        for i in items:
            try:
                s=i.index("<DOCNO> ")+len("<DOCNO> ")
                e=i.index(" </DOCNO>",s)
                key = i[s:e]
            except ValueError:
                key=""
            j = re.sub( r'<DOCNO>.*</DOCNO>', "", i)
            val = j.replace("\n", " ")

            val = re.compile('[_!@\s#$%=+~()}{\][^?&*;,.\\/|<>"\']').sub(' ',val)
            val = val.encode("utf-8")
            val = val.lower()
            val = val.split()
            val = " ".join(val)
            
            of.write(str(key)+"\t"+str(val)+"\n")

        of.close()

###########################################################

if __name__ == "__main__":
    clean_query()


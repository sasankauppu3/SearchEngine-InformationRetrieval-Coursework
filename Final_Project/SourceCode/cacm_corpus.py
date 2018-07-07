import re
from glob import glob
import os

#DESCRIPTION: This File reads the cacm file directory and generates a cleaned corpus

#Global Constants
InputFolder = os.path.join(os.getcwd(),'cacm')
OutputFolder = os.path.join(os.getcwd(),'corpus')
#:-
def generate_corpus():
    for file in glob(os.path.join(InputFolder,'*.html')):
        f1 = open(file, 'r')

        curfile=""
        for l in f1.readlines():
            l = l.lower()
            
            l=l.replace("<html>","")
            l=l.replace("</html>","")
            l=l.replace("<pre>","")
            l=l.replace("</pre>","")
            
            #handling special chars
            l = re.compile('[_!@\s#$%=+~()}{\][^?&*;,.\\/|<>"\']').sub(' ',l)

            l = l.encode("utf-8")
            l = l.split()
            l = " ".join(l)
            if l=="":
                continue
            curfile += l + "\n"
            if l[-3:]==" pm" or l[-3:]==" am":
                break
            
        #writing to output file
        o_file  = open(OutputFolder+"/"+file.replace(InputFolder,'')[1:6]+str(int(file.replace(InputFolder,'')[6:-5]))+".txt",'w')
        o_file.write(curfile)
        o_file.close()

###########################################################

if __name__ == "__main__":
    generate_corpus()


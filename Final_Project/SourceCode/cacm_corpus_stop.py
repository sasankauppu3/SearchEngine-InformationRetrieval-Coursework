import re
from glob import glob
import os

#DESCRIPTION: This File reads the cacm file directory and generates a cleaned corpus
#             of stopped documents

#Global Constants
InputFolder = os.path.join(os.getcwd(),'cacm')
OutputFolder = os.path.join(os.getcwd(),'corpus_stopped')
#:-

#Function to get stop words from the file
def stopwords_loader():
    stopList=[]
    f = open(os.getcwd()+"/common_words",'r')
    for line in f.readlines():
        stopList.append(line.lower().replace("\n",""))
    f.close()
    return stopList

def generate_corpus():
    stop=stopwords_loader()
    for file in glob(os.path.join(InputFolder,'*.html')):
        f1 = open(file, 'r')
        
        curfile=""
        fl=0
        for l in f1.readlines():
            l = l.lower()
            l=" ".join(l.split())
            if l[-3:]==" pm" or l[-3:]==" am":
                fl=1
            l=l.replace("<html>","")
            l=l.replace("</html>","")
            l=l.replace("<pre>","")
            l=l.replace("</pre>","")
            
            #handling special chars
            l = re.compile('[_!@\s#$%=+~()}{\][^?&*;,.\\/|<>"\']').sub(' ',l)

            l = l.encode("utf-8")
            l = l.split()
            newl=[]
            for i in l:
                if i not in stop:
                    newl.append(i)
            l = " ".join(newl)
            if l=="":
                continue
            curfile += l + "\n"

            if fl==1:
                break
            
        #writing to output file
        o_file  = open(OutputFolder+"/"+file.replace(InputFolder,'')[1:6]+str(int(file.replace(InputFolder,'')[6:-5]))+".txt",'w')
        o_file.write(curfile)
        o_file.close()

###########################################################

if __name__ == "__main__":
    generate_corpus()


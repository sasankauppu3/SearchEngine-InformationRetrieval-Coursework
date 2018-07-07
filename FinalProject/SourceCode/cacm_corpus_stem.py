import re
import os

#DESCRIPTION: This File reads the cacm_stem.txt file and generates a corpus
#             of stemmed documents

#enter the folder where the stemmed file needs to be created needs to be created
writefile=os.getcwd()+"/corpus_stemmed/"

#enter the path of the stemmed corpus
stemfile = "cacm_stem.txt"
file=open(stemfile)

#file name and the details of the file
filedetails={}
stringl=""

def clean(l):
    if re.search('[a-zA-Z]', l)==None:
        return ""

    l=l.replace("<html>","")
    l=l.replace("</html>","")
    l=l.replace("<pre>","")
    l=l.replace("</pre>","")

    l = re.compile('[_!@\s#$%=+~()}{\][^?&*;,.\\/|<>"\']').sub(' ',l)
    l = l.encode("utf-8")
    l = l.lower()
    l = l.split()
    l = " ".join(l)
    
    return l

#read the stem file 
for l in file.readlines():
    if "pm " in l and l.index("pm ")==0:
        l="pm"
    elif "am " in l and l.index("am ")==0:
        l="am"
    elif len(l.split(' pm ')) == 2:
        l=l.split(' pm ')[0]+' pm'
    elif len(l.split(' am ')) == 2:
        l=l.split(' am ')[0]+' am'
    context=[x for x in l.split()]
    le=context
    if ('#' in context) and (len(context)==2):
        if stringl!="":
            filedetails.update({filename:stringl})
        filename="CACM-"+str(le[1])+".txt"
        stringl=""
    else:
        
        stringl=stringl+clean(l)
        stringl=stringl+"\n"
        
filedetails.update({filename:stringl})
#write to a flight
def write_file():
    for keys in filedetails.iterkeys():
        f=open(writefile+keys,"w+")
        f.write(filedetails[keys])
        f.close()


write_file()



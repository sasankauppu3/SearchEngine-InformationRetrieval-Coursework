from glob import glob
import operator
import os
import json

#Global Constants
InputFolder = path = os.path.join(os.getcwd(),'corpus')
 
def main():
    docidmap={}
    Unigram_inverted_index = {}     #Inverted Index for Unigrams 
    counter=1
    for file in glob(os.path.join(InputFolder,'*.txt')):
        doc=open(file, 'r').read()
        docId=counter
        terms = doc.split()
        docidmap[docId]=os.path.basename(file)[:-4]
        for i in range(len(terms)):

            #Unigram
            term=terms[i]
            if not Unigram_inverted_index.has_key(term):
                doc_term_freq={docId:1}
                Unigram_inverted_index[term]=doc_term_freq
            elif not Unigram_inverted_index[term].has_key(docId):
                Unigram_inverted_index[term][docId]=1
            else:
                Unigram_inverted_index[term][docId]+=1

        counter+=1

    f=open('docidmap.txt','w')
    for k,v in docidmap.items():
        f.write(str(k))
        f.write("\t")
        f.write(v)
        f.write("\n")
    index_to_file(Unigram_inverted_index,1)


#Common function to write an inverted index to a file
def index_to_file(inv_index, grams):
    df={} #document frequency
    
    for term in inv_index:
        frequency=0
        docList=[]
        for docId in inv_index[term].keys():
            docList.append(docId)
            frequency += inv_index[term][docId]
        df.update({term:docList})

    
    #writing document frequency
    df = sorted(df.items(),key=operator.itemgetter(0))
    o_file = open("unigram-indexer.txt",'w')
    for item in df:
        o_file.write(str(item[0])+"\t"+','.join(map(str,item[1]))+"\t"+str(len(item[1]))+"\n")
    o_file.close()



###########################################################

if __name__ == "__main__":
    main()

import os
from math import log
from glob import glob

#DESCRIPTION: This File is used to run the TfIdf Algorithm on a stemmed corpus 
#             as well as query. The output is present in TfIdf-Stem-Output.txt

#Global Constants
os.chdir("..")
os.chdir("..")
InputFolder = os.path.join(os.getcwd(),'corpus_stemmed')

#Function to load unigram inverted index
def unigramloader():
    Unigram_inverted_index = {}
    docWC={}
    for file in glob(os.path.join(InputFolder,'*.txt')):
        doc=open(file, 'r')
        docId=os.path.basename(file)
        docWC[docId]=0
        for terms in doc.readlines():
            terms=terms.split()
            for i in range(len(terms)):
                if terms[i]=='':
                    continue
                docWC[docId]+=1
                term=terms[i]
                if not Unigram_inverted_index.has_key(term):
                    doc_term_freq={docId:1}
                    Unigram_inverted_index[term]=doc_term_freq
                elif not Unigram_inverted_index[term].has_key(docId):
                    Unigram_inverted_index[term][docId]=1
                else:
                    Unigram_inverted_index[term][docId]+=1
    return (Unigram_inverted_index,docWC)

#Function to load queries from the query input file
def queryloader():
    f = open(os.getcwd()+'/cacm_stem.query.txt','r')
    queries=[]
    for line in f.readlines():
        q=line.lower()
        if q!="":
            queries.append(q)
    return queries

#Function to run TfIdf for a given query on whole corpus and store results in a dict
def tfidf(uni_index,N,query):
    result = {}

    #Calculating Query wordcounts
    wc = {}
    for q in query:
        if q not in wc:
            wc[q] = 1
        else:
            wc[q] += 1
            
    docL = {}
    for term in wc:
        docL = {}
        if term in uni_index:
            docL = uni_index[term]
            #calculating idf for every term
            idf = log(N, 10) - log(len(docL), 10)
            for d in docL:
                x = (1.0 + log(docL[d], 10)) * idf
                if d not in result:
                    result[d] = x
                else:
                    result[d] += x
    return result


def main():
    queries = queryloader()
    uni_index,docWC=unigramloader()
    N = len(docWC)
    
    results={}
    for qid in range(0, len(queries)):  #Running TfIdf on each query
        results[qid] = tfidf(uni_index,N,queries[qid].split())

    #Obtaining the top 100 results for every query
    topresults={}
    os.chdir("Phase1/task3")
    f = open("TfIdf-Stem-Output.txt", "w")
    for r in results:
        topresults = results[r]
        rank = 1
        for i in sorted(topresults, key=topresults.get, reverse=True)[:100]:
            f.write(str(r+1) + " Q0 " + str(i)[:-4] + " " + str(rank) + " " + str(topresults[i]) + " TfIdf-Stem-JSY" + "\n")
            rank+=1
    f.close()

###########################################################
    
if __name__ == "__main__":
    main()

import os
from math import log
from glob import glob

#DESCRIPTION: This File is used to run the BM25 Algorithm on a stemmed corpus 
#             as well as query. The output is present in BM25Stem-Output.txt

#Global Constants
os.chdir("..")
os.chdir("..")
InputFolder = os.path.join(os.getcwd(),'corpus_stemmed')
k1 = 1.2
k2 = 100
b = 0.75

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

#Function to load the relevant documents for every query
def relevance_loader():
    relevant={}
    f=open(os.getcwd()+"/cacm.rel",'r')
    for line in f.readlines():
        w = line.split()
        if w[0] not in relevant:
            relevant[w[0]] = [w[2]]
        else:
            relevant[w[0]].append(w[2])
    f.close()
    return relevant

#Function to calculate the matheatical BM25 score given the input params 
def bm25score(n, f, qf, r, R, N, dl, avgdl):
    K = k1 * ((1-b) + b * (float(dl)/float(avgdl)))
    res = log( ((r+0.5)/(R-r+0.5)) / ((n-r+0.5) / (N-n-R+r+0.5)) )
    res *= ((k1+1)*f) / (K+f)
    res *= ((k2+1)*qf) / (k2+qf)
    return res

#Function to calculate query frequency of the given term in query
def qf_calc(term, query):
    qf = 1
    for i in query:
        if i == term:
            qf += 1
    return qf


#Function to calculate r
def r_calc(q, qid,relevant):
    c = 0
    if str(qid) in relevant:
        for fname in relevant[str(qid)]:
            f1 = open(InputFolder+"/"+ fname +".txt", "r")
            x = f1.read().split()
            if q in x:
                c += 1
    return c


#Function to run BM25 for a given query on whole corpus and store results in a dict
def run_bm25(uni_index,relevant,query, docWC, qid):
    result={}
    sum = 0.0
    for length in docWC:
        sum += docWC[length]
    avgdl=float(sum) / float(len(docWC))

    N = len(docWC)

    #calculating R
    if str(qid) in relevant:
        R = len(relevant[str(qid)])
    else:
        R = 0
    
    for term in query:
        #calculating r
        r = r_calc(term, qid,relevant)
        if term in uni_index:
            docDict = uni_index[term]
            qf = qf_calc(term, query)
            for docid,freq in docDict.iteritems():
                score = bm25score(len(docDict), freq, qf, r, R, N, docWC[docid], avgdl)
                if docid in result:
                    result[docid] += score
                else:
                    result[docid] = score
    return result


def main():
    queries = queryloader()
    relevant = relevance_loader()
    uni_index,docWC=unigramloader()

    results = {}
    for qid in range(0, len(queries)): #Running Bm25 on each query
        results[qid] = (run_bm25(uni_index,relevant,queries[qid].split(), docWC, qid+1))

    #Obtaining the top 100 results for every query
    topresults = {}
    os.chdir("Phase1/task3")
    f = open("BM25Stem-Output.txt", "w+")
    for r in results:
        topresults = results[r]
        rank = 1
        for i in sorted(topresults, key=topresults.get, reverse=True)[:100]:
            f.write(str(r+1) + " Q0 " + str(i)[:-4] + " " + str(rank) + " " + str(topresults[i]) + " BM25-Stem-JSY" + "\n")
            rank += 1
    f.close()
    
###########################################################

if __name__ == "__main__":
    main()

import os
from math import log
from glob import glob
import re

#DESCRIPTION: This File is used to run the BM25 Algorithm with Query Expansion
#             and produces output for the queries in BM25QE-Output.txt

#Global Constants
os.chdir("..")
os.chdir("..")
InputFolder = os.path.join(os.getcwd(),'corpus')
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
    f = open(os.getcwd()+'/cacm.query.clean.txt','r')
    queries=[]
    for line in f.readlines():
        q=line.split("\t")[1].replace("\n","")
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

#Function to get stop words from the file
def stopwords_loader():
    stopList=[]
    f = open(os.getcwd()+"/common_words",'r')
    for line in f.readlines():
        stopList.append(line.lower().replace("\n",""))
    f.close()
    return stopList


#Function to check if given term is present in a query array
def term_in_query(term, query):
    for q in query:
        if q == term:
            return True
    return False


#Function to calculate the significance factor
def sig_calc(sentence, query):
    L = sentence.split()
    lo = 0
    hi = 0
    counter = 0
    for each in L:
        if term_in_query(each, query.split()):
            lo = L.index(each)
            break
    for i in range(len(L) - 1, 0, -1):
        if term_in_query(L[i], query.split()):
            hi = i
            break
    for j in L[lo: (hi + 1)]:
        if term_in_query(j, query.split()):
            counter += 1
    if len(L[lo: (hi + 1)]) == 0:
        sig = 0.0
    else:
        sig = (float)(counter * counter) / (float)(len(L[lo: (hi + 1)]))

    return sig

#Function to generate a summary for file based on query
def generate_snip(filename, query):
    f = open(InputFolder + '/' + filename, 'r+')
    s = f.read().lower()
    s = s.split("\n")
    snips = {}
    for sentence in s:
        snips[sentence] = sig_calc(sentence, query)
    counter = 1
    snippet = ""
    for i in sorted(snips, key=snips.get, reverse=True):
        if counter < 6:
            snippet += " " + str(i)
            counter += 1
    return snippet


#Function to generate a new query
def query_expansion(doc_list, query, stopList):
    snipDict = {}
    for filename in doc_list:
        f = open(InputFolder + '/' + filename, 'r+')
        snip = generate_snip(filename, query).split()
        for i in snip:
            if i not in snipDict:
                snipDict[i] = 1
            else:
                snipDict[i] += 1
        f.close()

    terms = []
    count = 0
    for i in sorted(snipDict, key=snipDict.get, reverse=True):
        if str(i).lower() not in stopList and count < 31:   #extract top 30 terms
            terms.append(i)
            count += 1

    return " ".join(terms)


def main():
    queries = queryloader()
    relevant = relevance_loader()
    uni_index,docWC=unigramloader()
    stopList = stopwords_loader()
    
    results={}
    for qid in range(0, len(queries)):

        #Running Bm25 on query and extracting the 50 top docs
        initial_results = run_bm25(uni_index,relevant,queries[qid].split(), docWC, str(qid+1))
        top_iresults = sorted(initial_results, key=initial_results.get, reverse=True)[:50]

        #Performing query expansion based on the retrieved 50 docs
        newQuery = query_expansion(top_iresults, queries[qid],stopList) + " " + queries[qid]

        #Running Bm25 on new expanded query
        results[qid] = run_bm25(uni_index,relevant,newQuery.split(), docWC, str(qid+1))

    #Obtaining the top 100 results for every query
    topresults = {}
    os.chdir("Phase1/task2")
    f = open("BM25QE-Output.txt", "w")
    for r in results:
        topresults = results[r]
        rank = 1
        for i in sorted(topresults, key=topresults.get, reverse=True)[:100]:
            f.write(str(r+1) + " Q0 " + str(i)[:-4] + " " + str(rank) + " " + str(topresults[i]) + " BM25QE-JSY" + "\n")
            rank += 1
    f.close()


###########################################################

if __name__ == "__main__":
    main()

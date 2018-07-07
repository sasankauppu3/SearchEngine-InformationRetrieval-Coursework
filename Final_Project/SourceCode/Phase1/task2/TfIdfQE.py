import os
from math import log
from glob import glob

#DESCRIPTION: This File is used to run the TfIdf Algorithm with Query Expansion
#             and produces output for the queries in TfIdfQE-Output.txt

#Global Constants
os.chdir("..")
os.chdir("..")
InputFolder = os.path.join(os.getcwd(),'corpus')

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
        if counter < 9:
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
        if str(i).lower() not in stopList and count < 8:   #extract top 8 terms
            terms.append(i)
            count += 1

    return " ".join(terms)

                    
def main(): 
    queries = queryloader()
    uni_index,docWC=unigramloader()
    stopList = stopwords_loader()
    N = len(docWC)
    
    results={}
    for qid in range(0, len(queries)):
        
        #Running TfIdf on query and extracting the 50 top docs
        initial_results = tfidf(uni_index,N,queries[qid].split())
        top_iresults = sorted(initial_results, key=initial_results.get, reverse=True)[:60]

        #Performing query expansion based on the retrieved 50 docs
        newQuery = query_expansion(top_iresults, queries[qid],stopList) + " " + queries[qid]

        #Running TfIdf on new expanded query
        results[qid] = tfidf(uni_index,N,newQuery.split())

    #Obtaining the top 100 results for every query
    topresults = {}
    os.chdir("Phase1/task2")
    f = open("TfIdfQE-Output.txt", "w")
    for r in results:
        topresults = results[r]
        rank = 1
        for i in sorted(topresults, key=topresults.get, reverse=True)[:100]:
            f.write(str(r+1) + " Q0 " + str(i)[:-4] + " " + str(rank) + " " + str(topresults[i]) + " TfIdfQE-JSY" + "\n")
            rank += 1
    f.close()

###########################################################

if __name__ == "__main__":
    main()

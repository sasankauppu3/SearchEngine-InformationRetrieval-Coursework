import json
from math import log
import operator
import sys
import os

#Global Constants
qnum = 100 #number of results to be shown for each query
k1 = 1.2
k2 = 100
b = 0.75
R = 0.0
InputFolder = path = os.path.join(os.getcwd(),'corpus')

def queryloader():
    f = open('query.txt','r')
    lines = ''.join(f.readlines())
    queries = []
    for line in lines.split('\n'):
        queries.append(line.lower().rstrip().split())
    return queries

def unigramloader():
    f = open('unigram-indexer.txt','r')
    ugram={}
    for line in f.readlines():
        t=line.split("\t")
        ugram[t[0]]=[]
        for i in t[1].split(','):
            ugram[t[0]].append(i)
            
    return ugram

def docidmaploader():
    docidmap={}
    f = open('docidmap.txt','r')
    for line in f.readlines():
        docidmap[line.split()[0]] = line.split()[1]
    return docidmap



def bm25score(n,f,qf,r, N,dl,avgdl):
    K = k1 * ((1-b) + b * (float(dl)/float(avgdl)))
    res = log( ((r+0.5)/(R-r+0.5)) / ((n-r+0.5) / (N-n-R+r+0.5)) )
    res *= ((k1+1)*f) / (K+f)
    res *= ((k2+1)*qf) / (k2+qf)
    return res


def main():
    invIndex = unigramloader()
    docidmap = docidmaploader()
    queries = queryloader()
    
    docWC={}
    for k,v in docidmap.items():
        docWC[k]=0
        tfile = open(InputFolder+'/'+docidmap[k]+'.txt','r')
        for line in tfile:
            docWC[k]+=len(line.split())
        tfile.close()
    
    results = []
    qid=1
    scoref = open('Doc_score.txt','w')
    for query in queries:
        result = (run_bm25(invIndex, query, docWC, docidmap))

        sorted_x = sorted(result.iteritems(), key=operator.itemgetter(1), reverse=True)
        rank = 1
        for i in sorted_x[:int(qnum)]:
            temp = (qid, docidmap[i[0]], rank, i[1])
            print '{:>1} Q0 {:>4}\t{:>2}\t{:>10}\tBM25_sas'.format(*temp)
            scoref.write(str(qid)+" ")
            scoref.write('Q0 ')
            scoref.write(docidmap[i[0]]+"\t")
            scoref.write(str(rank)+"\t")
            scoref.write(str(i[1])+"\t"+"BM25_sas\n")
            rank += 1
        qid += 1
    

def run_bm25(index, query, docWC, docidmap):
    result = dict()
    qf = 1
    r = 0
    N = len(docWC)

    avdl = 0
    for length in docWC.values():
        avdl += length
    avgdl = float(avdl) / float(len(docWC))

    for term in query:
        if term in index:
            doc_list = index[term]  
            for docid in doc_list:
                tfile = open(InputFolder+'/'+docidmap[docid]+'.txt','r')
                f = 0
                for line in tfile:
                    f+=line.split().count(term)
                tfile.close()
                n = len(doc_list)
                dl = docWC[docid]
                score = bm25score(n,f,qf,r,N,dl,avgdl)  
                if docid in result:  
                    result[docid]+=score
                else:
                    result[docid]=score
    return result

#####################################################################

if __name__ == '__main__':
    main()

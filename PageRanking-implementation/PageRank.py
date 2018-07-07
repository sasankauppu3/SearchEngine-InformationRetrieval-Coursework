import math
import operator

#Global variables
S=[]     # S is the set of sink nodes
M={}     # M is the inlinks dictionary with page as key and all its inlinks as val
P=[]     # P is the set of all pages
L={}     # L is the outlinks dictionary with page as key and the no. of outlinks as value.
PR={}    # PR is the dictionary containing pages and their respective page ranks
newPR={} # newPR is the dictionary of temporary page ranks
inpfile = "G1"

def main():
    load_inlinks(open(inpfile+".txt","r").readlines())
    global P;
    P=M.keys()
    load_outlinks()
    load_sinkpages()
    page_rank()
    top50_pages()

def load_inlinks(lines):
    for line in lines:
        docs=line.split()
        if len(docs)>1:
            M[docs[0]]=docs[1:] 
        else:
            M[docs[0]]=[]           

def load_outlinks():
    global L;
    for i in P:
        for doc in M[i]:
            if doc in L:
                L[doc] += 1
            else:
                L[doc] = 1

def load_sinkpages():
    global S;
    S = (list(set(P) - set(L.keys())))


def page_rank():
    global PR,newPR;
    total_pages = len(P)
    #initial page rank
    for p in P:
        PR[p]=1.0/total_pages
    d=0.85
    perplexity = 0 # perplexity value
    cc = 0 #initializing the convergence counter to 0
    counter = 0
    outfile = open(inpfile+"perplexity.txt","w")
    while  cc < 4:
        sinkPR = 0
        for s in S:
            sinkPR += PR[s]
        for p in P:
            newPR[p] = (1.0 - d)/total_pages #teleportation factor
            newPR[p] += (d*sinkPR/total_pages) 
            for p1 in M[p]:
                newPR[p] += (d * PR[p1])/L[p1] 

        for page in P:
            PR[page] = newPR[page] 

        sumPR = 0
        for i in P:
            sumPR += PR[i] * math.log(PR[i], 2)
        new_perplexity = math.pow(2, -sumPR)
        
        if abs(new_perplexity - perplexity) < 1.0 :
            cc +=1
        else:
            cc = 0
        perplexity = new_perplexity
        counter+=1
        outfile.write("Perplexity for the iteration: " + str(counter)+" is: "+ str(perplexity) + "\n")

    outfile.close()

'''
#G1-G2-Stats
print ("sinks: "+ str(len(S)))

c=0
for p in M:
    if not M[p]:
        c+=1
    print ("sources: "+ str(c))
'''

def top50_pages():
    p_dict={}
    p_dict = sorted(PR.iteritems(), key=operator.itemgetter(1), reverse=True)
    outfile = open(inpfile+"top50.txt","w")
    count=0
    for sp in range(len(p_dict)):
        if count==50:
            break
        outfile.write(str(p_dict[sp][0]) +"  "+str(p_dict[sp][1])+ "\n")
        count+=1
    outfile.close()


###########################################################

if __name__ == "__main__":
    main()

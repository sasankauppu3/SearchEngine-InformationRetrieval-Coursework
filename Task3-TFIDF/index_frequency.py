from glob import glob
import operator
import os

#Global Constants
InputFolder = path = os.path.join(os.getcwd(),'corpus')

def main():

    Unigram_inverted_index = {}     #Inverted Index for Unigrams
    Bigram_inverted_index = {}      #Inverted Index for Bigrams
    Trigram_inverted_index = {}     #Inverted Index for Trigrams
    
    counter=1
    for file in glob(os.path.join(InputFolder,'*.txt')):
        doc=open(file, 'r').read()
        docId=counter
        terms = doc.split()
        
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

            #Bigrams
            if i >= len(terms)-1 :
                continue
            term = terms[i]+" "+terms[i+1]
            if not Bigram_inverted_index.has_key(term):
                doc_term_freq={docId:1}
                Bigram_inverted_index[term]=doc_term_freq
            elif not Bigram_inverted_index[term].has_key(docId):
                Bigram_inverted_index[term][docId]=1
            else:
                Bigram_inverted_index[term][docId]+=1

            #Trigrams
            if i >= len(terms)-2:
                continue
            term = terms[i]+" "+terms[i+1]+" "+terms[i+2]
            if not Trigram_inverted_index.has_key(term):
                doc_term_freq={docId:1}
                Trigram_inverted_index[term]=doc_term_freq
            elif not Trigram_inverted_index[term].has_key(docId):
                Trigram_inverted_index[term][docId]=1
            else:
                Trigram_inverted_index[term][docId]+=1

        counter+=1

    index_to_file(Unigram_inverted_index,1)
    index_to_file(Bigram_inverted_index,2)
    index_to_file(Trigram_inverted_index,3)


#Common function to write an inverted index to a file
def index_to_file(inv_index, grams):
    tf={} #term frequency
    df={} #document frequency
    
    for term in inv_index:
        frequency=0
        docList=[]
        for docId in inv_index[term].keys():
            docList.append(docId)
            frequency += inv_index[term][docId]
        tf.update({term:frequency})
        df.update({term:docList})

    #writing term frequency
    tf = sorted(tf.items(),key=operator.itemgetter(1),reverse=True)
    o_file = open(str(grams)+"-gram-TF.txt",'w')
    for item in tf:
        o_file.write(str(item[0])+":"+str(item[1])+"\n")
    o_file.close()
    
    #writing document frequency
    df = sorted(df.items(),key=operator.itemgetter(0))
    o_file = open(str(grams)+"-gram-DF.txt",'w')
    for item in df:
        o_file.write(str(item[0])+":"+str(item[1])+" "+str(len(item[1]))+"\n")
    o_file.close()


###########################################################

if __name__ == "__main__":
    main()

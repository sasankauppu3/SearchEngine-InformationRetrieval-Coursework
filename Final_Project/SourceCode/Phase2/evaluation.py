import os
import operator
#To get the current working directory path
path = os.getcwd();

#to get relevent docs from the relvence docs
#the doc should be in the form of
#Query Q0 doc relevence
#example :- 1 Q0 CACM-1410 1
relevant={}
def get_relevant():
    try:
        with open("cacm.rel") as f:
            for line in f:
                words = line.split()
                if words[0] not in relevant:
                    relevant[words[0]] = [words[2]]
                else:
                    relevant[words[0]].append(words[2])
        f.close()
    except:
        print "please check the relevence retrival method"



#get BM25 scores from the bm text
#the doc should be in the form of
#query Q0 doc rank score systemname
#1 Q0 CACM-1519 1 24.6480639058 JSYBM25
BM25={}
def get_BM25():
    try:
        print "enter file name including extension"
        fn=raw_input()
        with open(path + "/" + fn) as f:
            for line in f:
                words = line.split()
                if words[0] not in BM25:
                    BM25[words[0]] = {words[3]: words[2]}
                else:
                    BM25[words[0]].update({words[3]: words[2]})
    except:
        print "error in get_BM25"


#get BM25 relevance docs
BM25_rel = {}
def get_BM25_rel():
    for q_id in BM25:
        rank_list = BM25[q_id]
        for each in rank_list:
            if q_id in relevant:
                if rank_list[each] in relevant[q_id]:
                    if q_id not in BM25_rel:
                        BM25_rel[q_id] = {each: rank_list[each]}
                    else:
                        BM25_rel[q_id].update({each: rank_list[each]})


precision = {}
recall = {}
def get_recall():
    for each in relevant:
        if each in BM25_rel:
            precision[int(each)] = float(len(BM25_rel[each])) / 100.0
            recall[int(each)] = float(len(BM25_rel[each])) / float(len(relevant[each]))

avprecision = {}
def get_avp():
    for each in relevant:
        if each in BM25_rel:
            i = BM25_rel[each]
            si = i.keys()
            int_lst = []
            for k in si:
                int_lst.append(int(k))
            int_lst.sort()
            count = 0;
            avp = 0.0;
            for j in int_lst:
                count = count +1
                avp =  avp + (float(count)/float(j))
            avprecision[int(each)] = avp/float(len(i))

reciporcalRank = {}
def get_rr():
    for each in relevant:
        if each in BM25_rel:
            i = BM25_rel[each]
            si = i.keys()
            int_lst = []
            for k in si:
                int_lst.append(int(k))
            int_lst.sort()
            rankFirstRel = int_lst[0]
            rr = float(1)/float(rankFirstRel)
            reciporcalRank[int(each)] = rr

#precision at k = 5 and k =20
precisionAt5 = {}
precisionAt20 = {}
def get_precision():
    for each in relevant:
        if each in BM25_rel:
            i = BM25_rel[each]
            si = i.keys()
            int_lst = []
            for k in si:
                int_lst.append(int(k))
            int_lst.sort()


            int_lst2 = int_lst
            count5 = 0
            count20 = 0

            for i in int_lst:
                if(i <= 5):
                    count5 = count5+1

                if(i <= 20):
                    count20 = count20+ 1
                else:
                    break

            pAt5 = float(count5)/5.0
            pAt20 = float(count20)/20.0

            precisionAt5[int(each)] = pAt5
            precisionAt20[int(each)] = pAt20

def cal_avg():
    #Mean average precision calculation
    #----------------------------------
    mvp = 0.0
    for i in avprecision:
        mvp = mvp + avprecision[i]

    mvp = mvp / float(len(avprecision))
    print "Mean avarage precision"
    print mvp
    #-----------------------------------

    #Mean reciprocal rank
    mrr = 0.0
    for i in reciporcalRank:
        mrr = mrr + reciporcalRank[i]

    mrr = mrr / float(len(reciporcalRank))
    print "Mean reciprocal rank"
    print mrr

    #---------------------------------------
def main():
    get_relevant()
    get_BM25()
    get_BM25_rel()
    get_recall()
    get_avp()
    get_rr()
    get_precision()
    
    
    print "reciprocal Rank"
    rr= dict(sorted(reciporcalRank.items(),key=operator.itemgetter(0)))
    print rr
    
    print "precision"
    pr= dict(sorted(precision.items(),key=operator.itemgetter(0)))
    print pr
    
    print "recall"
    r= dict(sorted(recall.items(),key=operator.itemgetter(0)))
    print r

    print "Average precision"
    avp= dict(sorted(avprecision.items(),key=operator.itemgetter(0)))
    print avp

    print "precision at 5"
    p5= dict(sorted(precisionAt5.items(),key=operator.itemgetter(0)))
    print p5

    print "precision at 20"
    p20= dict(sorted(precisionAt20.items(),key=operator.itemgetter(0)))
    print p20
    
    cal_avg()


#call to main function
main()

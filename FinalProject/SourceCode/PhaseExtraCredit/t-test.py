import math
# the file that needs to be fed to this program is obtained by running the evaluation.py
# that produces the file in the form of
# Query_id,Reciprocal_rank,Precision,Recall,Avg_Precision

#give the model A (tf-idf) avg precision file path
path1="tfidfavgP.txt"
#give the model B (BM25) avg precision file path
path2="BMavgP.txt"


a={}
b={}
#read the file to get A
f1=open(path1,'r+')
for line in f1.readlines():
    l=line.split(',')
    a.update({l[0]:l[4]})
f1.close()
#read the file to get B
f1=open(path2,'r+')
for line in f1.readlines():
    l=line.split(',')
    b.update({l[0]: l[4]})
f1.close()

#cal A-B
AB=[]
def cal_AB():
    for keys in a :
        ai = float(a[keys])
        bi = float(b[keys])
        AB.append(bi-ai)

#cal mean A-B
mAB=0
def cal_meanAB():
    sum=0.0
    for i in AB:
        sum=sum+i
    return  sum/len(AB)

#cal the statistical tests i.e t-test
def cal_dev():
    sum=0.0
    mAB=cal_meanAB()
    N=len(AB)
    for i in AB:
        x=math.pow((i-mAB),2)
        sum+=(x/N)
    y=math.sqrt(sum)
    t=(mAB/y)*math.sqrt(len(AB))
    return t

#main function call
def main():
    cal_AB()
    val=cal_dev()
    print "t-test value is",val

main()

################## INFORMATION RETRIEVAL - COURSE PROJECT ##################

#############################################################################


All the tasks in this project are implemented using Python-2.7 except Lucene which was done using Java 8.
So make sure Java and Python are installed in your system before running the code.

Executing Python code:

	Open terminal and navigate to working directory, run the comand below:
	    python <filename>.py


Executing Java code:
	
	Open terminal and navigate to working directory, run the 2 commands below:
		javac -d . -cp ./lucene-analyzers-common-4.7.2.jar:lucene-core-4.7.2.jar:lucene-queryparser-4.7.2.jar:. <filename>.java
		java -cp ./lucene-analyzers-common-4.7.2.jar:lucene-core-4.7.2.jar:lucene-queryparser-4.7.2.jar:. <filename>

	[NOTE: replace ":" with ";"" if you are running windows]


#############################################################################
 
In the current directory we have Project report and scores.xls
Make sure to check different worksheets in the xlsx files to view the scores of different runs

#############################################################################

Firstly, we have all the provided files in the main directory of SourceCode which are
1) cacm              --   Input Html files dir
2) cacm_stem.txt     --   Stemmed version of all html files in one file
3) cacm.query        --   Query File
4) cacm_stem.query   --   Stemmed Query File 
5) cacm.rel          --   Releveant documents list
6) common_words.txt  --   Stop words list


Before running any of the tasks we need cleaned,stemmed,stopped corpuses respectively so we have 
neccessary python scripts for the same

1) cacm_corpus.py            --   takes cacm directory and cleans it to produce corpus directory  
								  	[make sure you create corpus dir before running incase not present]
2) cacm_corpus_stem.py       --   takes cacm_stem.txt and splits them into files to produce corpus_stemmed directory  
								  	[make sure you create corpus_stemmed dir before running incase not present]
3) cacm_corpus_stop.py       --   takes cacm directory, cleans and does stopping to produce corpus_stopped directory  
								  	[make sure you create corpus_stopped dir before running incase not present]

Since we have cleaned corpus we need to clean the query as well so we have the required scripts for the same
1) cacm_query_clean.py      --    takes cacm.query.txt and cleans it. It stores each query its id in tsv to produce cacm.query.clean.txt

NOTE: Stemmed query is already provided and Stopping on query is done explicitly in the code. 

Once you have run the above 4 python files you will then be able to run induvidual tasks


#############################################################################
NOTE: Do not change the internal directory structure
#############################################################################

Phase1 directory -- contains all phase 1 tasks

task1 directory -
	Files
		1) BM25.py     	 --  Contains implementation of the BM25 ranking algorithm
							 Takes input from corpus, cacm.rel, cacm_query_clean.txt which are present 2 directories above
							 Produces output in BM25-Output.txt


		2) TfIdf.py    	 --  Contains implementation of the TfIdf ranking algorithm
							 Takes input from corpus, cacm_query_clean.txt which are present 2 directories above
							 Produces output in TfIdf-Output.txt

		3) lucene/HW4.java  -- Contains implementation of the Lucene ranking algorithm.
							 Takes input from corpus, cacm_query.txt which are present 2 directories above
							 Produces output in LuceneDocScore.txt


task2 directory -
	Files
		1) BM25QE.py     	 --  Contains implementation of the BM25 ranking algorithm with query expansion
							 Takes input from corpus, cacm.rel, cacm_query_clean.txt, common_words which are present 2 directories above
							 Produces output in BM25QE-Output.txt


		2) TfIdfQE.py    	 --  Contains implementation of the TfIdf ranking algorithm
							 Takes input from corpus, cacm_query_clean.txt, common_words which are present 2 directories above
							 Produces output in TfIdfQE-Output.txt

task3 directory -
	Files
		1) BM25-Stem.py      --  Contains implementation of the BM25 ranking algorithm on stemmed corpus
							 Takes input from corpus_stemmed, cacm.rel, cacm_stem.query which are present 2 directories above
							 Produces output in BM25Stem-Output.txt

		2) BM25-Stop.py      --  Contains implementation of the BM25 ranking algorithm on stoppped corpus
							 Takes input from corpus_stopped, cacm.rel, cacm_query_clean.txt which are present 2 directories above
							 Produces output in BM25Stop-Output.txt
							 NOTE: Query stopping is done explicitly in the code

		3) TfIdf-Stem.py     --  Contains implementation of the TfIdf ranking algorithm on stemmed corpus
							 Takes input from corpus_stemmed, cacm_stem.query which are present 2 directories above
							 Produces output in TfIdf-Stem-Output.txt

		4) TfIdf-Stop.py     --  Contains implementation of the TfIdf ranking algorithm on stoppped corpus
							 Takes input from corpus_stopped, cacm_query_clean.txt which are present 2 directories above
							 Produces output in TfIdf-Stop-Output.txt
							 NOTE: Query stopping is done explicitly in the code



#############################################################################

Phase2 directory -- contains phase 2 task
	
	Files
		All output files for the above runs are copied into this directory
		evaluation.py       --    generates the different scores based on the given input file which is the query outputs obtained above



#############################################################################

PhaseExtraCredit directory -- contains extra credit task
	
	Files
		snippet.py       --    given a list of files and query , it generates snippets for each file based on significance factor

		t-test.py 		 --    given the scores of bm25,tfidf model it ouputs the t-test value score of it.

Implementation of a Focused/non-focused crawler using Breadth first search and Depth first search algorithms

#####################################################################
Different tasks for the Crawler

Task	1: Crawling	the	documents:
A. Start	with	the	following	seed URL: https://en.wikipedia.org/wiki/Sustainable_energy;	a	Wikipedia	article	about	green	energy.

B. Your	crawler	must	assume	that	pages	in	a	shallower	depth	are	more	
important	than	deeper	ones,	also,	within	each	individual	webpage,	
hyperlinks	appearing	earlier	on	in	the	webpage	should	be	crawled	first.

B. Crawl	to	depth	5.	The	seed	page	is	the	first	URL	in	your	frontier and	thus	
counts	for	depth	1. Stop	once	you’ve	crawled	1000	unique	URLs

Task	2:	Focused	Crawling:
Your	crawler	should	be	able	to	consume	two	arguments:	a	URL	and	a	keyword	to	be	
matched	against	anchor	text	or	text	within	a	URL.		Starting	with	the	same	seed	in	
Task	1,	crawl	to	depth	5	at	most,	using	the	keyword	“solar”.	You	should	return	at	
most	1000	URLS	for	each	of	the	following:
A. Breadth	first	crawling
B. Depth	first	crawling

Task	3:		Combined	Results
Repeat	Task	1	this	time	using	the	seed	https://en.wikipedia.org/wiki/Solar_power.
Assume	you	were	asked	to	combine	the	results of	these	two	independent	runs into	
one	file with	1000	links	at	most.	Describe	briefly	(in	a	few	steps)	how	you	would	
approach	the	merging	process	with	minimal	loss	of	information	about	the	deemed	
importance	of	the	hyperlinks	(reflected	by	the	order	in	which	they	are	crawled – as	
described	in	Task	1).

Source Code:

Filenames for different tasks

	Task 1   ===== task-1.py
	Task 2 A ===== task-2a.py
	Task 2 B ===== task-2b.py
	Task 3   ===== task-3.py

   Execute each file with the command: python filneame.py

####################################################################

Output Files:

Filenames for the output files for the above tasks.

	Task 1(E) ===== Output-task-1.txt
	Task 2 A  ===== Output-task-2a.txt
	Task 2 B  ===== Output-task-2b.txt
	Task 3    ===== Output-task-3.txt

#####################################################################

import re
#Function to generate a summary for file based on query
def generate_snip(filename, query):
    f = open(filename, 'r+')
    s = f.read().lower()
    s = s.replace("<html>","")
    s = s.replace("</html>","")
    s = s.replace("<pre>","")
    s = s.replace("</pre>","")
    s = s.split("\n")
    snips = {}
    for sentence in s:
        if re.search('[a-zA-Z]', sentence)==None:
            continue
        snips[sentence] = sig_calc(sentence, query)
    counter = 1
    snippet = []
    for i in sorted(snips, key=snips.get, reverse=True):
        if counter < 6:
            snippet.append(str(i))
            counter += 1
    return snippet

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


#Function to generate a summary for a list of files the query term in the summary is
#present in red color
def generate_snippet(file_list, query):
    for filename in file_list:
        snippet = generate_snip(filename, query.lower())
        output = ""
        print "*****************************************************************************************"
        print filename
        for each in snippet:
            output += "..."
            for i in str(each).split():
                if term_in_query(i, query.lower().split()):
                    output += '\033[1m' + '\033[91m' + i + '\033[0m' + " "
                else:
                    output += i + " "
            output += "..."
            output += '\n'
        print output
        print "========================================================================================="

def main():
    generate_snippet(["CACM-3189.html", "CACM-3188.html", "CACM-3187.html" ], "fortran")


###########################################################

if __name__ == "__main__":
    main()


import re
from glob import glob
import os
from bs4 import BeautifulSoup

#Global Constants
InputFolder = os.path.join(os.getcwd(),'downloaded_docs')
OutputFolder = os.path.join(os.getcwd(),'corpus')
specialChars= [",",".","-",":",";",'"']

def generate_corpus():
    for file in glob(os.path.join(InputFolder,'*.txt')):
        curfile = open(file, 'r').read().lower()
        curfile = curfile.split()
        curfile = " ".join(curfile)
        #removing last unnecessary sections
        if (curfile.find('<span class="mw-headline" id="see_also">')!=-1):
            curfile=curfile[:curfile.index('<span class="mw-headline" id="see_also">')]
        elif (curfile.find('<span class="mw-headline" id="References">')!=-1):
            curfile=curfile[:curfile.index('<span class="mw-headline" id="References">')]
        if (curfile.find('<div class="toc" id="toc">')!=-1):
            part1=curfile[:curfile.index('<div class="toc" id="toc">')]
            part2=curfile[curfile.find('</div>', (curfile.find('</div>',(curfile.index('<div class="toc" id="toc">') + 1)) + 1)):]
            curfile = part1+part2
        curfile = curfile.split()
        curfile = " ".join(curfile)
        htmlpage = BeautifulSoup(curfile, "html.parser")
        htmlpage.prettify().encode("utf-8")
        body_data = htmlpage.findAll('div', attrs={'id':'bodycontent'})
        body=""
        for div in body_data:
            body+=div.get_text()

        title=htmlpage.find('title').get_text()
        h1= htmlpage.find('h1').get_text()

        title = title.split()
        title = " ".join(title)
        h1 = h1.split()
        h1 = " ".join(h1)
        body = body.split()
        body = " ".join(body)
        
        curfile =h1+" "+title+" "+body
        curfile = curfile.encode("utf-8")
        #handling special chars
        curfile = re.compile('[_!@\s#$%=+~()}{\][^?&*:;\\/|<>"\']').sub(' ',curfile)
        curfile = curfile.split()
        word_list = []
        for word in curfile:
            word=word.strip()
            if word!='':
                firstchar=word[:1]
                if firstchar in specialChars:
                    if not re.match(re.compile("^[\-]?[0-9]*\.?[0-9]+$"),word):
                        word=word[1:]
                lastchar=word[((len(word))-1):(len(word))]
                if lastchar in specialChars :
                    word=word[:-1]
                
                word_list.append(word)
        while '' in word_list:   #Removing empty strings
                del word_list[word_list.index('')]
        #writing to output file
        o_file  = open(OutputFolder+"/"+file.replace(InputFolder,'')[1:],'w')
        word_list=" ".join(word_list) 
        o_file.write(word_list)
        o_file.close()

###########################################################

if __name__ == "__main__":
    generate_corpus()


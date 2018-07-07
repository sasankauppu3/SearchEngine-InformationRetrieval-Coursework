import re
import time
from bs4 import BeautifulSoup
import requests

#Global Constants
crawl_limit = 1000   #Number of links to be crawled
depth_limit = 5      #Maximum Depth to crawl
frontier = []        #Frontier which is a queue in this case of BFS Crawler
visited = []         #Visited links list
keyword = "solar"    #Keyword for focused based crawling. Change here if required.

seed_link = "https://en.wikipedia.org/wiki/Sustainable_energy"
Wiki = "https://en.wikipedia.org"


def main():
    crawler(seed_link)
    fname = 'Output-task-2b.txt'
    o_file = open(fname, 'w')
    index = 1
    
    #Prints to the output file
    for i in visited:
        row =  str(index) + " " + str(i) + "\n"
        o_file.write(row)
        index += 1
    o_file.close()


#Function which takes a Url and crawls that page and gets the url's list in it
def page_crawler(cur):
    if cur[1]==depth_limit or len(visited)==crawl_limit:
        return
    link_info=""
    url=cur[0]
    depth=cur[1]   
    time.sleep(1)    #Politeness policy
    document = requests.get(url)
    document = BeautifulSoup(document.text, 'html.parser')
    content = document.find('div', {'id': 'mw-content-text'})
    
    tempfrontier = []  #to restore the order of links obtained
    
    if len(content.find('ol',class_='references') or ()) > 1:
        content.find('ol',class_='references').decompose()

    for link in content.find_all('a', {'href': re.compile("^/wiki")}):
        if ':' not in link.get('href') and len(frontier)+len(visited)!=crawl_limit:
            try:
                link_info = str(link.text)
            except UnicodeEncodeError as e:
                pass
            if (keyword.lower() in str(link.get('href')).lower()) or (keyword.lower() in link_info.lower()):
                link = Wiki + link.get('href')
                link = link.split('#')
                link = link[0]
                if not((link in tempfrontier) or (link in visited)):
                    tempfrontier.append((link,depth+1))

    #orginal link order restored                
    while len(tempfrontier)!=0:
        frontier.append(tempfrontier.pop())


#Crawler which stores Url's and chooses which url to crawl next (In a DFS fashion in this case) 
def crawler(seed):
    frontier.append((seed,1))
    while len(visited)!=crawl_limit and len(frontier)!=0:
        cur = frontier.pop()                  #to achieve stack like fashion
        url = cur[0]
        if url in visited:
            continue
        visited.append(url)
        page_crawler(cur)

    while len(frontier)!=0:
        cur = frontier.pop()
        visited.append(cur[0])

###########################################################

if __name__ == "__main__":
    main()

import re
import time
from bs4 import BeautifulSoup
import requests

#Global Constants
seed_link = 'https://en.wikipedia.org/wiki/Sustainable_energy'
crawl_limit = 1000  #Number of links to be crawled
depth_limit = 5     #Maximum Depth to crawl
frontier = []       #Frontier which is a queue in this case of BFS Crawler
visited = []        #Visited links list
Wiki = "https://en.wikipedia.org"


def main():
    crawler(seed_link)
    fname = 'Output-task-1.txt'
    o_file = open(fname, 'w')
    index = 1

    #Prints to the output file
    for i in visited:
        row = str(index) + " " + str(i) + "\n"
        o_file.write(row)
        index += 1
    o_file.close()


#Function which takes a Url and crawls that page and gets the url's list in it
def page_crawler(cur):
    url = cur[0]
    depth = cur[1]
    time.sleep(1)   #Politeness policy
    document = requests.get(url)
    document = BeautifulSoup(document.text, 'html.parser')
    content = document.find('div', {'id': 'mw-content-text'})

    if len(content.find('ol', class_='references') or ()) > 1:
        content.find('ol', class_='references').decompose()

    for link in content.find_all('a', {'href': re.compile("^/wiki")}):
        if ':' not in link.get('href') and len(frontier)+len(visited)!=crawl_limit:
            link = Wiki + link.get('href')
            link = link.split('#')
            link = link[0]
            if link_not_visited(link):
                frontier.append((link,depth+1))


#Helper function to check if a link is ever visited by the crawler
def link_not_visited(u1):
    if u1 in visited:
        return False
    for url,depth in frontier:
        if u1 == url:
            return False
    return True

#Crawler which stores Url's and chooses which url to crawl next (In a BFS fashion in this case) 
def crawler(seed):
    frontier.append((seed,1))
    while len(frontier)+len(visited)!=crawl_limit and len(frontier)!=0:
        cur = frontier.pop(0)
        if cur[1]==depth_limit:
            break
        url = cur[0]
        visited.append(url)
        page_crawler(cur)
    while len(frontier)!=0:
        cur = frontier.pop(0)
        visited.append(cur[0])
        
###########################################################

if __name__ == "__main__":
    main()

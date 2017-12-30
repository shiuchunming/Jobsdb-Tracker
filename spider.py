import sys
import logging
import requests
import time
import re
from bs4 import BeautifulSoup

def extractURL():
    urls = set()
    try:
        soup = BeautifulSoup(open("information-technology.html"), "html.parser")
    except:
        logging.exception("ERROR: BaseURL file not exist.")

    for link in soup.find_all('a', {"class": "posLink", "href": re.compile("(/job/)")}):
        if link.attrs['href'] not in urls:
            urls.add(str(link.attrs['href']))

    return urls

def download(url):
    file_name = "data/urls/" + "" + str(url).split('/')[-1]
    # print(file_name)
    try:
        web = requests.get(url)
    except:
        with open("log/errorlog", mode='a') as file:
            logging.exception("ERROR: Network/HTMLStatus encounter en error.")
            file.write("time: " + time.asctime(time.localtime(time.time())))
            file.write("\nURL: " + url)
            sys.exit(1)

    with open(file_name, mode='wb') as file:
        content = web.text
        file.write(content.encode(web.encoding))

if __name__ == '__main__':

    baseURL = 'https://hk.jobsdb.com/hk/jobs/information-technology/'

    try:
        web = requests.get(baseURL)
    except:
        with open("log/errorlog", mode='a') as file:
            logging.exception("ERROR: Network/HTMLStatus encounter en error.")
            file.write("time: " + time.asctime(time.localtime(time.time())))
            file.write("\nBaseURL: " + url)
            sys.exit(1)

    with open("information-technology.html", mode='wb') as file:
        content = web.text
        file.write(content.encode(web.encoding))
    
    urls = extractURL()
    for url in urls:
        download(url)
    
    
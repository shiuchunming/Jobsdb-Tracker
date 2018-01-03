import sys
import logging
import os
import requests
import time
import re
import smtplib

from bs4 import BeautifulSoup
from metaManager import metaManager
from email.message import EmailMessage

def extractURL():
    urls = set()
    try:
        soup = BeautifulSoup(open("data/baseurl/information-technology.html"), "html.parser")
    except:
        logging.exception("ERROR: BaseURL file not exist.")

    for link in soup.find_all('a', {"class": "posLink", "href": re.compile("(/job/)")}):
        if link.attrs['href'] not in urls:
            file_name = download(str(link.attrs['href']))
            urls.add(file_name)
            metaManager.write_to_meta(file_name, str(link.attrs['href']))

    return urls

def download(url):
    file_name = "data/urls/" + "" + url.split('/')[-1] + ".html"
    print(file_name)

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
    
    return file_name

def send_mail(result):
    TO = "hugoshiu1222@gmail.com"
    FROM = "hugoshiu1222@gmail.com"
    SUBJECT = "Your Spiderman Found A Matched Job"

    msg = EmailMessage()
    msg.set_content(result)

    msg['Subject'] = SUBJECT
    msg['From'] = FROM
    msg['To'] = TO
    password = input(Password: )

    server = smtplib.SMTP('smtp.gmail.com', port=587)
    server.ehlo()
    server.starttls()
    server.login(FROM, password)
    server.send_message(msg)
    server.quit()


if __name__ == '__main__':
    
    baseURL = 'https://hk.jobsdb.com/hk/jobs/information-technology/'
    results = set()

    try:
        web = requests.get(baseURL)
    except:
        with open("log/errorlog", mode='a') as file:
            logging.exception("ERROR: Network/HTMLStatus encounter en error.")
            sys.exit(1)

    with open("data/baseurl/information-technology.html", mode='wb') as file:
        content = web.text
        file.write(content.encode(web.encoding))
    
    for file in os.listdir("data/urls"):
        os.remove("data/urls/" + file)

    urls = extractURL()
    for url in urls:
        soup = BeautifulSoup(open(url), "html.parser")
        for item in soup.find_all('div', {'class': 'jobad-primary'}):
            if re.search(re.compile("(?i)trading|cloud computing|fintech"), item.text.rstrip().replace(" ", "")):
                result = metaManager.read_meta(url)
                results.add(result)
    
    for result in results:
        send_mail(result)
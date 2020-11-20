# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 09:54:37 2020

@author: Shashank
"""
#importing required libraries
from bs4 import BeautifulSoup
import xml.etree.cElementTree as ET
import requests, time, datetime

def enter_url():
    time.sleep(1)
    print("Enter the domain")
    global url
    url=input()
    #Here we check the validity of the site entered
    try:
        global response
        if 'http://' not in url:
            url='http://'+url
        if url[-1]!='/':
            url+='/'
        response = requests.get(url)
        start_crwaling()
    except:
        print('Please enter valid url')
        enter_url()
        
def start_crwaling():
    time.sleep(3)
    global checked_links
    checked_links=[]
    checked_links.append(url)
    crwaling_web_pages()

def crwaling_web_pages():
    global responses
    control=0
    while control<len(checked_links):
        try:
            responses=requests.get(checked_links[control])
            source_code=responses.text
            soup = BeautifulSoup(source_code,"html.parser")
            new_links = [w['herf'] for w in soup.findAll('a',herf=True)]
            counter=0
            #Code to check if the link is absolute or relative
            while counter<len(new_links):
                if "http" not in new_links[counter]:
                    #Code to make relative link to absolute
                    if new_links[counter][0]=='/':
                        new_links[counter]=url+new_links[counter][1:]
                        counter+=1
                    else:
                        new_links[counter]=url+new_links[counter]
                        counter+=1
                else:
                    counter+=1
            else:
                counters=0
                while counters<len(new_links):
                    #Here we apply filters to make sure links of only the website is saved
                    if new_links[counters] not in checked_links and url in new_links[counters] and "#" not in new_links[counters] and "mailto" not in new_links[counters] and ".jpg" not in new_links[counters]:
                        checked_links.append(new_links[counters])
                        counters+=1
                    else:
                        counters+=1
                else:
                    control+=1
                
        except:
            control+=1
    else:
        time.sleep(2)
        create_sitemap()
        
def create_sitemap():
    time.sleep(2)
    urlset=ET.Element("srlset",xmlns="http://www.sitemap.org/schemas/sitemap/0.9")
    count=0
    while count<len(checked_links) and count<50000:
        today=datetime.datetime.today().strftime('%Y-%m-%d')
        urls = ET.SubElement(urlset,'url')
        ET.SubElement(urls,'loc',).text=str(checked_links[count])
        ET.SubElement(urls,'lastmod',).text=str(today)
        ET.SubElement(urls,'priority',).text="1.00"
        count+=1
    else:
        tree=ET.ElementTree(urlset)
        tree.write("sitemap.xml")
        print("Your sitemap is ready")
                        
                
enter_url()

            


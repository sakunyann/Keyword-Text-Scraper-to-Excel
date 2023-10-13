#!/usr/bin/env python3

from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

url = "http://www.google.com"
keywords = ['google', 'search', 'isnone']

def keyword_rip(url_input, keyword_list):

    html = urlopen(url_input).read()
    soup = BeautifulSoup(html, features="html.parser")

    output = []
    url_col = []
    for keyword in keyword_list:
        # kill all script and style elements
        for script in soup(["script", "style"]):
            script.extract()    # rip it out

        # get text
        text = soup.get_text()

        # break into lines and remove leading and trailing space on each
        lines = ([line.strip() for line in text.splitlines() if keyword in line])
   
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
      
        # drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        output.append([text])
        url_col.append([url_input])

    df_list = list(zip(keyword_list, output, url_col))
    df = pd.DataFrame(df_list, columns = ['keyword', 'returned', 'url'])
    print(df)
    df.to_excel("output.xlsx", index=False)
    
          
keyword_rip(url, keywords)

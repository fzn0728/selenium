
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

def find_hidden_link(url):
    '''
    Find the hidden link given by text indicator "page:", in case that they change the link
    '''
    soup = BeautifulSoup(urlopen(url).read(),'lxml')
    sentence = soup.find("iframe", id = "_48_INSTANCE_2rBHjKjrfC0Q_iframe").text
    if "page:" in sentence:    
        msg, link = sentence.split("page:",1)
    else:
        raise NameError('The original content changed and auto link fetching has failed,'\
                        'please check the html file and find the hidden link manually.')
    return link[1:-2]
    
def get_soup(url_table):
    # url_table = 'https://app2.msci.com/webapp/indexperf/pages/IEIPerformanceRegional.jsf'
    soup = BeautifulSoup(urlopen(url_table).read(),'lxml')
    return soup

def get_value():
    '''
    Find 'tbody' first, and locate the 'tr' tag, then extract all text after 'td' tag.
    '''
    data = []
    table = soup.find("tbody", id = "templateForm:tableResult0:tbody_element")
    rows = table.find_all('tr')
    for tr in rows:
        cols = tr.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele]) # Get rid of empty values    
    return data


if __name__ == "__main__":
    # Get the hidden link
    url = 'https://www.msci.com/end-of-day-data-search'
    link = find_hidden_link(url)
    # Fetch html from url (jsf in this case)
    soup = get_soup(link)
    # Parse raw data from the table 
    data = get_value()
    # Clean the format and change it into dataframe
    df = pd.DataFrame([part for part in data])
    df.columns=['MSCI Index','Index Code','Last','Day','MTD','3MTD','YTD','1 Yr','3 Yr','5 Yr','10 Yr']
    df.to_csv('MSCI_table.csv')
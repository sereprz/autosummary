import re
import requests
from bs4 import BeautifulSoup


class PageParser():
    '''
        Sends a get request and extracts the main content of the page
    '''
    def __init__(self, url):

        r = requests.get(url)

        self.url = url
        self.soup = BeautifulSoup(r.text, 'html.parser')

    def get_content(self, tag='p'):
        '''
            Extracts a list of Tag objects that match the given
            criteria and returns an object of type Document

            :param tag: the html elements to be extracted, defaults to paragraph
        '''
        text = ' '.join([p.get_text() for p in self.soup.find_all(tag)])
        return re.sub(' {2,}|\\n+', '', text)

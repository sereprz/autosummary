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
        self.raw = self.get_content()

    def get_content(self, tag='p'):
        '''
            Extracts a list of Tag objects that match the given
            criteria and returns an object of type Document

            :param tag: the html elements to be extracted, defaults to paragraph
        '''
        paragraphs = [p.get_text().strip() for p in self.soup.find_all(tag)
                      if len(p.get_text().strip()) > 1]
        text = ' '.join([p if p[-1] == '.' else p + '.' for p in paragraphs])
        return re.sub(' {2,}|\\n+', '', text)

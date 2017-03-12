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
        self.content = self.get_page_content()

    def get_page_content(self, tag='p'):
        '''
            Extracts a list of Tag objects that match the given
            criteria and returns the list of all child strings

            :param tag: the html elements to be extracted, defaults to paragraph
        '''
        return [p.get_text() for p in self.soup.find_all(tag)]

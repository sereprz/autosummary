import nltk
from nltk.tokenize import RegexpTokenizer

from autosummary.parser import PageParser

stopwords = nltk.corpus.stopwords.words('english')
tokenizer = RegexpTokenizer(r'\w+')


class Sentence():

    def __init__(self, text):

        self.text = text
        self.tokens = [w for w in tokenizer.tokenize(text) if w not in stopwords]
        self.length = len(self.tokens)


class Document():

    def __init__(self, text=None, url=None):

        if not url and not text:
            raise TypeError('Missing required argument: url or text')

        if url:
            parser = PageParser(url=url)
            text = parser.get_content()

        self.text = text

        sentences = nltk.sent_tokenize(text)
        self.sentences = [Sentence(s) for s in sentences]

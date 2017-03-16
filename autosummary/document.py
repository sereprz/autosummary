import re
import nltk
import numpy as np
from nltk.tokenize import RegexpTokenizer
from gensim.models import KeyedVectors

from autosummary.parser import PageParser

stopwords = nltk.corpus.stopwords.words('english')
tokenizer = RegexpTokenizer(r'\w+')

w2v = KeyedVectors.load_word2vec_format(
    fname='./data/GoogleNews-vectors-negative300.bin',
    binary=True)


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

        sentences = re.split('\\. *', text)
        self.sentences = [Sentence(s) for s in sentences]

    def summary(self, ratio=0.2):
        '''
            Summary of the document. Each sentence is scored and ranked based
            on the total Word Mover's Distance from every other sentence in the text

            :param ratio: float, proportion of sentences do be included in the
            summary
        '''
        scored = [(s.text, np.mean([w2v.wmdistance(s.text, s_.text)
                  for s_ in self.sentences]))
                  for s in self.sentences]
        ranked = sorted(scored, key=lambda x: x[1])
        return '\n'.join([s for s, r in ranked[:int(len(ranked)*ratio)]])

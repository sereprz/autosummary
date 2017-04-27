import re
import nltk
import numpy as np
from nltk import sent_tokenize, word_tokenize
from gensim.models import KeyedVectors
from scipy.spatial.distance import cosine

from autosummary.parser import PageParser

stopwords = nltk.corpus.stopwords.words('english')

w2v = KeyedVectors.load_word2vec_format(
    fname='./data/w2v-brown.bin',
    binary=True)


class Sentence():

    def __init__(self, text):

        self.text = text
        self.tokens = [w for w in word_tokenize(text) if w not in stopwords]
        self.vect = self.to_vector()

    def to_vector(self):
        '''
            Vector representation of a sentence as sum of all it's tokens in the
            word2vec space
        '''
        return np.mean([w2v[w] for w in self.tokens if w in w2v.vocab], axis=0)


class Document():

    def __init__(self, text=None, url=None):

        if not url and not text:
            raise TypeError('Missing required argument: url or text')

        if url:
            text = PageParser(url=url).raw

        self.text = text

        # split sentences and remove text between parentheses
        # (assuming it's not relevant)
        text = re.sub('\(.*?\)', '', text)
        sentences = sent_tokenize(text)
        self.sentences = dict(
            zip(range(len(sentences)), [Sentence(s) for s in sentences if len(s) > 1]))

    def pairwise_dist(self):
        '''
            Calculate matrix of pairwise cosine similarities between sentences
        '''
        n = len(self.sentences)
        m_dist = np.empty((n, n))

        for i in range(n):
            for j in range(i, n):
                if i == j:
                    m_dist[i, j] = 0
                else:
                    try:
                        m_dist[i, j] = cosine(self.sentences[i].vect, self.sentences[j].vect)
                    except:
                        m_dist[i, j] = 1
                    m_dist[j, i] = m_dist[i, j]
        return m_dist

    def summary(self, ratio=0.2):
        '''
            Summary of the document by extraction of key sentences.
            Each sentence is scored and ranked based on the total cosine
            distance from every other sentence in the text

            :param ratio: float, proportion of sentences do be included in the
            summary
        '''
        scored = zip(range(len(self.sentences)), np.sum(self.pairwise_dist(), axis=1))
        ranked = sorted(scored, key=lambda x: x[1])
        n_ = int(len(ranked) * ratio)
        top = sorted([t[0] for t in ranked[:(n_ if n_ > 0 else 1)]])
        return [self.sentences[i].text for i in top]

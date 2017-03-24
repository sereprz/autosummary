import re
import nltk
import numpy as np
from nltk.tokenize import RegexpTokenizer
from gensim.models import KeyedVectors
from scipy.spatial.distance import cosine

#from autosummary.parser import PageParser
from newspaper import Article

stopwords = nltk.corpus.stopwords.words('english')
w_tokenizer = RegexpTokenizer(r'\w+')
REGEX = re.compile(u'([^\u201c\u201d.]*)(\u201c[^\u201c\u201d]*\u201d)*([^\u201c\u201d.]*[.?!])')
sent_tokenizer = RegexpTokenizer(REGEX)

w2v = KeyedVectors.load_word2vec_format(
    fname='./data/GoogleNews-vectors-negative300.bin',
    binary=True)


class Sentence():

    def __init__(self, text):

        self.text = text
        self.tokens = [w for w in w_tokenizer.tokenize(text) if w not in stopwords]
        self.vect = self.to_vector()

    def to_vector(self):
        '''
            Vector representation of a sentence as sum of all it's tokens in the
            word2vec space
        '''
        return np.mean([w2v[w] for w in self.tokens if w in w2v.vocab])


class Document():

    def __init__(self, text=None, url=None):

        if not url and not text:
            raise TypeError('Missing required argument: url or text')

        if url:
            #parser = PageParser(url=url)
            #text = parser.get_content()
            a = Article(url)
            a.download()
            a.parse()
            text = a.text

        self.text = text

        # split sentences and remove text between parentheses
        # (assuming it's not relevant)
        #sentences = re.split('\\)*\\. *', re.sub('\(.*?\)', '', text))[:-1]
        text = re.sub('\(.*?\)', '', text)
        sentences = [''.join(grp).strip() for grp in sent_tokenizer.tokenize(text)]
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
                    m_dist[i, j] = cosine(self.sentences[i].vect, self.sentences[j].vect)
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
        return [value.text for key, value in self.sentences.items()
                if key in [i for (i, s) in ranked[:n_]]]

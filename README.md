# autosummary

A simple algorithm for summarising the content of web pages

## Extraction based summarisation

Words in the text are projected in a vector space using [Google's pre-trained word2vec](https://code.google.com/archive/p/word2vec/). Then the meaning of sentences is captured as the mean of the individual term vectors. The text is then represented as a fully connected weighted graph where sentences are nodes and edges between them are assigned a weight equal to the cosine distance between the sentence's vectors.

Each sentence is assigned an individual score given by the sum of distances from each other sentence in the text.

The final summary is built by ranking the sentences according to their final score and using the top 20%


### TODO
- [ ] improve parser
- [ ] code TextRank
- [x] text as input

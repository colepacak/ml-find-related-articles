import pandas as pd
import nltk
from nltk.stem.snowball import SnowballStemmer
import re
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

class tfidf:

    # instance props:
    # df_articles
    # tfidf_matrix - document/term matrix
    # feature_names - vector of terms, order matches tfidf_matrix

    def __init__(self, df_articles):
        self.df_articles = df_articles

        self.createTfidfMatrix()
        self.getRelatedArticles()
        self.getOrderedTerms()

        print(self.df_articles)

    def getStems(self, text):
        stopwords = nltk.corpus.stopwords.words('english')
        stemmer = SnowballStemmer("english")
        # First tokenize by sentence then by word to ensure that punctuation is caught as it's own token
        tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]

        # Filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
        # Filter our stopwords
        filtered_tokens = []
        for token in tokens:
            if re.search('[a-zA-Z]', token) and token not in stopwords:
                filtered_tokens.append(token)

        stems = [stemmer.stem(t) for t in filtered_tokens]
        return stems

    def createTfidfMatrix(self):
        tfidf_vectorizer = TfidfVectorizer(max_df=0.8, max_features=200000,
                                         min_df=0.2, stop_words='english',
                                         use_idf=True, tokenizer=self.getStems, ngram_range=(1,3))
        article_bodies = self.df_articles['body']
        tfidf_matrix_sparse = tfidf_vectorizer.fit_transform(article_bodies)
        self.tfidf_matrix = tfidf_matrix_sparse.toarray()
        self.feature_names = tfidf_vectorizer.get_feature_names()

    def getRelatedArticles(self):
        self.df_articles['related_articles'] = self.df_articles.apply(self.getRelatedArticlesByRow, axis=1)

    def getRelatedArticlesByRow(self, row):
        # Use current row as subject for comparison.
        subject_id = row.name
        subject_index = self.df_articles.index.get_loc(row.name)
        subject = self.tfidf_matrix[subject_index]

        # Calculate distances from subject to all articles.
        distances = np.sqrt(np.sum(np.power(subject - self.tfidf_matrix, 2), axis=1))
        # Create distances data frame for ordering and dropping subject
        article_ids = self.df_articles.index.values
        df_distances = pd.DataFrame(data=distances, index=article_ids, columns=['distance'])
        df_distances = df_distances.drop([subject_id])
        # Return a sorted list of of article indices for the current row.
        return df_distances.sort_values(by=['distance']).index.values.tolist()

    def getOrderedTerms(self):
        self.df_articles['ordered_terms'] = self.df_articles.apply(self.getOrderedTermsByRow, axis=1)

    def getOrderedTermsByRow(self, row):
        # Get location index of current row.
        index = self.df_articles.index.get_loc(row.name)
        # Sort - in descending order - the terms for the current row.
        ordered_term_indices = np.argsort(self.tfidf_matrix[index,:])[::-1][:5]
        result = list(map(lambda x: self.feature_names[x], ordered_term_indices))
        return result

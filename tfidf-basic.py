import sys
import pandas as pd
import RelatedArticles as RA

# Generate articles dataframe and then find related articles.
df_articles = pd.read_csv('./data/articles-basic.txt', index_col=0, names=['id','body'])
ra = RA.tfidf(df_articles)

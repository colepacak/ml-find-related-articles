import pandas as pd
import RelatedArticles as RA
import numpy as np

# Generate articles dataframe and then find related articles.
article_ids = open('./data/npr/article-ids.txt').read().split('\n')
article_titles = open('./data/npr/article-titles.txt').read().split('\n')
article_bodies = open('./data/npr/article-bodies.txt').read().split('\nBREAKS HERE')
# print article_ids
df_articles = pd.DataFrame({'body': article_bodies}, index=article_ids)
# Remove the new line at the end of the bodies file that is getting counted.
df_articles['body'].replace('\n', np.nan, inplace=True)
df_articles.dropna(subset=['body'], inplace=True)
ra = RA.tfidf(df_articles)

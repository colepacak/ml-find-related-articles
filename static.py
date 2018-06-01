import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Get subject id from command line argument
if __name__ == "__main__":
    subject_id = int(sys.argv[1])
    articles_data_path = sys.argv[2]
    article_profiles_data_path = sys.argv[3]

article_ids = np.loadtxt(articles_data_path, delimiter=',', dtype=int, usecols=(0))
article_profiles = np.loadtxt(article_profiles_data_path, delimiter=',')

# The subjects is the basis of comparision. In this case, it is one of the article profiles, and we will compare it to all of the other article profiles.
subject = article_profiles[subject_id - 1]
# TODO: turn this part into a module that takes args: subject (article profile vector), article_profiles (matrix), article ids (vector). Returns data frame of article ids ordered by distance.
distances = np.sqrt(np.sum(np.power(subject - article_profiles, 2), axis=1))

# Create dataframe and remove subject
df = pd.DataFrame(data=distances, index=article_ids, columns=['distance'])
df = df.drop([subject_id])

print 'Articles ordered by distance from subject: {subject_id}'.format(subject_id=subject_id)
print df.sort_values(by=['distance'])

# Plot - currently only works for 2D.
plt.scatter(article_profiles[:,0], article_profiles[:,1])
for label, x, y in zip(article_ids, article_profiles[:,0], article_profiles[:,1]):
    plt.annotate('%s' % label, xy=(x, y))
plt.xlim(0, 1)
plt.ylim(0, 1)
plt.gca().set_aspect('equal', adjustable='box')
plt.show()

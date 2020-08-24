import pandas as pd

df = pd.read_csv('data/ode_test_10k_w_source.csv')

sources = df['source'].unique()
distrib_sources = df.source.value_counts()

distrib_titles = df.title.value_counts()
distrib_titles = distrib_titles[distrib_titles>1]

distrib = pd.DataFrame(sources[sources['title']distrib_titles)

print(distrib)
import pandas as pd
import numpy as np

# reading in csv files
user_anime = pd.read_csv("anime_data/UserAnimeListTrimmed.csv", usecols=['username', 'anime_id', 'my_score'],
    dtype={'username': str, 'anime_id': int, 'my_score': float})

animes = pd.read_csv("anime_data/AnimeListTrimmed.csv", usecols=['anime_id', 'title', 'image_url', 'genre'],
    dtype={'anime_id': int, 'title': str, 'image_url': str, 'genre': str})

# merging animes and user_anime
joined_df = pd.merge(user_anime, animes, on='anime_id', how='inner')

# reducing the dataframe to the top 1000 users based off the # of scores
agg_scores = joined_df.groupby('username').agg(num_scores = ('my_score', 'count')).reset_index()
agg_scores = agg_scores.sort_values('num_scores', ascending=False)
agg_scores = agg_scores[0:1000]

joined_df_cleaned = pd.merge(joined_df, agg_scores[['username']], on='username', how='inner')

# creating the matrix of animes and user scores and normalizing scores
matrix = joined_df_cleaned.pivot_table(index="username", columns='title', values='my_score')

matrix = matrix.subtract(matrix.mean(axis=1), axis='rows')
matrix = matrix.divide(matrix.std(axis=1), axis='rows')

# creating the adjacency matrix of user similarity scores
user_similarity = matrix.T.corr()

# dropping diagonal values
np.fill_diagonal(user_similarity.values, 0.0)
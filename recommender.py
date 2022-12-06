import pandas as pd
import numpy as np

# base user: list of animes that base user has watched
# most_similar_users: dictionary of most similar users to base user w/ similarity scores
def anime_recommender(base_user, most_similar_users, similarity_graph):
    # creating dictionary of animes
    animes = {}
    for user in most_similar_users.keys():
        for anime in similarity_graph[user][1].keys():
            # ignore animes already watched by base user
            if anime in base_user:
                continue
            # add anime to dictionary and multiply similarity score by user rating
            if anime not in animes.keys():
                animes[anime] = [most_similar_users[user] * similarity_graph[user][1][anime], 1]
            else:
                animes[anime][0] += most_similar_users[user] * similarity_graph[user][1][anime]
                animes[anime][1] += 1
    # create dataframe of summed weighted scores and count
    anime_df = pd.DataFrame(data=animes, index=['sum_score', 'count'])
    anime_df = anime_df.transpose()
    # calculate weighted average rating for all animes
    anime_df['weighted_averages'] = anime_df['sum_score'] / anime_df['count']
    # extract top 5 rated animes and return it as a list
    recommendations = anime_df.sort_values(by='weighted_averages', ascending=False)[0:5]
    rec_animes = list(recommendations.index)
    return(rec_animes)

def similarity_matrix_generator(user_prefs_df):
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
    matrix = pd.concat([matrix, user_prefs_df])

    # creating the adjacency matrix of user similarity scores
    user_similarity = matrix.T.corr()

    # dropping diagonal values
    np.fill_diagonal(user_similarity.values, 0.0)

    return user_similarity, matrix

def create_user_df(user_rated_animes, user_ratings):
    # convert user input into dictionary then DataFrame of user scores
    user_prefs = {'username':['sample_base_user'] * len(user_rated_animes), 'title': user_rated_animes, 'my_score': user_ratings}
    user_prefs_df = pd.DataFrame(data=user_prefs)
    user_prefs_df = user_prefs_df.pivot_table(index="username", columns='title', values='my_score')

    # normalize user scores
    user_prefs_df = user_prefs_df.subtract(user_prefs_df.mean(axis=1), axis='rows')
    user_prefs_df = user_prefs_df.divide(user_prefs_df.std(axis=1), axis='rows')

    return(user_prefs_df)
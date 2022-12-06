import pandas as pd

anime_info = pd.read_csv("src/anime_filtered_modified.csv", usecols=['title', 'genre'], dtype={'title': str, 'genre': str})

import pandas as pd
import ast
import pickle

# Load raw CSVs
movies_df = pd.read_csv('data/tmdb_5000_movies.csv')
credits_df = pd.read_csv('data/tmdb_5000_credits.csv')

# Merge on title
movies = movies_df.merge(credits_df, on='title')

# Keep only needed columns
movies = movies[['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]

# Convert stringified lists to Python objects
for col in ['genres', 'keywords', 'cast', 'crew']:
    movies[col] = movies[col].apply(ast.literal_eval)

# Extract genre names
movies['genres'] = movies['genres'].apply(lambda x: [i['name'] for i in x])

# Build tags column (used for recommendation)
movies['overview'] = movies['overview'].fillna('')
movies['tags'] = movies['overview'] + ' ' + movies['genres'].astype(str)

# Keep only relevant columns
final_movies = movies[['movie_id', 'title', 'genres', 'tags']]

# Save to .pkl
with open('model/movies.pkl', 'wb') as f:
    pickle.dump(final_movies, f)

print("✅ movies.pkl rebuilt and saved with genres")

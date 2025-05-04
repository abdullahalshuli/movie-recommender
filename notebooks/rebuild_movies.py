import pandas as pd
import ast
import pickle

# 1. Load the CSVs (adjust path if needed)
movies_df = pd.read_csv('data/tmdb_5000_movies.csv')
credits_df = pd.read_csv('data/tmdb_5000_credits.csv')

# 2. Merge them using the 'title' column
movies = movies_df.merge(credits_df, on='title')

# 3. Keep only the useful columns
movies = movies[['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]

# 4. Convert stringified JSON lists into real Python lists
for col in ['genres', 'keywords', 'cast', 'crew']:
    movies[col] = movies[col].apply(ast.literal_eval)

# 5. Extract genre names (['Action', 'Drama'], etc.)
movies['genres'] = movies['genres'].apply(lambda x: [i['name'] for i in x])

# ✅ Optional: add 'tags' column for recommendation model
movies['tags'] = movies['overview'] + ' ' + movies['genres'].astype(str)

# 6. Save the cleaned dataframe to model/movies.pkl
with open('model/movies.pkl', 'wb') as f:
    pickle.dump(movies, f)

print("✅ movies.pkl rebuilt and saved.")

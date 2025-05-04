import streamlit as st
import pickle
import pandas as pd
import requests
import os



from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load or rebuild data
movies = pickle.load(open("model/movies.pkl", "rb"))

similarity_path = "model/similarity.pkl"

if os.path.exists(similarity_path):
    similarity = pickle.load(open(similarity_path, "rb"))
else:
    cv = CountVectorizer(max_features=5000, stop_words='english')
    vectors = cv.fit_transform(movies['tags']).toarray()
    similarity = cosine_similarity(vectors)
    pickle.dump(similarity, open(similarity_path, "wb"))

# ✅ Now safely inspect genres
st.write(movies.columns)


similarity_path = "model/similarity.pkl"

if os.path.exists(similarity_path):
    similarity = pickle.load(open(similarity_path, "rb"))
else:
    cv = CountVectorizer(max_features=5000, stop_words='english')
    vectors = cv.fit_transform(movies['tags']).toarray()
    similarity = cosine_similarity(vectors)
    pickle.dump(similarity, open(similarity_path, "wb"))

import os
API_KEY = os.environ.get("TMDB_API_KEY")

def fetch_poster(movie_id):
    if not API_KEY:
        return "https://via.placeholder.com/150?text=Missing+API+Key"

    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
        response = requests.get(url)
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500" + poster_path
    except:
        pass
    
    return "https://via.placeholder.com/150?text=No+Poster"

# Load saved movie data and similarity matrix
movies = pickle.load(open('model/movies.pkl', 'rb'))
similarity = pickle.load(open('model/similarity.pkl', 'rb'))

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = list(enumerate(similarity[index]))
    movies_list = sorted(distances, key=lambda x: x[1], reverse=True)[1:11]

    recommended_titles = []
    recommended_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_titles.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_titles, recommended_posters

# Streamlit UI
st.title("🎬 Movie Recommender System")

# Generate list of all unique genres
all_genres = sorted(set(genre for sublist in movies['genres'] for genre in sublist))

# Genre filter
selected_genre = st.selectbox("Filter by Genre", ["All"] + all_genres)

# Movie selector based on genre
if selected_genre == "All":
    filtered_movies = movies['title'].values
else:
    filtered_movies = movies[movies['genres'].apply(lambda x: selected_genre in x)]['title'].values

movie_name = st.selectbox("Choose a movie", filtered_movies)

if st.button("Recommend"):
    names, posters = recommend(movie_name)

    cols_per_row = 5
    for i in range(0, len(names), cols_per_row):
        cols = st.columns(cols_per_row)
        for j in range(cols_per_row):
            if i + j < len(names):
                with cols[j]:
                    st.image(posters[i + j])
                    st.caption(names[i + j])

  

import streamlit as st
import pickle
import pandas as pd
import requests
import os
import random

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

movies = pickle.load(open("model/movies.pkl", "rb"))

similarity_path = "model/similarity.pkl"

if "selected_movie" not in st.session_state:
    st.session_state.selected_movie = ""
if "base_movie" not in st.session_state:
    st.session_state.base_movie = ""
if "recommendations" not in st.session_state:
    st.session_state.recommendations = {"names": [], "posters": [], "trailers": []}

if os.path.exists(similarity_path):
    similarity = pickle.load(open(similarity_path, "rb"))
else:
    cv = CountVectorizer(max_features=5000, stop_words='english')
    vectors = cv.fit_transform(movies['tags']).toarray()
    similarity = cosine_similarity(vectors)
    pickle.dump(similarity, open(similarity_path, "wb"))

import os, streamlit as st
API_KEY = os.environ.get("API_KEY") or st.secrets["API_KEY"]

def fetch_movie_details(movie_id):
    if not API_KEY:
        return {
            "poster": "https://via.placeholder.com/150?text=Missing+API+Key",
            "rating": "N/A",
            "genres": [],
            "imdb_id": None
        }

    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
        response = requests.get(url)
        data = response.json()

        poster_path = data.get('poster_path')
        rating = data.get('vote_average')
        genres = [genre['name'] for genre in data.get('genres', [])]
        imdb_id = data.get('imdb_id')

        poster_url = "https://image.tmdb.org/t/p/w500" + poster_path if poster_path else "https://via.placeholder.com/150?text=No+Poster"

        return {
            "poster": poster_url,
            "rating": rating,
            "genres": genres,
            "imdb_id": imdb_id
        }
    except:
        return {
            "poster": "https://via.placeholder.com/150?text=Error",
            "rating": "N/A",
            "genres": [],
            "imdb_id": None
        }

def fetch_trailer(movie_id): 
    if not API_KEY:
        return None

    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={API_KEY}&language=en-US"
        response = requests.get(url)
        data = response.json()
        videos = data.get('results', [])

        for video in videos:
            if video['site'] == 'YouTube' and video['type'] == 'Trailer':
                return f"https://www.youtube.com/watch?v={video['key']}"
    except:
        pass

    return None

movies = pickle.load(open('model/movies.pkl', 'rb'))
similarity = pickle.load(open('model/similarity.pkl', 'rb'))

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = list(enumerate(similarity[index]))
    distances = sorted(distances, key=lambda x: x[1], reverse=True)[1:]
    random.shuffle(distances)
    movies_list = distances[:10]

    recommended_titles = []
    recommended_posters = []
    recommended_trailers = []
    recommended_ratings = []
    recommended_genres = []
    recommended_links = []
    recommended_imdb = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_titles.append(movies.iloc[i[0]].title)

        details = fetch_movie_details(movie_id)

        recommended_posters.append(details["poster"])
        recommended_ratings.append(details["rating"])
        recommended_genres.append(details["genres"])
        recommended_trailers.append(fetch_trailer(movie_id))

        recommended_links.append(f"https://www.themoviedb.org/movie/{movie_id}")
        imdb_id = details.get("imdb_id")
        recommended_imdb.append(f"https://www.imdb.com/title/{imdb_id}" if imdb_id else "")

    return (
        recommended_titles,
        recommended_posters,
        recommended_trailers,
        recommended_ratings,
        recommended_genres,
        recommended_links,
        recommended_imdb
    )

st.title("🎬 Movie Recommender System")

all_genres = sorted(set(genre for sublist in movies['genres'] for genre in sublist))

selected_genre = st.selectbox("Filter by Genre", ["All"] + all_genres)

if selected_genre == "All":
    filtered_movies = movies['title'].values
else:
    filtered_movies = movies[movies['genres'].apply(lambda x: selected_genre in x)]['title'].values

if "selected_movie" not in st.session_state:
    st.session_state.selected_movie = filtered_movies[0]  

if "favorites" not in st.session_state:
    if os.path.exists("favorites.txt"):
        with open("favorites.txt", "r") as f:
            st.session_state.favorites = [line.strip() for line in f.readlines()]
    else:
        st.session_state.favorites = []

movie_name = st.selectbox(
    "Choose a movie", 
    filtered_movies, 
    index=filtered_movies.tolist().index(st.session_state.selected_movie) if st.session_state.selected_movie in filtered_movies else 0
)
col1, col2 = st.columns(2)

names = []
posters = []
trailers = []

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🎯 Recommend", key="recommend"):
        st.session_state.selected_movie = movie_name
        st.session_state.base_movie = movie_name
        names, posters, trailers, ratings, genres, links, imdb_links = recommend(movie_name)
        st.session_state.recommendations = {
    "names": names,
    "posters": posters,
    "trailers": trailers,
    "ratings": ratings,
    "genres": genres,
    "links": links,
    "imdb": imdb_links
}

with col2:
    if st.button("🎲 Surprise Me", key="surprise"):
        random_movie = random.choice(filtered_movies)
        st.session_state.selected_movie = random_movie
        st.session_state.base_movie = random_movie
        st.info(f"Randomly selected: **{random_movie}**")
        names, posters, trailers, ratings, genres, links, imdb_links = recommend(movie_name)
        st.session_state.recommendations = {
    "names": names,
    "posters": posters,
    "trailers": trailers,
    "ratings": ratings,
    "genres": genres,
    "links": links,
    "imdb": imdb_links
}

with col3:
    if (
        "recommendations" in st.session_state and
        st.session_state.recommendations.get("names")
    ):
        if st.button("🔄 Shuffle Again", key="shuffle_top"):
            movie_name = st.session_state.base_movie
            names, posters, trailers, ratings, genres, links, imdb_links = recommend(movie_name)
            st.session_state.recommendations = {
    "names": names,
    "posters": posters,
    "trailers": trailers,
    "ratings": ratings,
    "genres": genres,
    "links": links,
    "imdb": imdb_links
}

if st.session_state.recommendations["names"]:
    names = st.session_state.recommendations["names"]
    posters = st.session_state.recommendations["posters"]
    trailers = st.session_state.recommendations["trailers"]
    ratings = st.session_state.recommendations["ratings"]
    genres = st.session_state.recommendations["genres"]
    links = st.session_state.recommendations["links"]
    imdb_links = st.session_state.recommendations["imdb"]

    selected_movie = st.session_state.base_movie
    st.subheader(f"🎥 Selected Movie: {selected_movie}")
    selected_index = movies[movies['title'] == selected_movie].index[0]
    selected_id = movies.iloc[selected_index].movie_id
    selected_poster = fetch_movie_details(selected_id)["poster"]
    selected_trailer = fetch_trailer(selected_id)

    col_main = st.columns(1)[0]
    col_main.image(selected_poster)
    col_main.caption(selected_movie)

    if selected_trailer:
        col_main.video(selected_trailer)

    st.markdown("---")
    st.subheader("🎬 Recommended Movies")

    cols_per_row = 5
    for i in range(0, len(names), cols_per_row):
        cols = st.columns(cols_per_row)
        for j in range(cols_per_row):
            idx = i + j
            if idx < len(names):
                with cols[j]:
                    st.image(posters[idx])
                    st.markdown(f"**{names[idx]}**")
                    st.markdown(f"⭐ **{ratings[idx]}**  \n🎭 *{', '.join(genres[idx])}*")
                    if trailers[idx]:
                        st.video(trailers[idx])
                        st.markdown(
    f"[🔗 TMDb]({links[idx]}) &nbsp;|&nbsp; [🎬 IMDb]({imdb_links[idx]})",
    unsafe_allow_html=True
)

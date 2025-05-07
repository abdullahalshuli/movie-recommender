# Movie Recommender System

An interactive movie recommendation app built with **Streamlit**, using content-based filtering and the **TMDb API**. 

Choose a movie, filter by genre, get intelligent recommendations, and view posters, trailers, ratings, genres, and links to both **TMDb** and **IMDb**. You can also save favorites that persist between sessions.

---

## Features

- **Select a movie** and get 10 similar recommendations  
- **Surprise Me**: random movie recommendations  
- **Shuffle Again**: re-roll similar movies from your selected base  
- **Posters & YouTube Trailers** embedded  
- **IMDb Ratings** and **Genres**  
- Links to **TMDb** and **IMDb** for each recommendation  
- **Favorites** section that saves across sessions (using `favorites.txt`)  
- **Remove from Favorites** with one click  

---

## Demo
https://movie-matchmaker.streamlit.app/
---

## Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/your-username/movie-recommender.git
cd movie-recommender
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Add your TMDb API key

Open `app.py`, find the line:

```python
API_KEY = "your_tmdb_api_key"
```

And replace it with your real TMDb API key. [Get one here](https://developer.themoviedb.org/docs/authentication).

### 4. Run the app

```bash
streamlit run app.py
```

---

## Project Structure

```
movie-recommender/
├── app.py
├── model/
│   ├── movies.pkl
│   └── similarity.pkl
├── favorites.txt
├── requirements.txt
└── README.md
```

---

## Requirements

- Python 3.10+
- Streamlit
- pandas, scikit-learn, requests, etc.

---

## How it Works

This app uses **content-based filtering**:
- Each movie’s metadata is transformed into tags
- A **CountVectorizer** encodes the tags
- **Cosine similarity** finds the closest matches

---

## License

MIT — free to use and modify.

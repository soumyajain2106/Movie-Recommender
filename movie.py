import streamlit as st
import pickle
import pandas as pd
import requests

# -------------------- CONFIG --------------------
st.set_page_config(page_title="Movie Recommender", layout="wide")

OMDB_API_KEY = "7784a19"  # 🔑 Put your OMDb API key here

# -------------------- LOAD DATA --------------------
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# -------------------- FETCH POSTER FUNCTION --------------------
def fetch_poster(movie_title):
    movie_title = movie_title.strip()

    url = f"http://www.omdbapi.com/?t={movie_title}&apikey={OMDB_API_KEY}"

    try:
        response = requests.get(url)
        data = response.json()

        if data.get("Response") == "True" and data.get("Poster") != "N/A":
            return data.get("Poster")
        else:
            return None
    except:
        return None


# -------------------- RECOMMENDATION FUNCTION --------------------
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_names = []
    recommended_posters = []

    for i in movies_list:
        title = movies.iloc[i[0]].title
        recommended_names.append(title)
        recommended_posters.append(fetch_poster(title))

    return recommended_names, recommended_posters


# -------------------- UI --------------------
st.title("🎬 Movie Recommender System - Because You Have Great Taste ❤️")

selected_movie = st.selectbox(
    "Select a movie",
    movies['title'].values
)

if st.button("Recommend 🎥"):

    names, posters = recommend(selected_movie)

    cols = st.columns(5)

    for idx in range(5):
        with cols[idx]:
            if posters[idx]:
                st.image(posters[idx], use_container_width=True)
            else:
                st.write("Poster not available")
            st.caption(names[idx])

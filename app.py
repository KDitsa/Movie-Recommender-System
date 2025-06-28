import streamlit as st
from utils.poster_api import get_poster_url
import pandas as pd
import numpy as np

df = pd.read_pickle('./models/movies.pkl')
similarity = pd.read_csv('./models/similarityMat.csv')

st.set_page_config(page_title="Movie Recommender System", layout="wide")
st.markdown("""
    <style>
        body {
            background-color: #0f0f0f;
            color: #ffffff;
        }
        .title {
            font-size: 3em;
            font-weight: bold;
            text-align: center;
            margin-bottom: 20px;
            color: #FF4B4B;
        }
        .movie-card {
            background-color: #FFFFFF;
            padding: 20px;
            border-radius: 15px;
            margin: 10px;
            text-align: center;
        }
        .movie-title {
            font-size: 1.2em;
            color: #1e1e1e;
            text-align: center;
        }
        img {
            border-radius: 10px;
            width: 100%;
            height: auto;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🍿 Movie Recommender System")
col1, col2 = st.columns([3, 1])
with col1:
    selected_movie = st.selectbox(
        "🎥 Pick a movie you like",
        df['title'].values,
        index=0
    )

with col2:
    top_n = st.number_input(
        "🔢 How many recommendations?",
        min_value=1,
        max_value=30,
        value=5
    )

def recommend(movie,top_n):
    matched = df[df['title'] == movie]
    if matched.empty:
        print("it is not in database")
        return
    movie_index = matched.index[0]
    distances = np.array(similarity.iloc[movie_index])
    top_n += 1
    movie_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:top_n]
    recommended_titles = [df.iloc[i[0]].title for i in movie_list]
    return recommended_titles

if st.button("✨ Recommend Similar Movies"):
    recommendations = recommend(selected_movie,top_n)
    if recommendations:
        cols = st.columns(len(recommendations))
        for idx, title in enumerate(recommendations):
            poster_url = get_poster_url(title)
            with cols[idx]:
                st.markdown('<div class="movie-card">', unsafe_allow_html=True)
                if poster_url:
                    st.image(poster_url)
                else:
                    st.image("https://via.placeholder.com/200x300?text=No+Image")
                st.markdown(f"<div class='movie-title'>{title}</div>", unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("No recommendations found.")
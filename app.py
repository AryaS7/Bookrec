import streamlit as st
import pickle
import numpy as np
import pandas as pd

# Load the data
popular_df = pd.read_pickle('popular.pkl')
pt = pd.read_pickle('pt.pkl')
books = pd.read_pickle('books.pkl')
similarity_scores = pd.read_pickle('similarity_scores.pkl')

# Streamlit App Configuration
st.set_page_config(page_title="Book Recommendation System", layout="wide")

# Custom CSS for better styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');
    body {
        font-family: 'Montserrat', sans-serif;
        background-color: #333333; /* Updated to grey */
        color: #FFA500;
    }
    .main-header {
        color: #FFA500;
        text-align: center;
        font-size: 3em;
        font-weight: bold;
        margin-bottom: 20px;
    }
    .sub-header {
        color: #FFA500;
        font-size: 2em;
        font-weight: bold;
        margin-top: 50px;
        margin-bottom: 20px;
    }
    .book-title {
        font-size: 1.2em;
        font-weight: bold;
        color: #FFA500;
    }
    .author {
        color: #FFA500;
    }
    .rating {
        color: #FFA500;
    }
    .book-container {
        background-color: #333333;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
        transition: transform 0.2s;
    }
    .book-container:hover {
        transform: scale(1.05);
    }
    .recommendation-container {
        margin-top: 30px;
    }
    .input-container {
        margin-bottom: 30px;
        display: flex;
        justify-content: center;
    }
    .text-input {
        width: 50%;
        padding: 10px;
        border: 2px solid #FFA500;
        border-radius: 5px;
        font-size: 1em;
    }
    .recommend-button {
        background-color: #FFA500;
        color: #ffffff;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        font-size: 1em;
        cursor: pointer;
        transition: background-color 0.2s;
    }
    .recommend-button:hover {
        background-color: #cc8400;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="main-header">Book Recommendation System</div>', unsafe_allow_html=True)

# Recommendation Section
st.markdown('<div class="sub-header">Recommend Books</div>', unsafe_allow_html=True)
st.markdown('<div class="input-container">', unsafe_allow_html=True)
user_input = st.text_input('', placeholder='Enter book title here...', key='user_input')
st.markdown('</div>', unsafe_allow_html=True)

if st.button('Recommend', key='recommend_button'):
    try:
        index = np.where(pt.index == user_input)[0][0]
        similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:6]

        st.markdown(f'<div class="sub-header recommendation-container">Books similar to <i>{user_input}</i>:</div>', unsafe_allow_html=True)
        for i in range(0, len(similar_items), 3):
            cols = st.columns(3)
            for j, col in enumerate(cols):
                if i + j < len(similar_items):
                    item = similar_items[i + j]
                    temp_df = books[books['Book-Title'] == pt.index[item[0]]].drop_duplicates('Book-Title')
                    with col:
                        st.markdown('<div class="book-container">', unsafe_allow_html=True)
                        st.image(temp_df['Image-URL-M'].values[0], width=150)
                        st.markdown(f'<div class="book-title">{temp_df["Book-Title"].values[0]}</div>', unsafe_allow_html=True)
                        st.markdown(f'<div class="author">by {temp_df["Book-Author"].values[0]}</div>', unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)
    except IndexError:
        st.write("Book not found. Please enter a valid book title.")

# Popular Books Section
st.markdown('<div class="sub-header">Popular Books</div>', unsafe_allow_html=True)
for i in range(0, len(popular_df), 3):
    cols = st.columns(3)
    for j, col in enumerate(cols):
        if i + j < len(popular_df):
            with col:
                st.markdown('<div class="book-container">', unsafe_allow_html=True)
                st.image(popular_df['Image-URL-M'].values[i + j], width=150)
                st.markdown(f'<div class="book-title">{popular_df["Book-Title"].values[i + j]}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="author">by {popular_df["Book-Author"].values[i + j]}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="rating">Rating: {popular_df["avg_rating"].values[i + j]} ({popular_df["num_ratings"].values[i + j]} votes)</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)








import requests
import streamlit as st
import pickle
import pandas as pd
import os

# Configure the page
st.set_page_config(
    page_title="Movie Recommender System",
    page_icon="🎬",
    layout="wide"
)

def fetch_poster(movie_id):
    try:
        api_key = os.getenv("TMDB_API_KEY", "32093a00302155e261380888da3fdfee")
        response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}", timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if 'poster_path' in data and data['poster_path']:
            poster_path = data['poster_path']
            full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
            return full_path
        else:
            return "https://via.placeholder.com/300x450?text=No+Image"
    except Exception as e:
        return "https://via.placeholder.com/300x450?text=No+Image"

def recommend(movie):
    try:
        movie_index = movies[movies["title"] == movie].index[0]
        distances = similarity[movie_index]
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
        
        recommended_movies = []
        recommended_movies_poster = []

        for i in movies_list:
            movie_id = movies.iloc[i[0]].movie_id
            recommended_movies.append(movies.iloc[i[0]].title)
            recommended_movies_poster.append(fetch_poster(movie_id))
        
        return recommended_movies, recommended_movies_poster
    except Exception as e:
        st.error(f"Error generating recommendations: {str(e)}")
        return [], []

# Load data with error handling
@st.cache_data
def load_data():
    try:
        if not os.path.exists("movie_dict.pkl"):
            st.error("movie_dict.pkl file not found!")
            return None, None
        if not os.path.exists("similarity.pkl"):
            st.error("similarity.pkl file not found!")
            return None, None
            
        movies_dict = pickle.load(open("movie_dict.pkl", "rb"))
        movies = pd.DataFrame(movies_dict)
        similarity = pickle.load(open("similarity.pkl", "rb"))
        
        return movies, similarity
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None, None

# Streamlit app
st.title("🎬 Movie Recommender System")
st.markdown("Discover your next favorite movie based on your preferences!")

# Load data
with st.spinner("Loading movie data..."):
    movies, similarity = load_data()

if movies is None or similarity is None:
    st.error("Could not load movie data. Please check if the pickle files are present.")
    st.stop()

if len(movies) == 0:
    st.error("No movies data available!")
    st.stop()

st.success(f"Loaded {len(movies)} movies successfully!")

st.markdown("---")

selected_movie_name = st.selectbox(
    "🎭 Type or select a movie", 
    movies["title"].values,
    help="Choose a movie you like to get personalized recommendations"
)

if st.button('🔍 Show Recommendations', type="primary"):
    with st.spinner('Finding your perfect movie matches...'):
        recommended_movie_names, recommended_movie_posters = recommend(selected_movie_name)
    
    if recommended_movie_names:
        st.success(f"Here are 5 movies similar to '{selected_movie_name}':")
        
        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.text(recommended_movie_names[0])
            st.image(recommended_movie_posters[0])

        with col2:
            st.text(recommended_movie_names[1])
            st.image(recommended_movie_posters[1])

        with col3:
            st.text(recommended_movie_names[2])
            st.image(recommended_movie_posters[2])

        with col4:
            st.text(recommended_movie_names[3])
            st.image(recommended_movie_posters[3])

        with col5:
            st.text(recommended_movie_names[4])
            st.image(recommended_movie_posters[4])
    else:
        st.error("Could not generate recommendations. Please try again.")

st.markdown("---")
st.markdown("Built with ❤️ using Streamlit")

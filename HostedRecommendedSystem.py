import pickle 
import streamlit as st 
import requests 
import pandas as pd

class MovieRecommendationSystem:
    def __init__(self, movies_file='pickle_dataset/film_list.pkl', similarity_file='pickle_dataset/similarity.pkl'):
        self.movies = pd.read_pickle(movies_file)
        self.similarity = pd.read_pickle(similarity_file)

    def get_poster(self, movie_id):
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=ec7412101cbdcc83162c3829936b4f67"
        data = requests.get(url).json()
        poster_path = data['poster_path']
        return f"https://image.tmdb.org/t/p/w185{poster_path}"

    def recommend(self, movie):
        index = self.movies[self.movies['title'] == movie].index[0]
        distances = sorted(list(enumerate(self.similarity[index])), reverse=True, key=lambda x: x[1])
        recommended_movies = []
        for i in distances[1:6]:
            movie_id = self.movies.iloc[i[0]]['movie_id']
            recommended_movies.append({
                'title': self.movies.iloc[i[0]]['title'],
                'poster': self.get_poster(movie_id)
            })
        return recommended_movies

class UserInterface:
    def __init__(self, recommendation_system):
        self.recommendation_system = recommendation_system

    def run(self):
        st.header("Movies Recommendation System Using Machine Learning")
        movie_list = self.recommendation_system.movies['title'].values
        selected_movie = st.selectbox(
            'Type or Select a Movie to get recommendation',
            movie_list
        )
        if st.button('Show Recommendation'):
            recommended_movies = self.recommendation_system.recommend(selected_movie)
            c1, c2, c3, c4, c5 = st.columns(5)
            for movie in recommended_movies:
                c1.image(movie['poster'], width=120)
                c1.write(movie['title'])
                c1 = c2
                c2 = c3
                c3 = c4
                c4 = c5
                c5 = st.columns(1)[0]

if __name__ == "__main__":
    recommendation_system = MovieRecommendationSystem()
    ui = UserInterface(recommendation_system)
    ui.run()
    
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Load Datasets
movies = pd.read_csv('movies.csv')
ratings = pd.read_csv('ratings.csv')
data = pd.merge(ratings, movies, on='movieId')
data = data[['userId', 'title', 'rating']]

# Create pivot table
rating_matrix = data.pivot_table(index='userId', columns='title', values='rating')
rating_matrix.fillna(0, inplace=True)

# Calculate cosine similarity
similarity_matrix = cosine_similarity(rating_matrix.T)
similarity_df = pd.DataFrame(similarity_matrix, index=rating_matrix.columns, columns=rating_matrix.columns)

# Recommendation function
def recommend_movies(movie_title, num_recommendations=5):
    if movie_title not in similarity_df.columns:
        print("Movie not found")
        return []
    similar_scores = similarity_df[movie_title].sort_values(ascending=False)
    recommendations = similar_scores.iloc[1: num_recommendations + 1]
    return recommendations

# Example Usage
movie_title = 'Toy Story (1995)'
print(f"Recommendations for '{movie_title}': ")
movie_recommendations = recommend_movies(movie_title)
print(movie_recommendations)

# Saving to csv
movie_recommendations.to_csv('movie_recommendation.csv', index=True)

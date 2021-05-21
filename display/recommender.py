import numpy as np
import pandas.io.sql as sqlio
import psycopg2


def recommend(movie_user_likes, cosine_sim):
    with psycopg2.connect(user="PyCharm", password="123456", database="Movie Rec") as connection:
        cmd = '''SELECT * FROM "Everything";'''
        df = sqlio.read_sql_query(cmd, connection)

    # cosine_sim = np.load('D:\\Documents\\Python\\movieRec\\similarity.npy')

    def get_index_from_title(title):
        return df[df.Title == title].index.values[0]

    movie_index = get_index_from_title(movie_user_likes)
    similar_movies = list(enumerate(cosine_sim[movie_index]))
    sorted_similar_movies = sorted(similar_movies, key=lambda x: x[1], reverse=True)

    recommendations = [(df[df.index == i[0]]["Title"].values[0], df[df.index == i[0]]["Image URL"].values[0],
                        df[df.index == i[0]]["IMDB ID"].values[0]) for i in sorted_similar_movies[1:6]]
    return recommendations


if __name__ == '__main__':
    print(recommend('PK'))

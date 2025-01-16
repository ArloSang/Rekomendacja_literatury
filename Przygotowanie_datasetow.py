
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

books = pd.read_csv('data/Books.csv')
#st.write(books.head(2))
#st.write(books.shape)
# print(books.columns)
books = books[['ISBN', 'Book-Title', 'Book-Author', 'Year-Of-Publication', 'Publisher', 'Image-URL-L']]
# print(books.head(2))

books.rename(columns={
    "Book-Title": "title", 
    "Book-Author":"author", 
    'Year-Of-Publication':"year", 
    'Publisher':"publisher", 
    'Image-URL-L':"img_url"}, inplace = True)


users = pd.read_csv('data/Users.csv')
# print(users.head())

ratings = pd.read_csv('data/Ratings.csv')
# print(ratings.head())

ratings.rename(columns={
    "User-ID": "user_id", 
    "Book-Rating":"rating"}, inplace = True)

# print(books.shape, users.shape, ratings.shape)

# print(ratings['user_id'].value_counts())

x = ratings['user_id'].value_counts() > 200
y = x[x].index
ratings = ratings[ratings['user_id'].isin(y)]
# print(ratings.head())
rating_books = ratings.merge(books, on = 'ISBN')
# print(rating_books.head())

num_rating = rating_books.groupby('title')['rating'].count().reset_index()
#print(num_rating.sort_values(by=['rating'], ascending=False))

num_rating.rename(columns={"rating":"number_of_ratings"}, inplace=True)

final_rating = rating_books.merge(num_rating, on="title")

final_rating = final_rating[final_rating['number_of_ratings']>=50]

final_rating.drop_duplicates(['user_id','title'], inplace=True)

#print(final_rating.sort_values(by=['number_of_ratings'], ascending=False))
# print(final_rating.shape)
ilosc_recenzji = final_rating[['ISBN','title', 'number_of_ratings', 'img_url']]
ilosc_recenzji.drop_duplicates(['title','number_of_ratings'], inplace=True)
# print(ilosc_recenzji.sort_values(by=['number_of_ratings'], ascending=False))
book_pivot = final_rating.pivot_table(columns='user_id', index='title', values='rating')
book_pivot.fillna(0, inplace=True) 

from scipy.sparse import csr_matrix
book_sparse = csr_matrix(book_pivot)

from sklearn.neighbors import NearestNeighbors
model = NearestNeighbors(algorithm='brute')

model.fit(book_sparse)

distance, suggestion = model.kneighbors(book_pivot.iloc[237,:].values.reshape(1,-1), n_neighbors=6)
# print(distance, suggestion)

# for i in range(len(suggestion)):
#     print(book_pivot.index[suggestion[i]])

books_name = book_pivot.index

import pickle
pickle.dump(ilosc_recenzji, open('artifacts/ilosc_recenzji.pkl','wb'))
# pickle.dump(model, open('artifacts/model.pkl','wb'))
# pickle.dump(books_name, open('artifacts/books_names.pkl','wb'))
# pickle.dump(final_rating, open('artifacts/final_rating.pkl','wb'))
# pickle.dump(book_pivot, open('artifacts/book_pivot.pkl','wb'))
def recommend_book(book_name):
    book_id = np.where(book_pivot.index == book_name)[0][0]
    distance, suggestion = model.kneighbors(book_pivot.iloc[book_id,:].values.reshape(1,-1), n_neighbors=6)

    for i in range(len(suggestion)):
        books = book_pivot.index[suggestion[i]]
        for j in books: 
            print(j)

book_name = 'Harry Potter and the Chamber of Secrets (Book 2)'
# recommend_book(book_name)
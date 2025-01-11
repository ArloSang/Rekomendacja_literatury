import pickle 
import streamlit as st
import numpy as np
from sqlalchemy import text

if not st.session_state:
    st.info('Please Login from the Home page and try again.')
    if st.button("Powrot na strone glowna"):
        st.switch_page("Strona_startowa.py")
    st.stop()

else:
    
    conn = st.connection("mysql", type="sql")
    wyloguj = st.sidebar.button("Wyloguj")
    if wyloguj:
        del st.session_state['autoryzacja']
        del st.session_state['uzytkownik']
        st.cache_data.clear()
        st.switch_page("Strona_startowa.py")

    st.header("System rekomendacji literatury")
    
    model = pickle.load(open('artifacts/model.pkl','rb'))
    books_names = pickle.load(open('artifacts/books_names.pkl','rb'))
    book_pivot = pickle.load(open('artifacts/book_pivot.pkl','rb'))
    final_rating = pickle.load(open('artifacts/final_rating.pkl','rb'))
    uzytkownik = st.session_state['uzytkownik']
    

    def fetch_poster(suggestion):
        book_name = []
        ids_index = []
        poster_url = []
        isbn_numbers = []

        for book_id in suggestion:
            book_name.append(book_pivot.index[book_id])

        for name in book_name[0]:
            ids = np.where(final_rating['title'] == name)[0][0]
            ids_index.append(ids)

        for idx in ids_index:
            url = final_rating.iloc[idx]['img_url']
            poster_url.append(url)

            isbn = final_rating.iloc[idx]['ISBN']
            isbn_numbers.append(isbn)
        
        return poster_url, isbn_numbers

    def recommend_books(book_name):
        book_list = []
        book_id = np.where(book_pivot.index == book_name)[0][0]
        distance, suggestion = model.kneighbors(book_pivot.iloc[book_id,:].values.reshape(1,-1), n_neighbors=6)

        poster_url, isbn_numbers = fetch_poster(suggestion)

        for i in range(len(suggestion)):
            books = book_pivot.index[suggestion[i]]
            for j in books:
                book_list.append(j)
        return book_list, poster_url, isbn_numbers   
    
    selected_books = st.selectbox(
        "Wpis albo wyszukaj tytuł z listy",
        books_names, 
    )

    def zqpytaniesql(recommendation_books):
        zapytanie = "SELECT * FROM tabela2 WHERE User=:name AND title = :title"
        param = {"name": uzytkownik, "title": recommendation_books}
        sprawdzenie = conn.query(zapytanie, params=param)
        return sprawdzenie

    if selected_books:
        recommendation_books, poster_url, isbn_numbers = recommend_books(selected_books)
        kol = st.columns(5)
        for x in range(0,5):
            with kol[x]:
                st.text(recommendation_books[x+1])
                st.image(poster_url[x+1])
                
                sprawdzenie = zqpytaniesql(recommendation_books[x+1])
                # zapytanie = "SELECT * FROM tabela2 WHERE User=:name AND title = :title"
                # param = {"name": uzytkownik, "title": recommendation_books[x+1]}
                # sprawdzenie = conn.query(zapytanie, params=param)
                if sprawdzenie.empty:
                    if st.button(f"Dodaj {x+1} pozycję do swojej biblioteki!"):
                        with conn.session as session:
                            session.execute(text("INSERT INTO tabela2 (User, ISBN, title, img_url) VALUES (:name, :isbn, :title, :img_url)"), 
                                            {"name": uzytkownik, "isbn": isbn_numbers[x+1], "title": recommendation_books[x+1], "img_url": poster_url[x+1]})
                            session.commit()
                            st.success("dodano książkę")
                else:
                    st.button("Juz dodane", disabled=True, key={x+1})

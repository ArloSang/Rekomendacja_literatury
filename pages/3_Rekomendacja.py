import pickle 
import streamlit as st
import numpy as np
from sqlalchemy import create_engine
from sqlalchemy import text
import json

def weryfikacja():
    if not st.session_state:
        st.session_state['autoryzacja'] = False
        st.switch_page("Strona_startowa.py")
    
    if st.session_state.autoryzacja == False:
        st.switch_page("Strona_startowa.py")

    if "uzytkownik" not in st.session_state:
        st.session_state['autoryzacja'] = False
        st.switch_page("Strona_startowa.py")
    return 0

wyloguj = st.sidebar.button("Wyloguj")
if wyloguj:
    del st.session_state['autoryzacja']
    del st.session_state['uzytkownik']
    st.cache_data.clear()
    st.switch_page("Strona_startowa.py")

# weryfikacja użytkownika
weryfikacja()

# Implementacja danych
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

#Konfiguracja połączenia z bazą
with open("dbconfig.json") as config_file:
    config = json.load(config_file)
connection_url = f"mysql+pymysql://{config['db_user']}:{config['db_password']}@{config['db_host']}:{config['db_port']}/{config['db_name']}"
engine = create_engine(connection_url)

st.header("System rekomendacji literatury")
selected = st.selectbox("Wpis albo wyszukaj tytuł na bazie którego chcesz otrzymać rekomendację",books_names, index=None)

def rekomendacja(ksiazka):
    recommendation_books, poster_url, isbn_numbers = recommend_books(ksiazka)
    kol = st.columns(5)
    for x in range(0,5):
        with kol[x]:
            st.text(recommendation_books[x+1])
            st.image(poster_url[x+1])
            try:
                with engine.connect() as connection:
                    query = text("SELECT name FROM Biblioteka where name=:name and title= :zmienna")
                    result = connection.execute(query, {"name":uzytkownik,"zmienna": recommendation_books[x+1]})
                    row = result.fetchone()
                    if row:
                        st.success("Książka już się znajduje w bibliotece!")
                    else:
                        if st.button(f"Dodaj {x+1} pozycję do swojej biblioteki!", use_container_width=True):
                            try:
                                with engine.connect() as connection2:
                                    query2 = text("INSERT INTO Biblioteka (name, ISBN, title, img_url) VALUES (:name, :isbn, :title, :img_url)")
                                    connection2.execute(query2, {"name":uzytkownik, "isbn": isbn_numbers[x+1], "title": recommendation_books[x+1], "img_url": poster_url[x+1]})
                                    connection2.commit()
                                    st.rerun()
                            except Exception as e:
                                st.error(f"Błąd podczas dodawania pozycji do bazy: {e}")
            except Exception as e:
                st.warning(f"huh, {e}")

if "transport" in st.session_state:
    st.write(st.session_state["transport"])
    rekomendacja(st.session_state["transport"])
    del st.session_state["transport"]

def update_selection():
    st.session_state["selected_option"] = selected
    
if "selected_option" not in st.session_state:
    st.session_state["selected_option"] = None

if selected is not None:
    update_selection()
    st.write("Wybrana opcja:", st.session_state["selected_option"])
    rekomendacja(st.session_state["selected_option"])
    

import pickle 
import streamlit as st
import numpy as np
from sqlalchemy import create_engine
from sqlalchemy import text
import json

def weryfikacja():
    if "autoryzacja" not in st.session_state:
        st.session_state['autoryzacja'] = False
        st.switch_page("Strona_startowa.py")
    
    if st.session_state.autoryzacja == False:
        st.switch_page("Strona_startowa.py")

    if "uzytkownik" not in st.session_state:
        st.session_state['autoryzacja'] = False
        st.switch_page("Strona_startowa.py")
    return 0

# weryfikacja użytkownika
weryfikacja()

wyloguj = st.sidebar.button("Wyloguj")
if wyloguj:
    del st.session_state['autoryzacja']
    del st.session_state['uzytkownik']
    st.cache_data.clear()
    st.switch_page("Strona_startowa.py")

#Konfiguracja połączenia z bazą
with open("dbconfig.json") as config_file:
    config = json.load(config_file)
connection_url = f"mysql+pymysql://{config['db_user']}:{config['db_password']}@{config['db_host']}:{config['db_port']}/{config['db_name']}"
engine = create_engine(connection_url)

#Wczytanie zawartości plików
books_names = pickle.load(open('artifacts/books_names.pkl','rb'))
final_rating = pickle.load(open('artifacts/final_rating.pkl','rb'))
uzytkownik = st.session_state['uzytkownik']

st.header("Dodaj wybrane książki")
selected = st.selectbox("Wpis albo wyszukaj tytuł z listy",books_names, index=None)

if "selected_option" not in st.session_state:
    st.session_state["selected_option"] = None

def update_selection():
    st.session_state["selected_option"] = selected

if selected is not None:
    update_selection()
    try:
        with engine.connect() as connection:
            query = text("SELECT User FROM tabela2 where User=:name and title= :zmienna")
            result = connection.execute(query, {"name":uzytkownik,"zmienna": st.session_state["selected_option"]})
            row = result.fetchone()
            if row:
                st.success("Książka już się znajduje w bibliotece!")
            else:
                if st.button(f"Dodaj {st.session_state["selected_option"]} do biblioteki"):
                    x = (np.where(final_rating['title'] == st.session_state["selected_option"])[0][0])
                    y = final_rating[x:x+1]
                    try:
                        with engine.connect() as connection:
                            query = text("INSERT INTO tabela2 (User, ISBN, title, img_url) VALUES (:name, :isbn, :title, :img)")
                            connection.execute(query, {"name": uzytkownik,"isbn": y['ISBN'].values[0], "title": st.session_state["selected_option"], "img": y['img_url'].values[0]})
                            connection.commit()
                            st.rerun()
                    except Exception as e:
                        st.error(f"Wystąpił błąd podczas wprowadzania danych: {e}")
    except Exception as e:
        st.error(f"Wystąpił błąd podczas wprowadzania danych: {e}")
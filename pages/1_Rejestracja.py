import streamlit as st
from sqlalchemy import text

if st.session_state.autoryzacja == True:
    st.switch_page("pages/2_Profil.py")
    
st.set_page_config(initial_sidebar_state="collapsed")
conn = st.connection("mysql", type="sql")
st.header("Załóż konto")

login = st.text_input("Nazwa użytkownika: ")
password = st.text_input("Hasło: ", type="password")
password2 = st.text_input("Podaj ponownie hasło: ", type="password")

if st.button("Zarejestruj się"):
    if not login or not password or not password2:
        st.error("Wypełnij wszystkie części formularza")
    else:
        query = "SELECT name FROM test WHERE name = :name"
        params = {"name": login}
        wynik = conn.query(query, params=params)
        if wynik.empty:
            if password == password2:
                with conn.session as session:
                    session.execute(text("INSERT INTO test (name, pass) VALUES (:name, :pass)"), {"name": login, "pass": password})
                    session.commit()
                    st.cache_data.clear()
                    st.switch_page("Strona_startowa.py")
            else:
                st.error("Podano różne hasła")
        else:
            st.error("Nazwa użytkownika jest już zajęta")

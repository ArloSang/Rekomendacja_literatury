import streamlit as st
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
    uzytkownik = st.session_state['uzytkownik']

    query = "SELECT DISTINCT title, img_url FROM tabela2 WHERE User = :name"
    params = {"name": uzytkownik}
    lista = conn.query(query, params=params)

    if not lista.empty:
        st.header("Twoja Biblioteka")
        rows = lista.to_dict('records')  

        kolumny = st.columns(5)  
        for idx, row in enumerate(rows):
            with kolumny[idx % 5]: 
                st.text(row['title'])  
                st.image(row['img_url'], use_container_width=True) 
    else:
        st.warning("Nie masz jeszcze żadnych książek w swojej bibliotece.")
        if st.button("Powrót"):
            st.switch_page("pages/2_Profil.py")

import streamlit as st
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
weryfikacja()

wyloguj = st.sidebar.button("Wyloguj")
if wyloguj:
    del st.session_state['autoryzacja']
    del st.session_state['uzytkownik']
    st.cache_data.clear()
    st.switch_page("Strona_startowa.py")

def zapytanie():
    st.header("Twoja biblioteka")
    try:
        with engine.connect() as connection:
            query = text("SELECT DISTINCT title, img_url FROM Biblioteka WHERE name=:name")
            result = connection.execute(query, {"name": uzytkownik})
            rows = result.fetchall()  
            
            if rows:
                kolumny = st.columns(5)  
                for idx, row in enumerate(rows):
                    with kolumny[idx % 5]:
                        st.text(row[0])
                        st.image(row[1], use_container_width=True)
                        if st.button(f"Sprawdź tytuły podobne do tej książki!", key=idx, use_container_width=True):
                            st.session_state['transport'] = row[0]
                            st.switch_page("pages/3_Rekomendacja.py")
                        if st.button("Usun", key=row, use_container_width=True):
                            with engine.connect() as connection2:
                                query2 = text("DELETE FROM Biblioteka WHERE name=:name AND title=:title")
                                connection2.execute(query2, {"name": uzytkownik, "title": row[0]})
                                connection2.commit()
                                st.rerun()
            else:
                st.warning("Brak tytułów w bazie dla podanego użytkownika.")
    except Exception as e:
        st.error(f"Wystąpił błąd podczas pobierania danych: {e}")

#Ustalenie połączenia z bazą
with open("dbconfig.json") as config_file:
    config = json.load(config_file)
connection_url = f"mysql+pymysql://{config['db_user']}:{config['db_password']}@{config['db_host']}:{config['db_port']}/{config['db_name']}"
engine = create_engine(connection_url)
uzytkownik = st.session_state['uzytkownik']

zapytanie()

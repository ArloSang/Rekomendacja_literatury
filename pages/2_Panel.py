import pickle 
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
    del st.session_state['ksiazki']
    st.cache_data.clear()
    st.switch_page("Strona_startowa.py")

#Ustalenie połączenia z bazą
with open("dbconfig.json") as config_file:
    config = json.load(config_file)
connection_url = f"mysql+pymysql://{config['db_user']}:{config['db_password']}@{config['db_host']}:{config['db_port']}/{config['db_name']}"
engine = create_engine(connection_url)
uzytkownik = st.session_state['uzytkownik']

kolumna = st.columns(1)
with kolumna[0]:
    st.markdown(f"<h1 style='text-align: center;'>Witaj, {uzytkownik}</h1>", unsafe_allow_html=True)

    if st.button("Wyszukaj ksiązki w katalogu", use_container_width=True):
        st.switch_page("pages/5_Wyszukaj.py")

    if st.button("Poszukaj nowych książek!", use_container_width=True):
        st.switch_page("pages/3_Rekomendacja.py")
        
    if st.button("Przeglądaj swoją bibliotekę", use_container_width=True):
        st.switch_page("pages/4_Biblioteka.py")

if "ksiazki" not in st.session_state:
    ranking = pickle.load(open('artifacts/ilosc_recenzji.pkl','rb'))
    ranking = ranking.sort_values(by=['number_of_ratings'], ascending=False).head(20).sample(n=3)
    st.session_state['ksiazki'] = ranking


ranking = st.session_state['ksiazki']
st.markdown("<h1 style='text-align: center;'>Najpopularniejsze książki</h1>", unsafe_allow_html=True)
columns = st.columns(3)
for x in range(3):
    with columns[x]:
        st.markdown(f"<h4 style='text-align: center;'>{ranking.iloc[x]['title']}</h4>", unsafe_allow_html=True)
        st.image(ranking.iloc[x]['img_url'],use_container_width=True)
        try:
            with engine.connect() as connection:
                if st.button(f"Sprawdź tytuły podobne do tej książki!", key=x, use_container_width=True):
                    st.session_state['transport'] = ranking.iloc[x]['title']
                    st.switch_page("pages/3_Rekomendacja.py")
                query = text("SELECT name FROM Biblioteka where name=:name and title= :zmienna")
                result = connection.execute(query, {"name":uzytkownik,"zmienna": ranking.iloc[x]['title']})
                row = result.fetchone()
                if row:
                    st.success("Książka już się znajduje w bibliotece!")
                else:
                    if st.button(f"Dodaj {x+1} pozycję do swojej biblioteki!", use_container_width=True):
                        try:
                            with engine.connect() as connection2:
                                query2 = text("INSERT INTO Biblioteka (name, ISBN, title, img_url) VALUES (:name, :isbn, :title, :img_url)")
                                connection2.execute(query2, {"name":uzytkownik, "isbn": ranking.iloc[x]['ISBN'], "title": ranking.iloc[x]['title'], "img_url": ranking.iloc[x]['img_url']})
                                connection2.commit()
                                st.rerun()
                        except Exception as e:
                            st.error(f"Błąd podczas dodawania pozycji do bazy: {e}")
        except Exception as e:
            st.warning(f"huh, {e}")
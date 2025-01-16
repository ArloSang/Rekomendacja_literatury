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

    if st.button("Dodaj książki do biblioteki", use_container_width=True):
        st.switch_page("pages/5_Wyszukaj_twoje_ulubione_ksiazki.py")

    if st.button("Poszukaj nowych książek!", use_container_width=True):
        st.switch_page("pages/3_Rekomendacja.py")
        
    if st.button("Przeglądaj swoją bibliotekę", use_container_width=True):
        st.switch_page("pages/4_Biblioteka.py")

st.markdown("<h1 style='text-align: center;'>Najpopularniejsze książki</h1>", unsafe_allow_html=True)
ranking = pickle.load(open('artifacts/ilosc_recenzji.pkl','rb'))
ranking = ranking.sort_values(by=['number_of_ratings'], ascending=False).head(10).sample(n=3)
columns = st.columns(3)
for x in range(3):
    with columns[x]:
        st.write(ranking.iloc[x]['title'])
        st.image(ranking.iloc[x]['img_url'])
        try:
            with engine.connect() as connection:
                query = text("SELECT User FROM tabela2 where User=:name and title= :zmienna")
                result = connection.execute(query, {"name":uzytkownik,"zmienna": ranking.iloc[x]['title']})
                row = result.fetchone()
                if row:
                    st.success("Książka już się znajduje w bibliotece!")
                else:
                    if st.button(f"Dodaj {x+1} pozycję do swojej biblioteki!"):
                        try:
                            with engine.connect() as connection2:
                                query2 = text("INSERT INTO tabela2 (User, ISBN, title, img_url) VALUES (:name, :isbn, :title, :img_url)")
                                connection2.execute(query2, {"name":uzytkownik, "isbn": ranking.iloc[x]['ISBN'], "title": ranking.iloc[x]['title'], "img_url": ranking.iloc[x]['img_url']})
                                connection2.commit()
                                st.rerun()
                        except Exception as e:
                            st.error(f"Błąd podczas dodawania pozycji do bazy: {e}")
        except Exception as e:
            st.warning(f"huh, {e}")
import streamlit as st

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

tekst = st.session_state.uzytkownik
st.header(f"Witaj, {tekst}!")
# Pobieranie wartości id
id_value = st.query_params.get("id", [None])[0]

if st.button("Poszukaj nowych książek!"):
    st.switch_page("pages/3_Rekomendacja.py")
    
if st.button("Przeglądaj swoją bibliotekę"):
    st.switch_page("pages/4_Biblioteka.py")
    
if st.button("Dodaj książki do biblioteki"):
    st.switch_page("pages/4_Biblioteka.py")
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
kolumna = st.columns(1)
with kolumna[0]:
    st.markdown(f"<h1 style='text-align: center;'>Witaj, {st.session_state['uzytkownik']}</h1>", unsafe_allow_html=True)


    if st.button("Poszukaj nowych książek!", use_container_width=True):
        st.switch_page("pages/3_Rekomendacja.py")
        
    if st.button("Przeglądaj swoją bibliotekę", use_container_width=True):
        st.switch_page("pages/4_Biblioteka.py")
        
    if st.button("Dodaj książki do biblioteki", use_container_width=True):
        st.switch_page("pages/4_Biblioteka.py")
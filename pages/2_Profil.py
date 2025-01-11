import streamlit as st


if not st.session_state:
    st.info('Please Login from the Home page and try again.')
    if st.button("Powrot na strone glowna"):
        st.switch_page("Strona_startowa.py")
    st.stop()

else:
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

# st.title("Strona 2")
# if id_value:
#     st.write(f"Pobrane id: {id_value}") 
#     st.write("Debugowanie query_params:", st.query_params)
# else:
#     st.write("Nie znaleziono parametru 'id'.")

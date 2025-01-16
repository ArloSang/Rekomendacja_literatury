import streamlit as st

st.set_page_config(initial_sidebar_state="collapsed")

if "autoryzacja" not in st.session_state:
    st.session_state["autoryzacja"] = None

if st.session_state.autoryzacja == False:
    st.info("Proszę się zalogować")

if st.session_state.autoryzacja == True:
    st.switch_page("pages/2_Profil.py")


conn = st.connection("mysql", type="sql")
st.header("Witaj w SRL - systemie rekomendacji literatury")

login = st.text_input("Nazwa użytkownika: ")
password = st.text_input("Hasło: ", type="password")
lewy, prawy = st.columns(2)

if lewy.button("Zaloguj", use_container_width=True):
    query = "SELECT name, pass FROM test WHERE name = :name AND pass = :pass"
    params = {"name":login, "pass":password}
    results = conn.query(query, params=params)
    if not results.empty:
        st.session_state['autoryzacja'] = True
        st.session_state['uzytkownik'] = login
        st.switch_page("pages/2_Profil.py")
    else:
        st.error("Podano niewłaściwe dane logowania")

if prawy.button("Załóż konto", use_container_width=True):
    st.switch_page("pages/1_Rejestracja.py")
import streamlit as st
import bcrypt
import json
from sqlalchemy import create_engine
from sqlalchemy import text
st.set_page_config(initial_sidebar_state="collapsed")

if "autoryzacja" not in st.session_state:
    st.session_state["autoryzacja"] = None

if st.session_state.autoryzacja == False:
    st.info("Proszę się zalogować")

if st.session_state.autoryzacja == True:
    st.switch_page("pages/2_Panel.py")

with open("dbconfig.json") as config_file:
    config = json.load(config_file)
connection_url = f"mysql+pymysql://{config['db_user']}:{config['db_password']}@{config['db_host']}:{config['db_port']}/{config['db_name']}"
engine = create_engine(connection_url)

def logowanie():
    with engine.connect() as connection:
        query = text("SELECT pass FROM Users WHERE name =:name")
        hashed_password = connection.execute(query,{"name":login}).fetchone()
    if hashed_password:
        hashed_password2 = hashed_password[0]
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password2.encode('utf-8')):
            st.session_state['autoryzacja'] = True
            st.session_state['uzytkownik'] = login
            st.switch_page("pages/2_Panel.py")
        else:
            st.error("Podano niewłaściwe dane logowania")
    else:
        st.error("Podano niewłaściwe dane logowania")

login = st.text_input("Nazwa użytkownika: ")
password = st.text_input("Hasło: ", type="password")
lewy, prawy = st.columns(2)

if lewy.button("Zaloguj", use_container_width=True):
   logowanie()

if prawy.button("Załóż konto", use_container_width=True):
    st.switch_page("pages/1_Rejestracja.py")
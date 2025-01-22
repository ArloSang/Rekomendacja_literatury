from sqlalchemy import create_engine
from sqlalchemy import text
import json
import bcrypt
import pytest

with open("dbconfig.json") as config_file:
    config = json.load(config_file)
connection_url = f"mysql+pymysql://{config['db_user']}:{config['db_password']}@{config['db_host']}:{config['db_port']}/{config['db_name']}"
engine = create_engine(connection_url)

def logowanie(login, haslo):
    print("Próba logowania dla danych: ",login, haslo)
    with engine.connect() as connection:
        zapytanie = text("SELECT pass FROM Users WHERE name =:login")
        hashed_password = connection.execute(zapytanie,{"login":login}).fetchone()
    if hashed_password:
        hashed_password2 = hashed_password[0]
        if bcrypt.checkpw(haslo.encode('utf-8'), hashed_password2.encode('utf-8')):
            return True
        else:
            return False
    else:
        return False

# def test_logowanie():
#     print("\nTest logowania do systemu:")
#     login = ['123','user','admin']
#     haslo = ['123','user2341','4dm1n']

#     for i in range(len(login)):
#         try:
#             assert logowanie(login[i],haslo[i])
#             print("Test udany")
#         except AssertionError as e:
#             print("Test nieudany dla użytkownika: ", login[i])
# test_logowanie()

def Dodawanie(isbn,title,img,login):
    print("\tTest dla tytułu", title)
    try:
        with engine.connect() as connection2:
            query2 = text("SELECT ISBN FROM Biblioteka WHERE name=:login AND title =:title")
            wynik = connection2.execute(query2,{"login":login,"title":title}).fetchone()
            if not wynik:
                query = text("INSERT INTO Biblioteka (name, ISBN, title, img_url) VALUES (:name, :isbn, :title, :img_url)")
                connection2.execute(query, {"name":login, "isbn": isbn, "title": title, "img_url": img})
                connection2.commit()
                return True
            else: 
                return False
    except Exception as e:
        print(f"Błąd podczas dodawania pozycji do bazy: {e}")

def test_dodawanie():
    login = ['123','admin']
    haslo = ['123','4dm1n']

    isbn = ['0385306024','0425145638','0446604232']
    title = ['Accident','Fatal Cure','Exclusive']
    img = ['http://images.amazon.com/images/P/0385306024.01.LZZZZZZZ.jpg','http://images.amazon.com/images/P/0425145638.01.LZZZZZZZ.jpg','http://images.amazon.com/images/P/0446604232.01.LZZZZZZZ.jpg']
    for i in range(len(login)):
        print("Test zapisywania książek do biblioteki uzytkownika ",login[i])
        try:
            assert logowanie(login[i],haslo[i])
            print("Test logowania zakończony sukcesem")
            for j in range(len(isbn)):
                try:
                    assert Dodawanie(isbn[j],title[j],img[j],login[i])
                    print("\tTest dodania książki zakończony sukcesem")
                except AssertionError as e:
                    print("\tTest nieudany")
        except AssertionError as e:
            print("Test logowania nieudany dla użytkownika: ", login[i])
    
    
test_dodawanie()
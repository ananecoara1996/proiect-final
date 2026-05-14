import sqlite3
import logging
from typing import List, Tuple, Optional

logging.basicConfig(
    filename = 'app.log',
    level = logging.INFO,
    format = '%(asctime)s - %(levelname)s - %(message)s',
    encoding = 'utf-8'
)


class DataBaseManager:


    def __init__(self, db_nume: str ='manager_cheltuieli.db') -> None:
        self._db_nume = db_nume
        self._creaza_tabel()



    def _creaza_tabel(self):
        """

        Creeaza tabela in baza de date daca aceasta nu exista deja.

        """
        with sqlite3.connect(self._db_nume) as connection:
            cursor = connection.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tranzactii(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    denumire TEXT NOT NULL,
                    suma REAL NOT NULL,
                    tip TEXT NOT NULL,
                    categorie TEXT NOT NULL,
                    data TEXT NOT NULL,
                    metoda TEXT NOT NULL
                )
            ''')
            connection.commit()
            logging.info("Tabela 'tranzactii' a fost verificata/creata.")

    
    def executa_inserare_inregistrare(self, nume: str, suma: float, tip: str, cat: str, data: str, metoda: str):
        """
        Insereaza o noua inregistrare in tabela.
        
        """

        with sqlite3.connect(self._db_nume) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                    INSERT INTO tranzactii (denumire, suma, tip, categorie, data, metoda) 
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (nume, suma, tip, cat, data, metoda))
            connection.commit()
            logging.info(f"Tranzactia a fost inserata: {nume}, {suma} RON, {tip}")

    

    def executa_modificare_suma(self, id_cautat: str, suma_noua: float) -> None:
        """
        
        Modifica suma unei tranzactii din tabela.
        
        
        """
        with sqlite3.connect(self._db_nume) as connection:
            cursor = connection.cursor()
            cursor.execute("UPDATE tranzactii SET suma = ? WHERE id = ? ", (suma_noua, id_cautat))
            connection.commit()
            logging.info(f"Suma tranzactiei cu ID {id_cautat} a fost modificata in {suma_noua}")



    def executa_modificare_data(self, id_cautat: str, data_noua: str) -> None:
        """
        
        Modifica data unei tranzactii din tabela.
        
        """
        with sqlite3.connect(self._db_nume) as connection:
            cursor = connection.cursor()
            cursor.execute("UPDATE tranzactii SET data = ? WHERE id = ? ", (data_noua, id_cautat))
            connection.commit()
            logging.info(f"Data tranzactiei cu ID {id_cautat} a fost modificata in {data_noua}")




    def executa_stergere(self, id_cautat: str) -> None:
        """
        
        Sterge o tranzactie pe baza ID-ului specificat de utilizator.
        
        """

        with sqlite3.connect(self._db_nume) as connection:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM tranzactii WHERE id = ?", (id_cautat,))
            connection.commit()
            logging.info(f"Tranzactia cu ID {id_cautat} a fost stearsa.")


    def afisare_toate_inregistrarile(self, ordine_data_descrescator: bool = False) -> Optional[Tuple]:
        """
        
        Returneaza toate inregistrarile din tabela.
        
        """

        with sqlite3.connect(self._db_nume) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM tranzactii ORDER BY data DESC" if ordine_data_descrescator else "SELECT * FROM tranzactii")
            connection.commit()
            return cursor.fetchall()
        
    

    def cautare_dupa_id(self, id_cautat: str) -> Optional[Tuple]:
        """
        
        Returneaza o singura tranzactie dupa ID.
        
        """
        with sqlite3.connect(self._db_nume) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM tranzactii WHERE id = ?", (id_cautat,))
            return cursor.fetchone()
        
    
    def selecteaza_dupa_luna(self, luna: str) -> List[Tuple]:
        """
        
        Filtreaza inregistrarile dupa luna.
        
        """
        with sqlite3.connect(self._db_nume) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM tranzactii WHERE data LIKE ?", (f"%{luna}%",))
            return cursor.fetchall()
        
    
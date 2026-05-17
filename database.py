import sqlite3
import logging
from typing import List, Tuple, Optional


# Configurare sistem centralizat de jurnalizare pentru baza de date
logging.basicConfig(
    filename = 'app.log',
    level = logging.INFO,
    format = '%(asctime)s - %(levelname)s - %(message)s',
    encoding = 'utf-8'
)


class DataBaseManager:
    """
    Clasa responsabila cu managementul direct al bazei de date SQLite.
    Asigura persistenta datelor, jurnalizarea actiunilor si abstractizarea interogarilor SQL.
    """

    def __init__(self, db_nume: str ='manager_cheltuieli.db') -> None:
        """
        Initializeaza managerul bazei de date si creeaza structura tabelului daca nu exista.

        Args:
            db_nume(str): Numele fisierului bazei de date SQLite       
        """
        #Salvarea numelui fisierului bazei de date
        self._db_nume = db_nume

        #Apelarea automata a metodei de creare a tabelului la instanțiere
        self._creaza_tabel()


    def _creaza_tabel(self):
        """
        Creeaza tabela 'tranzactii' in baza de date daca aceasta nu exista deja.
        Include campurile: id, denumire, suma, tip, categorie, data, metoda.
        """
        # Deschiderea conexiunii sigure cu baza de date prin Context Manager
        with sqlite3.connect(self._db_nume) as connection:
            #Crearea unui obiect cursor pentru executarea instrucțiunilor SQL
            cursor = connection.cursor()
            #Executarea comenzii SQL pentru crearea tabelului
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
            #Salvarea permanenta a modificarilor
            connection.commit()
            #Inregistrarea actiunii in fisierul de log 
            logging.info("Tabela 'tranzactii' a fost verificata/creata.")

    
    def executa_inserare_inregistrare(self, nume: str, suma: float, tip: str, cat: str, data: str, metoda: str) -> None:
        """
        Insereaza o noua inregistrare(tranzactie) in tabela.

        Args:
            nume(str): Denumirea tranzactiei.
            suma(float): Valoarea numerica a tranzactiei.
            tip(str): Tipul tranzactiei ('Venit' sau 'Cheltuiala').
            cat(str): Categoria din care face parte.
            data(str): Data tranzactiei in format YYYY-MM-DD.
            metoda(str): Metoda de plata utilizata(Cash/Card)      
        """
        with sqlite3.connect(self._db_nume) as connection:
            cursor = connection.cursor()
            #Utilizarea semnelor de intrebare (?) ca parametri securizati contra SQL Injection
            cursor.execute("""
                    INSERT INTO tranzactii (denumire, suma, tip, categorie, data, metoda) 
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (nume, suma, tip, cat, data, metoda))
            #Commit este obligatoriu pentru operatiile de scriere (INSERT)
            connection.commit()
            logging.info(f"Tranzactia a fost inserata: {nume}, {suma} RON, {tip}")

    

    def executa_modificare_suma(self, id_cautat: str, suma_noua: float) -> None:
        """
        Modifica suma unei tranzactii existente din tabela pe baza ID-ului.

        Args:
            id_cautat(str): ID-ul tranzactiei care urmeaza sa fie modificata
            suma_noua(float): Noua valoare numerica a trazactiei
        """
        with sqlite3.connect(self._db_nume) as connection:
            cursor = connection.cursor()
            #Clauza WHERE id = ? asigura ca modificam doar randul dorit, nu tot tabelul
            cursor.execute("UPDATE tranzactii SET suma = ? WHERE id = ? ", (suma_noua, id_cautat))
            connection.commit()
            logging.info(f"Suma tranzactiei cu ID {id_cautat} a fost modificata in {suma_noua}")



    def executa_modificare_data(self, id_cautat: str, data_noua: str) -> None:
        """
        Modifica data unei tranzactii existente din tabela pe baza ID-ului.

        Args:
            id_cautat(str): ID-ul tranzactiei care urmeaza sa fie modificata
            data_noua(str): Noua data in format YYYY-MM-DD       
        """
        with sqlite3.connect(self._db_nume) as connection:
            cursor = connection.cursor()
            cursor.execute("UPDATE tranzactii SET data = ? WHERE id = ? ", (data_noua, id_cautat))
            connection.commit()
            logging.info(f"Data tranzactiei cu ID {id_cautat} a fost modificata in {data_noua}")



    def executa_stergere(self, id_cautat: str) -> None:
        """     
        Sterge definitiv o tranzactie pe baza ID-ului specificat de utilizator.

        Args: 
            id_cautat(str): ID-ul tranzactiei care va fi eliminata       
        """
        with sqlite3.connect(self._db_nume) as connection:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM tranzactii WHERE id = ?", (id_cautat,))
            connection.commit()
            #Folosim logging.warning deoarece stergerea este o actiune definitiva
            logging.warning(f"Tranzactia cu ID {id_cautat} a fost stearsa definitiv.")


    def afisare_toate_inregistrarile(self, ordine_data_descrescator: bool = False) -> List[Tuple]:
        """       
        Returneaza toate inregistrarile din tabela, ordonate dupa data.

        Args:
            ordine_data_descrescator(bool): Daca este True, sorteaza rezultatele descrescator dupa data.

        Returns:
            List[Tuple]: O lista de tupluri continand toate randurile extrase din tabela.       
        """
        with sqlite3.connect(self._db_nume) as connection:
            cursor = connection.cursor()
            #Operator ternar inline pentru a alege interogarea SQL cu sau fara clauza de sortare
            cursor.execute("SELECT * FROM tranzactii ORDER BY data DESC" if ordine_data_descrescator else "SELECT * FROM tranzactii")
            # Extragerea tuturor randurilor returnate sub forma de lista de tupluri
            rezultat: List[Tuple] = cursor.fetchall()
            #Jurnalizare ce salveaza inclusiv numarul de randuri gasite
            logging.info(f"S-au extras toate inregistrarile din baza de date  gasite. S-au gasit {len(rezultat)} rezultate.")
            return rezultat
        
    

    def cautare_dupa_id(self, id_cautat: str) -> Optional[Tuple]:
        """       
        Cauta si returneaza o singura tranzactie pe baza ID-ului.

        Args:
            id_cautat(str): ID-ul tranzactiei cautate
        
        Returns:
            Optional[Tuple]: Un tuplu cu datele tranzactiei daca este gasita, astfel None.        
        """
        with sqlite3.connect(self._db_nume) as connection:
            cursor = connection.cursor()
            #Executarea interogarii parametrizate pentru a gasi inregistrarea dupa cheia primara
            cursor.execute("SELECT * FROM tranzactii WHERE id = ?", (id_cautat,))
            #Preluarea primului rezultat gasit sub forma de tuplu (sau None daca nu exista)
            rezultat: Optional[Tuple] = cursor.fetchone()

            #Verificarea existentei rezultatului pentru partea de jurnalizare (logging)
            if rezultat:
                logging.info(f"Cautare reusita pentru ID: {id_cautat}.")
            else:
                logging.info(f"Cautare esuata pentru ID: {id_cautat}.")

            # Intoarcerea datelor catre modulul apelant
            return rezultat


    def selecteaza_dupa_tip(self, tip: str) -> List[Tuple]:
        """
        Filtreaza si returneaza toate inregistrarile de un anumit tip.

        Args:
            tip(str): Tipul cautat ('Venit' 'Cheltuiala')

        Returns: 
            List[Tuple]: Lista de tupluri cu tranzactiile filtrate.       
        """
        with sqlite3.connect(self._db_nume) as connection:
            cursor = connection.cursor()
            #Extragerea tuturor coloanelor unde campul 'tip' se potriveste cu argumentul trimis
            cursor.execute("SELECT * FROM tranzactii WHERE tip = ?", (tip,))
            #Colectarea tuturor randurilor identificate intr-o lista de tupluri
            rezultat: List[Tuple] = cursor.fetchall()
            #Salvarea in log a numarului exact de elemente gasite la filtrare
            logging.info(f"Filtrare efectuata dupa tipul '{tip}'. S-au gasit {len(rezultat)} rezultate.")
            return rezultat

    
    def selecteaza_dupa_luna(self, luna: str) -> List[Tuple]:
        """      
        Filtreaza si returneaza toate inregistrarile dupa luna introdusa de utilizator.

        Args:
            luna (str): Luna sau perioada cautata.

        Returns:
            List[Tuple]: O lista de tupluri cu tranzactiile gasite.       
        """
        with sqlite3.connect(self._db_nume) as connection:
            cursor = connection.cursor()
            # Utilizarea operatorului LIKE si a wildcards (%) pentru cautare partiala in textul datei
            cursor.execute("SELECT * FROM tranzactii WHERE data LIKE ?", (f"%{luna}%",))
            rezultat: List[Tuple] = cursor.fetchall()
            logging.info(f"Filtrare efectuata dupa luna: '{luna}'. S-au gasit {len(rezultat)} rezultate.")
            return rezultat
        
    
    def calculeaza_sume(self, tip: str, categorie: Optional[str] = None) -> float:
        """       
        Calculeaza suma totala cumulata din baza de date in functie de tip si de categorie(optional).

        Args:
            tip (str): Tipul tranzactiilor pentru suma ('Venit' sau 'Cheltuiala').
            categorie (Optional[str]): Categoria specifica pentru filtrare (implicit None).

        Returns:
            float: Valoarea totala calculata (0.0 daca nu exista inregistrari).       
        """
        with sqlite3.connect(self._db_nume) as connection:
            cursor = connection.cursor()

            #Ramura 1: Filtrare folosita la calculul total pe o categorie specifica
            if categorie:
                #Utilizarea functiei agregate SUM din SQL pentru a aduna coloana 'suma'
                cursor.execute("SELECT SUM(suma) FROM tranzactii WHERE tip = ? AND categorie = ?", (tip, categorie))
                rezultat: Optional[Tuple] = cursor.fetchone()
                #Operator ternar inline: daca SQL returneaza None (tabela goala), se atribuie 0.0 pentru a preveni crash-ul
                valoare_cat: float = rezultat[0] if rezultat and rezultat[0] is not None else 0.0
                logging.info(f"Suma calculata pentru tipul '{tip}' si categoria '{categorie}': {valoare_cat} RON.")
                return valoare_cat
            
            #Ramura 2: Filtrare folosita la calcularea soldului total al contului
            else:
                cursor.execute("SELECT SUM(suma) FROM tranzactii WHERE tip = ?", (tip,))
                rezultat: Optional[Tuple] = cursor.fetchone()
                #Extragerea valorii numerice de pe prima pozitie din tuplul returnat
                valoare_totala: float = rezultat[0] if rezultat and rezultat[0] is not None else 0.0
                logging.info(f"Suma totala pentru tipul '{tip}': {valoare_totala} RON.")
                return valoare_totala
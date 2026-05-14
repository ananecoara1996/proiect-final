'''
Cerinta Proiect: Manager de cheltuieli
Sa se scrie un program care tine evidenta cheltuielilor si veniturilor unei persoane.
Informatiile care trebuie retinute pentru fiecare tranzactie sunt:

1. ID
2. Denumire
3. Suma
4. Tip
5. Categorie
6. Data
7. Metoda de plata

Programul trebuie sa dispuna de un meniu care ne pune la dispozitie urmatoarele optiuni:

1. Adaugare tranzactie
2. Cautare tranzactie
3. Modificare data tranzactie
4. Stergere tranzactie
5. Afisare istoric complet
6. Calcul sold total
7. Calcul total cheltuieli pe o anumita categorie
8. Analiza economii
9. Afisarea tranzactiilor pe baza tipului
10. Afisarea tranzactiilor dintr-o anumita luna
11. Iesire


Implementarea programului trebuie sa utilizeze conceptele de programare orientata pe obiect, cum ar fi clase, obiecte, mostenire, polimorfism, incapsulare si abstractizare.
Si o baza de date SQLlite pentru stocarea informatiilor si o aplicatie
'''

import sqlite3
from datetime import datetime
from typing import List, Tuple, Optional, Dict

class Tranzactie:
    """

    Clasa pentru structurarea datelor unei tranzactii.

    """

    def __init__(self, id: int, denumire: str, suma: float, tip: str, categorie: str, data: str, metoda: str) -> None:
        self.id = id
        self.denumire = denumire
        self.suma = suma
        self.tip = tip
        self.categorie = categorie
        self.data = data
        self.metoda = metoda

class AplicatieManager:
    """

    Clasa pentru gestionarea bazei de date SQlite si a operatiunilor financiare.

    """

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


    #Adaugare tranzactie
    def adaugare(self) -> None:
        """

        Colecteaza datele de la utilizator si insereaza o noua tranzactie.
        
        """
        print("\n--- Adaugare Tranzacție ---")
        try:
            nume: str = input("Denumire: ")
            suma: float = float(input("Suma: "))
            tip: str = input("Tip (Venit/Cheltuiala): ")
            cat: str = input("Categorie: ")
            #daca data ramane goale, se foloseste data curenta in format YYYY-MM-DD
            data: str = input("Data (YYYY-MM-DD) sau Enter pt azi: ") or datetime.now().strftime("%Y-%m-%d")
            metoda: str = input("Metoda plata (Card/Cash): ")

            with sqlite3.connect(self._db_nume) as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    INSERT INTO tranzactii (denumire, suma, tip, categorie, data, metoda) 
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (nume, suma, tip, cat, data, metoda))
                connection.commit()
            print(" Tranzactie adaugata cu succes!")
        except ValueError:
            print(" Eroare: Suma trebuie sa fie un numar!")


    #Cautare tranzactie
    def cautare(self) -> None:
        """
        
        Cauta o tranzactie specifica in baza de date folosind ID-ul.

        """
        print("\n--- Cautare Tranzactie ---")
        id_cautat: str = input("Introduceti ID-ul tranzactiei: ")

        with sqlite3.connect(self._db_nume) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM tranzactii WHERE id = ?", (id_cautat,))
            rezultat: Optional[Tuple] = cursor.fetchone()
            
            if rezultat:
                print(f"Rezultat: ID:{rezultat[0]} | {rezultat[1]} | {rezultat[2]} RON | {rezultat[3]}")
            else:
                print("Tranzactia nu a fost gasita.")
    
    def modificare_suma(self):
        id_cautat: str = input("Introduceti ID-ul tranzactiei pentru care vreti sa modificati suma: ")
        suma_noua: float = float(input("Suma noua: "))

        with sqlite3.connect(self._db_nume) as connection:
            cursor = connection.cursor()
            cursor.execute("UPDATE tranzactii SET suma = ? WHERE id = ? ", (suma_noua, id_cautat))
            connection.commit()
            print("Suma a fost modificata cu succes!")

    def modificare_data(self):
        id_cautat = input("Introduceti ID-ul tranzactiei pentru care vreti sa modificati data: ")
        data_noua = str(input("Data noua: "))

        with sqlite3.connect(self._db_nume) as connection:
            cursor = connection.cursor()
            cursor.execute("UPDATE tranzactii SET data = ? WHERE id = ? ", (data_noua, id_cautat))
            connection.commit()
            print("Data a fost modificata cu succes!")


    #Stergere tranzactie
    def stergere_tranzactie(self) -> None:
        """
        
        Sterge o inregistrare din baza de date in functie de ID.
        
        """
        id_cautat: str = input("Introduceti ID-ul pentru care vreti sa stergeti tranzactiaa: ")

        with sqlite3.connect(self._db_nume) as connection:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM tranzactii WHERE id = ?", (id_cautat,))
            connection.commit()
            print("Tranzactie stearsa!")



    #Afisare istoric complet
    def afisare_istoric_complet(self) -> None:
        """

        Afiseaza toate tranzactiile inregistrate ordonate descrescator dupa data.

        """ 
        
        with sqlite3.connect(self._db_nume) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM tranzactii ORDER BY data DESC")
            rezultat: List[Tuple] = cursor.fetchall()
            print("\n--- ISTORIC COMPLET ---")

            if not rezultat:
                print("Nu exista tranzactii inregistrate.")

            for r in rezultat:
                print(f"ID: {r[0]} | {r[1]} | {r[2]} RON | {r[3]} | {r[4]} | {r[5]} | {r[6]}")

    #Calcul sold total
    def calcul_sold_total(self) -> None:
        """
        
        Calculeaza si afiseaza totalul veniturilor, cheltuielilor si soldul net.
        
        """

        with sqlite3.connect(self._db_nume) as connection:
            cursor = connection.cursor()
            rez_venituri: Optional[Tuple] = cursor.execute("SELECT SUM(suma) FROM tranzactii WHERE tip='Venit'").fetchone()
            rez_cheltuieli: Optional[Tuple] = cursor.execute("SELECT SUM(suma) FROM tranzactii WHERE tip='Cheltuiala'").fetchone()

            #In cazul in care rezultatul din SQL este None(baza de date este goala)

            venituri: float = rez_venituri[0] if rez_venituri and rez_venituri[0] is not None else 0.0
            cheltuieli: float = rez_cheltuieli[0] if rez_cheltuieli and rez_cheltuieli[0] is not None else 0.0
            print(f"Sold total: {venituri-cheltuieli:} RON (Venituri: {venituri}) | Cheltuieli: {cheltuieli}")

    #Calculul total cheltuieli pe o anumita categorie
    def calcul_total_categorie(self) -> None:
        """
        
        Sumeaza toate cheltuielile dintr-o categorie specificata de utilizator.


        """

        cat: str = input("Introduceti categoria: ").strip().capitalize()
        with sqlite3.connect(self._db_nume) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT SUM(suma) FROM tranzactii WHERE tip = 'Cheltuiala' AND categorie=?", (cat,))

            rezultat: Optional[Tuple] = cursor.fetchone()

            total: float = rezultat[0] if rezultat and rezultat[0] is not None else 0.0

            print(f"Total cheltuieli pe {cat}: {total:.2f} RON")

    #Afisarea tranzactiilor pe baza tipului
    def afisare_dupa_tip(self) -> None:
        """
        
        Filtreaza si afiseaza inregistrarile de tip 'Venit' sau 'Cheltuiala'.
        
        """
        tip: str = input("Introduceti tipul dorit (Venit/Cheltuiala): ").strip().capitalize()

        if tip not in ["Venit", "Cheltuiala"]:
            print("Eroare: Tipul introdus trebuie sa fie exact 'Venit' sau 'Cheltuiala'")
            return
        
        with sqlite3.connect(self._db_nume) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM tranzactii WHERE tip = ?", (tip,))
            
            rezultat: List[Tuple] = cursor.fetchall()

            if not rezultat:
                print(f"Nu s-au gasit tranzactii de tipul '{tip}'.")
                return
            
            for r in rezultat:
                print(f"ID: {r[0]} | {r[1]} | {r[2]} RON | {r[3]} | {r[4]} | {r[5]} | {r[6]}")


    #Afisarea tranzactiilor dintr-o anumita luna
    def afisare_dupa_luna(self) -> None:
        """
        
        Filtreaza si afiseaza inregistrarile utilizand sortarea dupa data.

        """
        luna: str = input("Luna si anul (MM/YYYY): ").strip()
        with sqlite3.connect(self._db_nume) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM tranzactii WHERE data LIKE ?", (f"%{luna}",))
            rezultat: List[Tuple] = cursor.fetchall()

            print(f"\n--- TRANZACTII DIN LUNA {luna} ---")
            if not rezultat:
                print("Nu s-au gasit tranzactii.")
                return
            
            for r in rezultat:
                print(f"ID: {r[0]} | {r[1]} | {r[2]} RON | {r[3]} | {r[4]} | {r[5]} | {r[6]}")


    #Gestiunea Meniului aplicatiei
    def run(self) -> None:
        """
        
        Porneste bucla infinita a meniului interactiv pentru consola.

        """
        while True:
            print("\n=== MENIU MANAGER FINANCIAR ===")
            print("1. Adauga tranzactie | 2. Cauta tranzactie| 3. Modifica suma | 4. Modifica data | 5. Stergere tranzactie | " )
            print("6. Afisare istoric complet | 7. Sold Total | 8.Total Categorie | 9. Afisare dupa tip | 10. Afisare dupa luna | 11. Iesire program")
            
            optiune: str = input("Alege o optiune (1-11): ")
            
            if optiune == "1":
                self.adaugare()
            if optiune == "2":
                self.cautare()
            if optiune == "3":
                self.modificare_suma() 
            if optiune == "4":
                self.modificare_data()
            if optiune == "5":
                self.stergere_tranzactie()      
            if optiune == "6":
                self.afisare_istoric_complet()
            if optiune == "7":
                self.calcul_sold_total()
            if optiune == "8":
                self.calcul_total_categorie()
            if optiune == "9":
                self.afisare_dupa_tip()
            if optiune == "10":
                self.afisare_dupa_luna()   
            elif optiune == "11":
                print("Programul s-a inchis. La revedere!")
                break
            else:
                print("Opțiune în lucru sau invalidă.")








if __name__ == "__main__":
    app = AplicatieManager()
    app.run()

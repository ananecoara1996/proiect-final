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


Implementarea programului trebuie sa utilizeze conceptele de programare orientata pe obiect, cum ar fi clase, obiecte, polimorfism, incapsulare si abstractizare.
Si o baza de date SQLlite pentru stocarea informatiilor si o aplicatie GUI realizata in Tkinter.

'''

import sys
import sqlite3
from datetime import datetime
from typing import List, Tuple
from database import DataBaseManager
from rapoarte import GeneratorRapoarte


class Tranzactie:
    """
    Clasa pentru structurarea datelor unei tranzactii.
    """

    def __init__(self, id: int, denumire: str, suma: float, tip: str, categorie: str, data: str, metoda: str) -> None:
        #Salvarea identificatorului unic al tranzactiei
        self.id = id
        #Salvarea numelui sau descrierii tranzactiei
        self.denumire = denumire
        #Salvarea valorii numerice a tranzactiei
        self.suma = suma
        #Salvarea tipului tranzactiei pentru filtrare (Venit/Cheltuiala)
        self.tip = tip
        #Salvarea categoriei specifice din buget
        self.categorie = categorie
        #Salvarea datei in formatul standard text YYYY-MM-DD
        self.data = data
        #Salvarea modalitatii de plata folosite (Card/Cash)
        self.metoda = metoda

class AplicatieManager:
    """
    Clasa pentru gestionarea bazei de date SQlite si a operatiunilor financiare.
    """

    def __init__(self) -> None:
        #Instantierea managerului de baza de date
        self.db: DataBaseManager = DataBaseManager()
        #Instantierea generatorului de rapoarte prin injectarea dependentei de baza de date
        self.rapoarte: GeneratorRapoarte = GeneratorRapoarte(self.db)


    #1.Adaugare tranzactie
    def adaugare(self) -> None:
        """
        Colecteaza datele de la utilizator si insereaza o noua tranzactie.       
        """

        print("\n--- Adaugare Tranzatie ---")
        try:
            #Preluarea si curatarea datelor descriptive introduse de utilizator
            nume: str = input("Denumire: ")
            #Conversia textului sumei in format numeric cu zecimale
            suma: float = float(input("Suma: "))
            tip: str = input("Tip (Venit/Cheltuiala): ")
            cat: str = input("Categorie: ")
            #Daca utilizatorul apasa Enter fara sa scrie data, se utilizeaza automat data curenta a sistemului
            data: str = input("Data (YYYY-MM-DD) sau Enter pt azi: ") or datetime.now().strftime("%Y-%m-%d")
            metoda: str = input("Metoda plata (Card/Cash): ")

            #Transmiterea setului complet de date catre metoda de insert din baza de date
            self.db.executa_inserare_inregistrare(nume, suma, tip, cat, data, metoda)

            print(" Tranzactie adaugata cu succes!")
        except ValueError:
            #Interceptarea erorilor de conversie text-numar
            print(" Eroare: Suma trebuie sa fie un numar!")


    #2.Cautare tranzactie
    def cautare(self) -> None:
        """
        Cauta o tranzactie specifica in baza de date folosind ID-ul.
        """

        print("\n--- Cautare Tranzactie ---")
        id_cautat: str = input("Introduceti ID-ul tranzactiei: ")
        #Apelarea interogarii din baza de date bazata pe cheia primara
        rezultat = self.db.cautare_dupa_id(id_cautat)

        #Evaluarea existentei inregistrarii in tabela
        if rezultat:
            #Afisarea datelor formatate prin accesarea indexata a elementelor din tuplu
            print(f"Rezultat: ID:{rezultat[0]} | Descriere: {rezultat[1]} | Suma: {rezultat[2]} RON | Categorie: {rezultat[4]} ")
        else:
            print("Tranzactia nu a fost gasita.")
    
    #3.1.Modificare suma
    def modificare_suma(self) -> None:
        """       
        Modifica suma unei tranzactii deja existe cu o suma noua introdusa de catre utilizator.
        """

        print("\n--- Modificare Suma ---")
        id_cautat: str = input("Introduceti ID-ul tranzactiei pentru care vreti sa modificati suma: ")
        try:
            #Preluarea si validarea formatului numeric al noii sume
            suma_noua: float = float(input("Suma noua: "))
            #Transmiterea instructiunii de update catre baza de date
            self.db.executa_modificare_suma(id_cautat, suma_noua)
            print("Suma a fost modificata cu succes!")
        except ValueError:
            print("Eroare: Introduceti o suma valida!")

    #3.Modificare data
    def modificare_data(self) -> None:
        """       
        Modifica data unei tranzactii deja existe cu o data noua introdusa de catre utilizator.
        """

        print("\n--- Modificare Data ---")
        id_cautat: str = input("Introduceti ID-ul tranzactiei pentru care vreti sa modificati data: ")
        #Preluarea noii valori pentru data sub forma de sir de caractere
        data_noua: str = str(input("Data noua: "))
        #Executarea modificarii in tabela pe baza ID-ului selectat
        self.db.executa_modificare_data(id_cautat, data_noua)
        print("Data a fost modificata cu succes!")


    #4.Stergere tranzactie
    def stergere_tranzactie(self) -> None:
        """       
        Sterge o inregistrare din baza de date in functie de ID.      
        """

        print("\n--- Stergere Tranzactie ---")
        id_cautat: str = input("Introduceti ID-ul pentru care vreti sa stergeti tranzactiaa: ")
        #Transmiterea ID-ului spre executia comenzii distructive DELETE din SQL
        self.db.executa_stergere(id_cautat)
        print("Tranzactie stearsa cu succes!")



    #5.Afisare istoric complet
    def afisare_istoric_complet(self) -> None:
        """
        Afiseaza toate tranzactiile inregistrate ordonate descrescator dupa data.
        """ 

        print("\n--- Istoric complet ---")

        #Preluarea tuturor datelor din SQL setand sortarea cronologica inversa pe True
        rezultat: List[Tuple] = self.db.afisare_toate_inregistrarile(ordine_data_descrescator = True)
        
        #Opreste functia daca nu exista inregistrari salvate
        if not rezultat:
            print("Nu exista tranzactii inregistrate.")
            return 

        #Parcurgerea iterativa a listei pentru listarea detaliata a fiecarei tranzactii
        for rand in rezultat:
            print(f"ID: {rand[0]} | {rand[1]} | {rand[2]} RON | {rand[3]} | {rand[4]} | {rand[5]} | {rand[6]}")


    #6.Calcul sold total
    def calcul_sold_total(self) -> None:
        """      
        Calculeaza si afiseaza totalul veniturilor, cheltuielilor si soldul net.       
        """

        print("\n--- Afisare Sold Total ---")
        #Interogarea sumei totale strict pentru inregistrarile de tip Venit
        venituri: float = self.db.calculeaza_sume("Venit")
        #Interogarea sumei totale strict pentru inregistrarile de tip Cheltuiala
        cheltuieli: float = self.db.calculeaza_sume("Cheltuiala")

        #Calcularea in timp real a diferentei (soldul net) si afisarea datelor finale
        print(f"Sold total: {venituri-cheltuieli:} RON (Venituri: {venituri}) | Cheltuieli: {cheltuieli}")


    #7.Calculul total cheltuieli pe o anumita categorie
    def calcul_total_categorie(self) -> None:
        """      
        Sumeaza toate cheltuielile dintr-o categorie specificata de utilizator.
        """

        print("\n--- Afisare Calcul Total pe Categorie ---")
        #Preluarea categoriei eliminand spatiile libere accidentale si setand prima litera mare
        cat: str = input("Introduceti categoria: ").strip().capitalize()
       
        #Apelarea metodei de calcul din baza de date prin transmiterea argumentului de categorie
        total: float = self.db.calculeaza_sume("Cheltuiala", categorie = cat)

        #Afisarea sumei finale formatata curat cu exact doua zecimale (.2f)
        print(f"Total cheltuieli pe {cat}: {total:.2f} RON")


    #8.Analiza economii
    def analiza_economii(self) -> None:
        """      
        Foloseste modulul extern de rapoarte pentru a genera o fisa.
        """
    
        self.rapoarte.genereaza_raport_analiza()


    #9.Afisarea tranzactiilor pe baza tipului
    def afisare_dupa_tip(self) -> None:
        """     
        Filtreaza si afiseaza inregistrarile de tip 'Venit' sau 'Cheltuiala'.     
        """

        print("\n--- Afisare Tranzactii dupa tip ---")
        
        #Curatarea textului introdus pentru a corespunde formatului stocat in baza de date
        tip: str = input("Introduceti tipul dorit (Venit/Cheltuiala): ").strip().capitalize()

        #Respinge comanda daca textul difera de cele doua optiuni permise
        if tip not in ["Venit", "Cheltuiala"]:
            print("Eroare: Tipul introdus trebuie sa fie exact 'Venit' sau 'Cheltuiala'")
            return    # Oprirea imediata a functiei
        
        #Preluarea setului filtrat de tranzactii din tabela SQL
        rezultat: List[Tuple] = self.db.selecteaza_dupa_tip(tip)

        #Verifica daca lista returnata de baza de date este goala
        if not rezultat:
            print(f"Nu s-au gasit tranzactii de tipul '{tip}'.")
            return
        #Parcurgerea iterativa a listei pentru afisarea formatata a fiecarei inregistrari   
        for r in rezultat:
                print(f"ID: {r[0]} | {r[1]} | {r[2]} RON | {r[3]} | {r[4]} | {r[5]} | {r[6]}")


    #10.Afisarea tranzactiilor dintr-o anumita luna
    def afisare_dupa_luna(self) -> None:
        """    
        Filtreaza si afiseaza inregistrarile utilizand sortarea dupa data.
        """

        #Preluarea stringului care contine luna si anul in formatul dorit de utilizator
        luna: str = input("Luna si anul (MM/YYYY): ").strip()
        print(f"\n--- Afisare Tranzactii din perioada {luna} ---")

        #Executarea filtrului pe baza functiei LIKE implementata in database.py    
        rezultat: List[Tuple] = self.db.selecteaza_dupa_luna(luna)

        #Oprirea functiei in siguranta daca perioada nu are inregistrari
        if not rezultat:
            print("Nu s-au gasit tranzactii.")

        # Afisarea in terminal a componentelor tranzactiilor mapate pe indicii tuplului SQL   return    
        for r in rezultat:
            print(f"ID: {r[0]} | {r[1]} | {r[2]} RON | {r[3]} | {r[4]} | {r[5]} | {r[6]}")
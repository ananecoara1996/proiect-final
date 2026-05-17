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


Implementarea programului trebuie sa utilizeze conceptele de programare orientata pe obiect, 
o baza de date SQLlite pentru stocarea informatiilor si o aplicatie GUI realizata in Tkinter.

'''


import sys
import logging
from manager import AplicatieManager


def afiseaza_meniu() -> None:
    """
    Afisează pe ecran structura vizuala a meniului interactiv pentru consola.
    
    Aceasta functie listeaza cele 11 optiuni disponibile utilizatorului in terminal.
    """
    print("\n================ MENIU MANAGER CHELTUIELI ================")
    print("1. Adaugare tranzactie")
    print("2. Cautare tranzactie")
    print("3. Modificare data tranzactie")
    print("4. Stergere tranzactie")
    print("5. Afisare istoric complet")
    print("6. Calcul sold total")
    print("7. Calcul total cheltuieli pe o anumita categorie")
    print("8. Analiza economii")
    print("9. Afisarea tranzactiilor pe baza tipului")
    print("10. Afisarea tranzactiilor dintr-o anumita luna")
    print("11. Iesire")
    print("==========================================================")

def main():
    """ 
    Porneste bucla infinita a meniului interactiv pentru consola.
    Instantierea managerului (clasa din manager.py)
    """

    manager = AplicatieManager()
    
    logging.info("Aplicatia Manager de Cheltuieli a pornit din modulul principal main.py.")

    while True:
        #Apelarea functiei care afiseaza textul meniului la fiecare iteratie
        afiseaza_meniu()
        optiune = input("Alege o optiune (1-11): ").strip()

        logging.info(f"Meniu Consola: Utilizatorul a selectat optiunea: {optiune}")

        if optiune == "1":
            manager.adaugare()
        elif optiune == "2":
            manager.cautare()
        elif optiune == "3":
            manager.modificare_data()
        elif optiune == "4":
            manager.stergere_tranzactie()
        elif optiune == "5":
            manager.afisare_istoric_complet()
        elif optiune == "6":
            manager.calcul_sold_total()
        elif optiune == "7":
            manager.calcul_total_categorie()
        elif optiune == "8":
            manager.analiza_economii()
        elif optiune == "9":
            manager.afisare_dupa_tip()
        elif optiune == "10":
            manager.afisare_dupa_luna()
        elif optiune == "11":
            print("\nAplicatia s-a inchis. La revedere!")

            logging.info("Aplicatia a fost inchisa voluntar prin selectarea optiunii 11.")

            #Oprirea definitiva a interpretorului Python
            sys.exit()
        else:
            print("\nEroare: Optiune invalida! Te rugam sa introduci un numar intre 1 si 11.")
            logging.warning(f"Meniu Consola: Comanda invalida introdusa in terminal: '{optiune}'.")


#Rulează functia main() doar daca fisierul este pornit ca script principal
if __name__ == "__main__":
    main()


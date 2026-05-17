from datetime import datetime
import logging
from database import DataBaseManager
from typing import List, Tuple

class GeneratorRapoarte:
    """
    Clasa responsabila cu procesarea datelor financiare si exportarea analizelor sub forma de rapoarte text.
    """

    def __init__(self, db: DataBaseManager) -> None:
        """
        Initializeaza generatorul de rapoarte prin injectarea bazei de date.

        Args:
            db (DataBaseManager): Instanta activa a managerului bazei de date.
        """
        self.db: DataBaseManager = db


    def genereaza_raport_analiza(self) -> None:
        """
        Metoda (Optiunea 8). Genereaza o fisa de analiza financiara completa 
        si o salveaza intr-un fisier text extern 'raport_financiar.txt'.
        """

        print("\n--- Generare Raport Financiar ---")

        #Preluarea tuturor randurilor din baza de date, ordonate descrescator dupa data
        rezultat: List[Tuple] = self.db.afisare_toate_inregistrarile(ordine_data_descrescator=True)
        
        #Oprește executia functiei daca nu exista tranzactii stocate
        if not rezultat:
            print("Nu exista date pentru a genera un raport.")
            return

        #Interogarea sumei totale pentru toate inregistrarile de tip Venit
        venituri: float = self.db.calculeaza_sume("Venit")
        #Interogarea sumei totale pentru toate inregistrarile de tip Cheltuiala
        cheltuieli: float = self.db.calculeaza_sume("Cheltuiala")
        
        #Definirea numelui fisierului ce va aparea in folderul proiectului
        nume_fisier: str = "raport_financiar.txt"

        #Deschiderea securizata a fisierului in mod scriere ('w') cu suport complet pentru diacritice (utf-8)
        with open(nume_fisier, "w", encoding="utf-8") as fisier:
            #Scrierea elementelor decorative de design si a antetului de raport
            fisier.write("==========================================================================================================\n")
            fisier.write("                                RAPORT MANAGEMENT FINANCIAR             \n")

            #Injectarea datei si orei exacte la care utilizatorul a generat fisierul
            fisier.write(f"                            Generat la data: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
            fisier.write("==========================================================================================================\n\n")

            #Inregistrarea totalurilor financiare formatate cu exact doua zecimale (:.2f)
            fisier.write(f"TOTAL VENITURI:     {venituri:.2f} RON\n")
            fisier.write(f"TOTAL CHELTUIELI:   {cheltuieli:.2f} RON\n")

            #Calcularea pe loc a diferentei pentru obtinerea soldului net curent
            fisier.write(f"SOLD NET DISPONIBIL: {(venituri - cheltuieli):.2f} RON\n\n")
            fisier.write("----------------------------------------- Istoric Detaliat  ----------------------------------------------\n")
            
            #Parcurgerea iterativa a fiecarui rand extras din baza de date
            for r in rezultat:
                # Scriere linie cu linie in fisier folosind indicii tuplului:
                # r[5]=data, r[3]=tip, r[1]=denumire, r[2]=suma, r[4]=categorie, r[6]=metoda
                fisier.write(f"Data: [{r[5]}] {r[3]} - {r[1]} | Suma: {r[2]} RON | Cat: {r[4]} ({r[6]})\n")
                
            fisier.write("\n========================================================================================================\n")
        
        #Confirmare in consola pentru utilizator ca fisierul a fost salvat si poate fi deschis   
        print(f" Raportul a fost generat cu succes in fisierul '{nume_fisier}'!")
        #Jurnalizarea actiunii in app.log 
        logging.info(f"A fost generat raportul de analiza financiara text '{nume_fisier}'.")




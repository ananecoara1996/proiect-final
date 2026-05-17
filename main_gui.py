import tkinter as tk
from tkinter import ttk, messagebox
from database import DataBaseManager
from datetime import datetime
import logging
#from rapoarte import GeneratorRapoarte

class InterfataGrafica:
    """
    Clasa responsabila pentru generarea si gestionarea interfetei grafice (GUI) desktop.
    
    Implementeaza operatiunile vizuale de tip CRUD (Create, Read, Update, Delete).
    Se conecteaza direct la baza de date pentru managementul tranzactiilor.   
    """
    
    def __init__(self, root: tk.Tk) -> None:
        """
        Initializeaza fereastra principala a aplicatiei si injecteaza baza de date.

        Args:
            root (tk.Tk): Instanta ferestrei radacina furnizata de Tkinter.
        """
        #Salvarea referintei ferestrei principale
        self.root = root
        #Setarea titlului care apare pe bara superioara a ferestrei
        self.root.title("Manager Financiar")
        #Definirea dimensiunii ferestrei la pornire (latime x inaltime in pixeli)
        self.root.geometry("800x550")
        
        #Instantierea obiectului de conexiune la baza de date SQLite
        self.db: DataBaseManager = DataBaseManager()
        #Apelarea metodei care deseneaza componentele vizuale (butoane, casete text)
        self._construieste_componente()
        #Incarcarea initiala a datelor din baza de date direct in tabel
        self.refresh_tabel()

    def _construieste_componente(self) -> None:
        """
        Construieste si pozitioneaza toate elementele vizuale in interfata.
        
        Configureaza formularul de intrare a datelor, butoanele pentru actiunile CRUD, caseta de filtrare rapida si tabelul structurat de tip Treeview.       
        """

        #Cadru Formular Introducere
        frame_form = tk.LabelFrame(self.root, text=" Formular Gestionare Tranzactii ", padx=10, pady=5)
        #Fixarea cadrului pe ecran, extins pe orizontala (fill="x") cu margini exterioare
        frame_form.pack(fill="x", padx=15, pady=10)

        #Crearea etichetei statice pentru textul „Denumire:” pe rândul 0, coloana 0
        tk.Label(frame_form, text="Denumire:").grid(row=0, column=0, sticky="w")
        #Instantierea casetei de text pentru introducerea numelui tranzactiei
        self.ent_nume = tk.Entry(frame_form, width=18)
        #Pozitionarea casetei text la dreapta etichetei (linia 0, coloana 1)
        self.ent_nume.grid(row=0, column=1, padx=5, pady=5)

        #Crearea etichetei statice pentru „Suma (RON):” la linia 0, coloana 2
        tk.Label(frame_form, text="Suma (RON):").grid(row=0, column=2, sticky="w")
        self.ent_suma = tk.Entry(frame_form, width=18)
        self.ent_suma.grid(row=0, column=3, padx=5, pady=5)

        #Crearea etichetei pentru tip pe randul urmator (linia 1, coloana 0)
        tk.Label(frame_form, text="Tip:").grid(row=1, column=0, sticky="w")
        #Crearea unui dropdown controlat care contine tipurile permise de tranzactie
        self.cb_tip = ttk.Combobox(frame_form, values=["Venit", "Cheltuiala"], width=15, state="readonly")
        self.cb_tip.grid(row=1, column=1, padx=5, pady=5)
        #Stabilirea optiunii implicite pe indexul 1 ("Cheltuiala")
        self.cb_tip.current(1)

        #Crearea etichetei pentru categorie la linia 1, coloana 2
        tk.Label(frame_form, text="Categorie:").grid(row=1, column=2, sticky="w")
        self.ent_cat = tk.Entry(frame_form, width=18)
        self.ent_cat.grid(row=1, column=3, padx=5, pady=5)

        #Crearea etichetei pentru data pe randul al treilea (linia 2, coloana 0)
        tk.Label(frame_form, text="Data (YYYY-MM-DD):").grid(row=2, column=0, sticky="w")
        self.ent_data = tk.Entry(frame_form, width=18)
        #Autocompletarea casetei text cu data curenta formatata (An-Luna-Zi)
        self.ent_data.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.ent_data.grid(row=2, column=1, padx=5, pady=5)

        #Crearea etichetei pentru modul de plata la linia 2, coloana 2
        tk.Label(frame_form, text="Metoda Plata:").grid(row=2, column=2, sticky="w")
        self.cb_metoda = ttk.Combobox(frame_form, values=["Card", "Cash", "Transfer bancar"], width=15, state="readonly")
        self.cb_metoda.grid(row=2, column=3, padx=5, pady=5)
        self.cb_metoda.current(0)

        #Caseta Butoane CRUD
        frame_actiuni = tk.Frame(self.root)
        #Fixarea panoului de actiuni pe ecran extins pe toata latimea ferestrei
        frame_actiuni.pack(fill="x", padx=15, pady=2)
        
        #Crearea butonului verde pentru adaugarea datelor (Operatiunea CREATE)
        tk.Button(frame_actiuni, text="Adauga (Create)", bg="#4CAF50", fg="white", font=("Arial", 9, "bold"), command=self.gui_adauga).pack(side="left", padx=5)
        #Crearea butonului portocaliu pentru modificarea datei (Operatiunea UPDATE)
        tk.Button(frame_actiuni, text="Modifica Data (Update)", bg="#FF9800", command=self.gui_modifica_data).pack(side="left", padx=5)
        #Crearea butonului rosu pentru eliminarea randurilor (Operatiunea DELETE)
        tk.Button(frame_actiuni, text="Sterge Rand (Delete)", bg="#f44336", fg="white", command=self.gui_sterge).pack(side="left", padx=5)
        
        # Filtru dinamic rapid
        tk.Label(frame_actiuni, text="Filtru rapid luna/tip:").pack(side="left", padx=15)
        #Caseta text in care utilizatorul va tasta cuvantul de cautare
        self.ent_filtru = tk.Entry(frame_actiuni, width=10)
        #Alinierea casetei de filtrare in panoul de actiuni direct pe partea stanga
        self.ent_filtru.pack(side="left", padx=2)
        tk.Button(frame_actiuni, text="Cauta", command=self.refresh_tabel).pack(side="left", padx=2)

        # Tabel Vizual Structurat (Treeview)
        self.tabel = ttk.Treeview(self.root, columns=("id", "nume", "suma", "tip", "cat", "data", "metoda"), show="headings", height=10)
        #Proprietatile fill si expand permit tabelului sa se redimensioneze adaptiv cu mouse-ul
        self.tabel.pack(fill="both", expand=True, padx=15, pady=10)
        
        #Parcurgerea iterativa a identificatorilor de coloane pentru setarea proprietatilor lor
        for col in ("id", "nume", "suma", "tip", "cat", "data", "metoda"):
            self.tabel.heading(col, text=col.capitalize())
            self.tabel.column(col, width=95, anchor="center")

        #Bara sumar inferioara
        self.lbl_sumar = tk.Label(self.root, text="", font=("Arial", 11, "bold"), fg="#2c3e50")
        #Afisarea etichetei de sumar la baza ferestrei
        self.lbl_sumar.pack(pady=10)
        logging.info("Interfata Grafica: Toate componentele vizuale au fost pozitionate.")


    def refresh_tabel(self) -> None:
        """
        Reincarca, filtreaza si centralizeaza datele in tabelul grafic.
        
        Sterge liniile curente din Treeview, preia criteriul de cautare din caseta de text, 
        interogheaza baza de date SQLite si recalculeaza dinamic totalurile financiare afisate.      
        """
        #Stergerea tuturor randurilor din tabelul vizual pentru a evita duplicarea la reincarcare
        for i in self.tabel.get_children():
            self.tabel.delete(i)

        #Preluarea si curatarea textului din caseta de filtrare rapida   
        filtru = self.ent_filtru.get().strip().capitalize()

        #Stabilirea setului de date in functie de prezenta sau absenta filtrului
        if filtru:
            # Daca exista text in filtru, cauta dupa luna sau tip
            date = self.db.selecteaza_dupa_luna(filtru) or self.db.selecteaza_dupa_tip(filtru)
        else:
            date = self.db.afisare_toate_inregistrarile(ordine_data_descrescator=True)
            logging.info("Interfata Grafica: Tabelul a fost incarcat cu istoricul complet.")

        #Inserarea secventiala a noilor inregistrari in Treeview
        for r in date:
            self.tabel.insert("", "end", values=r)

        #Interogarea bazei de date pentru obtinerea sumelor actuale    
        v = self.db.calculeaza_sume("Venit")
        c = self.db.calculeaza_sume("Cheltuiala")

        #Actualizarea textului etichetei de sumar cu formatare de doua zecimale
        self.lbl_sumar.config(text=f"Total Venituri: {v:.2f} RON  |  Total Cheltuieli: {c:.2f} RON  |  Sold Net: {v-c:.2f} RON")

    def gui_adauga(self) -> None:
        """     
        Prelucreaza si insereaza o noua inregistrare in baza de date.

        Extrage informatiile din campurile formularului grafic, valideaza daca valoarea
        introdusa ca suma este numerica si reimprospateaza tabelul.
         
        Afiseaza un pop-up in caz de eroare.
        """
        try:
            # Extragerea datelor si inserarea lor in baza de date 
            self.db.executa_inserare_inregistrare(
                self.ent_nume.get().strip(),
                float(self.ent_suma.get().strip()),
                self.cb_tip.get(),
                self.ent_cat.get().strip(),
                self.ent_data.get().strip(),
                self.cb_metoda.get()
            )
            logging.info(f"Interfata Grafica: Tranzactia '{self.ent_nume.get().strip()}' a fost inserata cu succes.")

            # Sincronizarea imediata a tabelului vizual
            self.refresh_tabel()

        except ValueError:
            messagebox.showerror("Eroare", "Suma sau datele completate sunt invalide!")

    def gui_sterge(self) -> None:
        """     
        Sterge definitiv inregistrarea selectata de utilizator din sistem.

        Identifica randul evidentiat in Treeview, extrage ID-ul unic asociat acestuia din baza de date, transmite comanda de stergere
        si sincronizarea imediata a tabelului.        
        """

        #Preluarea randului selectat cu mouse-ul
        selectie = self.tabel.selection()

        #Verificarea existentei unei selectii
        if not selectie:
            messagebox.showwarning("Selectie", "Alegeti o linie din tabel!")
            logging.warning("Interfata Grafica: Niciun rand nu a fost selectat.")
            return
        
        #Extragerea ID-ului primar din prima coloana a randului selectat
        id_t = self.tabel.item(selectie)['values'][0]

        #Executarea comenzii SQL DELETE in baza de date
        self.db.executa_stergere(id_t)
        logging.info(f"Interfata Grafica: Tranzactia cu ID-ul {id_t} a fost eliminata cu succes din baza de date.")

        #Sincronizarea imediata a tabelului
        self.refresh_tabel()


    def gui_modifica_data(self) -> None:
        """       
        Actualizeaza data calendaristica a tranzactiei selectate in tabel.

        Identifica randul marcat, extrage ID-ul unic, citeste noul text si transmite comanda de modificare direct in baza de date.        
        """

        #Preluarea randului selectat cu mouse-ul
        selectie = self.tabel.selection()

        #Verificarea existentei unei selectii
        if not selectie:
            messagebox.showwarning("Selectie", "Alegeti o linie din tabel!")
            logging.warning("Interfata Grafica: Niciun rand nu a fost selectat.")
            return
        
        #Extragerea ID-ului primar din prima coloana a randului selectat
        id_t = self.tabel.item(selectie)['values'][0]

        #Preluarea si curatarea noului text pentru data 
        noua_data = self.ent_data.get().strip()

        #Executarea comenzii SQL UPDATE in baza de date
        self.db.executa_modificare_data(id_t, noua_data)

        #Sincronizarea imediata a tabelului
        self.refresh_tabel()

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfataGrafica(root)
    root.mainloop()
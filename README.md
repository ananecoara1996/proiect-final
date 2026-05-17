# Manager de Cheltuieli si Venituri Personale

Aplicatie modulara in Python conceputa pentru inregistrarea, filtrarea si generarea de rapoarte asupra tranzactiilor financiare.

## Tehnologii utilizate

Proiectul a fost implementat utilizand exclusiv librariile standard din Python, eliminand complet necesitatea instalarii unor dependente terte (fara pachete externe de tip `pip install`):
*   **Core:** Python 3.11
*   **Database:** `sqlite3` (Baza de date relationala locala tranzactionala).
*   **GUI:** `tkinter` & `tkinter.ttk` (Interfata grafica desktop).
*   **Audit și Depanare:** `logging` (Jurnalizarea automata a actiunilor in `app.log`).
*   **Time Management:** `datetime` (Formatarea cronologica a inregistrarilor).

## Structura Proiectului (Module)
*   `main.py` -> Punctul de pornire al aplicatiei. Gestioneaza bucla infinita a meniului interactiv din consola (optiunile 1-11).
*   `manager.py` -> Logica de business. Defineste clasa POO de model ('Tranzactie') si controlerul `AplicatieManager` responsabil de rutarea comenzilor.
*   `database.py` -> -> Abstractizarea bazei de date. Contine clasa `DataBaseManager` care rulează interogarile SQL, deschide conexiunile si izoleaza codul SQL pur.
*   `main_gui.py` -> Interfata grafica desktop autonoma, care ruleaza operatiunile CRUD in mod vizual.
*   `app.log` -> Fisier generat automat de sistemul de logging pentru stocarea istoricului tehnic al actiunilor.

## Mod de Instalare si Rulare

### Pasul 1: Clonarea depozitului
Deschide terminalul si descarca proiectul local de pe GitHub:
```bash
git clone https://github.com
cd proiect-final
```

### Pasul 2: Rularea aplicatiei principale (Consola)
Lanseaza meniul interactiv text ruland scriptul principal:
```bash
python main.py
```

### Pasul 3: Rularea directa a Interfetei Grafice (GUI)
Daca doresti sa pornesti direct fereastra desktop fara meniul din consola, ruleaza:
```bash
python main_gui.py
```

## Exemple de Utilizare

### 1. Meniul Text in Consola ('main.py)
La rulare, sistemul afiseaza un meniu numeric cu 11 optiuni:
```text
1. Adaugare tranzactie
2. Cautare tranzactie
...
8. Analiza economii (Genereaza Raport Text)
11. Iesire
```
Daca selectezi optiunea `6`, programul va interoga tabelele și va afișa:
```text
--- Afisare Sold Total ---
Sold total: 11240.5 RON (Venituri: 15000.0) | Cheltuieli: 3759.5
```

### 2. Managementul Vizual CRUD (`main_gui.py`)
*   **Adaugare (Create):** Introdu denumirea, suma, selecteaza tipul din meniul `Combobox` securizat (readonly) si apasa butonul verde *Adauga (Create)*.
*   **Vizualizare (Read):** Datele sunt citite automat din SQLite si afisate in grila `Treeview`. Bara de sumar calculeaza dinamic profitul net la fiecare modificare.
*   **Actualizare (Update):** Selecteaza o linie din tabel, tasteaza noua data in formular si apasa butonul portocaliu *Modifica Data (Update)*.
*   **Stergere (Delete):** Selecteaza orice tranzactie si apasa butonul rosu *Sterge Rand (Delete)* pentru eliminarea ei definitiva din baza de date.

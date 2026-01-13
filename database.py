import sqlite3

DB_NAME = "database.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def create_tables():
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Kategorie (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Nazwa TEXT NOT NULL,
            Opis TEXT
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Produkty (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Nazwa TEXT NOT NULL,
            Liczba INTEGER,
            Cena REAL,
            Kategoria_id INTEGER,
            FOREIGN KEY (Kategoria_id) REFERENCES Kategorie(id)
        )
        """)

        conn.commit()


# ---- Kategorie ----
def add_category(nazwa, opis):
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO Kategorie (Nazwa, Opis) VALUES (?, ?)",
            (nazwa, opis)
        )
        conn.commit()

def delete_category(category_id):
    with get_connection() as conn:
        conn.execute("DELETE FROM Kategorie WHERE id = ?", (category_id,))
        conn.commit()

def get_categories():
    with get_connection() as conn:
        return conn.execute("SELECT * FROM Kategorie").fetchall()


# ---- Produkty ----
def add_product(nazwa, liczba, cena, kategoria_id):
    with get_connection() as conn:
        conn.execute(
            """INSERT INTO Produkty (Nazwa, Liczba, Cena, Kategoria_id)
               VALUES (?, ?, ?, ?)""",
            (nazwa, liczba, cena, kategoria_id)
        )
        conn.commit()

def delete_product(product_id):
    with get_connection() as conn:
        conn.execute("DELETE FROM Produkty WHERE id = ?", (product_id,))
        conn.commit()

def get_products():
    with get_connection() as conn:
        return conn.execute("""
            SELECT Produkty.id, Produkty.Nazwa, Liczba, Cena, Kategorie.Nazwa
            FROM Produkty
            LEFT JOIN Kategorie ON Produkty.Kategoria_id = Kategorie.id
        """).fetchall()

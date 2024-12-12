import sqlite3
from datetime import datetime

def create_table():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            score INTEGER NOT NULL,
            date TEXT NOT NULL
        )
        """)

def add_to_base(score, 
                date = None):
    if date is None:
        date = datetime.now().strftime('%Y-%m-%d')

    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO scores (score, date)
        VALUES (?, ?)
        """, (score, date))
        conn.commit()
    
def fetch_all_scores():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        # Pobranie wszystkich rekordów
        cursor.execute("SELECT score, date FROM scores ORDER BY score DESC")
        rows = cursor.fetchall()  # Zwraca wszystkie wiersze jako listę krotek
        return rows
    

if __name__ == "__main__":
    create_table()
    #add_to_base(257)
    for row in fetch_all_scores():
        print(row)

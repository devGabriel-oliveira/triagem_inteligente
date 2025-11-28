import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "database.db")

def connect():
    return sqlite3.connect(DB_PATH)


def get_patient_data(patient_id):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, age, symptoms
        FROM patients
        WHERE id = ?
    """, (patient_id,))

    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    # Converte a tupla em dicionário
    return {
        "id": row[0],
        "name": row[1],
        "age": row[2],
        "symptoms": row[3]
    }


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            symptoms TEXT
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        );
    """)

    # Inserir dados iniciais
    cursor.execute("INSERT OR IGNORE INTO users (id, username, password) VALUES (1, 'admin', '1234')")
    cursor.execute("INSERT OR IGNORE INTO patients (id, name, age, symptoms) VALUES (1, 'João da Silva', 30, 'Febre e dor de cabeça')")
    cursor.execute("INSERT OR IGNORE INTO patients (id, name, age, symptoms) VALUES (2, 'Maria Souza', 54, 'Dor no peito e cansaço')")

    conn.commit()
    conn.close()

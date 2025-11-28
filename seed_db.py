import sqlite3
import os

os.makedirs("data", exist_ok=True)

conn = sqlite3.connect("data/health.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    gender TEXT,
    chronic_diseases TEXT,
    last_consult TEXT,
    medications TEXT,
    exams TEXT,
    notes TEXT
)
""")

cur.execute("""
INSERT INTO patients (name, age, gender, chronic_diseases, last_consult, medications, exams, notes)
VALUES
("João Silva", 45, "M", "Hipertensão, Diabetes Tipo 2", "2025-01-10", "Metformina, Enalapril", "Hemograma, Glicemia", "Paciente com histórico de pressão elevada."),
("Maria Souza", 33, "F", "Asma", "2024-12-22", "Bombinha broncodilatadora", "Raio-X, Espirometria", "Relata piora na respiração à noite.")
""")

conn.commit()
conn.close()

print("Banco populado com sucesso!")

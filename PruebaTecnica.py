import sqlite3
import pathlib
import pandas as pd
import numpy as np
from fastapi import FastAPI


con = sqlite3.connect("databasesCrediclub.db")
con.row_factory = sqlite3.Row
con.execute("PRAGMA foreign_keys = 1")

cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS expected_payments (id INTEGER PRIMARY KEY, batch TEXT, customer_name TEXT, amount REAL, expected_date DATE)")
cur.execute("CREATE TABLE IF NOT EXISTS received_payments (id INTEGER PRIMARY KEY, expec_pay_id INTEGER, batch TEXT, amount REAL, received_date DATE, FOREIGN KEY(expec_pay_id) REFERENCES expected_payments(id))")


counter = cur.execute("SELECT COUNT(*) FROM expected_payments")
if counter.fetchone()[0] == 0:
    expected_payments = pd.read_csv("expected_payments.csv")

    cur.executemany("INSERT INTO expected_payments (id, batch, customer_name, amount, expected_date) VALUES (?, ?, ?, ?, ?)", expected_payments.values.tolist())
    con.commit()

counter = cur.execute("SELECT COUNT(*) FROM received_payments")
if counter.fetchone()[0] == 0:
    data = [(1, 1, "BA-202401", 1500.0, "05/01/2024"),
            (2, 2, "BA-202401", 2350.5, "05/03/2024"),
            (3, 4, "BA-202401", 900.0, "06/01/2024")]
    cur.executemany("INSERT INTO received_payments (id, expec_pay_id, batch, amount, received_date) VALUES (?, ?, ?, ?, ?)", data)
    con.commit()



query = """
SELECT 
e.id,
e.batch,
e.customer_name,
e.expected_date,
e.amount as expectedPayment,
r.amount as receivedPayment,
r.received_date
FROM expected_payments e 
LEFT JOIN received_payments r ON e.id = r.expec_pay_id 
WHERE e.batch = 'BA-202401';
"""

pruebaDf = pd.read_sql_query(query, con)
conciliaciones = [
    pruebaDf["receivedPayment"].isna(),
    pruebaDf["receivedPayment"] != pruebaDf["expectedPayment"],
    pruebaDf["expectedPayment"] == pruebaDf["receivedPayment"]
]

resultado = [
    'NO_RECIBIDO', 'MONTO_DIFERENTE', 'CONCILIADO'
]

pruebaDf["Status"] = np.select(conciliaciones, resultado, 'Other')

print(pruebaDf.head())


# app = FastAPI()

# @app.get("/")
# def root():
#     return {"message": "API funciona"}

# @app.post("/reconciliation")
# def reconciliation(batch: str = "BA-202401"): 
#     cur.execute("SELECT * FROM expected_payments")
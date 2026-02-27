con = sqlite3.connect("databasesCrediclub.db", check_same_thread=False)
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



def conciliationDf(batch):
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
        WHERE e.batch = ?;
        """

    df = pd.read_sql_query(query, con, params=(batch,))
    conciliaciones = [
        df["receivedPayment"].isna(),
        df["receivedPayment"] != df["expectedPayment"],
        df["expectedPayment"] == df["receivedPayment"]
    ]

    resultado = [
        'NO_RECIBIDO', 'MONTO_DIFERENTE', 'CONCILIADO'
    ]

    df["Status"] = np.select(conciliaciones, resultado, 'Other')


    return df


app = FastAPI()

@app.post("/reconciliation")
def reconciliation(batch: str): 

    df = conciliationDf(batch)

    response = requests.get('https://v6.exchangerate-api.com/v6/d2e6dd3982783fddcfc973cc/latest/MXN') 
    data = response.json() 
    df['expectedPayment(USD)'] = data['conversion_rates']['USD'] * df['expectedPayment']
    df['receivedPayment(USD)'] = data['conversion_rates']['USD'] * df['receivedPayment']

    client = genai.Client(api_key="AIzaSyATUcPs1E3l(delete this section including parenthesis)CeG2x_7wv7xlVEXj6bzATpY")
    response = client.models.generate_content(
        model="gemini-3-flash-preview", contents="Summarize the info inside the dataframe as a data analyst" + df.to_json(orient="records")
    )

    df.loc[0, ['Summarize (LLM)']] = response.text

    filenameReport = f"Report_" + batch + "_" + dt.now().strftime("%Y-%m-%d") + ".xlsx"

    writer = pd.ExcelWriter(filenameReport, mode='w',if_sheet_exists=None)
    df.to_excel(writer, sheet_name='conciliation_sheet',index=False)
    writer.close()

    

    return FileResponse(filenameReport, media_type ='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', filename = filenameReport)






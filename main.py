import sqlite3
from fastapi import FastAPI
from createDatabases import create_databases


#create the needed databases if they do not exist
create_databases()

#define database connections for reading and writing to the databases
user_connection = sqlite3.connect("users.db")
users = user_connection.cursor()

sender_dastabase_connection = sqlite3.connect("sender_transactions.db")
sender_database_cursor = sender_dastabase_connection.cursor()

receiver_dastabase_connection = sqlite3.connect("receiver_transactions.db")
receiver_database_cursor = receiver_dastabase_connection.cursor()

accounts_connection = sqlite3.connect("accounts.db")
accounts_cursor = accounts_connection.cursor()

finished_transactions = sqlite3.connect("finished_transactions.db")
finished = finished_transactions.cursor()

error_database_connection = sqlite3.connect("error_database.db")
error_database_cursor = error_database_connection.cursor()

#define FastAPI app 
app = FastAPI()

#receive sender's half of the transaction information and store it to the temporary database
@app.post("/api/v1/send/{key}/{user_id}/{amount}/{operating_system}/{timestamp}")
async def send(user_id, amount, key, operating_system, timestamp):
    sender_database_cursor.execute(
        f"""INSERT INTO sent_transactions (key, user_id, paid_amount, sender_os, sent_timestamp) 
        VALUES ('{str(key)}', {int(user_id)}, {float(amount)}, '{str(operating_system)}', '{str(timestamp)}')""")
    sender_dastabase_connection.commit()

#receive receiver information
@app.post("/api/v1/recieve/{key}/{user_id}/{sender_id}/{amount}/{operating_system}")
async def recieve(key, user_id, sender_id, amount, operating_system):
    
    receiver_database_cursor.execute(
        F"""INSERT INTO received_transactions (key, user_id, sender_id, expected_amount, receiver_os)
        VALUES ('{str(key)}', {int(user_id)}, {int(sender_id)}, {float(amount)}, '{operating_system}')""")
    receiver_dastabase_connection.commit()

#create new account
@app.post("/api/v1/create/{user_id}/{account_number}/{balance}/{account_type}/{bank_sender}")
async def create_user(user_id, account_number, balance, account_type, bank_sender):
    accounts_cursor.execute(f"""INSERT INTO accounts (user_id, account_number, account_balance, account_type, bank_sender) 
                            VALUES ({int(user_id)}, {int(account_number)}, {float(balance)}, '{str(account_type)}', '{str(bank_sender)}')""")
    accounts_connection.commit()



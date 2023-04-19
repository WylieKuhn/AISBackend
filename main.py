import sqlite3
from fastapi import FastAPI
from createDatabases import create_databases
import hashlib
from datetime import datetime

#create the needed databases if they do not exist
create_databases()

#define database connections for reading and writing to the databases
user_connection = sqlite3.connect("users.db")
users = user_connection.cursor()
accounts_connection = sqlite3.connect("accounts.db")
accounts_cursor = accounts_connection.cursor()
transaction_connection = sqlite3.connect("transactions.db")
transactions = transaction_connection.cursor()
finished_transactions = sqlite3.connect("finished_transactions.db")
finished = finished_transactions.cursor()

#define FastAPI app 
app = FastAPI()

#receive sender information and store it to a temporary database
@app.post("/api/v1/send/{user_id}/{amount}/{key}/{salt}/{operating_system}")
async def send(user_id, amount, key, salt, operating_system):
    transactions.execute(
        f"""INSERT INTO transactions (user_id, paid_amount, key, salt, sender_os) 
        VALUES ({int(user_id)}, {float(amount)}, {int(key)}, {int(salt)}, '{str(operating_system)}')""")
    transaction_connection.commit()

#receive receiver information
@app.post("/api/v1/recieve/{user_id}/{key}/{operating_system}")
async def recieve(user_id, key, operating_system):
    
    # pull sender info from database
    user_key = int(key)
    transactions.execute(f"SELECT * FROM transactions WHERE key = {user_key}")
    sender_transaction_info = transactions.fetchone()
    print(sender_transaction_info)

    sender_key = sender_transaction_info[2]+sender_transaction_info[3]
    reciever_key = int(key)+sender_transaction_info[3]
    hashed_sender_key = hashlib.sha3_512(
        (str(sender_key)).encode()).hexdigest()
    hashed_reciever_key = hashlib.sha3_512(
        str(reciever_key).encode()).hexdigest()

    if hashed_sender_key != hashed_reciever_key:
        transactions.execute(
            f"DELETE FROM transactions WHERE key = {int(key)}")

    if hashed_sender_key == hashed_reciever_key:
        timestamp = str(datetime.now())

        # pull sender info from database as it will be the only entry with a matching key
        # get info of of transaction from sender from transactions database

        accounts_cursor.execute(
            f"SELECT * FROM accounts WHERE user_id = {int(user_id)}")
        reciever_account_info = accounts_cursor.fetchone()

        accounts_cursor.execute(
            f"SELECT * FROM accounts WHERE user_id = {sender_transaction_info[0]}")
        sender_account_info = accounts_cursor.fetchone()

        if sender_account_info[2] > sender_transaction_info[1]:

            # update account balances of the users
            new_sender_balance = sender_account_info[2] - \
                sender_transaction_info[1]
            new_reciever_balance = reciever_account_info[2] + \
                sender_transaction_info[1]

            accounts_cursor.execute(
                f"UPDATE accounts SET account_balance = {new_sender_balance} WHERE user_id = {sender_transaction_info[0]}")
            accounts_connection.commit()
            accounts_cursor.execute(
                f"UPDATE accounts SET account_balance = {new_reciever_balance} WHERE user_id = {int(user_id)}")
            accounts_connection.commit()

            finished.execute(F"""INSERT INTO transactions (account_number_sender, account_number_receiver,
                                transaction_timestamp, transfer_amount, beginning_balance_sender, bank_sender, os_sender, os_receiver,
                                unanimous_agreement, transaction_error) VALUES ({int(sender_account_info[0])}, {int(reciever_account_info[0])}, 
                                '{timestamp}', {float(sender_transaction_info[1])}, {float(sender_account_info[2])}, '{sender_account_info[4]}',
                                '{sender_transaction_info[4]}', '{operating_system}', 1, 0)""")
            finished_transactions.commit()
            transactions.execute(
                f"DELETE FROM transactions WHERE key = {int(key)}")
            transaction_connection.commit()

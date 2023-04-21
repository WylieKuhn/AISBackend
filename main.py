import sqlite3
from fastapi import FastAPI
from createDatabases import create_databases
from pydantic import BaseModel


#create the needed databases if they do not exist
create_databases()

#define database connections for reading and writing to the databases
database_connection = sqlite3.connect("app_database.db")
cur = database_connection.cursor()

#define FastAPI app 
app = FastAPI()

class SentTransaction(BaseModel):
    key: str
    user_id: int
    transfer_amount: float
    os_sender: str
    transaction_time: str
    
class ReceivedTransaction(BaseModel):
    key: str
    user_id: int
    sender_id: int
    expected_amount: float
    os_receiver: str
    
class NewAccount(BaseModel):
    user_id: int
    account_number: int
    balance: int
    account_type: str
    bank_sender: str
    

#receive sender's half of the transaction information and store it to the temporary database
@app.post("/api/v1/send/")
async def send(sender_transaction: SentTransaction):
    cur.execute("""INSERT INTO sent_transactions (key, user_id, paid_amount, sender_os, sent_timestamp) 
    VALUES (?, ?, ?, ?, ?)""", (sender_transaction.key, sender_transaction.user_id, sender_transaction.transfer_amount, 
    sender_transaction.os_sender, sender_transaction.transaction_time))
    database_connection.commit()

#receive receiver information
@app.post("/api/v1/recieve/")
async def recieve(received_transaction: ReceivedTransaction):
    
    cur.execute(
        """INSERT INTO received_transactions (key, user_id, sender_id, expected_amount, receiver_os)
        VALUES (?, ?, ?, ?, ?)""", (received_transaction.key, received_transaction.user_id, received_transaction.sender_id, 
        received_transaction.expected_amount, received_transaction.os_receiver))
    database_connection.commit()

#create new account
@app.post("/api/v1/create/")
async def create_user(account: NewAccount):
    cur.execute("""INSERT INTO accounts (user_id, account_number, account_balance, account_type, bank_sender) 
                            VALUES (?, ?, ?, ?, ?)""", (account.user_id, account.account_number, account.balance, 
                                                        account.account_type, account.bank_sender))
    database_connection.commit()



import sqlite3
from fastapi import FastAPI
from createDatabases import create_databases
from pydantic import BaseModel
import hashlib
from fastapi.security.api_key import APIKeyHeader
from fastapi import Security
from datetime import datetime

api_key_header = APIKeyHeader(name="api_key", auto_error=False)


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
async def send(sender_transaction: SentTransaction, api_key: str = Security(api_key_header)):
    
    cur.execute("SELECT * FROM accounts WHERE user_id = ?", (sender_transaction.user_id, ))
    
    account = cur.fetchone()
    salt = str(account[6])
    to_hash = str(api_key)+salt
    hashed_api_key = hashlib.sha3_512(to_hash.encode()).hexdigest()
    
    if account[5] == hashed_api_key: 
        cur.execute("""INSERT INTO sent_transactions (key, user_id, paid_amount, sender_os, sent_timestamp) 
        VALUES (?, ?, ?, ?, ?)""", (sender_transaction.key, sender_transaction.user_id, sender_transaction.transfer_amount, 
        sender_transaction.os_sender, sender_transaction.transaction_time))
        database_connection.commit()
        
    if account[5] != hashed_api_key: 
        error = "ERROR 500: UNRECOGNIZED API KEY"
        r_id = "None"
        endpoint = "/api/v1/send/"
        print(error)
        
        cur.execute("""INSERT INTO api_failures (attempted_api_key, sender_id, receiver_id, transfer_amount, operating_system, timestamp, endpoint) VALUES(?, ?, ?, ?, ?, ?, ?)""",
                    (str(api_key), sender_transaction.user_id, r_id, sender_transaction.transfer_amount, sender_transaction.os_sender, sender_transaction.transaction_time, endpoint))
        database_connection.commit()
    

#receive receiver information
@app.post("/api/v1/recieve/")
async def recieve(received_transaction: ReceivedTransaction, api_key: str = Security(api_key_header)):
    
    cur.execute("SELECT * FROM accounts WHERE user_id = ?", (received_transaction.user_id, ))
    
    receiver_account = cur.fetchone()
    receiver_salt = str(receiver_account[6])
    to_hash = str(api_key)+receiver_salt
    hashed_api_key = hashlib.sha3_512(to_hash.encode()).hexdigest()
    
    if receiver_account[5] == hashed_api_key:
        cur.execute(
            """INSERT INTO received_transactions (key, user_id, sender_id, expected_amount, receiver_os)
            VALUES (?, ?, ?, ?, ?)""", (received_transaction.key, received_transaction.user_id, received_transaction.sender_id, 
            received_transaction.expected_amount, received_transaction.os_receiver))
        database_connection.commit()
    
    if receiver_account[5] != hashed_api_key:
        error = "ERROR 500: UNRECOGNIZED API KEY"
        timestamp = str(datetime.now())
        receiver_endpoint = "/api/v1/recieve/"
        print(error)
        
        cur.execute("""INSERT INTO api_failures (attempted_api_key, sender_id, receiver_id, transfer_amount, operating_system, timestamp, endpoint) 
                    VALUES(?, ?, ?, ?, ?, ?, ?)""",(str(api_key), received_transaction.sender_id, received_transaction.user_id, received_transaction.expected_amount, 
                     received_transaction.os_receiver, timestamp, receiver_endpoint))
        database_connection.commit()
        

#create new account
@app.post("/api/v1/create/")
async def create_user(account: NewAccount):
    cur.execute("""INSERT INTO accounts (user_id, account_number, account_balance, account_type, bank_sender) 
                            VALUES (?, ?, ?, ?, ?)""", (account.user_id, account.account_number, account.balance, 
                                                        account.account_type, account.bank_sender))
    database_connection.commit()



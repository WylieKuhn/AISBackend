import requests
import random



def create_account():
    
    user_id = random.randint(100_000_000_000, 999_999_999_999)
    account_number = random.randint(100_000_000_000, 999_999_999_999)
    balance = float(input("Initial Balance: "))
    account_type = str(input("Account type: "))
    bank_sender = str(input("Bank sender: "))
    
    new_account = {"user_id": user_id, "account_number": account_number, "balance": balance, "account_type": account_type, "bank_sender": bank_sender}
    requests.post("http://127.0.0.1:8000/api/v1/create/", json=new_account)
    
create_account()
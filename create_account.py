import requests
import random



def create_account():
    
    user_id = random.randint(100_000_000_000, 999_999_999_999)
    account_number = random.randint(100_000_000_000, 999_999_999_999)
    balance = float(input("Initial Balance: "))
    account_type = str(input("Account type: "))
    bank_sender = str(input("Bank sender: "))
    requests.post(f"http://127.0.0.1:8000/api/v1/create/{user_id}/{account_number}/{balance}/{account_type}/{bank_sender}")
    
create_account()
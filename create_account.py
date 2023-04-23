import requests
import random
import ssl
import warnings
from requests.packages.urllib3.exceptions import SubjectAltNameWarning
import uuid
import hashlib

warnings.filterwarnings("ignore", category=SubjectAltNameWarning)

context = ssl.create_default_context()
context.load_verify_locations('cert.pem')



def create_account():
    
    user_id = random.randint(100_000_000_000, 999_999_999_999)
    account_number = random.randint(100_000_000_000, 999_999_999_999)
    balance = float(input("Initial Balance: "))
    account_type = str(input("Account type: "))
    bank_sender = str(input("Bank sender: "))
    
    new_api_key = str(uuid.uuid4())
    salt = str(uuid.uuid4())
    to_hash = new_api_key+salt
    main_hash = hashlib.sha3_512(to_hash.encode()).hexdigest()
    
    new_account = {"user_id": user_id, "account_number": account_number, "balance": balance, "account_type": account_type, 
                   "bank_sender": bank_sender, "salt": salt, "hashed_api_key": main_hash}
    requests.post("https://127.0.0.1:8000/api/v1/create/", json=new_account, verify="cert.pem", timeout=3)
    print(new_api_key)
    
create_account()
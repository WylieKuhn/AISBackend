import requests
import platform
import uuid
from datetime import datetime
import ssl
import warnings
from requests.packages.urllib3.exceptions import SubjectAltNameWarning
from key_file import sender_api_key, receiver_api_key

sender_api = sender_api_key
receiver_api = receiver_api_key

warnings.filterwarnings("ignore", category=SubjectAltNameWarning)

context = ssl.create_default_context()
context.load_verify_locations('cert.pem')
# get sender and receiver operating systems
sender_os = str(platform.platform())
reciever_os = str(platform.platform())

# enter amount to send
send_amount = float(input("Enter amount to send: "))

# randomly generate key and get timestamp of the transaction
key = str(uuid.uuid4())
timestamp = str(datetime.now())


# define sender information
sender = {"key": key,"user_id": 1234567890, "transfer_amount": send_amount,
          "os_sender": sender_os,  "transaction_time": str(timestamp)}

sender_header = {
    'Content-Type': 'application/json',
    'api_key': sender_api
}

receiver = {"key": str(key), "user_id": 2234567890, "sender_id": sender['user_id'], 
            "expected_amount": sender['transfer_amount'], "os_receiver": str(reciever_os)}

receiver_header = {
    'Content-Type': 'application/json',
    'api_key': receiver_api
}



# send sender transaction half to the API
requests.post("https://127.0.0.1:8000/api/v1/send/", json = sender, verify="cert.pem", headers=sender_header, timeout=3)


# send reciever transaction half to the API
requests.post("https://127.0.0.1:8000/api/v1/recieve/", json = receiver, verify="cert.pem",headers=receiver_header, timeout=3)


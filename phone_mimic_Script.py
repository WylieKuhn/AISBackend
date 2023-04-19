import requests
import json
import platform
import random
import time

#get sender and receiver operating systems
sender_os = platform.platform()
reciever_os = platform.platform()

#enter amount to send
send_amount = float(input("Enter amount to send: "))

#randomly generate key and salt
key = random.randint(1000, 9999)
salt = random.randint(1_000_000, 9_999_999)

#define sender information
sender = {"user_id": 1234567890, "transfer_amount": send_amount,
          "os_sender": sender_os, "key": key, "salt": salt}
sender_json = json.dumps(sender)

#send sender transaction half to the API
requests.post(
    f"http://127.0.0.1:8000/api/v1/send/{sender['user_id']}/{sender['transfer_amount']}/{sender['key']}/{sender['salt']}/{sender['os_sender']}")

time.sleep(2)

#define reciever information 
reciever = {"user_id": 2234567890, "key": key, "os_receiver": reciever_os}

#send reciever transaction half to the API
requests.post(
    f"http://127.0.0.1:8000/api/v1/recieve/{reciever['user_id']}/{reciever['key']}/{reciever['os_receiver']}")

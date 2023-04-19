import requests
import json
import platform
import random
import time


sender_os = platform.platform()
reciever_os = platform.platform()
send_amount = float(input("Enter amount to send: "))
key = random.randint(1000, 9999)
salt = random.randint(1_000_000, 9_999_999)

sender = {"user_id": 1234567890, "transfer_amount": send_amount,
          "os_sender": sender_os, "key": key, "salt": salt}
sender_json = json.dumps(sender)
requests.post(
    f"http://127.0.0.1:8000/api/v1/send/{sender['user_id']}/{sender['transfer_amount']}/{sender['key']}/{sender['salt']}/{sender['os_sender']}")

time.sleep(2)

reciever = {"user_id": 2234567890, "key": key, "os_receiver": reciever_os}
requests.post(
    f"http://127.0.0.1:8000/api/v1/recieve/{reciever['user_id']}/{reciever['key']}/{reciever['os_receiver']}")

import requests
import platform
import time
import uuid
from datetime import datetime
# get sender and receiver operating systems
sender_os = str(platform.platform())
reciever_os = str(platform.platform())

# enter amount to send
send_amount = float(input("Enter amount to send: "))

# randomly generate key and salt
key = str(uuid.uuid4())
timestamp = str(datetime.now())


# define sender information
sender = {"user_id": 1234567890, "transfer_amount": send_amount,
          "os_sender": sender_os, "key": key, "transaction_time": str(timestamp)}

receiver = {"user_id": 2234567890, "key": key,
            "os_receiver": reciever_os, "expected_amount": send_amount}

# send sender transaction half to the API
requests.post(
    f"http://127.0.0.1:8000/api/v1/send/{sender['key']}/{sender['user_id']}/{sender['transfer_amount']}/{sender['os_sender']}/{sender['transaction_time']}")

time.sleep(2)

# define reciever information


# send reciever transaction half to the API
requests.post(
    f"http://127.0.0.1:8000/api/v1/recieve/{receiver['key']}/{receiver['user_id']}/{sender['user_id']}/{receiver['expected_amount']}/{receiver['os_receiver']}")

import sqlite3
import platform
import uuid
from datetime import datetime, timedelta


database_connection = sqlite3.connect("app_database.db")
cur = database_connection.cursor()

key = str(uuid.uuid4())
timestamp = str(datetime.now())

old_time = datetime.now()-timedelta(minutes=10)


# define sender information
sender = {"user_id": 1234567890, "transfer_amount": 50,
          "os_sender": str(platform.platform()), "key": key, "transaction_time": str(old_time)}

receiver = {"user_id": 2234567890, "key": key,
            "os_receiver": str(platform.platform()), "expected_amount": 50}

cur.execute(f"""INSERT INTO sent_transactions (key, user_id, paid_amount, sender_os, sent_timestamp) 
                               VALUES ('{sender['key']}', {sender['user_id']}, {float(sender['transfer_amount'])}, 
                               '{sender['os_sender']}', '{sender['transaction_time']}')""")
database_connection.commit()

cur.execute(f"""INSERT INTO received_transactions (key, user_id, sender_id, expected_amount, receiver_os, transaction_time) 
                                 VALUES ('{receiver['key']}', {receiver['user_id']}, {sender['user_id']} , {float(receiver['expected_amount'])}, 
                                 '{receiver['os_receiver']}', '{old_time}')""")
database_connection.commit()
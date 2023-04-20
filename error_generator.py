import sqlite3
import platform
import uuid
from datetime import datetime


sender_dastabase_connection = sqlite3.connect("sender_transactions.db")
sender_database_cursor = sender_dastabase_connection.cursor()

receiver_dastabase_connection = sqlite3.connect("receiver_transactions.db")
receiver_database_cursor = receiver_dastabase_connection.cursor()

key = str(uuid.uuid4())
timestamp = str(datetime.now())


# define sender information
sender = {"user_id": 1234567890, "transfer_amount": 50,
          "os_sender": str(platform.platform()), "key": key, "transaction_time": str(timestamp)}

receiver = {"user_id": 2234567890, "key": key,
            "os_receiver": platform.platform, "expected_amount": 49.95}

sender_database_cursor.execute(f"""INSERT INTO sent_transactions (key, user_id, paid_amount, sender_os, sent_timestamp) 
                               VALUES ('{sender['key']}', {sender['user_id']}, {float(sender['transfer_amount'])}, 
                               '{sender['os_sender']}', '{sender['transaction_time']}')""")
sender_dastabase_connection.commit()

receiver_database_cursor.execute(f"""INSERT INTO received_transactions (key, user_id, sender_id, expected_amount, receiver_os) 
                                 VALUES ('{receiver['key']}', {receiver['user_id']}, 0987654321 , {float(receiver['expected_amount'])}, '{receiver['os_receiver']}')""")
receiver_dastabase_connection.commit()
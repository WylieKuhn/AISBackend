import sqlite3
from datetime import datetime, timedelta
import time

database_connection = sqlite3.connect("app_database.db")
cur = database_connection.cursor()


def complete_transactions():

    # pull sender info from database using public key
    cur.execute("""SELECT * FROM received_transactions""")
    received_transactions = cur.fetchall()
    cur.execute("""SELECT * FROM sent_transactions""")
    sent_transactions = cur.fetchall()
    time_of_check = datetime.now()

    for receieved_transaction in received_transactions:
        
        if receieved_transaction[5]:
            received_time = datetime.strptime(receieved_transaction[5], "%Y-%m-%d %H:%M:%S.%f")
            if received_time < time_of_check-timedelta(minutes=5):
                error = "ERROR 500: TRANSACTION TIMEOUT"
                cur.execute("DELETE FROM received_transactions WHERE key = ?", (str(receieved_transaction[0]), ))
                database_connection.commit()
                print("TIME ERROR SUCCESS")
                
                cur.execute("SELECT * FROM accounts WHERE user_id = ?", (receieved_transaction[1], ))
                r_account = cur.fetchone()
                cur.execute("SELECT * FROM accounts WHERE user_id = ?", (receieved_transaction[2], ))
                s_account = cur.fetchone()
                
                
                cur.execute("""INSERT INTO errors (account_number_sender, account_number_receiver,
                            transaction_timestamp, transfer_amount, beginning_balance_sender, bank_sender, os_sender, os_receiver,
                            unanimous_agreement, error_explanation, error_code, transaction_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                            (r_account[1], s_account[1], receieved_transaction[5], receieved_transaction[3], s_account[2],
                            s_account[4], 'None', receieved_transaction[4], 1, error, 500, receieved_transaction[0]))
                database_connection.commit()
    
    for sent_transaction in sent_transactions:
        if sent_transaction[4]:
            sent_time = datetime.strptime(sent_transaction[4], "%Y-%m-%d %H:%M:%S.%f")
            if sent_time < time_of_check-timedelta(minutes=5):
                error = "ERROR 500: TRANSACTION TIMEOUT"
                cur.execute("DELETE FROM sent_transactions WHERE key = ?", (str(sent_transaction[0]), ))
                database_connection.commit()
                print("TIME ERROR SUCCESS")
                
                cur.execute("SELECT * FROM accounts WHERE user_id = ?", (sent_transaction[1], ))
                s_account = cur.fetchone()
                
                
                cur.execute("""INSERT INTO errors (account_number_sender, account_number_receiver,
                            transaction_timestamp, transfer_amount, beginning_balance_sender, bank_sender, os_sender, os_receiver,
                            unanimous_agreement, error_explanation, error_code, transaction_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                            (s_account[1], 0, sent_transaction[4], sent_transaction[2], s_account[2],
                            s_account[4], sent_transaction[3], 'None', 1, error, 500, sent_transaction[0]))
                database_connection.commit()
                
                
                
    
    cur.execute("""SELECT * FROM received_transactions""")
    received_transactions = cur.fetchall()
    cur.execute("""SELECT * FROM sent_transactions""")
    sent_transactions = cur.fetchall()

    for receieved_transaction in received_transactions:
        for sent_transaction in sent_transactions:

            receiver_key = str(receieved_transaction[0])
            sender_key = str(sent_transaction[0])
            receiever_id = int(receieved_transaction[1])
            expected_sender_id = int(receieved_transaction[2])
            sender_id = sent_transaction[1]
            expected_amount = float(receieved_transaction[3])
            paid_amount = float(sent_transaction[2])
            # get time of transaction
            timestamp = str(sent_transaction[4])

            # verify transactions match
            if receiver_key == sender_key:

                # get sender's account info
                sender_account_info = cur.execute(
                    "SELECT * FROM accounts WHERE user_id = ?", (sender_id, )).fetchone()

                # get receiver's account info
                cur.execute(
                    "SELECT * FROM accounts WHERE user_id = ?", (receiever_id, ))
                receiver_account_info = cur.fetchone()

                if sender_id == expected_sender_id and expected_amount == paid_amount:

                    sender_balance = float(sender_account_info[2])

                    # make sure sender's account balance is enough to cover the amount being sent
                    if sender_balance > paid_amount:
                        receiver_balance = float(receiver_account_info[2])

                        # update account balances of the users
                        new_sender_balance = sender_balance - paid_amount
                        new_reciever_balance = receiver_balance + paid_amount

                        cur.execute(
                            "UPDATE accounts SET account_balance = ? WHERE user_id = ?", (new_sender_balance, sender_id))
                        database_connection.commit()
                        cur.execute(
                            "UPDATE accounts SET account_balance = ? WHERE user_id = ?", (new_reciever_balance, receiever_id))
                        database_connection.commit()

                        # insert final permanent trasaction record into the finished transactions databse
                        cur.execute("""INSERT INTO finished_transactions (transaction_key, account_number_sender, account_number_receiver,
                                            transaction_timestamp, transfer_amount, beginning_balance_sender, bank_sender, os_sender, os_receiver,
                                            unanimous_agreement, transaction_error) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                                    (sender_key, sender_account_info[1], receiver_account_info[1], timestamp, paid_amount, receiver_balance, sender_account_info[4],
                                     sent_transaction[3], receieved_transaction[4], 1, 0))
                        database_connection.commit()

                        # delete transaction verification record from temporary transaction database
                        cur.execute(
                            "DELETE FROM sent_transactions WHERE key = ?", (sender_key,))
                        database_connection.commit()

                        cur.execute(
                            "DELETE FROM received_transactions WHERE key = ?", (receiver_key, ))
                        database_connection.commit()
                        print(f"COMPLETED TRANSACTION {receiver_key}")

                    # deny and log error if balance is not enough to cover paid amount
                    elif sender_balance < paid_amount:
                        print(
                            "ERROR CODE 1OO: TRANSACTION FAILURE DUE TO ATTEMPTED OVERDRAW.")
                        receiver_balance = float(receiver_account_info[2])
                        error = "ATTEMPTED OVERDRAW: Paid amount exceeds balance"

                        # insert final permanent trasaction record into the finished transactions databse
                        cur.execute("""INSERT INTO errors (account_number_sender, account_number_receiver,
                                            transaction_timestamp, transfer_amount, beginning_balance_sender, bank_sender, os_sender, os_receiver,
                                            unanimous_agreement, error_explanation, error_code, transaction_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                                    (sender_account_info[1], receiver_account_info[1], timestamp, sent_transaction[2], sender_account_info[2],
                                     sender_account_info[4], sent_transaction[3], receieved_transaction[4], 1, error, 100, sender_key))
                        database_connection.commit()

                        # delete transaction verification record from temporary transaction database
                        cur.execute(
                            "DELETE FROM sent_transactions WHERE key = ?", (sender_key, ))
                        database_connection.commit()

                        cur.execute(
                            "DELETE FROM received_transactions WHERE key = ?", (receiver_key, ))
                        database_connection.commit()

            if sender_id != expected_sender_id:
                error = "ERROR CODE 200: SENDER ID MISMATCH."
                print(error)
                cur.execute("""INSERT INTO errors (account_number_sender, account_number_receiver,
                                transaction_timestamp, transfer_amount, beginning_balance_sender, bank_sender, os_sender, os_receiver,
                                unanimous_agreement, error_explanation, error_code, transaction_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                            (sender_account_info[1], receiver_account_info[1], timestamp, sent_transaction[2], sender_account_info[2],
                             sender_account_info[4], sent_transaction[3], receieved_transaction[4], 1, error, 200, sender_key))
                database_connection.commit()

            if expected_amount != paid_amount:
                error = "ERROR CODE 300: TRANSACTION AMOUNT MISMATCH."
                print(error)
                cur.execute("""INSERT INTO errors (account_number_sender, account_number_receiver,
                                transaction_timestamp, transfer_amount, beginning_balance_sender, bank_sender, os_sender, os_receiver,
                                unanimous_agreement, error_explanation, error_code, transaction_id) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                            (sender_account_info[1], receiver_account_info[1], timestamp, sent_transaction[2], sender_account_info[2],
                             sender_account_info[4], sent_transaction[3], receieved_transaction[4], 1, error, 300, sender_key))
                database_connection.commit()

            cur.execute(
                "DELETE FROM sent_transactions WHERE key = ?", (sender_key, ))
            database_connection.commit()

            cur.execute(
                "DELETE FROM received_transactions WHERE key = ?", (receiver_key, ))
            database_connection.commit()


while (True):
    complete_transactions()
    time.sleep(1)

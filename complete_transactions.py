import sqlite3
import time

accounts_connection = sqlite3.connect("accounts.db", check_same_thread=False)
accounts_cursor = accounts_connection.cursor()

finished_transactions = sqlite3.connect("finished_transactions.db", check_same_thread=False)
finished = finished_transactions.cursor()

sender_dastabase_connection = sqlite3.connect("sender_transactions.db", check_same_thread=False)
sender_database_cursor = sender_dastabase_connection.cursor()

receiver_dastabase_connection = sqlite3.connect("receiver_transactions.db", check_same_thread=False)
receiver_database_cursor = receiver_dastabase_connection.cursor()

error_database_connection = sqlite3.connect("error_database.db", check_same_thread=False)
error_database_cursor = error_database_connection.cursor()


def complete_transactions():
    
    # pull sender info from database using public key
    receiver_database_cursor.execute("""SELECT * FROM received_transactions""")
    received_transactions = receiver_database_cursor.fetchall()
    sent_transactions = sender_database_cursor.execute("""SELECT * FROM sent_transactions""")
    
    for receieved_transaction in received_transactions:
        for sent_transaction in sent_transactions:
            receiver_key = str(receieved_transaction[0])
            sender_key = str(sent_transaction[0])
            receiever_id = int(receieved_transaction[1])
            expected_sender_id = int(receieved_transaction[2])
            sender_id = sent_transaction[1]
            expected_amount = float(receieved_transaction[3])
            paid_amount = float(sent_transaction[2])
            
            #verify transactions match
            if receiver_key == sender_key and sender_id == expected_sender_id and expected_amount == paid_amount:
                #get time of transaction
                timestamp = str(sent_transaction[4])
                
                
                #get sender's account info
                accounts_cursor.execute(f"SELECT * FROM accounts WHERE user_id = {sender_id}")
                sender_account_info = accounts_cursor.fetchone()
                #get receiver's account info
                accounts_cursor.execute(f"SELECT * FROM accounts WHERE user_id = {receiever_id}")
                receiver_account_info = accounts_cursor.fetchone()
                
                sender_balance = float(sender_account_info[2])
                

                #make sure sender's account balance is enough to cover the amount being sent
                if sender_balance > paid_amount:
                    receiver_balance = float(receiver_account_info[2])

                    # update account balances of the users
                    new_sender_balance = sender_balance - paid_amount
                    new_reciever_balance = receiver_balance + paid_amount

                    accounts_cursor.execute(
                        f"UPDATE accounts SET account_balance = {new_sender_balance} WHERE user_id = {int(sender_id)}")
                    accounts_connection.commit()
                    accounts_cursor.execute(
                        f"UPDATE accounts SET account_balance = {new_reciever_balance} WHERE user_id = {int(receiever_id)}")
                    accounts_connection.commit()

                    #insert final permanent trasaction record into the finished transactions databse
                    finished.execute(F"""INSERT INTO finished_transactions (account_number_sender, account_number_receiver,
                                        transaction_timestamp, transfer_amount, beginning_balance_sender, bank_sender, os_sender, os_receiver,
                                        unanimous_agreement, transaction_error) VALUES ({int(sender_account_info[0])}, {int(receiver_account_info[0])}, 
                                        '{timestamp}', {float(sent_transaction[1])}, {receiver_balance}, '{str(sender_account_info[4])}',
                                        '{sent_transaction[3]}', '{receieved_transaction[4]}', 1, 0)""")
                    finished_transactions.commit()
                    
                    #delete transaction verification record from temporary transaction database
                    sender_database_cursor.execute(
                        f"DELETE FROM sent_transactions WHERE key = '{str(sender_key)}'")
                    sender_dastabase_connection.commit()
                    
                    receiver_database_cursor.execute(f"DELETE FROM received_transactions WHERE key = '{str(receiver_key)}'")
                    receiver_dastabase_connection.commit()
                    print(f"COMPLETED TRANSACTION {receiver_key}")
                
                #deny and log error if balance is not enough to cover paid amount
                elif sender_balance > paid_amount:
                    receiver_balance = float(receiver_account_info[2])
                    error = "ATTEMPTED OVERDRAW: Paid amount exceeds balance"

                    #insert final permanent trasaction record into the finished transactions databse
                    error_database_cursor.execute(F"""INSERT INTO errors (account_number_sender, account_number_receiver,
                                        transaction_timestamp, transfer_amount, beginning_balance_sender, bank_sender, os_sender, os_receiver,
                                        unanimous_agreement, transaction_error, error_explanation) VALUES ({int(sender_account_info[0])}, {int(receiver_account_info[0])}, 
                                        '{timestamp}', {float(sent_transaction[1])}, {receiver_balance}, '{str(sender_account_info[4])}',
                                        '{sent_transaction[3]}', '{receieved_transaction[4]}', 1, 1, '{str(error)}')""")
                    error_database_connection.commit()
                    
                    #delete transaction verification record from temporary transaction database
                    sender_database_cursor.execute(
                        f"DELETE FROM sent_transactions WHERE key = {sender_key}")
                    sender_dastabase_connection.commit()
                    
                    receiver_database_cursor.execute(f"DELETE FROM received_transactions WHERE key = {receiver_key}")
                    receiver_dastabase_connection.commit()
                    
while(True):
    complete_transactions()
    time.sleep(2)
    
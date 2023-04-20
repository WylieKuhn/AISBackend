import sqlite3

finished_connection = sqlite3.connect("finished_transactions.db")
finished_cursor = finished_connection.cursor()
finished_cursor.execute("DELETE FROM finished_transactions WHERE account_number_sender = 1234567890")
finished_connection.commit()

accounts_connection = sqlite3.connect("accounts.db")
accounts_cursor = accounts_connection.cursor()

accounts_cursor.execute("UPDATE accounts SET account_balance = 1000000 WHERE user_id = 1234567890")
accounts_connection.commit()
accounts_cursor.execute("UPDATE accounts SET account_balance = 1000000 WHERE user_id = 2234567890")
accounts_connection.commit()
accounts_cursor.execute("DELETE FROM accounts WHERE user_id = 638987499414")
accounts_connection.commit()

sender_dastabase_connection = sqlite3.connect("sender_transactions.db")
sender_database_cursor = sender_dastabase_connection.cursor()

receiver_dastabase_connection = sqlite3.connect("receiver_transactions.db")
receiver_database_cursor = receiver_dastabase_connection.cursor()

sender_database_cursor.execute("DELETE FROM sent_transactions WHERE user_id = 1234567890")
sender_dastabase_connection.commit()

receiver_database_cursor.execute("DELETE FROM received_transactions WHERE sender_id = 1234567890")
receiver_dastabase_connection.commit()

error_database_connection = sqlite3.connect("error_database.db")
error_database_cursor = error_database_connection.cursor()

error_database_cursor.execute("DELETE FROM errors WHERE account_number_sender = 1234567890;")
error_database_connection.commit()

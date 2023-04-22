import sqlite3

database_connection = sqlite3.connect("app_database.db")
cur = database_connection.cursor()

cur.execute("DELETE FROM finished_transactions WHERE account_number_sender = 222222222222222222")
database_connection.commit()

cur.execute("UPDATE accounts SET account_balance = 1000000 WHERE user_id = 1234567890")
database_connection.commit()
cur.execute("UPDATE accounts SET account_balance = 1000000 WHERE user_id = 2234567890")
database_connection.commit()


cur.execute("DELETE FROM sent_transactions WHERE user_id = 1234567890")
database_connection.commit()
cur.execute("DELETE FROM sent_transactions WHERE user_id = 2234567890")
database_connection.commit()

cur.execute("DELETE FROM received_transactions WHERE sender_id = 987654321")
database_connection.commit()
cur.execute("DELETE FROM received_transactions WHERE user_id = 2234567890")
database_connection.commit()


cur.execute("DELETE FROM errors WHERE account_number_sender = 222222222222222222;")
database_connection.commit()

cur.execute("DELETE FROM accounts WHERE account_type = 'SAVINGS'")
database_connection.commit()


"""
cur.execute("INSERT INTO accounts (user_id, account_number, account_balance, account_type, bank_sender) VALUES (1234567890, 222222222222222222, 1000000, 'CHECKING', 'JP MORGAN CHASE')")
database_connection.commit()

cur.execute("INSERT INTO accounts (user_id, account_number, account_balance, account_type, bank_sender) VALUES (2234567890, 333333333333333333, 1000000, 'CHECKING', 'SILICON VALLEY BANK')")
database_connection.commit()"""

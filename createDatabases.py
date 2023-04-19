import sqlite3

def create_databases() -> None:
    user_connection = sqlite3.connect("users.db")
    users_cursor = user_connection.cursor()
    accounts_connection = sqlite3.connect("accounts.db")
    accounts_cursor = accounts_connection.cursor()
    transaction_connection = sqlite3.connect("transactions.db")
    transactions = transaction_connection.cursor()
    finished_transactions = sqlite3.connect("finished_transactions.db")
    finished = finished_transactions.cursor()

    users_cursor.execute(
        """CREATE TABLE IF NOT EXISTS users (user_id BIGINT, bank_sender TEXT, first_name TEXT, last_name TEXT)"""
                        )
    user_connection.commit()
    accounts_cursor.execute("""CREATE TABLE IF NOT EXISTS accounts (user_id BIGINT, account_number BIGINT, account_balance DOUBLE(7, 2),
                            account_type TEXT, bank_sender TEXT)"""
                            )
    accounts_connection.commit()
    transactions.execute(
        """CREATE TABLE IF NOT EXISTS transactions (user_id BIGINT, paid_amount DOUBLE(7, 2), key BIGINT, salt BIGINT, sender_os TEXT)""")
    transaction_connection.commit()
    
    finished.execute("""CREATE TABLE IF NOT EXISTS transactions (account_number_sender BIGINT, account_number_receiver BIGINT, transaction_timestamp TEXT,
                        transfer_amount FLOAT(2), beginning_balance_sender DOUBLE(7, 2), bank_sender TEXT, os_sender TEXT, os_receiver TEXT,
                        unanimous_agreement BOOL, transaction_error BOOL)""")
    finished_transactions.commit()
    
                        
    
    
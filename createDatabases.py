import sqlite3

def create_databases() -> None:
    accounts_connection = sqlite3.connect("accounts.db")
    accounts_cursor = accounts_connection.cursor()
    
    finished_transactions = sqlite3.connect("finished_transactions.db")
    finished = finished_transactions.cursor()
    
    sender_dastabase_connection = sqlite3.connect("sender_transactions.db")
    sender_database_cursor = sender_dastabase_connection.cursor()
    
    receiver_dastabase_connection = sqlite3.connect("receiver_transactions.db")
    receiver_database_cursor = receiver_dastabase_connection.cursor()
    
    error_database_connection = sqlite3.connect("error_database.db")
    error_database_cursor = error_database_connection.cursor()

    
    accounts_cursor.execute("""CREATE TABLE IF NOT EXISTS accounts (user_id BIGINT, account_number BIGINT, account_balance DOUBLE(7, 2),
                            account_type TEXT, bank_sender TEXT)"""
                            )
    accounts_connection.commit()
    
    sender_database_cursor.execute(
        """CREATE TABLE IF NOT EXISTS sent_transactions (key TEXT, user_id BIGINT, paid_amount DOUBLE(7, 2), sender_os TEXT, sent_timestamp TEXT)""")
    sender_dastabase_connection.commit()
    
    receiver_database_cursor.execute(
        """CREATE TABLE IF NOT EXISTS received_transactions (key TEXT, user_id BIGINT, sender_id BIGINT, expected_amount DOUBLE(7, 2), receiver_os TEXT)""")
    receiver_dastabase_connection.commit()
    
    finished.execute("""CREATE TABLE IF NOT EXISTS finished_transactions (account_number_sender BIGINT, account_number_receiver BIGINT, transaction_timestamp TEXT,
                        transfer_amount FLOAT(2), beginning_balance_sender DOUBLE(7, 2), bank_sender TEXT, os_sender TEXT, os_receiver TEXT,
                        unanimous_agreement BOOL, transaction_error BOOL)""")
    finished_transactions.commit()
    
    error_database_cursor.execute("""CREATE TABLE IF NOT EXISTS errors (account_number_sender BIGINT, account_number_receiver BIGINT, transaction_timestamp TEXT,
                        transfer_amount FLOAT(2), beginning_balance_sender DOUBLE(7, 2), bank_sender TEXT, os_sender TEXT, os_receiver TEXT,
                        unanimous_agreement BOOL, error_explanation TEXT)""")
    error_database_connection.commit()
    
create_databases()
    
                        
    
    
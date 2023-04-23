import sqlite3

def create_databases() -> None:
    database_connection = sqlite3.connect("app_database.db")
    cur = database_connection.cursor()
    
    cur.execute("""CREATE TABLE IF NOT EXISTS accounts (user_id BIGINT, account_number BIGINT, account_balance DOUBLE(7, 2),
                            account_type TEXT, bank_sender TEXT, api_hash, salt)"""
                            )
    database_connection.commit()
    
    cur.execute(
        """CREATE TABLE IF NOT EXISTS sent_transactions (key TEXT, user_id BIGINT, paid_amount DOUBLE(7, 2), sender_os TEXT, sent_timestamp TEXT)""")
    database_connection.commit()
    
    cur.execute(
        """CREATE TABLE IF NOT EXISTS received_transactions (key TEXT, user_id BIGINT, sender_id BIGINT, expected_amount DOUBLE(7, 2), receiver_os TEXT)""")
    database_connection.commit()
    
    cur.execute("""CREATE TABLE IF NOT EXISTS finished_transactions (transaction_key TEXT, account_number_sender BIGINT, account_number_receiver BIGINT, transaction_timestamp TEXT,
                        transfer_amount FLOAT(2), beginning_balance_sender DOUBLE(7, 2), bank_sender TEXT, os_sender TEXT, os_receiver TEXT,
                        unanimous_agreement INT, transaction_error INT)""")
    database_connection.commit()
    
    cur.execute("""CREATE TABLE IF NOT EXISTS errors (account_number_sender BIGINT, account_number_receiver BIGINT, transaction_timestamp TEXT,
                        transfer_amount FLOAT(2), beginning_balance_sender DOUBLE(7, 2), bank_sender TEXT, os_sender TEXT, os_receiver TEXT,
                        unanimous_agreement int, error_explanation TEXT, error_code INT, transaction_id TEXT)""")
    database_connection.commit()
    
    cur.execute("CREATE TABLE IF NOT EXISTS api_failures (attempted_api_key TEXT, sender_id BIGINT, receiver_id BIGINT, transfer_amount DOUBLE (7, 2), operating_system TEXT, timestamp TEXT, endpoint TEXT)")
    database_connection.commit()

    
create_databases()
    
                        
    
    
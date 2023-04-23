# My Submission for AIS-A-Thon. Created a backend simulating 2 phones tapping together to send a payment from one phone app's account to the other  
  
## The Framework!
- Built on [FasAPI](https://fastapi.tiangolo.com/), a Python framework for building, well, fast API's!  
- It runs on [Uvicorn](https://www.uvicorn.org/), An ASGI web server for Python.  
  
## Secure!  
- Fully HTTPS encrypted between the simulated phones and the API endpoints.  
- API requests authorized by API keys included in the post request from the simulated phones, icluding [salting](https://www.techtarget.com/searchsecurity/definition/salt) and hashing.  
- Data sent via [JSON](https://en.wikipedia.org/wiki/JSON) payload.  
  
## Features!  
- Updates account balances.  
- Logs the transaction information.  
- Logs errors when they occur.  
- Deletes transactions older than 5 minutes from the temporary transaction half databases to maintain up to date information.  
  
## Above and Beyond!  
- Contains the data fields required by the data science prompt, because at a real company, the data scientists would have worked with us on this requirement.  
- Allows for account creation by auto generating an API key, salt, and full hash of them combined so the new user can by fully authenticated in the future.  
  
## Assumptions Made  
- The data transfer between the simulated phones is conducted via 256 bit encrypted AES signal.  
- Both users have already agreed to the transactions by pressing the UI to send and receive the NFC signal containing the transaction information.  
- App would have a function to detect if it can connect to the main server first, so transactions could not be sent at separate times.  
- The [SQLite3](https://en.wikipedia.org/wiki/SQLite) databases used in the current program would actually be secure full SQL databases like PostgreSQL in a company with actual funding and experts, secured with a password and encrypted.  
  
## Files and Their Uses  
  
### main.py:  
The main backend api for the appilication. Receives user transaction data and stores the transaction halves in their respective tables. Receives account creation data and stores it to the accounts table. verifies request authenticity via API key in the header by taking the key, adding it to the salt from the account with the matching user ID, hashing it using the [SHA3-512](https://en.wikipedia.org/wiki/SHA-3) hasing algorithm, and comparing the resulting hash to the API hash of the account.  
  
The file will need to run from the command line using `uvicorn main:app --reload --host 127.0.0.1 --port 8000 --ssl-certfile="cert.pem" --ssl-keyfile="key.pem"`  
  
However since you do not have a self signed SSL certificate this will not work unless you generate one. I have one that works for purposes of the demonstration.  
  
### complete_transactions.py:  
This program runs independently in the background and continously checks the transactions between the pending receiver and sender transaction tables. When it finds a key match it verifies that the sender_id and the amount from both halves match at if they do, conducts the required debits and credits to accounts, deletes both halves of the transaction from their respective tables, and stores the successful transaction information in the finished transactions table. If there is an overdraw attept, or a mismatch between the sender user ID and/or balance, it generates the errors, deletes the halves from their tables without moving any money around, and logs the errors to the errors table.  
  
You will need to run this program seperately from the command line using `py complete_transactions.py`  

### phone_mimic_script.py:  
This program mimics a transaction between 2 phones by generating a unique [UUID](https://en.wikipedia.org/wiki/Universally_unique_identifier) key, asking how much money is to be sent, and then sending the transaction halves to the respective API endpoints as a JSON payload.  
  
### create_databases.py:  
This program runs when the main file is launched and simply creates the needed database and tables if they do not exist.  
  
### error_generator.py:  
This program simulates a sender user ID and expected balance mismatch by inserting a transaction into each of the transaction tables with a matching UUID key but with different sender user ID's and expected transaction amounts. This will cause a mismatch error between both the sender's user ID as well as the expected transaction amount. This is to demonstrate that the error checking and logging works.  
  
### reset.py:  
This program simply exists as an easy way to reset the databases for demonstration purposes. Check before using.  
  
### create_account.py:  
This program simulates creating a new account on the app by asking for an initial balance, account type, and bank name, then generates a new user ID and account ID, API key, salt, main hash, and sending the information to the API as a JSON payload. The API key itself is not transmitted. Just the salt and main hash so even if an attacker steals these they cannot gain access to the API endpoints.  
  
### time_error.py:  
This program simulates a transaction timeout scenario by inserting a transaction into each half of the transaction tables with a time that is 10 minutes in the past.
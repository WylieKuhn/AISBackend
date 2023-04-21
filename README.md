# AISBackend
Submission for AIS-A-Thon. Created a backend simulating 2 phones tapping together to send a payment from one phone app's account to the other


FILES AND THEIR USES:

main.py: The main backend api for the appilication. Receives user transaction data and stores the transaction halves in their respective tables. Also receives account creation data and stores it to the accounts table. The file will need to run from the command line using 'Uvicorn main:app --reload'

complete_transactions.py: This program runs independently in the background and continously checks the transactions between the pending receiver and sender transaction tables. When it finds a key match it verifies that the sender_id and the amount from both halves match at if they do, conducts the required debits and credits to accounts, deletes both halves of the transaction from their respective tables, and stores the successful transaction information in the finished transactions table. If there is an overdraw attept, or a mismatch between the sender user ID and/or balance, it generates the errors, deletes the halves from their tables without moving any money around, and logs the errors to the errors table.

phone_mimic_script.py: This program mimics a transaction between 2 phones by generating a unique UUID key, asking how much money is to be sent, and then sending the transaction halves to the respective API endpoints as a JSON payload.

create_databases.py: This program runs when the main file is launched and simply creates the needed database and tables if they do not exist.

error_generator.py: This program inserts a transaction half into each side of the transaction tables with a matching UUID key but with different sender user ID's and expected transaction amounts. This will cause a mismatch error between both the sender's user ID as well as the expected transaction amount. This is to demonstrate that the error checking and logging works.

reset.py: This program simply exists as an easy way to reset the databases for demonstration purposes. Check before using.
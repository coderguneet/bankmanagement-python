import mysql.connector as m_c

pw = input("Enter database password: ")
con = m_c.connect(user="root", host="localhost", passwd=pw, port=3306)
if con.is_connected():
	print("CONNECTED")
else:
	print("ERROR")
cur =  con.cursor()

def init():
	cur.execute("create database if not exists BANK_MGMT")
	con.commit()
	cur.execute("use BANK_MGMT")
	cur.execute("create table if not exists bank(BankID char(5) primary key, BankName char(10))")
	cur.execute("create table if not exists branch(BranchCode char(5) primary key, BankID char(5), Address char(20), foreign key(BankID) references bank(BankID))")
	cur.execute("create table if not exists customer(AccID char(12) primary key, PIN char(4), BranchCode char(10), AccBalance int, Address char(10), PhoneNo char(10), foreign key (BranchCode) references branch(BranchCode))")
	con.commit()
	
def add(values, table):
	if table.lower() == "bank":
		s = "insert into bank values(%s, %s)"
		cur.execute(s, values)
	elif table.lower() == "branch":
		s = "insert into branch values(%s, %s, %s)"
		cur.execute(s, values)
	elif table.lower() == "customer":
		s = "insert into customer values(%s, %s, %s, %s, %s, %s)"
		cur.execute(s, values)
	con.commit()

def remove(ID, table):
	if table.lower() == "bank":
		s = "delete from bank where BankID = %s"
		cur.execute(s, (ID,))
	elif table.lower() == "branch":
		s = "delete from branch where BranchCode = %s"
		cur.execute(s, (ID,))
	elif table.lower() == "customer":
		s = "delete from customer where AccID = %s"
		cur.execute(s, (ID,))
	con.commit()

def edit(column, ID, newVal, table):
	if table.lower() == "bank":
		s = f"update bank set {column} = %s where BankID = %s"
		cur.execute(s, (newVal, ID))
	elif table.lower() == "branch":
		s = f"update branch set {column} = %s where BranchCode = %s"
		cur.execute(s, (newVal, ID))
	elif table.lower() == "customer":
		s = f"update customer set {column} = %s where AccID = %s"
		cur.execute(s, (newVal, ID))
	con.commit()

def money(AccID, amt):
	s = "update customer set AccBalance = AccBalance + %s where AccID = %s"
	cur.execute(s,(amt, AccID))
	con.commit()

def checkPIN(PIN, AccID):
	cur.execute("select PIN from customer where AccID = %s", (AccID,))
	x = cur.fetchall()
	if x[0][0] == PIN:
		return True
	else:
		return False

def getBal(AccID, PIN):
	if checkPIN(PIN, AccID):
		cur.execute("select AccBalance from customer where AccID = %s", (AccID,))
		x = cur.fetchall()
		return x[0][0]
	else:
		print("Incorrect PIN!!!")

init()
uId = input("Enter User ID (Case Sensitive): ")
pWord = input("Enter password (Case Sensitive): ")

if uId == "Admin" and pWord == "12345678":
	print("Enter 1 to add a bank")
	print("Enter 2 to remove a bank")
	print("Enter 3 to add a branch")
	print("Enter 4 to remove a branch")
	print("Enter 5 to edit a bank")
	print("Enter 6 to edit a branch")
	print("Enter 7 to display all banks with branches")
	print("Enter anything else to exit")
	
	while True:
		choice = int(input("Enter choice: "))
		if choice == 1:
			bID = input("Enter bank ID: ")
			bName = input("Enter bank name: ")
			add((bID, bName), "bank")
			print("Bank added.")
			print()
		elif choice == 2:
			bID = input("Enter ID of bank to be removed: ")
			remove(bID, "bank")
			print("Bank removed successfully.")
			print()
		elif choice == 3:
			bCode = input("Enter branch code: ")
			bID = input("Enter Bank ID: ")
			Address = input("Enter Address: ")
			add((bCode, bID, Address), "branch")
			print("Branch added successfully.")
			print()
		elif choice == 4:
			bCode = input("Enter code of branch to be removed: ")
			remove(bCode, "branch")
			print("Branch removed successfully.")
			print()
		elif choice == 5:
			bID = input("Enter ID of bank to be edited: ")
			col = input("Enter column to be edited: ")
			newVal = input("Enter new value: ")
			edit(col, bID, newVal, "bank")
			print("Value updated successfully.")
			print()
		elif choice == 6:
			bID = input("Enter branch code of branch to be edited: ")
			col = input("Enter column to be edited: ")
			newVal = input("Enter new value: ")
			edit(col, bID, newVal, "branch")
			print("Value edited successfully.")
			print()
		elif choice == 7:
			cur.execute("select bank.BankID, BankName, BranchCode, Address from bank, branch where bank.BankID = branch.BankID")
			x = cur.fetchall()
			for i in x:
				print(f"Bank ID: {i[0]}, Bank Name: {i[1]}, Branch Code: {i[2]}, Branch Address: {i[3]}")
			print()
		else:
			print("QUIT")
			con.close()
			break

elif uId == "Customer" and pWord == "ABCDEFGH":
	print("Enter 1 to create an account")
	print("Enter 2 to close an account")
	print("Enter 3 to deposit money")
	print("Enter 4 to withdraw money")
	print("Enter 5 to check balance")
	print("Enter 6 to edit account details")
	print("Enter 7 to see your bank details")
	print("Enter anything else to exit")
	
	while True:
		choice = int(input("Enter choice: "))
		if choice == 1:
			AccID = input("Enter Account ID: ")
			PIN = input("Enter PIN number: ")
			BranchCode = input("Enter Branch Code: ")
			AccBal = int(input("Enter initial deposit: "))
			Address = input("Enter Address: ")
			PhNo = input("Enter Phone number: ")
			add((AccID, PIN, BranchCode, AccBal, Address, PhNo), "customer")
			print("Account created successfully.")
			print()
		elif choice == 2:
			AccID = input("Enter ACCount ID to be removed: ")
			remove(AccID, "customer")
			print("Account close successfully.")
			print()
		elif choice == 3:
			AccID = input("Enter Account ID: ")
			amt = int(input("Enter Amount to be deposited: "))
			money(AccID, amt)
			print("Money deposited successfully.")
			print()
		elif choice == 4:
			AccID = input("Enter Account ID: ")
			PIN = input("Enter PIN: ")
			amt = int(input("Enter Amount to be withdrawn: "))
			if checkPIN(PIN, AccID):
				money(AccID, -amt)
				print("Money withdrawn successfully.")
			else:
				print("Incorrect PIN!!!")
			print()
		elif choice == 5:
			AccID = input("Enter Account ID: ")
			PIN = input("ENter PIN: ")
			print(getBal(AccID, PIN))
			print()
		elif choice == 6:
			AccID = input("Enter Account ID: ")
			PIN = input("Enter PIN: ")
			if checkPIN(PIN, AccID):
				col = input("Enter column to be edited: ")
				newVal = input("Enter new value: ")
				edit(col, AccID, newVal, "customer")
				print("Details updated successfully.")
			else:
				print("Incorrect PIN!!!")
			print()
		elif choice == 7:
			AccID = input("Enter your account ID: ")
			PIN = input("Enter PIN: ")
			if checkPIN(PIN, AccID):
				cur.execute("select * from bank, branch, customer where (customer.AccID = %s) and (customer.branchcode = branch.branchcode) and (branch.bankid = bank.bankid)", (AccID,))
				x = cur.fetchone()
				print(f"Bank ID: {x[0]}, Bank Name: {x[1]}, Branch Code: {x[2]}, Branch Address: {x[4]}, Account No.: {x[5]}, PIN: {x[6]}, Account Balance: {x[8]}, Address: {x[9]}, Phone No.: {x[10]}")
			else:
				print("Incorrect PIN!!!")
			print()
		else:
			print("QUIT")
			con.close()
			break

elif uId not in ["Admin", "Customer"]:
	print("INCORRECT USER ID!!!")

elif (uId == "Admin" and pWord != "12345678") or (uId == "Customer" and pWord != "ABCDEFGH"):
	print("INCORRECT PASSWORD!!!")

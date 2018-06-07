#...IMPORTS...

import os
import csv
import sys
import time
import imaplib
import email
import logging
from time import strftime

#...GLOBALS...

SERVER = "imap.gmail.com"
SERVER2 = "imap.buffalo.edu"

global UNIQUES, OLD_UNIQUES

#Colors

black = "\033[0;39;49m"
black_bold = "\033[1;39;49m"

#...DEFINITIONS...

#Recursive add Email Function

def add_email():

	email = input("Enter a Gmail Account: ")
	res = input("Would you like to add " + str(email) + "? (y/n): ")
	return res, email

#Recursive add Password Function

def add_password():

	password = input("Enter your Password: ")
	res = input("Is " + str(password) + " the correct password? (y/n): ")
	return res, password

#Recursive add More Accounts Function

def add_more():

	res = input("Would you like to add more accounts? (y/n): ")
	return res

#Add Gmail Accounts to Data List

def add_accounts():

	print(black_bold + "\nAttempting to add Gmail Accounts...\n" + black)

	try:

		accounts = []

		while 1:

			#Get Email Account

			while 1:
				res, email = add_email()
				if res == "y":
					break

			#Get Password

			while 1:
				res, password = add_password()
				if res == "y":
					break

			accounts.append([email, password])
			print(str(email) + " : " + str(password) + " added to accounts!!!")

			#Add more Accounts or exit

			res = add_more()
			print("")
			if res == "n":
				break

		with open(("DATA/EMAILS.csv"), "a", newline='') as f:
			writer = csv.writer(f)
			for i in range(0, len(accounts)):
				writer.writerows([accounts[i]])
		f.close()

		print("SUCCESS: Accounts added to data file!!!")

	except:
		print("\nFAILURE: Could not add accounts!!!")
		logging.exception(strftime("%m/%d/%Y %H:%M:%S ") + "FAILURE: Could not add accounts!!!")
		return 0

#Get Email Account Credentials

def fetch_creds():

	print(black_bold + "\nAttempting to fetch Email Credentials...\n" + black)

	try:

		emails = []

		with open("DATA/EMAILS.csv") as csvfile:
			my_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
			for row in my_reader:
				emails.append(row)
		csvfile.close()

		for i in range(0, len(emails)):
			print(emails[i][0] + " || " + emails[i][1])

		print("\nSUCCESS: Fetched emails from data file!!!")
		return emails

	except:
		print("\nFAILURE: Could not fetch Email Credentials!!!")
		logging.exception(strftime("%m/%d/%Y %H:%M:%S ") + "FAILURE: Could not fetch Email Credentials!!!")
		return 0

#Initial Print Statement

def initialize():

	print(black_bold + "Gmail for Slack and Lifx" + black)
	return 1

#Verify Data Structure

def data_collection():

	try:

		print(black_bold + "\nAttempting to verify data structure...\n" + black)

		#Set Current Directory

		os.chdir("/home/scripts/gslack")

		check = 0

		#Create Directories

		if not os.path.exists("LOGS"):
			os.makedirs("LOGS")
			print("LOGS Directory created...")
			check = 1

		if not os.path.exists("DATA"):
			os.makedirs("DATA")
			print("DATA Directory created...")
			check = 1

		#Logs

		log_file = "LOGS/LOG_" + strftime("%m%d%Y") + ".log"

		if not os.path.isfile(log_file):	
			os.mknod(log_file)
			print(log_file + " created...")
			check = 1

		#Data Files

		if not os.path.isfile("DATA/EMAILS.csv"):
			os.mknod("DATA/EMAILS.csv")
			print("EMAILS.csv file created...")
			check = 1

		if not os.path.isfile("DATA/UIDS.csv"):
			os.mknod("DATA/UIDS.csv")
			print("UIDS.csv file created...")
			check = 1

		if check == 1:
			print("")

		print("SUCCESS: Data Structure is complete!!!")
		return 1

	except:
		print("\nFAILURE: Could not verify data structure!!!")
		logging.exception(strftime("%m/%d/%Y %H:%M:%S ") + "FAILURE: Could not verify data structure!!!")
		return 0

#Get UIDS

def fetch_uids():

	global UNIQUES, OLD_UNIQUES

	UNIQUES = []
	OLD_UNIQUES = []

	try:

		with open("DATA/UIDS.csv") as csvfile:
			my_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
			for row in my_reader:
				UNIQUES.append(row)
				OLD_UNIQUES.append(row)
		csvfile.close()

		print(len(UNIQUES))

		return 1

	except:
		print("\nFAILURE: Could not fetch UIDS!!!")
		logging.exception(strftime("%m/%d/%Y %H:%M:%S ") + "FAILURE: Could not fetch UIDS!!!")
		return 0

#Fetch Most Recent Email in Plain Text

def fetch_gmail(_EMAIL, _PASS):

	global UNIQUES

	try:

		print(black_bold + "\nAttempting to fetch latest email from " + str(_EMAIL) + "...\n" + black)

		new_email = 0

		#Get Past UID's

		_emails = []
		_uids = []

		for i in range(0, len(UNIQUES)):
			_emails.append(UNIQUES[i][0])
			_uids.append(UNIQUES[i][1])

		#Login to Gmail
		
		if "@buffalo.edu" in _EMAIL:
			mail = imaplib.IMAP4_SSL(SERVER2)
		else:
			mail = imaplib.IMAP4_SSL(SERVER)

		mail.login(_EMAIL, _PASS)

		#Get Mail from Inbox

		mail.select("inbox")

		#Get Latest Email UID

		result, data = mail.uid("search", None, "ALL")
		uid = str(int(data[0].split()[-1]))

		if _EMAIL not in _emails:

			uniques = [_EMAIL, uid]

			with open(("DATA/UIDS.csv"), "a", newline='') as f:
				writer = csv.writer(f)
				writer.writerows([uniques])
			f.close()

		elif _EMAIL in _emails:

			if _uids[_emails.index(_EMAIL)] == uid:
				print("No new emails!!!")

			elif _uids[_emails.index(_EMAIL)] != uid:
				print("New email found!!!")
				new_email = 1
				UNIQUES[_emails.index(_EMAIL)][1] = uid

		print("UID: " + uid)

		#Get Latest Email Data

		result, data = mail.uid("fetch", uid, "(RFC822)")
		raw_email = data[0][1]

		#Print Latest Email Stats

		msg = email.message_from_bytes(raw_email)
		print("FROM: " + str(msg['From']))
		print("TO: " + str(msg['To']) + "\n")

		#Print Email Body

		maintype = msg.get_content_maintype()

		#Check for Multipart Message

		if maintype == 'multipart':

			for part in msg.get_payload():

				#Check for nested Multipart Message

				if part.get_content_maintype() == 'multipart':

					for rec_part in part.get_payload():

						#Print Text and Break

						if rec_part.get_content_maintype() == 'text':

							print(str(rec_part.get_payload()))
							break

				#Check for Text Message

				elif part.get_content_maintype() == 'text':

					#Print Text and Break

					print(str(part.get_payload()))
					break

		#Print Text Message

		elif maintype == 'text':

			print(str(msg.get_payload()))

		#Print ERROR if text part cannot be found

		else:

			print("ERROR: Preview not Available...")

		print("\nSUCCESS: Fetched latest email!!!")
		return 1

	except:
		print("\nFAILURE: Could not read latest email!!!")
		logging.exception(strftime("%m/%d/%Y %H:%M:%S ") + "FAILURE: Could not read email!!!")
		return 0

#Sync UID File Changes

def sync_uids():

	try:

		print(black_bold + "\nAttempting to sync UIDS.csv file with UNIQUES list...\n" + black)

		global UNIQUES, OLD_UNIQUES

		if len(UNIQUES) > 0:
			if UNIQUES != OLD_UNIQUES:

				with open(("DATA/UIDS.csv"), "a", newline='') as f:
					writer = csv.writer(f)
					writer.writerows([UNIQUES[i]])
				f.close()
				print("SUCCESS: UIDS.csv synced!!!")
			else:
				print("SUCCESS: UIDS.csv had no changes!!!")

		return 1
	except:
		print("\nFAILURE: Could not sync UIDS.csv with UNIQUES list!!!")
		logging.exception(strftime("%m/%d/%Y %H:%M:%S ") + "FAILURE: Could not sync UIDS.csv with UNIQUES list!!!")
		return 0

#...LOGIC...

initialize()
data_collection()
fetch_uids()
# add_accounts()
emails = fetch_creds()
for i in range(0, len(emails)):
	fetch_gmail(emails[i][0], emails[i][1])
sync_uids()

#...END PROGRAM...



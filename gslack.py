#...IMPORTS...

import os
import csv
import sys
import time
import imaplib
import email
import logging
from pifx import PIFX
from time import strftime
from slackclient import SlackClient

#...GLOBALS...

SERVER = "imap.gmail.com"
SERVER2 = "imap.buffalo.edu"

#UID Data Collection

global UNIQUES, OLD_UNIQUES

#API Keys

global SLACK_KEY, LIFX_KEY

#Colors

black = "\033[0;39;49m"
black_bold = "\033[1;39;49m"

COLORS = ["#EC7063", "#AF7AC5", "#5499C7", "#48C9B0", 
		"#52BE80", "#F4D03F", "#EB984E", "#EC7063",
		"#A569BD", "#5DADE2", "#45B39D", "#58D68D",
		"#F5B041", "#DC7633"]

#...DEFINITIONS...

#.................
#......SLACK......
#.................

#Custom slack message

def slack_custom(message, color, _channel="#general", _att=False):

	global SLACK_KEY

	try:

		print(black_bold + "\nAttempting to message updates in Slack...\n" + black)

		slack_token = SLACK_KEY
		sc = SlackClient(slack_token)

		if color == "Green" or color == "green":

			att_json = [
					{
						"fallback": "Lemur - Message.",
						"color": "#45e33a",
						"actions": [
							{
								"type": "button",
								"text": "Check Accounts Data :full_moon_with_face:",
								"url": "https://docs.google.com/spreadsheets/d/1rRsCLRcgtDEpFeC8jUZ2mWC39eEd1BHzhtOxLg0MnBY/edit?usp=sharing"
							}

						]

					}

				]

		elif color == "Red" or color == "red":

			att_json = [
					{
						"fallback": "Lemur - Message.",
						"color": "#e52424",
						"actions": [
							{
								"type": "button",
								"text": "Check Accounts Data :full_moon_with_face:",
								"url": "https://docs.google.com/spreadsheets/d/1rRsCLRcgtDEpFeC8jUZ2mWC39eEd1BHzhtOxLg0MnBY/edit?usp=sharing"
							}

						]

					}

				]

		if _att == True:

			sc.api_call(
				"chat.postMessage",
				channel=_channel,
				text=message,
				attachments=att_json
			)

		elif _att == False:

			sc.api_call(
				"chat.postMessage",
				channel=_channel,
				text=message
			)

		print("Slack message sent!!!")

		return 1

	except:
		print("Could not send slack message!!!")
		logging.exception(strftime("%m/%d/%Y %H:%M:%S ") + "Could not send slack message!!!")
		return 0

#Slack custom attachment

def slack_att_custom(_att, message=None, _channel="#general"):

	global SLACK_KEY

	try:

		print(black_bold + "\nAttempting to message updates in Slack...\n" + black)

		slack_token = SLACK_KEY
		sc = SlackClient(slack_token)

		if message == None:

			sc.api_call(
				"chat.postMessage",
				channel=_channel,
				attachments=_att
			)

		elif message != None:

			sc.api_call(
				"chat.postMessage",
				channel=_channel,
				text=message,
				attachments=_att
			)

		print("Slack attachment message sent!!!")

		return 1

	except:
		print("Could not send slack attachment message!!!")
		logging.exception(strftime("%m/%d/%Y %H:%M:%S ") + "Could not send slack attachment message!!!")
		return 0

#Slack miniature attachment

def slack_mini_att(title, message, _channel="#general", _color="green"):

	global SLACK_KEY

	if _color == "green":
		color_val = "#45e33a"
	if _color == "red":
		color_val = "#e52424"
	else:
		color_val = _color

	try:

		print(black_bold + "\nAttempting to message updates in Slack...\n" + black)

		slack_token = SLACK_KEY
		sc = SlackClient(slack_token)

		att_json = [
			{
				"fallback": "Lemur - Message.",
				"color": color_val,
				"fields": [
					{
						"title": str(title),
						"value": str(message)
					}
				],
				"ts": str(int(time.time()))
			}
		]

		sc.api_call(
			"chat.postMessage",
			channel=_channel,
			attachments=att_json
		)

		print("Slack mini attachment message sent!!!")

		return 1

	except:
		print("Could not send slack mini attachment message!!!")
		logging.exception(strftime("%m/%d/%Y %H:%M:%S ") + "Could not send slack mini attachment message!!!")
		return 0

#Slack miniature image attachment

def slack_mini_img_att(title, message, image, _channel="#general", _color="green"):

	global SLACK_KEY

	if _color == "green":
		color_val = "#45e33a"
	if _color == "red":
		color_val = "#e52424"
	try:

		print(black_bold + "\nAttempting to message updates in Slack...\n" + black)

		slack_token = SLACK_KEY
		sc = SlackClient(slack_token)

		att_json = [
			{
				"fallback": "Lemur - Message.",
				"color": color_val,
				"image_url": image,
				"fields": [
					{
						"title": str(title),
						"value": str(message)
					}
				],
				"ts": str(int(time.time()))
			}
		]

		sc.api_call(
			"chat.postMessage",
			channel=_channel,
			attachments=att_json
		)

		print("Slack mini image attachment message sent!!!")

		return 1

	except:
		print("Could not send slack mini image attachment message!!!")
		logging.exception(strftime("%m/%d/%Y %H:%M:%S ") + "Could not send slack mini image attachment message!!!")
		return 0

#Default Email Attachment Message

def email_attachment(_EMAIL, _COLOR, _FROM, _MSG):

	_attach = [
		{
			"fallback": "Lemur - Message",
			"color": _COLOR,
			"title": _EMAIL + ": New Email",
			"fields": [
				{
					"title": "From: " + _FROM,
					"value": _MSG
				}
			],
			"ts": str(int(time.time()))
		}
	]

	slack_att_custom(_attach, None, "#email")

#.................
#......LIFX.......
#.................

def lifx_notify(_COLOR, _EMAIL):

	global LIFX_KEY

	try:

		print(black_bold + "\nAttempting to send Lifx Notification...\n" + black)

		p = PIFX(api_key=LIFX_KEY)
		p.pulse_lights(color='red', cycles=3.0)

		slack_mini_att(_EMAIL, "Lifx New Email Notification was successful! :yum:", "#lifx_lights", _COLOR)

		print("SUCCESS: Lifx state changed successfully!!!")

	except:
		print("Could not modify Lifx state!!!")
		logging.exception(strftime("%m/%d/%Y %H:%M:%S ") + "Could not modify Lifx state!!!")
		return 0

#.................
#......GMAIL......
#.................

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

		# for i in range(0, len(emails)):
		# 	print(emails[i][0] + " || " + emails[i][1])

		print("\nSUCCESS: Fetched emails from data file!!!")
		return emails

	except:
		print("\nFAILURE: Could not fetch Email Credentials!!!")
		logging.exception(strftime("%m/%d/%Y %H:%M:%S ") + "FAILURE: Could not fetch Email Credentials!!!")
		return 0

#Initial Print Statement

def initialize():

	print(black_bold + "Gmail for Slack and Lifx" + black)
	fetch_keys()
	fetch_uids()
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

		if not os.path.isfile("DATA/KEYS.csv"):
			os.mknod("DATA/KEYS.csv")
			print("KEYS.csv file created...")
			check = 1

		if check == 1:
			print("")

		print("SUCCESS: Data Structure is complete!!!")
		return 1

	except:
		print("\nFAILURE: Could not verify data structure!!!")
		logging.exception(strftime("%m/%d/%Y %H:%M:%S ") + "FAILURE: Could not verify data structure!!!")
		return 0

#Get API Keys

def fetch_keys():

	global SLACK_KEY, LIFX_KEY

	print(black_bold + "\nAttempting to fetch Slack and Lifx API Keys...\n" + black)

	try:

		keys = []

		with open("DATA/KEYS.csv") as csvfile:
			my_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
			for row in my_reader:
				keys.append(row)
		csvfile.close()

		if len(keys) >=2:

			#Get Slack Key

			if keys[0][0] == "SLACK":

				SLACK_KEY = keys[0][1]

			elif keys[1][0] == "SLACK":

				SLACK_KEY = keys[1][1]

			print("SLACK KEY: " + SLACK_KEY)

			#Get Lifx Key

			if keys[0][0] == "LIFX":

				LIFX_KEY = keys[0][1]

			elif keys[1][0] == "LIFX":

				LIFX_KEY = keys[1][1]

			print("LIFX KEY: " + LIFX_KEY)

		print("\nSUCCESS: Fetched Slack and Lifx API Keys!!!")
		return 1

	except:
		print("\nFAILURE: Could not fetch API Keys!!!")
		logging.exception(strftime("%m/%d/%Y %H:%M:%S ") + "FAILURE: Could not fetch API Keys!!!")
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
				row2 = row[:]
				UNIQUES.append(row)
				OLD_UNIQUES.append(row2)
		csvfile.close()

		return 1

	except:
		print("\nFAILURE: Could not fetch UIDS!!!")
		logging.exception(strftime("%m/%d/%Y %H:%M:%S ") + "FAILURE: Could not fetch UIDS!!!")
		return 0

#Fetch Most Recent Email in Plain Text

def fetch_gmail(_EMAIL, _PASS, _itt=0):

	global UNIQUES

	try:

		print(black_bold + "\nAttempting to fetch latest email from " + str(_EMAIL) + "...\n" + black)

		new_email = 0
		MSG = ""

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
		FROM = str(msg['From'])
		print("FROM: " + FROM)
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

							MSG = str(rec_part.get_payload())
							print(MSG)
							break

				#Check for Text Message

				elif part.get_content_maintype() == 'text':

					#Print Text and Break

					MSG = str(part.get_payload())
					print(MSG)
					break

		#Print Text Message

		elif maintype == 'text':

			MSG = str(msg.get_payload())
			print(MSG)

		#Print ERROR if text part cannot be found

		else:

			MSG = "ERROR: Preview not Available..."
			print(MSG)

		if new_email == 1:
			email_attachment(_EMAIL, COLORS[_itt % 14], FROM, MSG)
			lifx_notify(COLORS[_itt % 14], _EMAIL)

		print("\nSUCCESS: Fetched latest email!!!")
		return 1

	except:
		print("\nFAILURE: Could not read latest email!!!")
		logging.exception(strftime("%m/%d/%Y %H:%M:%S ") + "FAILURE: Could not read email!!!")
		return 0

#Sync UID File Changes

def sync_uids():

	global UNIQUES, OLD_UNIQUES

	try:

		print(black_bold + "\nAttempting to sync UIDS.csv file with UNIQUES list...\n" + black)

		if len(UNIQUES) > 0:
			
			if UNIQUES != OLD_UNIQUES:

				with open(("DATA/UIDS.csv"), "w", newline='') as f:
					writer = csv.writer(f)
					for i in range(0, len(UNIQUES)):
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

#Fetch Most Recent Email from all Gmail Accounts

def fetch_all():

	emails = fetch_creds()
	for i in range(0, len(emails)):
		fetch_gmail(emails[i][0], emails[i][1], i)
	sync_uids()

#...LOGIC...

# initialize()
# fetch_all()
# data_collection()
# add_accounts()

#...END PROGRAM...
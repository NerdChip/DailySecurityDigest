# New security windows notificattion.
from datetime import date 
from bs4 import BeautifulSoup
import requests
import csv 
from win10toast import ToastNotifier as NF
import time
import os
import shutil 

#using the date time module to retrive the current date, the date when the program is executed.
today = date.today()

#Function that generates a notification when all the data has been collected by the webscraper.
def notification(fileloc):
	#using Wintoast to generte a notification (heading,summary, duration the notification should be visable for)
	n = NF()
	n.show_toast("Daily Security Digest Ready!",f"find it here {fileloc}",duration=10)

	#alert presented to the user if the file is already in the Security digest folder. 
def alertnotification():
	n = NF()
	n.show_toast("Daily Security Digest File Already Exists!","Check The Digest Folder",duration=10)

#Function to move the complete csv file from current working directory to a the Security digest folder.
def movefile(x):
	#getting the current working directory. 
	source = os.getcwd()
	#list all files in the current directory. 
	list_file_in_cwd = os.listdir(source)

	#Search every file in the directory and if it matches the parameter below set the location the file as the desired a variable.
	for file in list_file_in_cwd:
		if file == "Daliy Hacker News digest " + str(today) + ".csv":
			csv_file_attributes = file
			global source_file_location
			source_file_location = os.path.join(source, csv_file_attributes)

	#try to move the file to the Daily security digest folder, if the try is successful alert the user, if the try is not successful inform the user the file is alreay in the directory. 		
	try:
		move_file = shutil.move(source_file_location, x)
		notification(x)
	except:
		print(" File already exists")
		alertnotification()
	
	#Create a new Directory to store all daily security digest files, if the directory already exists do nothing.
def createdirectory():
	print("checking if Daily Security Digest Directory exists...")

	#directory name 
	directory = "Daily Security Digest"
	#directory path
	parent_dir = "C:/"

	path = os.path.join(parent_dir, directory)

	#try craete the directory if it is already there continue with the program 
	try:
		os.mkdir(path)
		print(f"Directory {path} has been successfully created")
	except OSError as error:
		print("Directory all ready exists")
		pass
	#calling the move function to move the file into the newly created directory 	
	movefile(path)

	#Main web scarping function that uses beautiful soup to get the main headlines from hackernews.com using the requests module to handle http communications. 
def webscrap():
	print("Welcome to the Hacker Daily Digest...")

	#name of the file where data will be written to.
	filename = "Daliy Hacker News digest " + str(today) + ".csv"

	#using the csv module create a csv file.
	csv_file = open(filename, "w", newline='', encoding='utf-8')
	writer = csv.writer(csv_file)
	writer.writerow(['Headline','Date Published','Author','Summary','URL Link'])

	print("Hi Just grabbing you daily security digest...I let you know when its done...")

	#make a http get request to the hackernews and get the html output back in text format
	source = requests.get("https://thehackernews.com/").text

	soup = BeautifulSoup(source, 'lxml')

	#iterate through the html output and retrive that data that is need for the security digest file and set them as variables 
	for container in soup.find_all('div', class_='body-post clear'):
		link = container.find('a').get('href')
		containertitle = container.find('h2', class_="home-title")
		date_author = container.find('div', class_="item-label")
		description = container.find('div', class_="home-desc")

		title = containertitle.text
		date_author_text_date = date_author.text.split("")[0][1:]
		date_author_text_author = date_author.text.split("")[1]
		desc = description.text

		#write data to csv file
		writer.writerow([title, date_author_text_date, date_author_text_author, desc, link])

	#program to sleep for 15 secs to allow time for all the data to be written into the csv file 
	time.sleep(15)

	#close file 
	csv_file.close()

	#call the next function that creates a directory for the file to be moved to. 
	createdirectory()		


webscrap()
print("Program Complete")	



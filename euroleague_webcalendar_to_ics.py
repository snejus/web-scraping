# encoding: utf-8

import requests
import re
import os
import pytz
from icalendar import Calendar, Event
from datetime import datetime
from bs4 import BeautifulSoup

def find_month_number(month_name):
    return {
        'January': 1,
        'February': 2,
        'March': 3,
        'April': 4,
        'May': 5,
        'June': 6,
        'July': 7,
        'August': 8,
        'September': 9,
        'October': 10,
        'November': 11,
        'December': 12
    }.get(month_name, 0)

# Create the calendar object and add necessary stuff
cal = Calendar()
cal.add('prodid', '-//My calendar product//mxm.dk//')
cal.add('version', '2.0')

# Loop through 30 euroleague pages containing the games
for i in range(1, 31):
	link = "http://www.euroleague.net/main/results?gamenumber=" + str(i) + "&phasetypecode=RS&seasoncode=E2018"
	myteam = 'Zalgiris Kaunas'

	# Extract html from the page
	html = requests.get(link)
	html.encoding = 'utf-8'

	# Create soup object from the html text
	soup = BeautifulSoup(html.text, features='lxml')

	# Find all the tags <a> that contain "game-link" class
	games = soup.find_all("a", class_="game-link")

	# 16 games will be found - extract ours
	for game in games:
		if game.find(string=re.compile("Zalgiris Kaunas")):
			# Get the underlying text of format
			# [<team 1> <team 2> <month> <day> <time> CET LIVE FINAL]
			# ignore the last three words as they are irrelevant
			our_game = game.get_text().split()[:-3]

	# Find whether Zalgiris is team 1 or team 2
	index = our_game.index('Zalgiris')

	# Assign data
	# Extract the opponent's team name, which can have any number of words,
	# but we know that we have 3 array items following it
	oppoteam = ' '.join(our_game[2:-3]) if index == 0 else ' '.join(our_game[0:index])

	# Get the month number
	month = find_month_number(our_game[-3])

	# Since the season starts in October and ends in May, we can infer the year
	year = 2018 if month > 9 else 2019

	# Get the day number and the time the match starts
	day = int(our_game[-2])
	time_hr = int(our_game[-1][0:2])
	time_min = int(our_game[-1][3:]) if our_game[-1][3:] != '00' else 0

	print 'Processing ' + myteam + ' vs ' + oppoteam

	# Create event and add it to the Calendar object
 	event = Event()
	event.add('summary', myteam + ' vs ' + oppoteam)
	event.add('dtstart', datetime(
								year,
								month,
								day,
								time_hr,
								time_min,
								0,
								tzinfo=pytz.timezone('Europe/Berlin')))
	event.add('dtend', datetime(year,
								month,
								day,
								time_hr+2,
								time_min,
								0,
								tzinfo=pytz.timezone('Europe/Berlin')))
	cal.add_component(event)

# Save the .ics file in the same directory where the script is located
directory = os.path.dirname(os.path.realpath(__file__))
f = open(os.path.join(directory, myteam + ' euroleague.ics'), 'wb')
f.write(cal.to_ical())
f.close()
# encoding: utf-8

import os
import re
from datetime import datetime

import pytz
import requests
from bs4 import BeautifulSoup
from icalendar import Calendar, Event

# Create the calendar object and add necessary stuff
cal = Calendar()
cal.add("prodid", "-//My calendar product//mxm.dk//")
cal.add("version", "2.0")

# Define the link to the schedule
link = "https://pmis.lsmuni.lt/pm/tvarkarasciai/show.php?a=showcycle&cycle=2747&subcycle=&trg=&groups=22"

# Extract html from the page
html = requests.get(link)
html.encoding = "utf-8"

# Create soup object from the html text
soup = BeautifulSoup(html.text, "html.parser")

# Find the title of the module
title = soup.find("h3").get_text()

# Find the lecture data
tds = soup.find_all("td", ["modclass", "date"])
for td in tds[:-1]:  # ignore the last item as it's invalid
    # The lectures information contained in tds are preceded with a td containing the date when they happen. Therefore, this date information is used for all of the lectures happening that day
    if td["class"][0] == "date":
        date = td.text
    else:
        # Assign lecture data
        summary = td.find_all("a")[1]["title"]
        location = td.span.a["title"]
        month = int(date[0:2])
        year = 2019 if month > 8 else 2020
        day = int(date[-2:])
        time_start_hr = int(td.text[0:2])
        time_start_min = int(td.text[3:5])
        time_end_hr = int(td.text[6:8])
        time_end_min = int(td.text[9:11])

        # Create event and add it to the Calendar object
        event = Event()
        event.add("summary", summary)
        event.add("location", location)
        # event.add('dtstart', datetime(year, month, day, time_start_hr, time_start_min, 0, tzinfo='Europe/Vilnius'))
        event.add(
            "dtstart",
            datetime(
                year,
                month,
                day,
                time_start_hr,
                time_start_min,
                0,
                tzinfo=pytz.timezone("Europe/Vilnius"),
            ),
        )
        event.add(
            "dtend",
            datetime(
                year,
                month,
                day,
                time_end_hr,
                time_end_min,
                0,
                tzinfo=pytz.timezone("Europe/Vilnius"),
            ),
        )
        cal.add_component(event)

# Save the .ics file in the same directory where the script is located
directory = os.path.dirname(os.path.realpath(__file__))
f = open(os.path.join(directory, title + ".ics"), "wb")
f.write(cal.to_ical())
f.close()

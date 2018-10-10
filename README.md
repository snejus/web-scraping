# web-scraping
repo containig various web-scraping scripts

## euroleague_webcalendar_to_ics.py
I was too lazy to manually add all of the games of my team in this year's Euroleague season, so I wrote a script to web scrape it for me and create an .ics file that can be imported to any calendar of choice. This can be also be done with any other team in the tournament.

Packages required: icalendar (ics writing), pytz (correct timezone), Beautiful Soup (web scraping). A html parser is required, I used lxml here (defined on line 41).

## lsmu_webcalendar_to_ics.py
The LSMU university provides students a badly formatted lectures schedule on the web in a barely readable table with no option to add the events to personal calendars. My job here is help them and web scrape the table to output an .ics file. The script core is the same as the euroleague script, only the html-reading part is different.


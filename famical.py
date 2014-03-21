"""
Batch file to read XML and update a display saying whether or not the classroom is in use.

Green if there is no class in the next 8 hours.
Yellow LED if there is a class later today in less than 8 hours.
Red if there is a class in session.

RGB LED <- Arduino ethernet ~ Internal FamiLAB HTTP on Pi <- gcalread output
"""

import pprint
from calendar_parser import CalendarParser
from datetime import datetime, timedelta

GCAL_XML_URL = 'https://www.google.com/calendar/feeds/familab.4am%40gmail.com/public/basic'
DEBUG = False


def getEvents():
	cal = CalendarParser(xml_url=GCAL_XML_URL)
	cal.sort_by_latest(sort_in_place=True)

	for event in cal.parse_calendar():		
		# Event has a location, and it is the meeting room
		# Event is in the future
		# Event is in progress
		if event.has_key('location') and \
		event['location'].lower().find('FamiLAB Meeting Room'.lower()) > -1 and \
		(datetime.now() - event['start_time'] <= timedelta(0) or \
		((event['end_time'] - datetime.now()) >= timedelta(0) and (event['start_time'] - datetime.now()) <= timedelta(0) )):



			if (event['start_time'] - datetime.now()) <= timedelta(0):
				# Red, in progress
				print "RED"
			elif (event['start_time'] - datetime.now()) <= timedelta(hours=8):
				# Yellow, soon
				print "YELLOW"
			elif (event['start_time'] - datetime.now()) >= timedelta(hours=8):
				# Green, not in the next 8 hours
				print "GREEN"

			print event['name']

			if DEBUG:
				print event['name']
				print event['start_time']
				print event['end_time']
				print "Time until start: "+str(event['start_time'] - datetime.now())

				if event.has_key('all_day'):
					print event['all_day']

			break

def main():	
	cal = getEvents()

if __name__ == '__main__':
	main()
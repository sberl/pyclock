#!/usr/bin/env python

import sys
import argparse
import datetime
import time
import ephem
import timezonefinder
import pytz
import gps
import math
import curses

format = "%H:%M:%S"
date_format = "%a, %b %d, %Y"

def find_timezone(latitude, longitude):
    tf = timezonefinder.TimezoneFinder()
    tzname = tf.timezone_at(lat=latitude, lng=longitude)
    return tzname

def find_location():
    session = gps.gps()
    session.stream(gps.WATCH_NEWSTYLE|gps.WATCH_ENABLE)

    for report in session:
        if report['class'] == 'TPV' and report['mode'] == 3:
            gps_lat = report['lat']
            gps_lon = report['lon']
            return (gps_lat,gps_lon)

def do_curses(screen):
    screen.box()
    curses.start_color();
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK);
    curses.curs_set(0) 
    (lat,lon) = find_location()
    print("loading timezone data")
    tzname = find_timezone(lat, lon)
    screen.erase()
    screen.addstr(1,1,"GPS Sidereal Clock",curses.color_pair(1))
    screen.addstr(3,1, "Latitude: ",curses.color_pair(1))
    screen.addstr(3,len("Latitude: ")+1, str(lat),curses.color_pair(1))
    screen.addstr(4,1, "Longitude: ", curses.color_pair(1))
    screen.addstr(4,len("Longitude: ")+1, str(lon), curses.color_pair(1))
    screen.refresh()

    local_tz = pytz.timezone(tzname)

    screen.addstr(5,1, tzname, curses.color_pair(1))
    screen.addstr(8,4, "Local Time",curses.color_pair(1))
    screen.addstr(8,26, "UTC Time",curses.color_pair(1))
    screen.addstr(14,7, "LMST",curses.color_pair(1))
    screen.addstr(14,25, "Julian Date",curses.color_pair(1))
    screen.refresh()

    obs = ephem.Observer()
    obs.lat = math.radians(lat)
    obs.lon = math.radians(lon)
    last_second = 0

    while 1 :
        u_time = datetime.datetime.utcnow()
        if u_time.second != last_second:
            last_second = u_time.second
            u_time = u_time.replace(tzinfo=pytz.utc)
            l_time = u_time.astimezone(local_tz)
            obs.date = u_time
            s_time = str(obs.sidereal_time()).split('.')[0]
            parts = s_time.split(':')
            s_time = datetime.time(int(parts[0]),int(parts[1]),int(parts[2]))

            screen.addstr(10,1, l_time.date().strftime(date_format),curses.color_pair(1))
            screen.addstr(11,5, l_time.time().strftime(format),curses.color_pair(1))

            screen.addstr(10,23, u_time.date().strftime(date_format),curses.color_pair(1))
            screen.addstr(11,26, u_time.time().strftime(format),curses.color_pair(1))

            screen.addstr(16,5, s_time.strftime(format),curses.color_pair(1))

            screen.addstr(16,24,str(ephem.julian_date(u_time)),curses.color_pair(1))

            screen.refresh()
                  
        time.sleep(0.1)
    

def run_curses():
    curses.wrapper(do_curses)
    return

def run_plaintext():
    (lat,lon) = find_location()
    print("Lat: ", lat, "Lon: ", lon)
    latitude = math.radians(lat)
    longitude = math.radians(lon)

    local_tz = pytz.timezone('America/Los_Angeles')

    obs = ephem.Observer()
    obs.lat = latitude
    obs.lon = longitude

    print(obs.lat, obs.lon)

    last_second = 0

    while 1 :
        u_time = datetime.datetime.utcnow()
        if u_time.second != last_second:
            last_second = u_time.second
            u_time = u_time.replace(tzinfo=pytz.utc)
            l_time = u_time.astimezone(local_tz)
            obs.date = u_time
            s_time = str(obs.sidereal_time()).split('.')[0]
            parts = s_time.split(':')
            s_time = datetime.time(int(parts[0]),int(parts[1]),int(parts[2]))

            print("Local:", l_time.time().strftime(format),
                "UTC:", u_time.time().strftime(format),
                "Sidereal: ", s_time.strftime(format))
        time.sleep(0.1)

def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dumb", action="store_true", help="Run clock in dumb terminal mode")
    parser.add_argument("-c", "--curses", action="store_true", help="Run clock in curses mode")
    args = parser.parse_args()
    if args.curses:
        print(args.curses, "Run in curses mode")
        run_curses()
    elif args.dumb:
        print(args.dumb, "Run in dumb mode")
        run_plaintext()
    else:
        print("Don't know mode to use -c for curses, -d for dumb")
        return 2

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

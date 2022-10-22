import gps, os, time

session = gps.gps()
session.stream(gps.WATCH_NEWSTYLE|gps.WATCH_ENABLE)

for report in session:
    #os.system('clear')

    # a = altitude, d = date/time, m=mode,  
    # o=postion/fix, s=status, y=satellites
    if report['class'] == 'TPV' and report['mode'] == 3:
        print report
        gps_mode = report['mode']
        gps_lat = report['lat']
        gps_lon = report['lon']
        gps_time = report['time']
        print "type of mode is ", type(gps_mode)
        print "type of time is ", type(gps_time)
        print "type of lat is ", type(gps_lat)



        print "Lat: ", report['lat']
        print "Lon: ", report['lon']
        print "UTC: ", report['time']
        print "mode: ", report['mode']
        break

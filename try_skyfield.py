#!/usr/bin/env python3

import zoneinfo
import datetime
from skyfield import api
from skyfield import almanac

def frac(n):
    i = int(n)
    f = round((n - int(n)), 4)
    return (i,f)

def hour_to_hms(hour):
    hours, _min = frac(hour)
    minutes, _sec = frac(_min*60)
    seconds, _msec = frac(_sec*60)
    return (hours, minutes, seconds)


def elongation_at(t):
    sun, earth, venus = eph['sun'], eph['earth'], eph['venus']
    e = earth.at(t)
    s = e.observe(sun).apparent()
    v = e.observe(venus).apparent()
    return s.separation_from(v).degrees

ts = api.load.timescale()
eph = api.load('de421.bsp')
observer_loc = api.wgs84.latlon(+37.81899, -122.18124)
observer_tz_name = "America/Los_Angeles"
observer_zoneinfo = zoneinfo.ZoneInfo(observer_tz_name)
utc_time_now = datetime.datetime.now(zoneinfo.ZoneInfo('UTC'))
local_time_now = datetime.datetime.now(observer_zoneinfo)
print("UTC: ", utc_time_now)
print("local: ", local_time_now, observer_zoneinfo)

t = ts.utc(utc_time_now)
observer_lmst = observer_loc.lst_hours_at(t)
(h, m, s) = hour_to_hms(observer_lmst)
print("LMST: %02d:%02d:%02d" % (h,m,s))

phase = almanac.moon_phase(eph, t)
print('Moon phase: {:.1f} degrees'.format(phase.degrees))


t0 = ts.utc(utc_time_now)
t1 = t0 + 1.25
t, y = almanac.find_discrete(t0, t1, almanac.sunrise_sunset(eph, observer_loc))

for ti, yi in zip(t, y):
    print('Sun ', 'Rise' if yi else 'Set',ti.astimezone(observer_zoneinfo))

f = almanac.risings_and_settings(eph, eph['Moon'], observer_loc)
t, y = almanac.find_discrete(t0, t1, f)

for ti, yi in zip(t, y):
    print('Moon', 'Rise' if yi else 'Set', ti.astimezone(observer_zoneinfo))

f = almanac.risings_and_settings(eph, eph['Venus'], observer_loc)
t, y = almanac.find_discrete(t0, t1, f)

for ti, yi in zip(t, y):
    print('Venus', 'Rise' if yi else 'Set', ti.astimezone(observer_zoneinfo))

print("Elongation of Venus: %2d°" % elongation_at(t0))

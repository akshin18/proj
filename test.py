import os, time
print(time.strftime('%Y-%m-%d %H:%M:%S')) # before timezone change
os.environ['TZ'] = 'America/Los_Angeles' # set new timezone
time.tzset()
print(time.strftime('%Y-%m-%d %H:%M:%S')) # after timezone change
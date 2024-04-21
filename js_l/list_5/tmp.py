import datetime


print(datetime.datetime.strptime("Jan  1 00:02:00","%b %d %H:%M:%S") - datetime.datetime.strptime("Jan  1 00:01:00","%b %d %H:%M:%S"))

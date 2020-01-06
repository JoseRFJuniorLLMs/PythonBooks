from ftplib import *
import os, getpass

noaa_url = "weather.noaa.gov"
#metar_dir = "/data/observations/metar/decoded/"
metar_dir = "/data/observations/metar/stations/"

user = getpass.getuser() 
if user == 'root':
	tmp = "/root/.pyweatherdat"
else: 
	tmp = "/home/" + user + "/.pyweatherdat"


metar = 'KPVD'
metar = metar + ".TXT"

#Random data init's
if os.path.exists(tmp) == 1:
	os.remove(tmp)

data = open(tmp,'w')

ftp = FTP(noaa_url)
print 'connected...'
ftp.login()            
print 'logged in...'
ftp.cwd(metar_dir)
print 'selected...'
ftp.retrbinary('RETR ' + metar, data.write)
print 'got data...'
ftp.quit

data.close()

report = open(tmp, 'r')
weather = report.read()

print weather

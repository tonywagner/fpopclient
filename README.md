fpopclient-alerts
=================

A Python 2.x based client for accessing [FreedomPop](http://www.freedompop.com/about.htm)'s (undocumented) API, and logging usage and emailing alerts. 

## Usage
Install Python 2.x if you haven't already.
Download ZIP of this repo and extract.
Edit "fp-alerts.py" in extracted folder, change the account info and email information near the top to your own, and run script as follows in a terminal session (Mac/Linux):
```
/usr/bin/python /Users/your-local-username/Downloads/fpopclient-alerts-master/fp-alerts.py
```
Or in the Windows command prompt
```
C:\Python27\python.exe C:\Users\my-local-username\Downloads\fpopclient-alerts-master\fp-alerts.py
```
Schedule script execution with crontab (Mac/Linux) or Task Scheduler (Windows) at your desired interval.

## License
Copyright for portions of project fpopclient are held by Dody Suria Wijaya, 2013 as part of project fpopclient. All other copyright for project fpopclient-alerts are held by Tony Wagner, 2017.
Licensed under the MIT license.

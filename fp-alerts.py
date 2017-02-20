import api, time, os.path, datetime, subprocess, sys, smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

# List of FreedomPop accounts to check
# set totalLimit to your plan's total data allocation in MB (usually 1000 for CDMA devices, or 700 for SIM cards)
# device is just your personal description of the device, can be anything
# set active to True only for devices that require monitoring and alerts (if you have devices or SIMs sitting inactive in a drawer, leave it False so you're not needlessly hammering the API server!)
accounts = [
	{u'username': u'my-fp-account-email+1@gmail.com', u'password': u'my-fp-account-password', u'totalLimit': 1000, u'device': "Andy's CDMA Phone", u'active': False},
	{u'username': u'my-fp-account-email+2@gmail.com', u'password': u'my-fp-account-password', u'totalLimit': 700, u'device': "Bill's LTE SIM", u'active': False},
	{u'username': u'my-fp-account-email+3@gmail.com', u'password': u'my-fp-account-password', u'totalLimit': 700, u'device': "Charlie's Global SIM", u'active': False}
]

# Email information
# set fromaddr to the email address you want to use for sending
# set frompassword to the password of your fromaddr account
# I recommend creating a "dummy" Gmail address for this purpose (maybe the same address you use on your FreedomPop accounts?)
# and be sure to allow "less secure apps" on this "dummy" Gmail account: https://www.google.com/settings/security/lesssecureapps
fromaddr = "YOUR ADDRESS"
frompassword = "YOUR PASSWORD"
# set toaddr to the address you want to receive the alerts
toaddr = "ADDRESS YOU WANT TO SEND TO"

inMB = 1024 * 1024

# Creates a log file, containing folder needs write permission
logfile = 'fp-alerts.log'
open(logfile, 'a').close()

curtime = time.ctime()

for account in accounts:
	if account['active']:
		fp = api.FreedomPop(account['username'], account['password'])
		info = fp.getInfo()
		usage = fp.getUsage()
		
		# create a basic informative message, based on "printMyInfo" function in api.py
		endTime = datetime.datetime.fromtimestamp(usage["endTime"] / 1000)
		delta = endTime - datetime.datetime.now()
		message = "Data used: %0.2f%% (%0.2f MB of %0.2f MB) Time until quota reset: %d days %d hours (%s)" % (usage['percentUsed'] * 100, usage['planLimitUsed'] / inMB, usage['totalLimit'] / inMB, delta.days, delta.seconds / 3600, endTime )
		
		# prints and logs that message with timestamp and account/device labels
		status = curtime + ' ' + account['device'] + ' on account ' + account['username'] + "\n" + message + "\n"
		print status
		with open(logfile, 'a') as myfile:
			myfile.write(status)
		
		# Checks if a particular file name exists to see if we've already sent an alert for this account on this billing cycle
		# (thereby preventing repeat alerts)
		alertflagfile = info['externalId'] + '.' + str(usage['endTime'])
		if not os.path.isfile(alertflagfile):
			balanceRemaining = usage['balanceRemaining'] / inMB
			totalLimit = usage['totalLimit'] / inMB
			
			# Usage threshold set to less than 200 MB balance remaining,
			# or if your data allocation is less than expected (i.e. you lost FreedomPop Friends)
			if (balanceRemaining < 200) or (totalLimit < account['totalLimit']):
				# if threshold is met, create empty file with particular name to suppress further alerts on this account & cycle
				open(alertflagfile, 'a').close()
				
				# sendmail code based on this tutorial: http://naelshiab.com/tutorial-send-email-python/
				msg = MIMEMultipart()
				msg['From'] = fromaddr
				msg['To'] = toaddr
				msg['Subject'] = 'FreedomPop Usage Alert for device ' + account['device'] + ' on account ' + account['username']
				msg.attach(MIMEText(message, 'plain'))
				server = smtplib.SMTP('smtp.gmail.com', 587)
				server.starttls()
				server.login(fromaddr, frompassword)
				text = msg.as_string()
				server.sendmail(fromaddr, toaddr, text)
				server.quit()

# add a blank line between iterations in the log file
with open(logfile, 'a') as myfile:
	myfile.write("\n")
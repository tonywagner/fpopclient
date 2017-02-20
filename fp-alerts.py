import api, time, os.path, datetime, subprocess, sys, smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

accounts = [
	{u'username': u'my-fp-account-email+1@gmail.com', u'password': u'my-fp-account-password', u'totalLimit': 1000, u'device': "Andy's CDMA Phone", u'active': False},
	{u'username': u'my-fp-account-email+2@gmail.com', u'password': u'my-fp-account-password', u'totalLimit': 700, u'device': "Bill's LTE SIM", u'active': False},
	{u'username': u'my-fp-account-email+3@gmail.com', u'password': u'my-fp-account-password', u'totalLimit': 700, u'device': "Charlie's Global SIM", u'active': False}
]

def sendEmail(subject, message):
    fromaddr = "YOUR ADDRESS"
    toaddr = "ADDRESS YOU WANT TO SEND TO"
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = subject
    
    body = message
    msg.attach(MIMEText(body, 'plain'))
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "YOUR PASSWORD")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()

inMB = 1024 * 1024

logfile = 'fp.log'

open(logfile, 'a').close()

curtime = time.ctime()

for account in accounts:
	if account['active']:
		fp = api.FreedomPop(account['username'], account['password'])
		info = fp.getInfo()
		usage = fp.getUsage()
		
		endTime = datetime.datetime.fromtimestamp(usage["endTime"] / 1000)
		delta = endTime - datetime.datetime.now()
		message = "Data used: %0.2f%% (%0.2f MB of %0.2f MB) Time until quota reset: %d days %d hours (%s)" % (usage['percentUsed'] * 100, usage['planLimitUsed'] / inMB, usage['totalLimit'] / inMB, delta.days, delta.seconds / 3600, endTime )
		
		status = curtime + ' ' + account['device'] + ' on account ' + account['username'] + "\n" + message + "\n"
		print status
		with open(logfile, 'a') as myfile:
			myfile.write(status)
		
		alertflagfile = info['externalId'] + '.' + str(usage['endTime'])
		
		if not os.path.isfile(alertflagfile):
			balanceRemaining = usage['balanceRemaining'] / inMB
			totalLimit = usage['totalLimit'] / inMB
			
			if (balanceRemaining < 200) or (totalLimit < account['totalLimit']):
				open(alertflagfile, 'a').close()
				sendEmail('FreedomPop Usage Alert for device ' + account['device'] + ' on account ' + account['username'], message)

with open(logfile, 'a') as myfile:
	myfile.write("\n")
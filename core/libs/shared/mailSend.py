#!/usr/bin/python
#support	:Nuno Pereira - nuno.pereira@hogarthww.com
#title     	:mailSend


#MAIL SENDER MODULE
import sys, smtplib, string, os

	
def send(mailType, mailMessage, releaseNotes):
	userName = os.environ["USERNAME"]
	asset, version, project, episode, sequence, shot_ = mailMessage
	
	##DEFINING MAILING LISTS##
	##TO UNCOMMENT WHEN PER SHOW MAILING LISTS ARE SETUP##
	#mailingList = "%s@gps-ldn.com" % project
	#mailingList = "ICARUS_publish@gps-ldn.com"
	mailingList = "nuno.pereira@gps-ldn.com"
	
	subject = "[%s] %s: %s_%s" % (mailType, project, asset, version)
	from_ = "ICARUS_publish@gps-ldn.com"
	to = mailingList
	text = "\n%s_%s\n\n\nEpisode: %s\n\nSequence: %s\n\nShot: %s\n\n\nNotes:\n%s" % (asset, version, episode, sequence, shot_, releaseNotes)
	
	body = string.join((
		"From: %s" % from_,
		"To: %s" % to,
		"Subject: %s" % subject,
		"",
		text
		), "\r\n")
	
	server = smtplib.SMTP("mail.hogarthww.com")
	server.sendmail(from_, [to], body)
	server.quit()
		

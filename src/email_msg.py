import smtplib

def send_email(text):
	gmail_user = 'hansworktests@gmail.com'
	gmail_password = 'A1b2c3d5e7'

	sent_from = gmail_user
	to = 'hansmaildump@gmail.com'
	subject = 'Coverage Automation Notification'
	body = text

	email_text = """\
	From: %s
	To: %s
	Subject: %s

	%s
	""" % (sent_from, to, subject, body)

	try:
	    smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
	    smtp_server.ehlo()
	    smtp_server.login(gmail_user, gmail_password)
	    smtp_server.sendmail(sent_from, to, email_text)
	    smtp_server.close()
	    print ("Email sent successfully!")
	except Exception as ex:
	    print ("Something went wrong….",ex)

if __name__ == '__main__':
	send_email()
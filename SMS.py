import smtplib
import os
from dotenv import load_dotenv

carriers = {
	'att':    '@txt.att.net',
	'sprint':   '@messaging.sprintpcs.com',
    'verizion': '@vtext.com'
}

load_dotenv()


def send(message, number, carrier):
        # Replace the number with your own, or consider using an argument\dict for multiple people.
    to_number = '{}{}'.format(number,carriers[carrier])

    auth = (os.getenv('EMAIL_USERNAME'), os.getenv('EMAIL_PASSWORD'))

	# Establish a secure session with gmail's outgoing SMTP server using your gmail account
    server = smtplib.SMTP( "smtp.gmail.com", 587 )
    server.starttls()
    server.login(auth[0], auth[1])

	# Send text message through SMS gateway of destination number
    server.sendmail( auth[0], to_number, message)
import smtplib
import getpass
# oyoozkmiytantahn
# Connect
smtp_object = smtplib.SMTP('smtp.gmail.com', 587)
# Confirm
smtp_object.ehlo()
# Setting protocol
smtp_object.starttls()
# Log on
email = input('Email: ')
password = getpass.getpass('Password: ')
smtp_object.login(email, password)
# Send
from_address = email
to_address = email
subject = input('Email Subject: ')
msg = input('Email message: ')
object_will_need_to_send = "Subject:" + subject + "\n" + msg

smtp_object.sendmail(from_address, to_address, object_will_need_to_send)

smtp_object.quit()
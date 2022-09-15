import smtplib
import datetime


def send_mail(attendance: list):

    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    s.login("mctattendance", "michigan_cycling")

    # message to be sent
    sub = f'Group Ride Attendance {datetime.date.today()}'
    txt = '\n'.join(attendance)
    message = 'Subject: {}\n\n{}'.format(sub, txt)

    # sending the mail
    s.sendmail("mctattendance@gmail.com", "cycling.officers@gmail.com", message)

    # terminating the session
    s.quit()

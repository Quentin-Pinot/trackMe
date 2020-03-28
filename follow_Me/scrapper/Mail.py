# coding: utf-8

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class Mail:

    def __init__(self, mailTo):
        self.msg = MIMEMultipart()
        self.mailFrom = "followmebotbigc@gmail.com"
        self.mailTo = mailTo
        self.msg['From'] = self.mailFrom
        self.msg['To'] = self.mailTo
        self.mailServeur = "smtp.gmail.com"
        self.portServeur = 587
        self.mdpFrom = "ghfgzotvtjdpumhj"

    def send_mail(self, title, price_Old, price_Current, url):
        print("Connecting by ttls to SMTP server")
        serveur = smtplib.SMTP(self.mailServeur, self.portServeur)
        serveur.ehlo()
        serveur.starttls()
        serveur.ehlo()

        print("Connected to the server")
        serveur.login(self.mailFrom, self.mdpFrom)

        print("Building the message")
        self.msg['Subject'] = 'Un item a baissé de prix de ' + \
            str(price_Old) + ' à ' + str(price_Current) + '€'
        message = title + ' a baissé de prix de ' + \
            str(price_Old) + ' à ' + str(price_Current) + '€'\
                '\nVoici le lien amazon : ' + url
        self.msg.attach(MIMEText(message))

        mailTo = [ self.mailTo ] + [ self.mailFrom ]

        print("Sending a mail to '" + self.mailTo + "' in progress...")
        serveur.sendmail(
            self.mailFrom,
            mailTo,
            self.msg.as_string(),
        )

        print("Mail sended !")

        serveur.quit()
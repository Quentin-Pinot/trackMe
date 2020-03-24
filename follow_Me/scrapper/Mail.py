class Mail:

    def __init__(self, mailTo):
        self.mailTo = mailTo
        self.mailFrom = "followmebotbigc@gmail.com"
        self.mailServeur = "smtp.gmail.com"
        self.portServeur = 587
        self.mdpFrom = "aqezfjnvlscigdkz"

    def send_mail(self, title, price_Alert, url):
        serveur = smtplib.SMTP(mailServeur, portServeur)
        serveur.ehlo()
        serveur.starttls()
        serveur.ehlo()

        serveur.login(mailFrom, mdpFrom)

        subject = title + ' a atteint le prix voulu : ' + \
            str(price_Alert) + ' euros'
        body = 'Voici le lien amazon : ' + str(url)

        msg = f"Subject: {subject}\n\n{body}"

        serveur.sendmail(
            self.mailFrom,
            str(self.mailTo),
            msg
        )

        serveur.quit()

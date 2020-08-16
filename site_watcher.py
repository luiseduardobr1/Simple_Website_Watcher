from bs4 import BeautifulSoup
import requests
import hashlib
from fake_useragent import UserAgent
import os
import filecmp
import time
import yagmail
from twilio.rest import Client

class Information():

    # Website Info
    URL = '<WEBSITE URL>'

    # Email Info
    FROM_EMAIL_LOGIN = 'XXXXXXX@hotmail.com'
    FROM_EMAIL_PASSW = '########'
    TO_EMAIL_LOGIN = 'XXXXXXX@hotmail.com'
    TO_EMAIL_TITLE = 'Warning: Website Updated'

    # SMS
    ACCOUNT_SID = '<TWILIO ACCOUNT_SID>'
    AUTH_TOKEN = '<TWILIO AUTH_TOKEN>'
    SMS_BODY = f'{URL} Updated'
    SMS_FROM = '<TWILIO PHONE NUMBER>'
    SMS_TO = '<YOUR PHONE NUMBER>'


class Site_watcher():

    def __init__(self, url):
        self._url = url

    def md5_code(self):

        # Fake user-agent
        ua = UserAgent()

        # Get source code
        response = requests.get(self._url, headers={'User-Agent': ua.random})
        soup = BeautifulSoup(response.text, "html.parser")

        # MD5 hash of source code
        md5_new = hashlib.md5(str(soup).encode()).hexdigest()

        # Save file
        with open('site_md5_new.txt', 'w') as f:
            f.write(md5_new)

        return md5_new

class Notification(Site_watcher):

    def send_email(self):
        yag = yagmail.SMTP(Information.FROM_EMAIL_LOGIN,
                           Information.FROM_EMAIL_PASSW,
                           host='smtp-mail.outlook.com', port=587,
                           smtp_starttls=True, smtp_ssl=False)

        yag.send(Information.TO_EMAIL_LOGIN,
                Information.TO_EMAIL_TITLE,
                f'Website Updated: {Information.URL}')

    def send_sms(self):
        client = Client(Information.ACCOUNT_SID, Information.AUTH_TOKEN)

        message = client.messages \
            .create(
                body = Information.SMS_BODY,
                from_ = Information.SMS_FROM,
                to = Information.SMS_TO
            )

    def __init__(self, mode=1):

        self.mode = mode

        # Email
        if mode == 1 or mode == 'email':
            self.send_email()

        # SMS
        elif mode == 2 or mode == 'sms':
            self.send_sms()


if __name__ == '__main__':

    while True:
        site_url = Information.URL
        md5_code = Site_watcher(site_url).md5_code()

        if os.path.isfile('site_md5.txt'):
            if filecmp.cmp('site_md5.txt', 'site_md5_new.txt'):
                print('Not Updated', md5_code)
            else:
                os.remove('site_md5.txt')
                os.rename('site_md5_new.txt', 'site_md5.txt')
                Notification('sms')
                Notification('email')
                print('WEBSITE UPDATED!!', md5_code)
        else:
            os.rename('site_md5_new.txt', 'site_md5.txt')

        # Check every 5 minutes
        time.sleep(300)

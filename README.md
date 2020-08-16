# Simple_Website_Watcher
Check for updates on a website and notify by email or SMS

## Requirements
* [BeautifulSoup](https://pypi.org/project/beautifulsoup4/)
* [Requests](https://pypi.org/project/requests/)
* [Fake User_Agent](https://pypi.org/project/fake-useragent/)
* [Yagmail](https://pypi.org/project/yagmail/)
* [Twilio](https://github.com/twilio/twilio-python)

## How to use it
1) Read the tutorial and get a phone number with SMS on [Twilio website](https://www.twilio.com/docs/sms/tutorials/how-to-send-sms-messages-python). 
2) Edit the ```Information``` class with your personal information to send the emails and SMS:
```Python
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
 ```
3) If your email isn't a *@hotmail.com*, you will need to change the *host* variable in ```Notification``` class (look at the table below for your specific *host*).
```Python
class Notification(Site_watcher):

    def send_email(self):
        yag = yagmail.SMTP(Information.FROM_EMAIL_LOGIN,
                           Information.FROM_EMAIL_PASSW,
                           host='smtp-mail.outlook.com', port=587,
                           smtp_starttls=True, smtp_ssl=False)
```

Port 587 is a common port for most of SMTP servers, however some may have different ports (like 465). 

This table from [Automate Boring Stuff with Python](http://automatetheboringstuff.com/2e/chapter18/) summarizes the majority of servers:

| Provider                | SMTP server domain name      |
|-------------------------|------------------------------|
| Gmail                   | smtp.gmail.com               |
| Outlook.com/Hotmail.com | smtp-mail.outlook.com        |
| Yahoo Mail              | smtp.mail.yahoo.com          |
| AT&T                    | smpt.mail.att.net (port 465) |
| Comcast                 | smtp.comcast.net             |
| Verizon                 | smtp.verizon.net (port 465)  |

### Warning
This is a very simple website watcher so be careful to not publish your private information online. Some emails will block this kind of activity, then you should confirm thats you. 

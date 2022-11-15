# -*- coding: utf-8 -*-
"""
Created on Sat Oct 8 17:43:12 2022

@author: Kauffman Analytics
"""


from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import datetime
import requests

now =datetime.datetime.now()
now2 = now.strftime("%Y-%m-%d")

days = 2

effr_api_url = requests.get(f"https://markets.newyorkfed.org/api/rates/unsecured/effr/last/{days}.json").json()

todays_fed_rate = (effr_api_url['refRates'][0]["percentRate"])
yest_fed_rate = (effr_api_url['refRates'][1]["percentRate"])

def fed_rate_delta():
    fed_delta = todays_fed_rate - yest_fed_rate
    fed_delta = round(fed_delta, 2)
    return fed_delta

def fed_up_or_down():
    if todays_fed_rate - yest_fed_rate > 0:
        return str("increased by")
    else:
        return str("decreased by")
    
def sendgrid_email():
    message = Mail(from_email='ryan@kauffmananalytics.com',
                   to_emails='ryan@kauffmananalytics.com',
                   subject='Fed Funds Rate as of ' + now2,
                   html_content="Good afternoon! <br/>"\
                       "The Fed Funds Rate is: " + str(todays_fed_rate) + ". The rate " + fed_up_or_down() + " " + " " + str(fed_rate_delta()) +\
                        " Thanks! Ryan")
    sg = SendGridAPIClient("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")
    response = sg.send(message)
    print(response.status_code, response.body)


sendgrid_email()

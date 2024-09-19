from bs4 import BeautifulSoup
import requests
import smtplib
import os
from dotenv import load_dotenv

SMPT_SERVER_ADDRESS = "smpt.gmail.com"
TARGET_PRICE = 100

load_dotenv()
smtplib.SMTP()

smtp_server = os.environ['SMTP_ADDRESS']
sender_email = os.environ['FROM_EMAIL_ADDRESS']
to_address = os.environ['TO_EMAIL_ADDRESS']
password = os.environ['EMAIL_PASSWORD']


url = "https://www.amazon.com/dp/B075CYMYK6?ref_=cm_sw_r_cp_ud_ct_FM9M699VKHTT47YD50Q6&th=1"
header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
}
response = requests.get(url,headers=header)

soup = BeautifulSoup(response.content, 'html.parser')

title = soup.find(id="productTitle").get_text().strip()
price = soup.find(class_="a-price-whole").get_text().strip('.')

if int(price) < TARGET_PRICE:
    message = f"the price of {title} is now dropped to {price}"
    try:
        with smtplib.SMTP(smtp_server, port=587) as connection:
            connection.starttls()
            connection.login(user=sender_email, password=password)
            connection.sendmail(from_addr=sender_email,
                                to_addrs=to_address,
                                msg=f"Subject: Amazon Priced dropped Alert!\n\n {message}\n {url}".encode("utf-8"))
    except ConnectionError:
        print("connection Error")



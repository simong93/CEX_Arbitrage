import datetime
import time
import CEX_Scrape_Bulk as CEX_Scrape_Bulk
import Ebay_Scrape_Bulk as Ebay_Scrape_Bulk
import concurrent.futures
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from smtplib import SMTP_SSL, SMTP_SSL_PORT
from email.mime.multipart import MIMEMultipart, MIMEBase
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

ToEmail = ""
FromEmail = ""
Password = ""
EmailServer = ""

class CEX:

    def __init__(self):
        driver = self.Driver()
        self.CEXScrape = []
        for i in range(1,10):
            try:
                self.CEXScrape.append(CEX_Scrape_Bulk.CEX_Scrape_Inside(i,driver).CEX)
            except Exception as E:
                print(E)
                err = ""
        self.End(driver)

    def Driver(self):
        # Setting Chrome Options
        option = webdriver.ChromeOptions()
        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('window-size=1920x1080')

        chrome_options.add_argument("--disable-infobars")

        # Pass the argument 1 to allow and 2 to block
        chrome_options.add_experimental_option(
            "prefs", {"profile.default_content_setting_values.notifications": 1}
        )

        driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=chrome_options)

        return driver

    def End(self, driver):
        driver.close()
        driver.quit()

class Main:

    def __init__(self, Comps):

        # Setup driver to be used and scrape CEX

        print("CEX Scrape",Comps)
        #Use data to scrape Ebay
        self.Complete = Ebay_Scrape_Bulk.Ebay_Scrape_Inside(Comps).Ebay_Master

        print("Complete End",self.Complete)

def SendEmail(ToEmail,FromEmail,Password):
    try:
        Email = ToEmail
        today = datetime.datetime.now()
        Date = today.strftime("%d/%m/%Y")
        Time = today.strftime("%H")

        Report = 'CEX_Arbitrage.csv'
        Subject = 'CEX Arbitrage - ' + str(Date)
        print(Subject)

        # Craft the email using email.message.EmailMessage
        from_email = FromEmail  # or simply the email address
        email_message = MIMEMultipart()
        email_message.add_header('To', Email)
        email_message.add_header('From', from_email)
        email_message.add_header('Subject', Subject)
        email_message.add_header('X-Priority', '3')  # Urgency, 1 highest, 5 lowest

        html_part = MIMEText(
            '<html><body><p>Please find attached the CEX Arbitrage excel sheet</p><p>Many Thanks</p></body></html>',
            'html')

        with open(Report, 'rb') as file:
            # Attach the file with filename to the email
            email_message.attach(MIMEApplication(file.read(), Name=Report))

        email_message.attach(html_part)
        # Connect, authenticate, and send mail
        smtp_server = SMTP_SSL(EmailServer, port=SMTP_SSL_PORT)
        smtp_server.set_debuglevel(1)  # Show SMTP server interactions
        smtp_server.login(FromEmail, Password)
        smtp_server.sendmail(from_email, Email, email_message.as_bytes())

        # Disconnect
        smtp_server.quit()

        print('Mail Sent')
    except Exception as ex:
        print("Something went wrong….", ex)

while True:
    #Convert to one list
    Master_Excel = []
    CexFoundComplete = []
    CexFound = CEX().CEXScrape
    print("Cex Found",CexFound)
    for Found in CexFound:
        for FoundTwo in Found:
            CexFoundComplete.append(FoundTwo)

    print("Cex found complete",CexFoundComplete)

    with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
        # Start the load operations and mark each future with its URL
        future_to_url = {executor.submit(Main, Comps): Comps for Comps in CexFoundComplete}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            data = future.result()
            try:
                # collect and sort the data
                data = future.result()
                for i in data.Complete:
                    print("1st",i)
                    if i != []:
                        print("2nd",i)
                        for b in i:
                            Master_Excel.append(b)
            except Exception as exc:
                print('%r generated an exception: %s' % (url, exc))


    print("Master Excel",Master_Excel)
    #Convert to excel
    df = pd.DataFrame(Master_Excel)
    df.to_csv('CEX_Arbitrage.csv',index=False)
    pd.read_csv('CEX_Arbitrage.csv')

    SendEmail(ToEmail,FromEmail,Password)
    time.sleep(72000)

import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from random import randint
import time


class CEX_Scrape_Inside:

    def __init__(self, ID,driver):
        self.CEX = self.MainDef(ID,driver)

    def MainDef(self,ID,driver):
        URL = "https://uk.webuy.com/boxsearch/?superCatId=" + str(ID)
        print(URL)
        driver.get(URL)


        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'superCatLink')))

        try:
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'onetrust-accept-btn-handler')))
            driver.find_element(By.ID, 'onetrust-accept-btn-handler').click()
        except:
            err = ""

        a = 0
        Random = randint(5, 10)
        Random = 1
        actions = ActionChains(driver)
        actions.send_keys(Keys.PAGE_DOWN).perform()
        actions.send_keys(Keys.PAGE_DOWN).perform()
        actions.send_keys(Keys.PAGE_DOWN).perform()
        actions.send_keys(Keys.PAGE_DOWN).perform()
        while a < Random:
            actions.send_keys(Keys.PAGE_DOWN).perform()
            actions.send_keys(Keys.PAGE_DOWN).perform()
            actions.send_keys(Keys.PAGE_DOWN).perform()
            actions.send_keys(Keys.PAGE_DOWN).perform()
            actions.send_keys(Keys.PAGE_DOWN).perform()
            actions.send_keys(Keys.PAGE_DOWN).perform()
            actions.send_keys(Keys.PAGE_DOWN).perform()
            actions.send_keys(Keys.PAGE_DOWN).perform()
            actions.send_keys(Keys.PAGE_DOWN).perform()
            actions.send_keys(Keys.PAGE_DOWN).perform()
            actions.send_keys(Keys.PAGE_DOWN).perform()
            actions.send_keys(Keys.PAGE_DOWN).perform()
            actions.send_keys(Keys.PAGE_DOWN).perform()
            actions.send_keys(Keys.PAGE_DOWN).perform()
            actions.send_keys(Keys.PAGE_DOWN).perform()
            time.sleep(randint(2, 3))
            a += 1
            driver.find_element(By.ID, 'showmoreresult').click()

        soup = BeautifulSoup(driver.page_source, features="lxml")
        #print(soup)
        #print(soup.find("div", {"class": "hotproducts"}))
        CEX_List = []

        #Get all product cons
        for i in soup.find_all("div", {"class": "hotproducts"}):
            print("Found",i)
            #Now get price etc from CEX
            try:
                CEX_Return = self.GetPrices(i,CEX_List)
                if CEX_Return != "Nope" :
                    CEX_List.append(CEX_Return)
            except Exception as E:
                print(E)


        return CEX_List


    def GetPrices(self,soup,CEX_List):
        try:
            CEX = {}

            Title_Con = soup.find("div",{"class":"savdiv"})
            CEX['Title'] = Title_Con.find("a").text.strip()

            CEX['URL'] = "https://uk.webuy.com" + Title_Con.find("a")['href']

            Cat_Con = soup.find("div",{"class":"superCatLink"})
            CEX['Catagory'] = Cat_Con.find_all("a")[1].text.replace("Games","").replace("Accessories","").replace("Consoles","").strip()

            Prices = soup.find_all("div",{"class":"priceTxt"})

            CEX['SellFor'] = Prices[0].text.replace("£","").strip()

            CEX['WeBuyCash'] = Prices[1].text.replace("£","").strip()

            CEX['WeBuyVoucher'] = Prices[2].text.replace("£","").strip()

            #print(CEX)
            if float(CEX['WeBuyCash']) > 4.00:
                return CEX
            else:
                return "Nope"
        except Exception as E:
            print(E)

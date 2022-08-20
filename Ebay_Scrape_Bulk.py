import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
import time


class Ebay_Scrape_Inside:

    def __init__(self, CEX):
        self.Ebay_Master = self.MainDef(CEX)

    def MainDef(self,CEX):
        Ebay_Finnished_List = []

        try:
            URL = "https://www.ebay.co.uk/sch/i.html?_nkw=" + CEX['Title'] + " " + CEX['Catagory'] + "&LH_Auction=1"

            response = requests.get(URL, headers=Headers(headers=True).generate(), timeout=5)
            if response.status_code == 200:
                print("Got Code for", URL, " - ", response.status_code)
                soup = BeautifulSoup(response.text, features="lxml")

                #Now get price etc from CEX
                try:
                    Ebay_Found = self.GetPrices(soup,CEX,URL)
                    if Ebay_Found != "Nope":
                        Ebay_Finnished_List.append(Ebay_Found)
                except Exception as E:
                    print(E)

        except Exception as E:
            print(E)

        return Ebay_Finnished_List

    def GetPrices(self,soup,CEX,URL):
        #print(soup)
        print(CEX)
        CashFound = 0
        VoucherFound = 0
        CashProfit = 0
        VoucherProfit = 0

        Ebay_Master = []

        for item in soup.findAll("li",{"class":"s-item"}):
            try:
                if CEX['Title'].lower() in item.find("h3",{"class":"s-item__title"}).text.lower():
                    #Setup Cex Dict
                    Ebay_Sub = {}
                    Ebay_Sub['Ready'] = "Not Ready"
                    Ebay_Sub['Name'] = CEX['Title']
                    Ebay_Sub['Link'] = ""
                    Ebay_Sub['Price'] = 0
                    Ebay_Sub['Postage'] = 0
                    Ebay_Sub['Total'] = 0
                    Ebay_Sub['TimeLeft'] = ""
                    Ebay_Sub['CashProfit'] = 0
                    Ebay_Sub['VoucherProfit'] = 0
                    Ebay_Sub['Total'] = 0

                    Ebay_Sub['Cex_Link'] = CEX['URL']
                    Ebay_Sub['Cex_Cash'] = CEX['WeBuyCash']
                    Ebay_Sub['Cex_Voucher'] = CEX['WeBuyVoucher']

                    #Get Link
                    Ebay_Sub['Link'] = item.find("a",{"class":"s-item__link"})['href']

                    #Sort price and postage
                    Ebay_Sub['Price'] = float(item.find("span",{"class":"s-item__price"}).text.replace("£",""))
                    if "collection in person" in item.find("span",{"class":"s-item__shipping"}).text:
                        return "Nope"
                    elif "Free" in item.find("span",{"class":"s-item__shipping"}).text:
                        Ebay_Sub['Postage'] = 0.00
                    else:
                        Ebay_Sub['Postage'] = float(item.find("span",{"class":"s-item__shipping"}).text.replace(" postage","").replace("+ £","").replace(" estimate","").replace("+£","").replace(" shipping",""))

                    Ebay_Sub['Total'] = Ebay_Sub['Price'] + Ebay_Sub['Postage']

                    #d = days,h = hours,m = minutes
                    Ebay_Sub['TimeLeft'] = item.find("span",{"class":"s-item__time-left"}).text
                    if "d" in Ebay_Sub['TimeLeft']:
                        if float(CEX['WeBuyCash']) > Ebay_Sub['Total']:
                            #Work out profit
                            Ebay_Sub['CashProfit'] = round(float(CEX['WeBuyCash']) - Ebay_Sub['Total'],2)
                            Ebay_Sub['Ready'] = "Not Time But Cash"

                            #Work out totals
                            CashFound +=1
                            CashProfit = CashProfit + Ebay_Sub['CashProfit']
                            #print("Can sell for Cash with",Ebay_Sub['CashProfit'])

                        elif float(CEX['WeBuyVoucher']) > Ebay_Sub['Total']:
                            #Work out profit
                            Ebay_Sub['VoucherProfit'] = round(float(CEX['WeBuyVoucher']) - Ebay_Sub['Total'],2)
                            Ebay_Sub['Ready'] = "Not Time But Voucher"

                            #Work out totals
                            VoucherFound +=1
                            VoucherProfit = VoucherProfit + Ebay_Sub['VoucherProfit']
                            #print("Can sell for voucher with",Ebay_Sub['VoucherProfit'])

                    elif "h" in Ebay_Sub['TimeLeft'] or "m" in Ebay_Sub['TimeLeft']:
                        if float(CEX['WeBuyCash']) > Ebay_Sub['Total']:
                            #Work out profit
                            Ebay_Sub['CashProfit'] = round(float(CEX['WeBuyCash']) - Ebay_Sub['Total'],2)
                            Ebay_Sub['Ready'] = "Ready Cash"

                            #Work out totals
                            CashFound +=1
                            CashProfit = CashProfit + Ebay_Sub['CashProfit']
                            #print("Can sell for Cash with",Ebay_Sub['CashProfit'])

                        elif float(CEX['WeBuyVoucher']) > Ebay_Sub['Total']:
                            #Work out profit
                            Ebay_Sub['VoucherProfit'] = round(float(CEX['WeBuyVoucher']) - Ebay_Sub['Total'],2)
                            Ebay_Sub['Ready'] = "Ready Voucher"

                            #Work out totals
                            VoucherFound +=1
                            VoucherProfit = VoucherProfit + Ebay_Sub['VoucherProfit']
                            #print("Can sell for voucher with",Ebay_Sub['VoucherProfit'])

                    print(Ebay_Sub)
                    if Ebay_Sub['Ready'] == "Ready Cash":
                        Ebay_Master.append(Ebay_Sub)
                    #print("==================================")
            except Exception as E:
                #print("==================================")
                print(E)

        print(CashFound,"Cash Profit",CashProfit)
        print(VoucherFound,"Voucher Profit",VoucherProfit)
        print("==================================")
        print("**********************************")
        print("==================================")

        return Ebay_Master
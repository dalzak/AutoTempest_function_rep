from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import Select
import re
import time as tm 
import statistics as stats

class lookingForCar:
   
   def __init__(self, make, model, file):
      self.make = make
      self.model = model
      self.file = file

   def scrapeForTopTen(self):
      url = f"https://www.autotrader.ca/cars/{self.make}/{self.model}/?rcp=15&rcs=0&srt=4&prx=-1&hprc=True&wcp=True&inMarket=advancedSearch"
      options = Options()
      options.headleass = True
      options.add_argument("--window-size=1920,1200")

      DRIVER_PATH = "/path/to/chromedriver"

      driver = webdriver.Chrome(executable_path = DRIVER_PATH)
      driver.get(url)

      soup = BeautifulSoup(driver.page_source, 'html.parser')

      #scraping info
      gen_info = soup.find_all("div", {"class": "col-xs-6 detail-center-area"})
      details_used = soup.find_all('p', {'class' : "details used"})
      price = soup.find_all("span", {"id": "price-amount-value"})
      title = soup.find_all("a", {'class':"result-title click"})


      #class info depending on variables needed (int, str, float)
      unformatted_gen_info = [str(info).replace('\n', '').replace(' ', '') for info in gen_info] 
      unformatted_details_used = [str(detail).replace('\n', '') for detail in details_used]
      unformatted_price = [str(prices).replace('\n', '') for prices in price]
      unformatted_title = [str(titles).replace('\n', '') for titles in title]
      

      #final list of each info
      formatted_km = [int(re.search(r'^.*<b>Mileage</b>(.*)km.*$', items).group(1).replace(',', '')) for items in unformatted_gen_info]
      formatted_links = [re.search(r'^.*href="(.*)"><span.*$', items).group(1) for items in unformatted_gen_info]
      formatted_details_used = [re.search(r'^.*<p class="details used">(.*)</p>.*$', the_tabarnak_de_details).group(1) for the_tabarnak_de_details in unformatted_details_used]
      formatted_price = [int(re.search(r'^.*>\$(.*)</.*$',items).group(1).replace(",", "")) for items in unformatted_price]
      formatted_title = [re.search(r'.*><span>                                        (.*)                                    <\/span><\/a>.*$', titles).group(1) for titles in unformatted_title]

      #returning a dictionnary of the info 
      return [{'km': formatted_km[i], "href": formatted_links[i], "details": formatted_details_used[i], "price" : formatted_price[i], 'title': formatted_title[i]} for i in range(0,len(formatted_price))]
      
         
   def scrapeForPrice(self):
##                   ##
   ##JAMESEDITION##
##                   ##
      url = f"https://www.jamesedition.com/cars/{self.make}/{self.model}"
      options = Options()
      options.headleass = True
      options.add_argument("--window-size=1920,1200")

      DRIVER_PATH = "/path/to/chromedriver"

      driver = webdriver.Chrome(executable_path = DRIVER_PATH)
      driver.get(url)
      soup = BeautifulSoup(driver.page_source, "html.parser")
      price = soup.find_all("div", {"class": "ListingCard__price"})

      price_list_james = []
      for items in price:
         matches = re.search(r'^.*\n\$(.*)\n.*$', str(items))
         try:  
            price_list_james.append(int(str(matches.group(1)).replace(",", "")))  
         except AttributeError:
            pass
      price_avg_james = stats.mean(price_list_james)
      driver.quit()

   ##                   ##
      ##AUTOTRADER##
   ##                   ##

      tm.sleep(2)

      url = f"https://www.autotrader.ca/cars/{self.make}/{self.model}"
      options = Options()
      options.headleass = True
      options.add_argument("--window-size=1920,1200")

      ##start driver
      DRIVER_PATH = "/path/to/chromedriver"

      driver = webdriver.Chrome(executable_path = DRIVER_PATH)
      driver.get(url)
      soup = BeautifulSoup(driver.page_source, "html.parser")
      price = soup.find_all("span", {"id": "price-amount-value"})

      price_list_auto_trade = []
      for items in price:
         matches = re.search(r'^.+>\$(.+)<.+$', str(items))
         try:   
            price_list_auto_trade.append(int(str(matches.group(1)).replace(",", "")))      
         except AttributeError:
            pass
      price_avg_auto_trade = stats.mean(price_list_auto_trade)

      driver.quit()
       
   ##                   ##
         ##Theparking##
   ##                   ##

      tm.sleep(2)
      url = f"https://www.theparking.ca/used-cars/{self.make}-{self.model}.html"
      options = Options()
      options.headleass = True
      options.add_argument("--window-size=1920,1200")

      ##start driver
      DRIVER_PATH = "/path/to/chromedriver"

      driver = webdriver.Chrome(executable_path = DRIVER_PATH)
      driver.get(url)
      soup = BeautifulSoup(driver.page_source, "html.parser")
      price = soup.find_all("p", {"class": "prix"})

      price_list_the_parking = []
      for items in price:
         matches = re.search(r"^.*\n.*\$(.*).<.*$", str(items))
         try:
            price_list_the_parking.append(int(str(matches.group(1)).replace(",", "")))
         except AttributeError:
            pass
      price_avg_the_parking = stats.mean(price_list_the_parking)
      driver.quit()

      return "%.2f" % round(stats.mean([price_avg_the_parking, price_avg_auto_trade, price_avg_james]),2)
   
      
      

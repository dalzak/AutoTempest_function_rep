import statistics
from scraper_tool import lookingForCar
import csv
import time as tm 
from datetime import date
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import sys
import os
from datetime import datetime
import sklearn

##website to scrape info from 
supported_website = ["autotrader", "jamesedition", "theparking"]

##cars that have data collected from 
fourEightEight = lookingForCar("ferrari", "488", "fourEightEight.csv")
lamborghiniHura = lookingForCar('lamborghini', "huracan", "lamborghiniHura.csv")
lamborghiniUrus = lookingForCar('lamborghini', "urus", 'lamborghiniUrus.csv')
mclaren720s = lookingForCar('mclaren', '720s', 'mclaren720s.csv')
mclarenSenna = lookingForCar('mclaren','senna', 'mclarenSenna.csv')


def main():
    #This function collect the averages over time for the graph being diplayed
    if input("do you need car info scrapped today? (Y/N): ").upper() == "Y":
        getGraphValues()
    else:
        None
    #Asking the user for a model to choose
    make_user = input('Input the make of the supercar: ').lower()
    model_user = input('Input the model of the supercar: ').lower()

    #creating a car object to interact with 
    car_from_user = lookingForCar(make_user, model_user, None)

    #scrape for top ten returns a list of info of the 10 cheapest cars
    car_result_from_user = car_from_user.scrapeForTopTen()

    #sorting the car dictionnary with its price
    listsorted = sorted(car_result_from_user, key=lambda x: x['price'])
    os.system('cls')
    x = None
    if len(listsorted) < 10:
        x = len(listsorted)
    else:
        x = 10

    for i in range(0, x):
        print(f"{listsorted[i]['title']}\n \nPrix: ${listsorted[i]['price']}\nKilometre: {listsorted[i]['km']} km\n \nDetails:\n{listsorted[i]['details']}\n \nCLICKABLE Link: https://www.autotrader.ca{listsorted[i]['href']}\n \n -----------------------------------------------------------------------------------------------------\n")


    supported_car_graphs = [fourEightEight, lamborghiniHura, lamborghiniUrus, mclaren720s, mclarenSenna]
    for obj in supported_car_graphs:
        if obj.make == make_user and obj.model == model_user:
            plotGraph(obj.file)
            break
        else:
            pass
    
    restart = input('Would you like to do another search? (y/n): ').lower()
    if restart == 'y':
        os.system('cls')
        main()
    else:        
        sys.exit("Thank you for using AUTOPY!")


def getGraphValues():
    supported_car_graphs = [fourEightEight, lamborghiniHura, lamborghiniUrus, mclaren720s, mclarenSenna]
    for objct in supported_car_graphs:
        tm.sleep(2)
        price = objct.scrapeForPrice()
        with open(objct.file, "a") as file:
            writer = csv.DictWriter(file, fieldnames=['date', 'make', 'model', 'price'])
            writer.writerow({'date': date.today(), 'make' : objct.make, 'model': objct.model, 'price': price})

def plotGraph(csvfile: str):
    plt.clf()
    data = []
    with open(csvfile) as file:
        reader = csv.DictReader(file)
        for rows in reader:
            data.append({'date': datetime.strptime(rows["date"], '%Y-%m-%d'), 'make' : rows["make"], 'model' : rows["model"], 'price': rows['price']})

    y = []
    x = []

    for i in range(0,len(data)):
        y.append(float(data[i]['price']))
        x.append(data[i]['date'])

    mean = statistics.mean(y)
    stdev = statistics.stdev(y)
    day_to_day_fluctuation = [0] + [abs(y[i]-y[i-1]) for i in range(1,len(y))]
    avg_day_to_day_fluctuation = statistics.mean(day_to_day_fluctuation)
    percentage_return = (y[-1] - y[0]) / y[0] * 100
    five_day_fluctuation = statistics.mean(day_to_day_fluctuation[-5:]) / y[-1] * 100
    fifteen_day_fluctuation = statistics.mean(day_to_day_fluctuation[-15:]) / y[-1] * 100
    thirty_day_fluctuation = statistics.mean(day_to_day_fluctuation[-30:]) / y[-1] * 100

    stats_str = f"Mean: ${mean:.2f}\nStandard deviation: ${stdev:.2f}\nDay-to-day fluctuation (average): ${avg_day_to_day_fluctuation:.2f}\n5-day average fluctuation: {five_day_fluctuation:.2f}%\n15-day average fluctuation: {fifteen_day_fluctuation:.2f}%\n30-day average fluctuation: {thirty_day_fluctuation:.2f}%\nPercentage return: {percentage_return:.2f}%"

    plt.subplot(2, 1, 1)
    plt.plot(x, y)
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=3))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.xticks(rotation=45)
    plt.title('Price History')
    plt.ylabel('Price')
    plt.text(0.05, 0.95, stats_str, transform=plt.gca().transAxes, fontsize=10, verticalalignment='top', bbox=dict(facecolor='white', alpha=0.5, boxstyle='round'))

    plt.subplot(2, 1, 2)
    data = []
    with open(csvfile) as file:
        reader = csv.DictReader(file)
        for rows in reader:
            data.append(float(rows['price']))
    plt.hist(data, bins=30, color = "lightblue", ec="black")
    plt.xlabel('Price')
    plt.ylabel('Frequency')
    plt.title('Price Distribution')

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    os.system('cls')
    print('Hello welcome to AUTOPY!\n \nIn this exotic car price scrapping program, when looking for your next hypercar, in order for us to make you save time we scrapped the top 10 cheapest super car you chosen from various auto selling platform.\nAlso, to help you visualize if your getting a good deal or not we added a graphical representation of how the price fluctuates to help you have the best deals!\n \nWe currently support graph visualisation for the:\n-  Ferrari 488\n-  Lamborghini Huracan\n-  Lamborghini Urus\n-  Mclaren 720s\n-  Mclaren Senna\n ')
    main()



    
from coinmarketcap import Market
from tkinter import *             
from tkinter import font  as tkfont
import pandas as pd
from tkinter import ttk
from PIL import Image, ImageTk

test = []
#############################################FRONTEND################################################################################

def raise_frame(frame):
    frame.tkraise()

root = Tk()

StartPage = Frame(root)
Introduction = Frame(root)
Amount = Frame(root)
Currencies = Frame(root)
Result = Frame(root)
Loading1 = Frame(root)
Loading2 = Frame(root)
Loading3 = Frame(root)
title_font = tkfont.Font(family='Comic Sans MS', size=18, weight="bold", slant="italic")
for frame in (StartPage, Loading1, Loading2, Loading3, Amount, Currencies, Result):
    frame.grid(row=0, column=0, sticky='news')

##StartPage
pic = PhotoImage(file="background.pgm",width=900,height=500)
Label(StartPage,compound=RIGHT,text="",image=pic, font=title_font,width=900,height=500).pack()
Button(StartPage, text='Start', command=lambda:raise_frame(Loading1),bg="#3333cc",height=2,width=15).pack()
Label(StartPage, text='•').pack()
Big_font = tkfont.Font(family='Verdana', size=30, weight="normal", slant="roman")
##Loading1
Label(Loading1,text="Loading modules and components",font=Big_font).pack()
progressbar = ttk.Progressbar(Loading1,orient=HORIZONTAL, length=1000, mode='determinate')
progressbar.pack(fill=BOTH, side=TOP,pady=125)
progressbar.start()
Label(Loading1, text='••').pack(side=BOTTOM)
Loading1.after(10000, lambda:raise_frame(Loading2))
##Loading2
progressbar2 = ttk.Progressbar(Loading2,orient=HORIZONTAL, length=1000, mode='determinate')
Label(Loading2,text="Establishing connection",font=Big_font).pack(side=TOP)
progressbar2.pack(fill=BOTH, side=TOP,pady=125)
progressbar2.start()
Label(Loading2, text='•••').pack(side=BOTTOM)
Loading2.after(20000, lambda:raise_frame(Loading3))
##Loading3
progressbar3 = ttk.Progressbar(Loading3,orient=HORIZONTAL, length=1000, mode='determinate')
Label(Loading3,text="Connecting to CoinmarketCap API",font=Big_font).pack(side=TOP)
progressbar3.pack(fill=BOTH, side=TOP,pady=125)
progressbar3.start()
Label(Loading3, text='••••').pack(side=BOTTOM)
Loading3.after(30000, lambda:raise_frame(Amount))
#Amount
Label(Amount,text="Please choose the amount you want to invest").pack()
Label(Amount, text='•••••').pack(side=BOTTOM)
capacity1 = StringVar(Amount)
capacity1.set("1000") # default value
ChosenAmount = OptionMenu(Amount, capacity1, "2000", "3000", "4000")
ChosenAmount.pack()
Label(Amount,text="Or type a custom value").pack(padx=5,pady=5)



raise_frame(StartPage)
root.iconbitmap('window.ico')

root.mainloop()
#####################################BACKEND##############################################################################################
curr =  {'Bitcoin Cash' : 'bch', 'Bitcoin' : 'btc', 'Dash' : 'dash', 'Decred' : 'dcr', 'Dogecoin' : 'doge',
         'Ethereum Classic' : 'etc', 'Ethereum' : 'eth', 'Litecoin' : 'ltc', 'PIVX' : 'pivx', 'Vertcoin' : 'vtc',
         'NEM' : 'xem', 'Monero' : 'xmr', 'Zcash' : 'zec'}
capacity = 1000
cp = Market()
def PriceFinder(*args,**kwargs):   #args are currencies choosen by user
	currencies = []       #Will hold currencies choosen by user
	for i in args:
		currencies.append(i)
	#print(currencies)
	
	prices = []
	for j in currencies:
		real_time_price = cp.ticker(currency=str(j),limit=1,convert='USD') 
		prices.append(real_time_price[0]['price_usd'])

	#print(prices)
	currency_dict = dict(zip(currencies,prices))
	extract(currency_dict)

def extract(price_dictionary):

	mean_of_30_Days = {}
	curr_list = list(price_dictionary.keys())
	for i in curr_list:
		data = pd.read_csv('DataSets\\'+curr[i].strip('')+'.csv',skiprows = range(1,337))
		prices = data.price_USD.tolist()
		summation = sum(prices)/30
		mean_of_30_Days[i] = summation
	performance(mean_of_30_Days,price_dictionary)


def performance(mean_of_30_Days,price_dictionary):  #gives 30 days performance of a currency
	currencyList = [str(i[0]) for i in mean_of_30_Days.items()]
	meanList = [float(i[1]) for i in mean_of_30_Days.items()]
	priceList = [float(i[1]) for i in price_dictionary.items()]
	performanceList = [priceList[i] - meanList[i] for i in range(min(len(priceList),len(meanList)))]
	performance_Dictionary = dict(zip(currencyList,performanceList))
	#print(performance_Dictionary)

	WeightDistributor(performance_Dictionary,price_dictionary)
	
	
def WeightDistributor(performance_Dictionary,price_dictionary):   #This algorithm will define weights
	weights = []

	Pf = [float(i[1]) for i in price_dictionary.items()] #real time price
	dict((k,float(v)) for k,v in price_dictionary.items())
	Gh = [float(i[1]) for i in performance_Dictionary.items()]    #gain-drop in previous 30 days
	#print(Gh)
	C = [str(i[0]) for i in performance_Dictionary.items()]
	#print(C)

	for i in tuple(zip(Pf,Gh)):
		temp_var = ((i[1]*i[0])/(i[0]-i[1]))%30
		weights.append(round(temp_var,3))

	#print(weights)

	FractionalKnapsack(capacity,weights,Pf,price_dictionary)            #Pf = values

def FractionalKnapsack(capacity: int, weights: list, Pf: list,price_dictionary ):
    Pf = [int(i) for i in Pf]
    weights = [int(i) for i in weights]
    #print(Pf)
    rows = len(Pf) + 1
    cols = capacity + 1

    # adding dummy values as later on we consider these values as indexed from 1 for convinence
    Pf = [0] + Pf[:]
    weights = [0] + weights[:]

    # row : values , #col : weights
    dp_array = [[0 for i in range(cols)] for j in range(rows)]

    # 0th row and 0th column have value 0

    # values
    for i in range(1, rows):
        # weights
        for j in range(1, cols):
            # if this weight exceeds max_weight at that point
            if j - weights[i] < 0:
                dp_array[i][j] = dp_array[i - 1][j]

            # max of -> last ele taken | this ele taken + max of previous values possible
            else:
                dp_array[i][j] = max(dp_array[i - 1][j], Pf[i] + dp_array[i - 1][j - weights[i]])

    # return dp_array[rows][cols]  : will have the max value possible for given wieghts

    values_chosen = []
    i = rows - 1
    j = cols - 1

    # Get the items to be picked
    while i > 0 and j > 0:

        # ith element is added
        if dp_array[i][j] != dp_array[i - 1][j]:
            # add the value
            values_chosen.append(Pf[i])
            # decrease the weight possible (j)
            j = j - weights[i]
            # go to previous row
            i = i - 1

        else:
            i = i - 1

    print("Based on previous 30 days data max Profit that can be made is {} by dividing {} in the following currencies:".format(dp_array[rows - 1][cols - 1],capacity))
    print(values_chosen)
    for i in values_chosen:
        for key, value in price_dictionary.items():
            if i == value:
                print(key)

PriceFinder('Bitcoin','Ethereum','Dash')


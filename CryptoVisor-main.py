from coinmarketcap import Market
import tkinter as tk              
from tkinter import font  as tkfont
import pandas as pd
test = []
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

#############################################FRONTEND################################################################################

class Engines(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageOne, PageTwo):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.config(bg="#383a39")
        self.pic = tk.PhotoImage(file="logo.PGM")
        label = tk.Label(self,compound=tk.CENTER,text="",image=self.pic, font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        button1 = tk.Button(self,fg="#a8dbcd",bg="#383a39", text="Start",
                            command=lambda: controller.show_frame("PageOne"),height = 2, width = 20)
        
        button1.pack()
      


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        label = tk.Label(self, font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 2", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()
if __name__ == "__main__":
    app = Engines()
    app.mainloop()

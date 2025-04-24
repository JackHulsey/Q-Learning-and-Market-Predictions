# environment for Amazon Q learner
import csv
from time import process_time

from PIL.GifImagePlugin import getdata


class AMZNStock(object):
    def __init__(self):
        self.state = (0, None, None)
        self.portfolio = (0, 1000) # num_shares, cash
        self.actions = [0,1,2] # sell, buy, hold
        self.k = 0.9 # how much less we value cash over stock (incentive)
        self.past = [] # array to hold past data
        self.data = []

    def reset(self):
        self.portfolio = (0, 1000)
        # self.state = (0, None, None)
        self.data = self.get_data()
        return self.state_update()

    def step(self, a, verbose=False):
        shares, cash = self.portfolio
        reward = 0
        price = self.state[1]

        if a == 0:
            if shares == 0:
                a = 2

            else: # sell
                if verbose:
                    print(f"Sold at: {price:<5}")
                self.portfolio = (0, cash + shares*price)
                reward = (self.portfolio_value(self.portfolio, price) - self.portfolio_value((shares, cash), price)) / self.portfolio_value((shares, cash), price)


        elif a == 1:
            if cash < price:
                a = 2
            else: # buy
                max_buy = cash // price
                if verbose:
                    print(f"Bought at: {price:<5}")
                extra = cash - (max_buy * price)
                self.portfolio = (shares + max_buy, extra)
                reward = (self.portfolio_value(self.portfolio, price) - self.portfolio_value((shares, cash), price)) / self.portfolio_value((shares, cash), price)
        elif a == 2: # hold
            if verbose:
                print(f"Held at: {price:<5}")
            reward = 0
        self.state = self.state_update()

        return reward, self.state_update(), self.portfolio


    def portfolio_value(self, portfolio, price):
        return portfolio[0]*price + portfolio[1]*self.k

    def state_update(self):
        if self.state != (0, None, None):
            self.past.append(self.state) # add previous state to our past data
        self.state = self.data[self.state[0]+1]
        return self.state

    def get_data(self):
        data = []

        with open('AMZN_stock_data.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            header = next(reader)
            for idx, row in enumerate(reader):
                (Date, Open, High, Low, Close, Volume, Dividends, Stock_Splits) = row
                # Convert values to float
                Open = float(Open)
                High = float(High)
                Low = float(Low)
                Volume = int(Volume)
                data.append((idx, Open, High, Low, Volume))
        return data
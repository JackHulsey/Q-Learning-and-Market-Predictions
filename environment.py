# environment for Amazon Q learner
import csv
from time import process_time

class AMZNStock(object):
    def __init__(self):
        self.state = (0, None, None)
        self.portfolio = (0, 0) # num_shares, cash
        self.actions = [0,1,2] # sell, buy, hold
        self.k = 0.9 # how much less we value cash over stock (incentive)
        self.past = [] # array to hold past data

    def reset(self):
        self.portfolio = (0, 0)
        self.state = (0, None, None)
        return self.state_update()

    def step(self, a):
        shares, cash = self.portfolio
        reward = 0
        price = self.state[1]


        if a == 0 and shares != 0:
            self.portfolio = (0, cash + shares*price)
            reward = self.portfolio_value(self.portfolio, price) - self.portfolio_value((shares, cash), price)


        elif a == 1 and cash >= price: # buy
            max_buy = cash // price
            extra = cash % price
            self.portfolio = (shares + max_buy, extra)
            reward = self.portfolio_value(self.portfolio, price) - self.portfolio_value((shares, cash), price)

        elif a == 2: # we hold
            reward = 0

        return reward, self.state_update(), self.portfolio


    def portfolio_value(self, portfolio, price):
        return portfolio[0]*price + portfolio[1]*self.k

    def state_update(self):
        if self.state != (0, None, None):
            self.past.append(self.state) # add previous state to our past data

        with open('AMZN_stock_data.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            header = next(reader)  # Skip header row
            for idx, row in enumerate(reader):
                if idx == self.state[0]+1:
                    (Date,Open,High,Low,Close,Volume,Dividends,Stock_Splits) = row

        return tuple(idx, Open, High, Low, Volume)
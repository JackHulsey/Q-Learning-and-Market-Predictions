from collections import defaultdict
from random import random, choice
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

class QLearner(object):
    def __init__(self, alpha, gamma, epsilon, decay):
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.decay = decay
        self.q = defaultdict(float)

    def ARIMA_predict(self, s, past):
        open_prices = []
        for day in past:
            open_prices.append(day[1])
        open_prices.append(s[0])
        open_ts = open_prices

        # Fit ARIMA(5,1,1)
        model = ARIMA(open_ts, order=(2, 1, 1)) # was (5, 1, 1)
        mod511 = model.fit()

        # Forecast the next time step
        forecast_result = mod511.get_forecast(steps=1)
        predict1 = forecast_result.predicted_mean[0]

        # Output
        return predict1

    def choose(self, s, actions):
        if random() < self.epsilon:
            return choice(actions)
        else:
            return max(actions, key=lambda a: self.q[s, a])

    def update(self, s, a, r, sp, actions, past):
        predicted_price = self.ARIMA_predict(s, past)

        if predicted_price < s[1] * 1.1 and a == 0:
            self.epsilon *= self.decay
            r += 5
        elif predicted_price > s[1] * 0.9 and a == 1:
            self.epsilon *= self.decay
            r += 5
        elif predicted_price < s[1] * 1.1 and predicted_price > s[1] * 0.9 and a == 2:
            self.epsilon *= self.decay
            r += 5
        else:
            self.epsilon *= self.decay
            r -= 2

        reward = r + self.gamma * max(self.q[sp, ap] for ap in actions)
        self.q[s, a] = self.alpha * reward + (1 - self.alpha) * self.q[s, a]



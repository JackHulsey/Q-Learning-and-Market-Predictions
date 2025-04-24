from matplotlib import pyplot as plt

from agent import QLearner
from environment import AMZNStock

def main():
    agent = QLearner(0.01, 0.99, 0.5, 0.99)
    env = AMZNStock()

    batches = 1
    episodes = 6000
    value = []
    profit = [0]*batches

    for i in range(batches):
        s = env.reset()
        for _ in range(episodes):
            a = agent.choose(s, env.actions)
            r, sp, portfolio = env.step(a, verbose=False)
            agent.update(s, a, r, sp, env.actions, env.past)
            s = sp
            value.append(env.portfolio_value(env.portfolio, s[1])-900)
            if _ % 1000 == 0:
                print(value[-1])
        print(env.portfolio_value(env.portfolio, s[1]))
        profit[i] = env.portfolio_value(env.portfolio, s[1]) - 900

    plt.plot(list(range(episodes)), value, color='green')
    plt.ylabel("Profit")
    plt.xlabel("Days since start")
    plt.show()

if __name__ == "__main__":
    main()



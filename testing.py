# test_environment.py
from environment import AMZNStock

def run_test():
    env = AMZNStock()

    # Reset environment and check initial state
    initial_state = env.reset()
    print("Initial state:", initial_state)

    # Initial portfolio should be (0 shares, 0 cash)
    print("Initial portfolio:", env.portfolio)

    # Give the agent some initial cash manually for testing
    env.portfolio = (0, 1000)

    actions = ["Sell", "Buy", "Hold"]

    # Run through each action once
    for action in range(3):
        print(f"\nTesting action: {actions[action]}")
        reward, new_state, new_portfolio = env.step(action)
        print(f"Reward: {reward}")
        print(f"New state: {new_state}")
        print(f"New portfolio: {new_portfolio}")

if __name__ == "__main__":
    run_test()
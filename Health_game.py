from Health_Env import *

env = Manage_healthcare()

done = False
state = env.reset()
print(f"Initial state: {state}")
while not done:
    print("\nChoose an action: 1. Invest in healthcare, 2. Invest in prevention, 3. Do nothing")
    action = input("Enter action (1/2/3): ")
    
    if action == '1':
        action = 1
    elif action == '2':
        action = 2
    elif action == '3':
        action = 3
    else:
        print("Invalid action! Please choose 1, 2, or 3.")
        continue
    
    state, reward, done = env.step(action)
   
    print(f"State after action: {state}")
    print(f"Reward: {reward}")
    
    if done:
        print("Simulation ended due to pandemic.")
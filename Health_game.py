from Health_Env import *

env = Manage_healthcare(budget=150, healthcare_level=60, health_risk_level=40)

done = False
state = env.reset()
print(f"Initial state: {state}")
while not done:
    print("\nChoose an action: 1. Invest in healthcare, 2. Invest in prevention, 3. Do nothing")
    action = input("Enter action (1/2/3): ")
    
    if action == '1':
        action = 'invest_in_healthcare'
    elif action == '2':
        action = 'invest_in_prevention'
    elif action == '3':
        action = 'do_nothing'
    else:
        print("Invalid action! Please choose 1, 2, or 3.")
        continue
    
    state, reward, done = env.step(action)
   
    print(f"State after action: {state}")
    print(f"Reward: {reward}")
    
    if done:
        print("Simulation ended due to pandemic.")
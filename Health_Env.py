import gymnasium as gym
from gym import spaces
import random


class Manage_healthcare(gym.Env):

    def __init__(self, initial_budget = 10.000, initial_healthcare = 50, initial_risk = 50, max_years = 30):
        super(Manage_healthcare, self).__init__()
        """
        Initialize the environment with the initial values 
        
        """
        self.initial_budget = initial_budget
        self.initial_healthcare = initial_healthcare
        self.initial_risk = initial_risk
        self.max_years = max_years
        self.state = (self.initial_budget, self.initial_healthcare, self.initial_risk)
        self.current_year = 0

        # invest in healthcare, invest in edu, do nothing
        self.action_space = spaces.Discrete(3)
        # budget, healthcare level, health risk are continuous
        self.observation_space = spaces.Box(low=0, high=float('inf'), shape=(3,), dtype=float)

        self.done = False

    def step(self, action):
        # Then take actions
        if action == 0: # invest in healthcare
            if self.budget >= 2:
                self.healthcare_level += 3
                self.budget -= 2
            else:
                print("Not enough budget to invest in healthcare.")
            
        elif action == 1: # invest in education & prevention
            if self.budget >= 1:
                self.risk_level = max (0, self.risk_level - 1)
                self.budget -= 1
            else:
                print("Not enough budget to invest in Education and Prevention.")

        elif action == 2: # do nothing
            self.budget += 2
        else:
            raise ValueError("Invalid action, please select one between: 0 = invest_healthcare, 1 = invest_edu or 2 = do_nothing.")
        
        self.risk_level += random.randint(1,3)

        pandemic_occurrence = False
        if self.risk_level > self.healthcare_level:
            pandemic_pr = (self.risk_level - self.healthcare_level) / self.risk_level
            if random.random() < pandemic_pr:
                pandemic_occurrence = True # pandemic has occured
                penalty = -1000 * (self.risk_level - self.healthcare_level)  # Penalty grows with the severity
                reward = penalty
                self.done = True
            else: 
                reward = self.budget
                self.done = False
        else: 
            reward = self.budget
            self.done = False

        self.current_year += 1
        if self.current_year >= self.max_years:
            self.done = True
        if self.budget <= 0:
            self.done = True

        current_state = (self.budget, self.healthcare_level, self.risk_level)
        info = {}
        
        return current_state, reward, self.done, info
    
    def reset(self):
        """
        Reset the environment to the initial state for a new simulation.
        """
        self.state = (self.initial_budget, self.initial_healthcare, self.initial_risk)
        self.current_year = 0
        self.done = False
        return self.state
    
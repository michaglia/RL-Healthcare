import gymnasium as gym
from gym import spaces
import random


class Manage_healthcare(gym.Env):

    def __init__(self, budget, healthcare_level, risk_level):
        super(Manage_healthcare, self).__init__()
        """
        Initialize the environment with the initial values 
        
        """
        self.budget = budget
        self.healthcare_level = healthcare_level
        self.risk_level = risk_level
        self.actions = ["invest_health", "invest_edu", "do_nothing"]
        self.done = False # true when the simulation ends
        
    @property
    def actions(self, action):
        if action == "invest_health":
            if self.budget >= 2:
                self.healthcare_level += 3
                self.budget -= 2
            else:
                print("Not enough budget to invest in healthcare.")
            
        elif action == "invest_edu":
            if self.budget >= 1:
                self.risk_level = max (0, self.risk_level - 1)
                self.budget -= 1
            else:
                print("Not enough budget to invest in Education and Prevention.")

        elif action == "do_nothing":
            self.budget += 2
        else:
            raise ValueError("Invalid action, please select one between: invest_healthcare, invest_edu or do_nothing.")
        
        self.risk_level += random.randint(1,3)

        if self.risk_level > self.healthcare_level:
            self.done = True # pandemic has occured
            reward = random.randint(-1000, -100)
        else: 
            reward = self.budget
        
        return self.done, reward, self.get_state()
    
    def get_state(self):
        """
        Returns the current state 
        """
        return (self.budget, self.healthcare_level, self.risk_level)
    
    def reset(self, initial_budget, initial_healthcare_level, initial_health_risk):
        """
        Reset the environment to the initial state for a new simulation.
        """
        self.budget = initial_budget
        self.healthcare_level = initial_healthcare_level
        self.health_risk = initial_health_risk
        self.done = False
        return self.get_state()
    
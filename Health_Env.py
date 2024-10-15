import gym
from gym import spaces
from gym.spaces import Discrete, Box
import numpy as np
import random
from gym.envs.registration import register


class HealthcareEnv(gym.Env):
    def __init__(self, initial_budget = 1000, initial_healthcare = 50, initial_risk = 50, risk_increment_prob = 0.2, election_interval = 5):
        super(HealthcareEnv, self).__init__()
        """
        Initialize the environment with the initial values 
        
        """
        self.initial_budget = initial_budget
        self.initial_healthcare = initial_healthcare
        self.initial_risk = initial_risk
        self.risk_increment_prob = risk_increment_prob
        self.election_interval = election_interval  # Elections every 5 years
        #self.max_years = max_years
        self.current_year = 0

        # 0 invest in healthcare, 1 invest in edu, 2 do nothing
        self.action_space = spaces.Discrete(3)
        # budget, healthcare level, health risk 
        self.observation_space = spaces.Dict({
            "budget": spaces.Box(low=0, high=1000, shape=(1,), dtype=np.float64),
            "health_level": spaces.Discrete(99),
            "risk_level": spaces.Discrete(99)
        })
        #self.do_nothing_count = 0
        self.done = False

    def _get_obs(self):
        return {
        "budget": np.clip(np.array([self.initial_budget], dtype=np.float64), 0, 10000),  # Budget remains as float
        "health_level": np.clip(np.int64(self.initial_healthcare), 0, 100),  # Ensure health_level is int64
        "risk_level": np.clip(np.int64(self.initial_risk), 0, 100)  # Ensure risk_level is int64
    }

    @property
    def actions_available(self):
        '''
        Returns the available actions based on the current state
        '''
        available_actions = []
        if self.initial_budget >= 2:
            # Can invest in healthcare
            available_actions.append(0)
        if self.initial_budget >= 1:
            # Can invest in education
            available_actions.append(1)
        if self.initial_budget < 2:
            # If budget is low, doing nothing becomes a viable option
            available_actions.append(2)

        # Return actions based on the current state
        return available_actions 
    
    def reward(self):
        """
        Calculates the reward based on the current state of the environment
        """
        pandemic_occurrence = False

        # increase health_risk randomly by the increment
        if random.random() < self.risk_increment_prob:
            self.initial_risk += random.randint(1,3)
            
            if self.initial_risk > self.initial_healthcare:
                pandemic_pr = (self.initial_risk - self.initial_healthcare) / self.initial_risk
                if random.random() < pandemic_pr:
                    pandemic_occurrence = True  # pandemic has occurred
                    penalty = -1000 * (self.initial_risk - self.initial_healthcare) # very large penalty
                    return penalty, True  # episode ends with large penalty due to pandemic
            else:
                return self.initial_budget, False

        if self.current_year % self.election_interval == 0:
            election_reward = 500 * (self.initial_healthcare - self.initial_risk)
            if election_reward < 0:
                return election_reward, True # you lose the election, end simulation
            else:
                return election_reward, False
        health_risk_reward = 1000 - 10 * self.initial_risk
        return health_risk_reward, False
    
    def step(self, action):
        # Take actions
        if action == 0: # invest in healthcare
            #self.do_nothing_count = 0
            if self.initial_budget >= 2:
                self.initial_healthcare += min(100, self.initial_healthcare + 3)
                self.initial_budget -= 2
        elif action == 1: # invest in education & prevention
            #self.do_nothing_count = 0
            if self.initial_budget >= 1:
                self.initial_risk = max(0, self.initial_risk - 1)
                self.initial_budget -= 1
        elif action == 2: # do nothing
            #self.do_nothing_count += 1
            self.initial_budget += 2

            #if self.do_nothing_count >= 2:
                #self.initial_budget = self.initial_budget - 3 
                # Penalty applied for doing nothing twice in a row

        reward, self.done = self.reward()

        self.current_year += 1
        # if self.current_year >= self.max_years or self.initial_budget <= 0:
        #    self.done = True

        truncated = False
        terminated = self.done
        observation = self._get_obs()
        info = {}
        
        return observation, reward, terminated, truncated, info
    
    def reset(self, seed=None, options:  dict = {}):
        super().reset(seed=seed)
        self.initial_budget = 1000
        self.initial_healthcare = 50
        self.initial_risk = 50
        self.current_year = 0
        #self.do_nothing_count = 0
        info = {}
        return self._get_obs(), info
    
gym.envs.registration.register(
    id='HealthcareEnv-v0',
    entry_point=HealthcareEnv,
    max_episode_steps=31,
)
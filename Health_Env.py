import gym
from gym import spaces
from gym.spaces import Discrete, Box
import numpy as np
import random
from gym.envs.registration import register


class HealthcareEnv(gym.Env):
    def __init__(self, initial_budget = 1000, initial_healthcare = 5, initial_risk = 5, max_years = 30):
        super(HealthcareEnv, self).__init__()
        """
        Initialize the environment with the initial values 
        
        """
        self.initial_budget = initial_budget
        self.initial_healthcare = initial_healthcare
        self.initial_risk = initial_risk
        self.max_years = max_years
        self.current_year = 0

        # 0 invest in healthcare, 1 invest in edu, 2 do nothing
        self.action_space = spaces.Discrete(3)
        # budget, healthcare level, health risk 
        self.observation_space = spaces.Dict({
            "budget": spaces.Box(low=0, high=1000, shape=(1,), dtype=np.float32),
            "health_level": spaces.Discrete(100),
            "risk_level": spaces.Discrete(100)
        })
        self.do_nothing_count = 0
        self.done = False

    def _get_obs(self):
        return {
        "budget": self.initial_budget,
        "health_level": self.initial_healthcare,
        "risk_level": self.initial_risk
    }

    @property
    def actions_available(self):
        '''
        Returns the available actions based on the current state
        '''
        max_budget = self.observation_space.spaces['budget'].high[0]
        assert self.initial_budget <= max_budget, 'Invalid state: Budget exceeds maximum limit'

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
    
    def step(self, action):
        # Then take actions
        if action == 0: # invest in healthcare
            self.do_nothing_count = 0
            if self.initial_budget >= 2:
                self.initial_healthcare += 3
                self.initial_budget -= 2
        elif action == 1: # invest in education & prevention
            self.do_nothing_count = 0
            if self.initial_budget >= 1:
                self.initial_risk = max(0, self.initial_risk - 1)
                self.initial_budget -= 1
        elif action == 2: # do nothing
            self.do_nothing_count += 1
            self.initial_budget += 2

            if self.do_nothing_count >= 2:
                self.initial_budget = self.initial_budget - 3 
                # Penalty applied for doing nothing twice in a row

        # increase health_risk randomly 
        self.initial_risk += random.randint(1,3)

        pandemic_occurrence = False
        if self.initial_risk > self.initial_healthcare:
            pandemic_pr = (self.initial_risk - self.initial_healthcare) / self.initial_risk
            if random.random() < pandemic_pr:
                pandemic_occurrence = True # pandemic has occured
                penalty = -1000 * (self.initial_risk - self.initial_healthcare) 
                reward = penalty
                self.done = True
            else: 
                reward = self.initial_budget
                self.done = False
        else: 
            reward = self.initial_budget
            self.done = False

        self.current_year += 1
        if self.current_year >= self.max_years or self.initial_budget <= 0:
            self.done = True

        truncated = False
        terminated = self.done
        observation = self._get_obs()
        info = {}
        
        return observation, reward, terminated, truncated, info
    
    def reset(self, seed=None, options:  dict = {}):
        super().reset(seed=seed)
        self.initial_budget = self.initial_budget
        self.initial_healthcare = self.initial_healthcare
        self.initial_risk = self.initial_risk
        self.current_year = 0
        self.do_nothing_count = 0
        info = {}
        return self._get_obs(), info
    
gym.envs.registration.register(
    id='HealthcareEnv-v0',
    entry_point=HealthcareEnv,
    max_episode_steps=31,
)
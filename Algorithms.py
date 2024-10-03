""" Implement the Healthcare Agents """
import numpy as np
import gym
import torch


class HealthQLearnVFA:
    """
    Q-learning VFA implementation
    """
    def __init__(self, environment: gym.Env, learning_rate: float, epsilon: float,
                 epsilon_decay: float,
                  final_epsilon: float,
                   gamma: float =.95, initial_w: np.ndarray = None) -> None:
        self.env = environment
        self.alpha = learning_rate
        self.gamma = gamma
        self.epsilon = epsilon
        self.e_decay = epsilon_decay
        self.e_final = final_epsilon
        self.training_error = []

        if initial_w is None:
            num_features = self.env.observation_space.shape[0]
            i_w = np.ones((self.env.action_space.n, num_features))
        else:
            i_w = initial_w
        self.w = torch.tensor(i_w, dtype=float, requires_grad=True)

    def x(self, state: dict) -> np.ndarray:
        """Returns the features that represents the state

        Args:
            state (dict): The state as a dictionary obtained as the observation object returned by a step
        Returns:
            torch.tensor: state observed by the agent in terms of state features 
        """
        features = np.array(list(state.values())) # current state of the environment into feature vector
        return torch.tensor(features, dtype=float, requires_grad=False)
    
    def q(self, state: int, action: int) -> float:
        return self.x(state) @ self.w[:, action]
        
    def policy(self, state: int) -> int:
        """Implements e-greedy strategy for action selection

        Args:
            state (tuple[int, int, bool]): state observed according to the environment

        Returns:
            int: action
        """
        available = self.env.actions_available
        options = [i for i, a in enumerate(available) if a == 1]
        if np.random.random() < self.epsilon:
            return np.random.choice(options)
        else:
            available_values = [self.q(state, a).detach().numpy() for a in options]
            return options[np.argmax(available_values)]

    def update(self, state: int, action: int, reward: float, s_prime: int):
        next_action = self.policy(state)
        q_target = reward + self.gamma * self.q(s_prime, next_action)
        q_value = self.q(state, action)
        delta = q_target - q_value
        q_value.backward()
        with torch.no_grad():
            self.w += self.alpha * delta * self.w.grad 
            self.w.grad.zero_()
        self.training_error.append(delta.detach().numpy())
    
    def decay_epsilon(self):
        self.epsilon = max(self.e_final, self.epsilon - self.e_decay)
        


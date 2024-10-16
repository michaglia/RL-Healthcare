# Healthcare Management Reinforcement Learning
### Project Overview
This project aims to develop a reinforcement learning (RL) environment for managing healthcare policies using Q-learning Value Function Approximation (VFA) and Deep Q-Learning (DQL) agents. The environment simulates a healthcare system of a government, where an agent must make decisions to optimize the healthcare level of a population while managing a limited budget and reducing the risk of a pandemic. The second important goal of the agent is to maintain a balance between healthcare and risk levels, while navigating through elections happening every 5 years and that can affect its tenure. 

_Will the agent maintain its job or be fired during the next elections?_

#### ENVIRONMENT
##### State space: budget, health level, risk level
##### Action space: 
###### - 0: Increase health and decrease risk.
###### - 1: Improve quality of care while slightly increasing health.
###### - 2: Allocate resources without significant changes to health or risk.
##### Rewards:
###### 1. A reward for maintaining or improving the health level while managing risk.
###### 2. A penalty for negative outcomes such as low health levels or high risk levels.
###### 3. An election reward based on the difference between health level and risk level, affecting the agent's tenure.

[Here](https://github.com/afflint/rlcoding/blob/main/2023-24/projects/rl-projects.pdf) you can find the project proposal!

### Contribution
Contributions to enhance the project are welcome! Please feel free to submit a pull request or open an issue for discussion.

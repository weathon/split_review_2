### Summary

The paper studies the problem of pursuit-evasion game (PEG) on graphs. The paper considers the setting where the evader can move asynchronously and has the knowledge of the pursuer's actions, and the pursers have only partial observability of the evader. The paper first extends a dynamic programming (DP) algorithm to capture the evader under these two new settings. Then, the paper proposes a learning approach for the pursuers, which can be applied to different graphs.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper considers two new settings for the pursuit-evasion game, which are more realistic than the standard assumption. Theoretical results are provided to show the proposed DP algorithm is correct.
2. The paper also proposes a learning approach for the pursuers, which can be applied to different graphs.

### Weaknesses

#### Some Related Works


#### comment

1. It is unclear to me if the learning approach is using the DP algorithm as a simulator or part of the learning approach.

2. It is also unclear to me what is the game-theoretic equilibrium concept that the learning approach is trying to compute. There is only one evader and multiple pursuers. The multiple pursuers are following the same policy, so it is not a competitive game and there is no competition among the pursuers.

### Suggestions

The paper needs to clarify the precise role of the dynamic programming (DP) algorithm within the learning framework. Specifically, it should be explicitly stated whether the DP algorithm is used solely as a simulator to generate training data for the learning algorithm, or if it is integrated more deeply into the learning process itself, perhaps as a component of the loss function or policy optimization. If the DP algorithm is used to generate optimal or near-optimal responses from the evader, this should be clearly stated, and the method for generating these responses should be detailed. Furthermore, the paper should explain how the outputs of the DP algorithm are used to train the pursuer's policy. For example, are the states, actions, and rewards from the DP simulation used to update the pursuer's policy network via backpropagation? Understanding this connection is crucial for evaluating the effectiveness of the learning approach.

Regarding the game-theoretic equilibrium concept, the paper needs to provide a more detailed explanation of how the concept of Nash equilibrium applies in this specific setting. While it is true that the multiple pursuers are following the same policy, the underlying game is still a two-player zero-sum game between the single evader and the team of pursuers. The paper should clarify that the Nash equilibrium is being computed at the level of teams, where each team is considered a single player. The evader's strategy is to minimize the capture time, while the pursuers' strategy is to maximize the capture time, given the evader's strategy. The paper should explicitly state that the learning algorithm aims to find a policy for the pursuers that is optimal against the best response of the evader, which is what a Nash equilibrium represents in this context. A more detailed explanation of how the cross-graph reinforcement learning framework achieves this would be beneficial.

Finally, the paper should provide more details on the cross-graph reinforcement learning framework. It is not clear how the pursuer's policy is trained across different graphs. Does the policy network take the graph structure as input? If so, how is this done? The paper should also explain how the reference policy is generated from the preprocessed distance tables. Are these tables computed using the DP algorithm? The paper should also clarify how the diversity of graph structures impacts the training process and the final performance of the pursuer's policy. A more detailed explanation of these aspects would greatly enhance the clarity and understanding of the proposed learning approach.

### Questions

1. How does the learning approach use the DP algorithm?
2. What is the game-theoretic equilibrium concept that the learning approach is computing?

### Rating

6

### Confidence

3

**********
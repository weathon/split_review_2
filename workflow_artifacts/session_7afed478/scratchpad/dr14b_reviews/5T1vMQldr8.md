### Summary

This paper focuses on offline preference-based reinforcement learning (PbRL) and aims to mitigate the reward extrapolation error that occurs when the policy encounters out-of-distribution data. The authors propose a method that leverages attention weights from the preference learning stage to extract subgoals, which are then used to guide the offline policy optimization stage. The approach is evaluated on various offline PbRL benchmarks, demonstrating both performance improvements and a reduction in extrapolation errors compared to prior methods.

### Soundness

2

### Presentation

3

### Contribution

2

### Strengths

The paper addresses a critical challenge in offline PbRL, focusing on the important problem of mitigating reward extrapolation errors. The proposed method is clearly explained and easy to understand. The authors provide comprehensive experimental results that effectively demonstrate the performance improvements and the reduction in extrapolation errors compared to prior methods.

### Weaknesses

#### Some Related Works


#### comment

The proposed method relies on the availability of attention weights from the preference learning stage, which may limit its applicability to certain preference learning methods. For example, it is not clear how this approach would be adapted to a reward neural network that does not incorporate an attention mechanism. Furthermore, while the method identifies state-action pairs with high attention weights and rewards as subgoals, it lacks a rigorous theoretical justification for why these specific points are optimal for guiding the policy. The method seems to assume that high attention and reward correlate with critical decision points, but this correlation is not formally proven, and it's possible that other selection strategies could be more effective. Additionally, while the authors conduct extensive experiments across various domains, the performance improvement of the proposed method appears to be somewhat marginal, and it does not consistently outperform baseline methods across all tasks. This raises concerns about the robustness and generalizability of the approach. Finally, the paper lacks a detailed analysis of the sensitivity of the method to the hyperparameter K, which controls the selection of subgoals. While ablation studies are presented, they do not fully explore the impact of different K values on the final performance, and it is unclear how to choose an appropriate K for different tasks.

### Suggestions

To strengthen the paper, the authors should first provide a more rigorous justification for their subgoal selection strategy. While the intuition behind using high attention and reward states is plausible, a theoretical analysis or formal proof demonstrating why these states are optimal or near-optimal for guiding the policy would significantly enhance the paper's contribution. This could involve analyzing the properties of the learned reward function and the attention mechanism, and showing how they relate to the identification of critical decision points. Furthermore, the authors should explore alternative subgoal selection methods and compare their performance to the proposed approach. This would help to validate the effectiveness of the chosen strategy and provide a more comprehensive understanding of the method's strengths and weaknesses. For example, one could consider using clustering algorithms to identify regions of the state space with high reward density, or using a diversity metric to ensure that the selected subgoals cover a wide range of behaviors. 

Second, the authors should conduct a more thorough analysis of the method's sensitivity to the hyperparameter K. The current ablation study is insufficient to fully understand the impact of K on the final performance. A more detailed analysis should explore a wider range of K values and examine how the selected subgoals change as K is varied. This analysis should also investigate the relationship between K and the characteristics of the task, such as the complexity of the environment and the diversity of the optimal policy. The authors should provide clear guidelines for selecting an appropriate K for different tasks, possibly based on the statistical properties of the attention weights or the reward distribution. This would make the method more practical and easier to apply in real-world scenarios. Additionally, the authors should consider adaptive methods for selecting K, which could potentially improve the robustness of the approach.

Finally, the authors should address the limitations of their method regarding its applicability to preference learning methods that do not use attention mechanisms. While the authors acknowledge this limitation, they should provide more concrete suggestions for how their approach could be adapted to other types of reward models. This could involve exploring alternative ways of identifying critical states in the absence of attention weights, such as using saliency maps or other techniques for interpreting neural networks. The authors could also consider using a hybrid approach that combines the strengths of different reward models. This would make the method more general and applicable to a wider range of offline PbRL problems. Furthermore, the authors should investigate the performance of their method on more challenging benchmarks, where the improvement over baseline methods is more significant. This would provide stronger evidence for the effectiveness of their approach and address concerns about its robustness and generalizability.

### Questions

1. In lines 259-260, it is mentioned that the subgoal state set $\mathcal{S}_g$ is constructed by selecting states that satisfy both attention-based and reward-based criteria. Could you clarify which value the reward $\hat{r}_t$ refers to? Is it the reward learned by the Preference Transformer, or is it the Bradley-Terry reward?
2. In lines 270-271, it states that the CVAE is trained with state-action-subgoal triplets $(s_t, a_t, g_t)$ sampled from preferred trajectories, where $g_t$ is a subgoal state. Could you clarify how $g_t$ is defined? Is it the state $s_{t+1}$ that the agent transits to after taking action $a_t$ in state $s_t$, or is it a state identified as a subgoal using the method described in Section 4.1.2?
3. In lines 431-432, it is mentioned that the number of queries differs for each environment. Could you provide more details on how these queries are obtained? Additionally, please explain how the results in Table 4 demonstrate the query efficiency of SPOT.
4. In line 259, the subgoal state set $\mathcal{S}_g(\sigma; K)$ is defined based on a hyperparameter $K$. Could you provide more details on how $K$ is selected? How sensitive is the method to the choice of $K$?

### Rating

5

### Confidence

3

**********
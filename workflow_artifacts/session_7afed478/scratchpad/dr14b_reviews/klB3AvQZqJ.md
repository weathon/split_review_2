### Summary

This paper introduces a minimalist approach to offline safe reinforcement learning (OSRL) that does not require any additional hyperparameters. The proposed method, Constraint-aware Reward (Re)Labeling (CARL), is designed to be wrapped around existing offline RL algorithms. CARL iteratively alternates between two steps for each sampled batch of data: updating the cost evaluation function using an off-policy evaluation procedure and updating the policy using relabeled rewards. The authors demonstrate that CARL reliably enforces safety constraints under small cost budgets, while achieving high rewards on the DSRL benchmark tasks.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper is well-written and easy to follow.
2. The proposed method is simple and effective. It does not introduce any additional hyperparameters, which makes it easy to implement and use.
3. The experimental results on the DSRL benchmark tasks are impressive. The authors demonstrate that CARL reliably enforces safety constraints under small cost budgets, while achieving high rewards.
4. The authors provide a thorough analysis of the proposed method, including ablation studies and comparisons with other state-of-the-art methods.

### Weaknesses

#### Some Related Works


#### comment

1. Theorem 1 is not rigorous enough. For example, the authors didn't explain the existence of $V_{max}$, and the authors didn't explain the existence of optimal policy $\pi^*$ for problem (2). The authors should provide a more detailed explanation of the conditions under which $V_{max}$ is finite and the existence of an optimal policy for the constrained problem (2). Specifically, the proof should address the potential for the cost constraint to render the problem infeasible, and how this impacts the existence of a solution. Furthermore, the proof should explicitly state the assumptions on the MDP (e.g., finiteness of state and action spaces, or specific properties of the transition probabilities) that guarantee the existence of $V_{max}$ and the optimal policy.
2. The authors didn't provide the convergence guarantee of CARL. The iterative nature of CARL, involving off-policy evaluation and policy optimization, raises concerns about convergence. The authors should provide a more detailed analysis of the convergence properties of the algorithm, including the conditions under which the iterative process is guaranteed to converge to a safe and optimal policy. This analysis should consider the potential for oscillations or divergence due to the alternating updates of the cost evaluation function and the policy.
3. The authors didn't provide the sensitivity analysis of CARL to different hyperparameters. While the authors claim that CARL doesn't introduce any additional hyperparameters, it is still important to analyze the sensitivity of the algorithm to the hyperparameters of the underlying offline RL algorithm and the off-policy evaluation method. The authors should provide a detailed analysis of how the performance of CARL varies with different choices of these hyperparameters, and provide guidelines for selecting appropriate values.

### Suggestions

The paper would benefit from a more rigorous treatment of the theoretical underpinnings of the proposed method. Specifically, the authors should provide a more detailed proof of Theorem 1, explicitly stating the assumptions on the MDP and addressing the potential for the cost constraint to render the problem infeasible. The proof should also clarify the conditions under which $V_{max}$ is finite and the existence of an optimal policy for the constrained problem (2). Furthermore, the authors should provide a convergence analysis of the CARL algorithm, including the conditions under which the iterative process is guaranteed to converge to a safe and optimal policy. This analysis should consider the potential for oscillations or divergence due to the alternating updates of the cost evaluation function and the policy. It would be beneficial to explore the use of techniques such as contraction mapping or Lyapunov analysis to establish convergence guarantees.

In addition to the theoretical analysis, the authors should provide a more comprehensive experimental evaluation of the proposed method. This evaluation should include a sensitivity analysis of CARL to the hyperparameters of the underlying offline RL algorithm and the off-policy evaluation method. The authors should provide a detailed analysis of how the performance of CARL varies with different choices of these hyperparameters, and provide guidelines for selecting appropriate values. Furthermore, the authors should compare the performance of CARL with a wider range of state-of-the-art offline safe RL algorithms, including those that use Lagrangian-based approaches. This comparison should include a detailed analysis of the strengths and weaknesses of each method, and should provide insights into the conditions under which CARL is most effective. The authors should also explore the performance of CARL on more complex and challenging benchmark tasks, to further demonstrate the robustness and generalizability of the proposed method.

Finally, the authors should provide a more detailed discussion of the limitations of the proposed method. This discussion should include the potential for the algorithm to fail in certain scenarios, such as when the cost constraint is very tight or when the offline dataset is not representative of the environment. The authors should also discuss the computational cost of the proposed method, and compare it with other offline safe RL algorithms. This discussion should provide a more balanced and realistic assessment of the proposed method, and should help to guide future research in this area. The authors should also consider the potential for the proposed method to be extended to other types of constraints, such as time-varying constraints or constraints that are not easily quantifiable.

### Questions

1. Could you provide more details about the implementation of CARL? For example, how do you choose the hyperparameters for the off-policy evaluation and policy optimization steps?
2. How does CARL compare to other state-of-the-art offline safe RL algorithms in terms of computational efficiency and scalability?
3. What are the limitations of CARL? Are there any scenarios where it might not work well?

### Rating

6

### Confidence

3

**********
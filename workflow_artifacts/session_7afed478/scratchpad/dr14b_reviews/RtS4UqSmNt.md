### Summary

The paper studies a planner who controls the information precision of agents while they also learn from the decisions of earlier agents. The planner may seek to improve social welfare (an altruistic planner) or to induce a specific action the planner prefers (a biased planner). The paper presents a new optimization problem for social learning that combines dynamic programming with decentralized action choices and Bayesian belief updates. In this setting, the paper proves the convexity of the value function and characterizes the optimal policies of altruistic and biased planners. The characterization reveals that the optimal planner operates in different modes depending on the range of belief values. The modes include investing the maximum allowed resource, not investing any resource, or the investment increasing or decreasing with increase in the belief. Notably, for some ranges of belief the biased planner even intentionally obfuscates the agents’ signals. Even under stringent transparency constraints–information parity with individuals, no lying or cherry-picking, and full observability–the paper shows that information mediation can substantially shift social welfare in either direction. The paper also uses LLMs in simulations, where LLMs act as both planner and agents. The LLM-based planner in simulations exhibits emergent strategic behavior in steering public opinion that broadly mirrors the trends predicted by the model, though key deviations suggest the influence of non-Bayesian reasoning–consistent with the cognitive patterns of both human users and LLMs trained on human-like data.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

The paper provides a novel framework for studying controlled social learning, integrating a dynamic control problem for a centralized information planner with the mechanism of sequential social learning. The framework is complete and can characterize the optimal policies for both altruistic and biased planners as a function of the evolving public belief. The model is also validated by empirical simulations, where LLMs act as both planners and agents. The paper demonstrates that a planner that accounts for social learning can dramatically influence public opinion and social welfare, far more than a myopic one. The paper also shows that the strategic behavior that emerges from the LLM planner largely aligns with the theoretical predictions, suggesting the model is robust to non-Bayesian agent behavior. The paper is well-written and organized.

### Weaknesses

#### Some Related Works


#### comment

The model makes several simplifying assumptions that may limit its realism. For example, it assumes binary states and actions, symmetric signals, and a specific functional form for the cost of precision. The paper does not provide extensive empirical validation of its model using real-world data. The paper does not deeply engage with the literature on the limitations of Bayesian reasoning in both humans and LLMs, which could further contextualize its findings. The theoretical results are mostly qualitative, and the paper does not provide any quantitative or comparative analysis of the performance of the optimal policies or the welfare implications of different planner types. The paper does not discuss the robustness of its results to different parameter values or model specifications. The paper does not explore the implications of its model for the design of information-mediated systems or the potential ethical concerns associated with strategic information control.

### Suggestions

The paper could be strengthened by exploring the impact of relaxing some of its core assumptions. Specifically, the binary state and action space, while simplifying the analysis, may not capture the nuances of real-world social learning scenarios. Investigating the model's behavior with more complex state and action spaces, perhaps through simulations or by considering a continuous approximation, could provide valuable insights. Furthermore, the assumption of symmetric signals is a significant limitation. In many real-world settings, signals are likely to be asymmetric and potentially biased. Analyzing the model's performance under asymmetric signal structures, perhaps by introducing a parameter to control the degree of asymmetry, would enhance the model's applicability. The specific functional form of the cost of precision also warrants further investigation. Exploring alternative cost functions, such as those with non-linearities or step functions, could reveal different optimal policies and provide a more comprehensive understanding of the trade-offs involved in information control.

To enhance the empirical grounding of the work, the authors should consider incorporating real-world data into their validation process. While the LLM-based simulations are a good starting point, they do not fully capture the complexities of human behavior. Conducting experiments with human subjects, where participants interact with an LLM-based planner, would provide a more robust validation of the model's predictions. Furthermore, the paper should delve deeper into the literature on cognitive biases and heuristics, which are known to affect human decision-making. Specifically, the authors should discuss how the model's assumptions about agent rationality might be violated in practice and how these violations could impact the planner's optimal strategies. This would involve a more detailed analysis of the limitations of Bayesian reasoning in both humans and LLMs, and how these limitations might affect the model's predictions. The paper could also benefit from a more thorough discussion of the ethical implications of strategic information control. The authors should consider the potential for manipulation and the ethical guidelines that should govern the use of LLMs as information mediators. This discussion should include a consideration of the potential for bias in the planner's objectives and the impact of these biases on social welfare.

Finally, the paper should provide more quantitative and comparative analysis of the model's results. The current analysis is largely qualitative, focusing on the characterization of optimal policies. The authors should provide more concrete examples of how the optimal policies vary with different parameter values and model specifications. This could involve conducting sensitivity analysis to assess the robustness of the results. Furthermore, the paper should provide a more detailed analysis of the welfare implications of different planner types. This could involve comparing the social welfare achieved under altruistic and biased planners, and analyzing the conditions under which each type of planner is more effective. The paper should also explore the implications of its model for the design of information-mediated systems. This could involve discussing how the model's insights could be used to design more effective and ethical information platforms. The authors should also consider the potential for using their model to develop tools for detecting and mitigating manipulation by biased planners.

### Questions

Can the model be extended to more complex settings, such as those with larger state spaces, more general signal structures, or heterogeneous agents?

How does the model account for the potential for manipulation or deception by the planner?

What are the ethical implications of using LLMs as information mediators in socially-critical functions?

How robust are the findings to different parameter values or model specifications?

### Rating

6

### Confidence

3

**********
### Summary

This paper proposes a reinforcement learning framework for automatic jailbreak strategy exploration, i.e., discovering diverse and effective prompts capable of bypassing the safety restrictions of LLMs. It introduces two key techniques to improve exploration efficiency and attack effectiveness: 1) Dynamic Strategy Pruning, which focuses exploration on high-potential strategies by eliminating highly redundant paths early, and 2) Progressive Reward Tracking, which leverages intermediate downgrade models and a novel First Inverse Rate (FIR) metric to smooth sparse rewards and guide learning. Extensive experiments across diverse white-box and black-box LLM settings demonstrate that AUTO-RT significantly improves success rates (by up to 16.63%), expands vulnerability coverage, and accelerates discovery compared to existing methods.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper introduces a novel reinforcement learning framework for automatic jailbreak strategy exploration, which is a unique approach to discovering diverse and effective prompts capable of bypassing the safety restrictions of LLMs.
2. The paper proposes two key techniques, Dynamic Strategy Pruning and Progressive Reward Tracking, to improve exploration efficiency and attack effectiveness. These techniques are well-motivated and supported by theoretical analysis.
3. The paper conducts extensive experiments across diverse white-box and black-box LLM settings, demonstrating that AUTO-RT significantly improves success rates, expands vulnerability coverage, and accelerates discovery compared to existing methods.
4. The paper is well-written and easy to follow, with clear explanations of the proposed methods and experimental results.

### Weaknesses

#### Some Related Works


#### comment

1. The paper does not provide a detailed analysis of the limitations of the proposed method. For example, the authors do not discuss the potential limitations of the method in terms of the types of attacks that it can defend against, or the potential limitations of the method in terms of the computational resources required to train and deploy the method.
2. The paper does not provide a detailed analysis of the computational resources required to train and deploy the method. For example, the authors do not discuss the time and memory requirements for training the model, or the computational resources required to run the model in real-time.

### Suggestions

The paper should include a more thorough discussion of the limitations of the proposed method, specifically addressing the types of attacks it might be vulnerable to. For instance, the current approach focuses on jailbreak strategies, but it is unclear how well it would generalize to other types of adversarial attacks, such as those designed to elicit specific biased responses or manipulate the model's reasoning. A detailed analysis of the attack space and the method's coverage within that space would be beneficial. Furthermore, the paper should explore the potential for the method to be circumvented by adversarial examples that are specifically crafted to evade the learned jailbreak strategies. This could involve analyzing the robustness of the discovered strategies against perturbations or variations in the input prompts. A discussion of these limitations would provide a more complete picture of the method's capabilities and boundaries.

In addition to the limitations of the attack space, the paper should also provide a more detailed analysis of the computational resources required to train and deploy the method. This should include a breakdown of the time and memory requirements for each stage of the training process, such as the reinforcement learning phase and the strategy pruning phase. The authors should also discuss the scalability of the method to larger models and datasets, as well as the potential for parallelization to reduce training time. Furthermore, the paper should address the computational resources required to run the model in real-time, including the latency and throughput of the method when generating jailbreak prompts. This analysis should consider the practical implications of deploying the method in resource-constrained environments. A clear understanding of the computational costs is crucial for assessing the feasibility of the method in real-world applications.

Finally, the paper should include a more detailed analysis of the sensitivity of the method to different hyperparameters. This should include a discussion of how the choice of hyperparameters affects the performance of the method, as well as guidelines for selecting appropriate values for different scenarios. The authors should also explore the potential for using automated hyperparameter tuning techniques to optimize the performance of the method. A thorough analysis of the hyperparameter sensitivity would provide a more robust and reliable evaluation of the method's performance and its potential for practical use.

### Questions

1. How does the proposed method compare to other state-of-the-art methods in terms of computational resources required for training and deployment?
2. What are the potential limitations of the proposed method in terms of the types of attacks that it can defend against?
3. How does the proposed method perform on different types of datasets and in different domains?
4. How sensitive is the proposed method to the choice of hyperparameters, and how can these hyperparameters be tuned for optimal performance?

### Rating

6

### Confidence

3

**********
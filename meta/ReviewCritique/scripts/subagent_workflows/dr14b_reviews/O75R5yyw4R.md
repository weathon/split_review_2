### Summary

The paper introduces IterRef, a test-time scaling method for discrete diffusion models that uses reward-guided noising-denoising transitions to refine intermediate states. The authors formalize this process within a Multiple-Try Metropolis (MTM) framework, proving convergence to the reward-aligned distribution. The method is evaluated on diverse discrete diffusion models across text and image domains, showing consistent improvements in reward-guided generation quality, especially under low compute budgets.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

* The paper is well-written and easy to follow.
* The proposed method is simple and effective.
* The authors provide a theoretical guarantee for the convergence of the proposed method.
* The authors conduct extensive experiments to demonstrate the effectiveness of the proposed method.

### Weaknesses

#### Some Related Works


#### comment

 * The proposed method requires a large number of function evaluations (NFEs), which may limit its practicality in real-world applications. Specifically, the iterative refinement process, while effective, introduces a significant computational overhead, especially when compared to single-pass methods. The need for multiple denoising steps at each refinement stage compounds this issue, making it potentially unsuitable for time-sensitive or resource-constrained environments.
* The authors only compare their method with a few baselines. It would be better if the authors could compare their method with more baselines to further demonstrate the effectiveness of the proposed method. The current comparison set lacks diversity in terms of both algorithmic approaches and model architectures. For instance, comparisons with methods that employ different sampling strategies or those that are optimized for specific types of diffusion models would provide a more comprehensive evaluation.
* The authors only conduct experiments on a few tasks. It would be better if the authors could conduct experiments on more tasks to further demonstrate the effectiveness of the proposed method. The current evaluation is limited to a narrow set of tasks, which may not fully capture the generalizability of the proposed method. Expanding the evaluation to include tasks with different characteristics, such as those involving different data modalities or requiring different types of reasoning, would provide a more robust assessment.

### Suggestions

To address the high computational cost, the authors should explore techniques to reduce the number of function evaluations (NFEs) required by IterRef. One potential avenue is to investigate adaptive refinement strategies, where the number of refinement steps is dynamically adjusted based on the progress of the generation process. For example, the method could employ a heuristic to determine when the intermediate states have reached a satisfactory level of alignment with the reward function, thus avoiding unnecessary computations. Another approach could involve exploring more efficient sampling techniques within the MTM framework, such as using low-discrepancy sequences or quasi-random number generators to reduce the variance of the estimates and potentially reduce the number of required samples. Furthermore, the authors could investigate the use of knowledge distillation techniques to transfer the learned refinement process to a smaller, more efficient model, thereby reducing the computational overhead without sacrificing performance.

To strengthen the experimental evaluation, the authors should include a more diverse set of baselines, encompassing a wider range of algorithmic approaches and model architectures. This should include methods that employ different sampling strategies, such as those based on stochastic gradient descent or Hamiltonian Monte Carlo, as well as methods that are specifically designed for discrete diffusion models. Additionally, the authors should consider including baselines that are optimized for specific types of diffusion models, such as those that use different noise schedules or those that are tailored for specific data modalities. This would provide a more comprehensive assessment of the proposed method's performance and allow for a more nuanced understanding of its strengths and weaknesses. Furthermore, the authors should provide a detailed analysis of the computational cost of each baseline, including the number of function evaluations and the wall-clock time, to allow for a fair comparison.

To further demonstrate the generalizability of the proposed method, the authors should conduct experiments on a wider range of tasks, including those that involve different data modalities and require different types of reasoning. This should include tasks that involve structured data, such as graphs or tables, as well as tasks that require more complex reasoning, such as question answering or text summarization. Additionally, the authors should consider including tasks that involve different types of reward functions, such as those that are based on different metrics or those that are learned from data. This would provide a more robust assessment of the proposed method's ability to adapt to different task settings and allow for a more comprehensive understanding of its limitations.

### Questions

* Could the authors provide more details on the computational cost of the proposed method compared to the baselines? For example, the authors could provide a table or graph that shows the wall-clock time or the number of function evaluations required by each method.
* Could the authors provide more details on the hyperparameter settings used in the experiments? For example, the authors could provide a table or list that shows the values of all hyperparameters used in the experiments.
* Could the authors provide more details on the potential applications of the proposed method in real-world scenarios? For example, the authors could discuss how the proposed method could be used in applications such as image generation, text generation, or decision-making under uncertainty.

### Rating

6

### Confidence

3

**********
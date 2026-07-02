### Summary

The paper introduces BuilderBench, a benchmark for evaluating generalist agents in open-ended exploration and learning. BuilderBench requires agents to learn how to build structures using blocks, testing their understanding of physics, mathematics, and long-horizon planning. The benchmark includes a hardware-accelerated simulator and a task suite with over 42 diverse target structures. The authors provide single-file implementations of six algorithms as a reference for researchers. The paper argues that BuilderBench can accelerate research towards agents that learn to explore and generalize through interaction with the environment.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

- The paper introduces a novel benchmark, BuilderBench, which is designed to evaluate the exploration, reasoning, and generalization abilities of AI agents. This is a significant contribution to the field of AI research.
- The benchmark is equipped with a hardware-accelerated simulator, which allows for faster training compared to purely CPU-based benchmarks. This is a practical advantage for researchers.
- The task suite is carefully curated to include a wide range of tasks that require different skills, making it a comprehensive benchmark for evaluating AI agents.
- The paper provides single-file implementations of six algorithms, which serves as a reference point for researchers and helps to ensure the reproducibility of the results.
- The paper is well-written and easy to follow, making it accessible to a wide audience.

### Weaknesses

#### Some Related Works


#### comment

 - The paper could benefit from a more detailed discussion of the limitations of the benchmark and potential future directions for research.
- The paper could provide more insights into the types of algorithms that are likely to perform well on the benchmark and why.
- The paper could discuss the potential for using the benchmark to evaluate other types of AI agents, such as those that use different learning paradigms or architectures.

### Suggestions

The paper would benefit from a more thorough discussion of the benchmark's limitations, particularly concerning the scope of reasoning and generalization it can effectively evaluate. While the current tasks cover a range of skills, it's crucial to acknowledge that the block-based environment might not fully capture the complexities of real-world scenarios. For instance, the benchmark could be limited in its ability to assess agents' capacity for dealing with noisy or incomplete sensory information, which is a common challenge in practical applications. Furthermore, the benchmark's reliance on a simulated environment might not fully account for the physical constraints and uncertainties present in real-world robotic manipulation tasks. A more detailed discussion of these limitations would provide a more balanced perspective on the benchmark's utility and guide future research efforts to address these shortcomings. This could include exploring the use of more complex environments, incorporating sensor noise, and evaluating the transferability of learned policies to real-world settings.

To enhance the paper's practical value, it would be beneficial to provide more specific insights into the types of algorithms that are likely to perform well on the benchmark. While the paper includes implementations of several reinforcement learning algorithms, it lacks a detailed analysis of why certain algorithms might be better suited for particular tasks. For example, the paper could discuss the trade-offs between model-free and model-based approaches in the context of the benchmark's tasks. Model-based methods, with their ability to reason about the environment, might be better suited for tasks requiring long-horizon planning, while model-free methods might be more effective for tasks with shorter time horizons. Additionally, the paper could explore the potential of hierarchical reinforcement learning methods, which could decompose complex tasks into simpler sub-tasks, making them more manageable for the agent. A more in-depth analysis of these aspects would provide valuable guidance for researchers seeking to develop effective algorithms for the benchmark.

Finally, the paper should explore the potential of the benchmark to evaluate a wider range of AI agents, including those that use different learning paradigms or architectures. While the current focus is on reinforcement learning, the benchmark could be extended to evaluate agents that use imitation learning, evolutionary algorithms, or other approaches. Furthermore, the paper could discuss the potential of using the benchmark to evaluate agents with different architectures, such as those that use transformers or graph neural networks. This would broaden the benchmark's applicability and make it a more comprehensive tool for evaluating the progress of AI research. The paper could also explore the potential of using the benchmark to evaluate the robustness of AI agents to adversarial attacks or other forms of perturbations, which is an important consideration for real-world applications.

### Questions

- How does the benchmark address the issue of reward shaping and exploration in the context of open-ended learning?
- What are the computational requirements for training and evaluating agents on the benchmark?
- How does the benchmark compare to other existing benchmarks in terms of difficulty and diversity of tasks?
- What are the potential applications of the benchmark beyond evaluating AI agents?

### Rating

6

### Confidence

4

**********
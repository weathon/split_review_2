### Summary

This paper introduces Terminal-Bench, a benchmark for evaluating AI agents on challenging tasks in command-line interfaces. The benchmark consists of 89 tasks across diverse domains, including software engineering, system administration, and data science. The authors evaluate several state-of-the-art agents on the benchmark and provide a detailed analysis of their performance.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The benchmark is carefully designed to be challenging and realistic, with tasks that require agents to demonstrate a wide range of skills.
2. The paper provides a detailed analysis of agent performance, including error analysis and identification of common failure modes.
3. The benchmark is open-sourced and publicly available, allowing other researchers to use and build upon it.

### Weaknesses

#### Some Related Works


#### comment

1. The benchmark may not be sufficiently challenging for the most advanced AI agents, as some tasks may be too easy or too difficult. This could make it difficult to differentiate between the performance of different agents.
2. The benchmark may not be representative of all possible tasks that agents may need to perform in real-world scenarios. For example, it may not include tasks that require agents to interact with other agents or to adapt to changing environments.
3. The benchmark may be biased towards certain types of tasks or domains, which could affect the generalizability of the results.

### Suggestions

To address the issue of task difficulty, the benchmark should incorporate a more granular approach to task complexity. Currently, the tasks are presented as a monolithic set, making it difficult to assess the specific capabilities of agents at different skill levels. A more effective approach would be to categorize tasks based on their inherent difficulty, perhaps using a tiered system (e.g., easy, medium, hard) or by assigning a complexity score to each task based on factors such as the number of steps required, the level of domain knowledge needed, and the degree of reasoning involved. This would allow for a more nuanced evaluation of agent performance and enable researchers to identify specific areas where agents excel or struggle. Furthermore, the benchmark could include a mechanism to dynamically adjust task difficulty based on the agent's performance, allowing for a more personalized and challenging evaluation. This could be achieved by incorporating adaptive algorithms that modify task parameters or introduce additional constraints based on the agent's success rate. Such an approach would not only provide a more accurate assessment of agent capabilities but also help to identify the limits of current AI systems.

To enhance the benchmark's representativeness of real-world scenarios, it should include tasks that involve multi-agent interactions and dynamic environments. Currently, the benchmark focuses primarily on isolated command-line tasks, which may not fully capture the complexities of real-world scenarios where agents need to collaborate with other agents or adapt to changing conditions. For example, the benchmark could include tasks that require agents to coordinate their actions with other agents to achieve a common goal, or tasks that involve adapting to unexpected changes in the environment, such as the introduction of new constraints or the modification of existing ones. This would not only make the benchmark more realistic but also provide a more comprehensive evaluation of agent capabilities in complex, interactive scenarios. Furthermore, the benchmark could incorporate tasks that require agents to learn from their interactions with the environment and other agents, which would be essential for developing more robust and adaptable AI systems.

To mitigate potential biases in the benchmark, a more systematic approach to task selection and validation is needed. Currently, the benchmark appears to be heavily focused on tasks related to software engineering, system administration, and data science, which may not be representative of all possible tasks that agents may need to perform in real-world scenarios. To address this, the benchmark should include a more diverse set of tasks that cover a wider range of domains and task types. This could be achieved by incorporating tasks from other areas such as robotics, natural language processing, and decision-making under uncertainty. Furthermore, the benchmark should be validated by a diverse group of experts from different domains to ensure that it is representative of real-world tasks and does not favor certain types of agents or approaches. This would help to ensure that the benchmark is fair, unbiased, and generalizable to a wide range of applications.

### Questions

1. How do you ensure that the tasks in the benchmark are representative of real-world scenarios and that the benchmark is not biased towards certain types of tasks or domains?
2. How do you plan to keep the benchmark up-to-date with the latest advancements in AI and agent architectures?
3. How do you plan to address the potential limitations of the benchmark, such as the possibility of agents cheating or the difficulty of creating a truly realistic and challenging benchmark?

### Rating

6

### Confidence

3

**********
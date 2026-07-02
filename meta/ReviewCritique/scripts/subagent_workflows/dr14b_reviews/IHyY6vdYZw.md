### Summary

This paper introduces VisualPRM400K, a dataset of 400K multimodal process supervision data, and VisualPRM, a multimodal Process Reward Model (PRM) that estimates the value score of each step in the reasoning process. The authors also construct VisualProcessBench, a benchmark for measuring the abilities of PRMs and MLLMs to detect incorrect steps in multimodal reasoning tasks. The results show that PRMs trained on VisualPRM400K outperform Outcome Reward Models and Self-Consistency during Best-of-N evaluation, and VisualPRM enhances the reasoning performance of various MLLMs across different model scales and families.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper introduces a novel dataset, VisualPRM400K, and a benchmark, VisualProcessBench, which are valuable resources for the research community.
2. The proposed VisualPRM model demonstrates superior performance compared to existing methods, such as Outcome Reward Models and Self-Consistency, in Best-of-N evaluation.
3. The paper provides extensive experimental results, demonstrating the effectiveness of VisualPRM in enhancing the reasoning performance of various MLLMs across different model scales and families.

### Weaknesses

#### Some Related Works


#### comment

1. The paper could benefit from a more detailed discussion of the limitations of the VisualPRM model and potential areas for future research.
2. While the paper presents a comprehensive evaluation, it could include a more in-depth analysis of the cases where VisualPRM does not lead to performance improvements, to better understand its limitations.

### Suggestions

The paper would benefit from a more thorough discussion of the limitations of the VisualPRM model. Specifically, the authors should explore the model's sensitivity to the quality of the input reasoning steps. For instance, how does the model perform when the reasoning process contains subtle errors or inconsistencies that are not explicitly marked as incorrect? A detailed analysis of the model's behavior in such scenarios would provide valuable insights into its robustness and generalizability. Furthermore, the authors should investigate the potential for the model to be biased towards certain types of reasoning patterns or visual features, which could limit its effectiveness in diverse multimodal reasoning tasks. This could involve analyzing the model's performance across different subcategories of the VisualProcessBench benchmark and identifying any systematic biases. Addressing these limitations would strengthen the paper's contribution and provide a more complete picture of the model's capabilities and shortcomings.

In addition to the general limitations, the paper should include a more in-depth analysis of the cases where VisualPRM does not lead to performance improvements. The authors should categorize the types of reasoning tasks or error patterns where VisualPRM struggles, and provide a qualitative analysis of these failure cases. For example, are there specific types of visual reasoning problems or complex logical inferences where the model fails to provide useful feedback? Are there instances where the model's step-wise evaluations are inconsistent with the overall correctness of the reasoning process? A detailed examination of these failure cases would help to identify the boundaries of the model's applicability and guide future research efforts to improve its performance in these challenging scenarios. This analysis should go beyond simply reporting aggregate metrics and delve into the specific reasons behind the model's shortcomings.

Finally, the paper should explore the impact of different training strategies on the performance of VisualPRM. The authors should investigate the effect of varying the size of the training dataset, the diversity of the reasoning steps, and the impact of different optimization algorithms. For example, how does the model's performance change when trained on a smaller subset of VisualPRM400K, or when trained with different data augmentation techniques? Furthermore, the authors should explore the use of techniques such as curriculum learning or adversarial training to improve the model's robustness and generalization ability. A systematic investigation of these factors would provide valuable insights into the model's training dynamics and its potential for further improvement.

### Questions

1. How does the performance of VisualPRM vary across different types of multimodal reasoning tasks, and are there specific tasks where it excels or underperforms?
2. What are the computational requirements for training and deploying VisualPRM, and how do they compare to existing models?
3. How does the size of the VisualPRM400K dataset impact the performance of the trained models, and is there a point of diminishing returns?

### Rating

8

### Confidence

3

**********
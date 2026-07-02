### Summary

This paper addresses the challenge of ensuring safe reasoning in Large Reasoning Models (LRMs), where unsafe intermediate reasoning steps can persist even when the final responses are safe. The authors propose Intervened Preference Optimization (IPO), a method that aligns LRMs towards safe reasoning by substituting unsafe compliance steps with safety triggers and constructing preference learning pairs with strong signals. Experiments on jailbreak and adversarial safety benchmarks demonstrate that IPO significantly improves both reasoning and response safety, outperforming existing baselines with a relative reduction of over 30% in harmfulness, while preserving excellent performance across diverse reasoning tasks.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper addresses a critical and timely issue in the field of AI safety by focusing on the safety of reasoning processes in Large Reasoning Models (LRMs), which is often overlooked in favor of output safety. This focus on reasoning safety is particularly important as LRMs are deployed in more complex and potentially high-stakes applications where unsafe intermediate steps could lead to harmful outcomes even if the final response is safe.

2. The introduction of Intervened Preference Optimization (IPO) is a novel contribution that combines insights from preference learning with safety alignment. The method is innovative in its approach to substituting compliance steps with safety triggers, which is a creative way to enforce safe reasoning paths.

3. The empirical evaluation is comprehensive, covering multiple models and benchmarks, including jailbreak and adversarial safety benchmarks. The results demonstrate a significant improvement in safety, with a relative reduction of over 30% in harmfulness, which is a substantial achievement.

4. The paper provides valuable insights into the characteristics of safe reasoning, identifying critical steps such as safety triggers and compliance cues. These insights are not only theoretically interesting but also practically useful for developing safer LRMs.

### Weaknesses

#### Some Related Works


#### comment

1. The paper's reliance on GPT-4o for identifying compliance cues and safety triggers could introduce biases or inconsistencies, especially if the model's understanding of safety evolves or differs across contexts. This dependency on a single model for critical safety judgments might limit the robustness and generalizability of the proposed method. Specifically, the use of a closed-source model like GPT-4o makes it difficult to assess the consistency of its judgments across different versions or deployments, and the lack of transparency in its decision-making process makes it challenging to debug or improve the system. Furthermore, the paper does not explore the sensitivity of the results to different prompts or configurations used with GPT-4o, which could significantly impact the identified safety triggers and compliance cues.

2. The computational cost of IPO, while claimed to be comparable to other alignment methods, is not thoroughly analyzed. The paper mentions the need for multiple generations to identify safety triggers and compliance cues, but it does not provide a detailed breakdown of the time and resources required for each step. This lack of detailed analysis makes it difficult to assess the practical feasibility of the method, especially for large-scale models or real-time applications. A more rigorous analysis should include the time complexity of each step, the memory requirements, and the impact of different hyperparameter settings on the overall computational cost.

3. The paper could benefit from a more detailed discussion on the limitations of IPO, particularly in scenarios where safety triggers might not be readily available or where the distinction between safe and unsafe reasoning is ambiguous. The current discussion lacks a thorough exploration of edge cases where the method might fail or underperform. For example, the paper does not address how the method would handle situations where the unsafe reasoning is subtle or indirectly harmful, or where the safety triggers are not clearly defined or easily identifiable. A more comprehensive analysis of these limitations would provide a more balanced and realistic assessment of the method's applicability.

### Suggestions

To address the reliance on GPT-4o, the authors should explore alternative methods for identifying compliance cues and safety triggers. This could involve using multiple models, including open-source options, and comparing their performance. Additionally, the authors should investigate the sensitivity of the results to different prompts and configurations used with GPT-4o. A more robust approach would involve a systematic evaluation of the impact of different prompt variations on the identified safety triggers and compliance cues. Furthermore, the authors could explore methods for incorporating human feedback or expert judgment into the process of identifying safety triggers, which could help to mitigate the biases and inconsistencies introduced by relying solely on a single model. This would also enhance the transparency and interpretability of the method.

To improve the analysis of computational cost, the authors should provide a detailed breakdown of the time and resources required for each step of the IPO process. This should include the time complexity of each step, the memory requirements, and the impact of different hyperparameter settings on the overall computational cost. The authors should also compare the computational cost of IPO with other alignment methods, providing a more comprehensive analysis of the trade-offs between safety and computational efficiency. This analysis should include a discussion of the scalability of the method to larger models and datasets, as well as its suitability for real-time applications. Furthermore, the authors should explore potential optimizations to reduce the computational cost of the method, such as using more efficient sampling techniques or parallelizing the computation.

To address the limitations of IPO, the authors should provide a more detailed discussion of scenarios where the method might fail or underperform. This should include an analysis of edge cases where safety triggers are not readily available or where the distinction between safe and unsafe reasoning is ambiguous. The authors should also explore alternative approaches for handling these scenarios, such as using more sophisticated methods for identifying safety triggers or incorporating additional safety mechanisms. Furthermore, the authors should investigate the robustness of the method to adversarial attacks, which could potentially bypass the safety triggers. A more comprehensive analysis of these limitations would provide a more balanced and realistic assessment of the method's applicability and guide future research in this area.

### Questions

1. How does the choice of GPT-4o as the external detector for identifying compliance cues and safety triggers impact the robustness and generalizability of the IPO method? Could alternative models or methods be used to improve the reliability of this detection process?

2. What are the potential limitations of IPO in scenarios where safety triggers are not readily available or where the distinction between safe and unsafe reasoning is ambiguous? How does the method handle such edge cases?

3. How does the computational cost of IPO compare to other alignment methods in more complex or large-scale settings? Are there any optimizations that could be made to improve the efficiency of the method?

### Rating

6

### Confidence

3

**********
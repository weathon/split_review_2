### Summary

The paper investigates data contamination in LLMs within multilingual contexts, specifically examining how contamination manifests when benchmarks are translated into Arabic. The authors fine-tune several open-weight LLMs on varying proportions of Arabic datasets and evaluate them on English benchmarks, using an extended Tested Slot (TS)-Guessing method to detect memorization. Their results show that while translation masks traditional contamination signals, models still benefit from contaminated data, particularly those with stronger Arabic capabilities. To address this, they propose a Translation-Aware Contamination Detection framework, which checks contamination across multiple translated versions of benchmarks. The paper highlights the need for multilingual contamination-aware pipelines to ensure fair and transparent LLM evaluation.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper addresses a critical gap in LLM evaluation by exploring data contamination in a multilingual context, specifically through the lens of Arabic translations. 
2. The proposed Translation-Aware Contamination Detection framework is a practical step towards addressing multilingual contamination, with potential for broad application in LLM evaluation.
3. The paper is well-organized and clearly written, making complex ideas accessible to a broad audience.

### Weaknesses

#### Some Related Works


#### comment

1. The study focuses exclusively on Arabic translations, leaving questions about how contamination dynamics might vary across different language families, resource levels, or translation methods. Specifically, the paper does not explore how the observed contamination effects might differ with languages that have different word orders, morphological structures, or levels of linguistic resources available for translation. This narrow focus limits the generalizability of the findings and raises concerns about the robustness of the proposed framework across diverse linguistic contexts.
2. The framework is proposed at a conceptual level without a full implementation or empirical validation, which may limit its immediate practical utility. The paper lacks concrete details on the specific algorithms or computational resources required for implementation. Without a working prototype or detailed experimental results demonstrating the framework's effectiveness, it is difficult to assess its real-world applicability and scalability. The absence of quantitative metrics for evaluating the framework's performance further hinders its practical evaluation.

### Suggestions

To strengthen the paper, the authors should expand their investigation to include a more diverse set of languages, encompassing different language families and resource levels. This would involve selecting languages with varying linguistic characteristics, such as those with different word orders (e.g., Subject-Object-Verb vs. Subject-Verb-Object) or morphological systems (e.g., fusional vs. agglutinative). Additionally, the study should consider languages with varying levels of translation resources, including both high-resource and low-resource languages. This would provide a more comprehensive understanding of how contamination dynamics are affected by linguistic and resource-related factors. For example, the authors could include languages like French or Spanish, which are well-resourced, and also languages like Swahili or Hindi, which have different linguistic structures and resource availability. This would allow for a more robust analysis of the generalizability of their findings and the effectiveness of their proposed framework.

Furthermore, the authors should provide a more detailed description of the proposed Translation-Aware Contamination Detection framework, including specific algorithms, data structures, and computational requirements. This should include a clear explanation of how the framework handles different translation methods and how it identifies contamination signals across multiple translated versions of benchmarks. A prototype implementation of the framework, along with empirical validation on a range of datasets and models, would significantly enhance the practical utility of the proposed approach. The authors should also define quantitative metrics for evaluating the framework's performance, such as precision, recall, and F1-score, to provide a more objective assessment of its effectiveness. This would allow for a more rigorous evaluation of the framework's ability to detect contamination and its scalability for real-world applications. The authors could also consider comparing their framework with existing contamination detection methods to demonstrate its advantages and limitations.

Finally, the authors should explore the impact of different translation strategies on the observed contamination effects. This could involve comparing the performance of models trained on data translated using different techniques, such as rule-based translation, statistical machine translation, and neural machine translation. The study should also investigate how the choice of translation model affects the detection of contamination signals. For example, the authors could explore the use of different neural machine translation models with varying architectures and training data. This would provide a more nuanced understanding of how translation quality and methodology influence the manifestation of contamination in multilingual contexts. The authors should also consider the potential for translation errors or biases to affect the detection of contamination and propose methods to mitigate these effects.

### Questions

1. How do the authors anticipate their findings and proposed framework would generalize to other low-resource languages with different linguistic structures than Arabic?
2. What are the computational and practical challenges of implementing the TACD framework for large-scale multilingual models, and how might these be addressed?

### Rating

6

### Confidence

4

**********
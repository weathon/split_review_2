### Summary

This paper introduces a benchmark for evaluating text-to-image models in generating images for taxonomy concepts in a zero-shot manner. It assesses 12 models using 9 novel metrics and human feedback, pioneering pairwise evaluation with GPT-4. Results differ from standard tasks, with Playground-v2 and FLUX top-performing. This highlights automation potential for curating structured data resources.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper is well-written and easy to follow.
2. The paper introduces a novel benchmark for evaluating text-to-image models in generating images for taxonomy concepts in a zero-shot manner.
3. The paper assesses 12 models using 9 novel metrics and human feedback, pioneering pairwise evaluation with GPT-4.
4. The paper's findings highlight the potential for automating the curation of structured data resources.

### Weaknesses

#### Some Related Works


#### comment

1. Lack of detailed explanation of the metrics. The paper introduces 9 metrics, but the explanation of each metric is not detailed enough. For example, the paper does not explain how the KL Divergence and Mutual Information are calculated and used in the evaluation process. The paper should provide more details on the calculation process of each metric and the specific formulas used.
2. Limited scope of application scenarios. The paper only focuses on the generation of taxonomy concepts and does not discuss the potential application scenarios of the proposed benchmark in other fields. The paper should discuss the potential application scenarios of the proposed benchmark in other fields, such as e-commerce, education, and so on.
3. The paper does not discuss the potential biases of the proposed benchmark. For example, the paper does not discuss the potential biases of the WordNet dataset used in the evaluation process. The paper should discuss the potential biases of the WordNet dataset and how these biases may affect the evaluation results.
4. The paper does not discuss the limitations of the proposed benchmark. For example, the paper does not discuss the limitations of the proposed benchmark in terms of the types of concepts that can be evaluated. The paper should discuss the limitations of the proposed benchmark and suggest directions for future research.

### Suggestions

The paper should provide a more detailed explanation of the nine metrics used for evaluation. Specifically, for metrics derived from KL Divergence and Mutual Information, the paper should include the exact formulas used, the specific probability distributions being compared, and a clear explanation of how these measures relate to the quality of the generated images. For instance, when using KL Divergence, it is crucial to specify which distribution is considered the 'true' distribution and which is the model's approximation. Furthermore, the paper should clarify how Mutual Information is calculated between the generated image and the taxonomy concept, including the specific features extracted from the images and the method used to estimate the joint and marginal probabilities. Providing concrete examples of how these metrics are calculated for specific cases would greatly enhance the reader's understanding and allow for better reproducibility of the results. The paper should also discuss the sensitivity of these metrics to different types of image variations and how this might affect the overall evaluation.

To broaden the impact of the work, the paper should explore potential applications of the proposed benchmark beyond taxonomy concept generation. For example, in e-commerce, the benchmark could be used to evaluate the ability of text-to-image models to generate product images based on textual descriptions, which could help improve the quality of product listings and enhance user experience. In education, the benchmark could be used to assess the ability of models to generate visual aids for complex concepts, potentially improving learning outcomes. The paper should also consider the potential use of the benchmark in fields like art and design, where the generation of novel and creative images is important. Discussing these potential applications would highlight the versatility of the benchmark and encourage further research in these areas. Furthermore, the paper should discuss the challenges and limitations of applying the benchmark in these new domains, such as the need for domain-specific metrics or the potential for biases in the evaluation process.

Finally, the paper should address the potential biases inherent in the WordNet dataset and the proposed metrics. WordNet, being a human-curated dataset, may contain biases related to culture, language, and the specific perspectives of its contributors. The paper should discuss how these biases might affect the evaluation results, particularly for concepts that are sensitive to cultural or social contexts. For example, the paper should analyze whether the benchmark favors certain types of concepts or images over others due to the inherent structure of WordNet. Additionally, the paper should discuss the potential biases in the metrics themselves, such as whether they are more sensitive to certain types of image variations or whether they favor certain types of models. The paper should also suggest methods for mitigating these biases, such as using more diverse datasets or developing bias-aware evaluation metrics. Addressing these limitations will make the benchmark more robust and reliable for future research.

### Questions

1. Can you provide more details on the nine metrics used for evaluation? Specifically, how are the metrics derived from KL Divergence and Mutual Information calculated and used in the evaluation process?
2. What are the potential application scenarios of the proposed benchmark in other fields? How can the proposed benchmark be used in other fields, such as e-commerce, education, and so on?
3. What are the potential biases of the proposed benchmark? How can these biases be mitigated?
4. What are the limitations of the proposed benchmark? What are the directions for future research?

### Rating

6

### Confidence

3

**********
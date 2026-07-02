### Summary

This paper investigates the characteristics of LLM-generated references by comparing them to human-generated references. The authors use a dataset of 10,000 focal papers with ground truth references and generate reference lists for these papers using GPT-4o and Claude Sonnet 4.5. They construct citation graphs for ground truth, LLM-generated, and random reference lists, and analyze these graphs using various structural and semantic features.

The key findings show that while LLM-generated citation graphs are structurally similar to human-generated ones, they differ significantly in their semantic embeddings. Specifically, the study finds that:
Structural features alone cannot reliably distinguish LLM-generated references from human-generated ones.
Semantic embeddings of titles and abstracts provide a strong signal for distinguishing LLM-generated references.
Graph Neural Networks (GNNs) that incorporate semantic embeddings can effectively differentiate between human and LLM-generated references, achieving high accuracy.

The paper demonstrates that LLMs can mimic the structural properties of human citation networks but leave detectable semantic fingerprints. This suggests that detection and debiasing efforts should focus on content signals rather than global graph structure.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper presents a novel and timely approach to understanding the characteristics of LLM-generated references by comparing their citation graphs to those of human-generated references. This is an important and under-explored area, given the increasing use of LLMs in scientific writing and literature review processes.

2. The methodology is rigorous and well-designed. The authors use a large dataset of 10,000 focal papers and construct paired ground truth and LLM-generated citation graphs. They employ a robust set of structural and semantic features, and use both Random Forest classifiers and Graph Neural Networks to analyze the data. The inclusion of a field-matched random baseline provides a strong control for comparison.

3. The paper is generally clear and well-organized. The authors provide a detailed explanation of their methodology, including the construction of citation graphs, feature extraction, and model training. The results are presented with clear visualizations and statistical analysis.

4. The findings have important implications for the development of tools to detect and mitigate the biases in LLM-generated scientific content. The paper highlights the need to focus on semantic content rather than just structural features for effective detection.

### Weaknesses

#### Some Related Works


#### comment

1. The study focuses on a specific set of LLMs (GPT-4o and Claude Sonnet 4.5) and embedding models (OpenAI text-embedding-3-large and SPECTER2). The generalizability of the findings to other LLMs and embedding models is not fully explored. It is unclear whether the observed patterns would hold for other models with different architectures or training data. For instance, models with different attention mechanisms or pre-training corpora might exhibit different citation behaviors, and this is not addressed.

2. The analysis is limited to title-abstract information for generating citation graphs. The impact of using full-text information, which might provide richer context and more accurate citation recommendations, is not considered. This is a significant limitation because the abstract and title often lack the necessary context for a comprehensive understanding of the paper's contributions and its relationship to other works. The study does not explore how the inclusion of full-text data might alter the structural and semantic properties of the generated citation graphs.

3. The paper does not provide a detailed analysis of the specific types of errors or biases that LLMs introduce in reference generation. While the study shows that semantic embeddings can distinguish LLM-generated references, it does not delve into the nature of these semantic differences. For example, are LLMs more likely to cite papers from specific venues or with certain keywords? Are there systematic biases in the recency or age of the cited papers? A more granular analysis of these error patterns would be beneficial.

### Suggestions

To strengthen the paper, the authors should investigate the generalizability of their findings across a wider range of LLMs and embedding models. This could involve including models with different architectures, training data, and sizes. For example, models like Llama or other open-source alternatives could be included to see if the observed patterns hold. Furthermore, the authors should explore the impact of different embedding models beyond OpenAI's and SPECTER2, such as Sentence-BERT or other domain-specific embeddings. This would help to determine if the observed semantic differences are consistent across various representation spaces. The analysis should also include a discussion of the potential limitations of the chosen models and how these limitations might affect the results.

Additionally, the authors should explore the impact of using full-text information on the generated citation graphs. This could involve comparing the structural and semantic properties of citation graphs generated using only titles and abstracts versus those generated using full-text data. This would provide a more comprehensive understanding of how the availability of different levels of information affects the citation behavior of LLMs. The authors should also consider the computational cost and feasibility of using full-text data, and discuss the trade-offs between accuracy and efficiency. This analysis should also include a discussion of how the use of full-text data might affect the generalizability of the findings, as full-text data may not always be available.

Finally, a more detailed analysis of the specific types of errors and biases introduced by LLMs in reference generation is needed. This could involve examining the citation patterns of LLMs in more detail, looking at the distribution of cited venues, the age of cited papers, and the semantic similarity between cited papers and the focal paper. The authors should also investigate whether LLMs exhibit biases towards certain topics or authors. This analysis should include a discussion of the potential implications of these biases for the scientific community. The authors should also consider how these biases might be mitigated in future work. This could involve developing methods for detecting and correcting biased citation patterns, or for training LLMs to generate more balanced and accurate reference lists.

### Questions

1. How do the findings generalize to other LLMs and embedding models not included in the study? Are there specific characteristics of GPT-4o and Claude Sonnet 4.5 that might influence the results?

2. What is the impact of using full-text information in addition to titles and abstracts on the generated citation graphs? Would this change the structural and semantic properties of the graphs, and how would it affect the ability to distinguish LLM-generated references?

3. What are the specific types of errors or biases that LLMs introduce in reference generation? Are there patterns in the semantic or structural features of the generated references that could provide more insights into the limitations of LLMs in this task?

### Rating

6

### Confidence

3

**********
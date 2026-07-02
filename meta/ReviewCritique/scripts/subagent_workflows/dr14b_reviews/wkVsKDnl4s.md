### Summary

The paper presents a novel approach to metagenomic classification called HighClass, which aims to improve both accuracy and computational efficiency in processing large volumes of sequencing data. The authors introduce several key innovations, including replacing alignment operations with hash-based token mapping, using variable-length tokens, and incorporating quality-aware scoring with learned sensitivity. The paper also provides a rigorous theoretical foundation, including generalization bounds and concentration inequalities under dependent tokens, and demonstrates significant empirical improvements in speed and memory usage compared to state-of-the-art methods.

### Soundness

4

### Presentation

4

### Contribution

4

### Strengths

The paper introduces a novel approach to metagenomic classification that significantly improves computational efficiency while maintaining competitive accuracy. The use of hash-based token mapping and variable-length tokens is a creative solution to the limitations of traditional alignment-based methods. The theoretical framework is comprehensive and well-developed, providing a solid foundation for the proposed method. The empirical results are strong, showing a 4.2x speedup and 68% memory reduction compared to existing methods, which is a substantial achievement. The paper is well-written and clearly explains the technical details and contributions.

### Weaknesses

#### Some Related Works


#### comment

1. The paper primarily evaluates HighClass on the CAMI II benchmark, which, while comprehensive, may not fully capture the method's performance across diverse real-world datasets. Specifically, the CAMI II dataset, while useful for benchmarking, may not fully represent the complexity and variability found in clinical or environmental samples, which often contain a higher prevalence of novel or highly divergent sequences. The lack of evaluation on datasets with different characteristics, such as those with varying read lengths, error rates, or taxonomic distributions, limits the generalizability of the findings.
2. While the paper provides a theoretical framework, some aspects, such as the assumptions underlying the α-mixing analysis, could be explained more intuitively for a broader audience. The current explanation of the α-mixing conditions and their implications for the convergence of token scores is somewhat dense and could benefit from a more accessible explanation. For example, the paper could provide a more concrete example of how the mixing conditions relate to the genomic structure and how violations of these conditions might affect the performance of the method. The paper should also discuss the limitations of the theoretical framework, particularly in scenarios where the assumptions do not hold.
3. The paper could benefit from a more detailed discussion of the computational resources required for training and deploying HighClass, especially in comparison to other methods. While the paper mentions speedup and memory reduction, it lacks a detailed breakdown of the computational costs associated with different stages of the pipeline, such as tokenization, indexing, and classification. A more thorough analysis of the memory footprint and runtime for different dataset sizes and complexities would be beneficial. Furthermore, the paper should discuss the scalability of the method, particularly in the context of large-scale metagenomic datasets.

### Suggestions

To address the limitations in dataset diversity, the authors should include evaluations on a broader range of real-world datasets, particularly those derived from clinical and environmental samples. These datasets should include samples with varying read lengths, error rates, and taxonomic distributions to provide a more comprehensive assessment of the method's robustness and generalizability. Specifically, datasets with a high prevalence of novel or highly divergent sequences would be valuable to test the method's ability to handle unseen genetic material. Furthermore, the authors should consider including datasets with different levels of contamination or noise to evaluate the method's sensitivity to these factors. This would provide a more realistic assessment of the method's performance in practical applications. The inclusion of such datasets would significantly strengthen the paper's claims and demonstrate the method's applicability to a wider range of scenarios.

To improve the clarity of the theoretical framework, the authors should provide a more intuitive explanation of the α-mixing conditions and their implications for the convergence of token scores. This could include concrete examples of how the mixing conditions relate to the genomic structure and how violations of these conditions might affect the performance of the method. For instance, the authors could discuss how the choice of token size and the presence of repetitive elements might influence the mixing properties of the token sequences. Additionally, the paper should include a more detailed discussion of the limitations of the theoretical framework, particularly in scenarios where the assumptions do not hold. This would provide a more balanced and nuanced perspective on the theoretical underpinnings of the method. The authors should also consider providing a more accessible explanation of the mathematical derivations, perhaps through the use of visual aids or simplified examples.

To provide a more comprehensive analysis of the computational resources required for training and deploying HighClass, the authors should include a detailed breakdown of the computational costs associated with different stages of the pipeline, such as tokenization, indexing, and classification. This should include a discussion of the memory footprint and runtime for different dataset sizes and complexities. Furthermore, the paper should discuss the scalability of the method, particularly in the context of large-scale metagenomic datasets. The authors should also compare the computational resource requirements of HighClass with those of other state-of-the-art methods, providing a more detailed analysis of the trade-offs between accuracy, speed, and memory usage. This would allow practitioners to make informed decisions about the suitability of HighClass for their specific needs. The authors should also consider providing guidelines for optimizing the performance of the method on different hardware platforms.

### Questions

1. How does HighClass perform on datasets with highly divergent or novel genetic material not well represented in the reference database? Additional experiments on such datasets would provide a clearer picture of the method's robustness.
2. Could the authors provide more intuitive explanations or examples for some of the theoretical assumptions, such as the α-mixing conditions? This would make the theoretical contributions more accessible to a broader audience.
3. What are the computational resource requirements for training and deploying HighClass, particularly in comparison to other methods? A detailed comparison would help practitioners understand the trade-offs involved.

### Rating

6

### Confidence

3

**********
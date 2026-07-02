### Summary

This paper presents a benchmarking dataset for spatial transcriptomics data. The authors collected 10 spatial transcriptomics datasets, including histology images, spot gene expression, and spatial locations. They also provided downstream task annotations from pathologists. Besides, they reviewed some commonly used methods for batch correction and spatial clustering.

### Soundness

1

### Presentation

1

### Contribution

1

### Strengths

The authors collected 10 public spatial transcriptomics datasets, covering various organs and species.

### Weaknesses

#### Some Related Works


#### comment

1. The novelty of this work is very limited. The authors just downloaded and combined existing datasets without adding any new data or proposing new methods. 
2. The authors did not conduct any batch correction or spatial clustering on the collected datasets. Therefore, it is hard to evaluate the effectiveness of the proposed benchmarking dataset. 
3. The authors did not provide any code for data processing and batch correction. Therefore, it is hard to reproduce their results and further limit the usefulness of this benchmarking dataset.
4. The writing of this paper is poor. Many sentences are too long and hard to understand. The authors should carefully polish their manuscripts.

### Suggestions

The authors should perform a more thorough analysis of the collected datasets to demonstrate the utility of the benchmark. This could include applying several state-of-the-art batch correction methods and spatial clustering algorithms to the data. The results of these analyses should be presented in the paper, including quantitative metrics that assess the performance of each method. For example, the authors could measure the degree of batch effect removal using metrics like iLISI or kBET, and evaluate the quality of spatial clusters using metrics like silhouette scores or spatial correlation coefficients. This would provide a much stronger justification for the benchmark and allow other researchers to compare their methods against a common standard. Without such analysis, the benchmark is essentially just a collection of raw data, which limits its impact and usefulness.

Furthermore, the authors should provide a detailed description of the data processing pipeline used to create the benchmark. This should include all steps from raw data download to the final format provided in the benchmark, including any filtering, normalization, or transformation steps. The authors should also provide the code used for these steps, ideally in a modular and well-documented format. This would ensure that the benchmark is reproducible and that other researchers can easily adapt it to their own needs. The lack of code and detailed processing information makes it difficult to verify the integrity of the data and hinders the ability of other researchers to build upon this work. The authors should also consider providing a tutorial or example scripts that demonstrate how to use the benchmark for common tasks such as batch correction and spatial clustering.

Finally, the authors should significantly improve the writing quality of the manuscript. Many sentences are indeed too long and complex, making them difficult to understand. The authors should break down long sentences into shorter, more digestible units. They should also pay close attention to clarity and conciseness, avoiding jargon and unnecessary technical details. The introduction should clearly motivate the need for the benchmark, and the methods section should provide a detailed description of the data collection and processing steps. The results section should present the analysis of the benchmark in a clear and organized manner, and the discussion should highlight the limitations of the benchmark and suggest directions for future work. A careful revision of the manuscript is necessary to ensure that it is accessible to a wider audience and meets the standards of a scientific publication.

### Questions

See weakness

### Rating

3

### Confidence

5

**********
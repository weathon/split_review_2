### Summary

The paper introduces Blueprint-Bench, a benchmark designed to evaluate the spatial reasoning capabilities of AI models by converting apartment photographs into accurate 2D floor plans. The authors evaluate several LLMs, image generation models, and agent systems on this benchmark. The scoring algorithm measures the similarity between generated and ground-truth floor plans based on room connectivity graphs and size rankings. The results reveal that most models perform at or below a random baseline, while human performance remains substantially superior.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper introduces a new benchmark, Blueprint-Bench, which is designed to evaluate the spatial reasoning capabilities of AI models. This is an important area of research, as spatial reasoning is a fundamental aspect of intelligence that is not well-captured by existing benchmarks.
2. The paper evaluates a wide range of models, including LLMs, image generation models, and agent systems. This provides a comprehensive overview of the current state of AI capabilities in spatial reasoning.
3. The paper provides a detailed description of the dataset, generation process, and evaluation metrics. This makes the results reproducible and allows for future research to build upon the work.

### Weaknesses

#### Some Related Works


#### comment

1. The paper lacks a clear and concise formulation of the problem. The authors should explicitly define the input, output, and the mapping function that represents the model's task. This would greatly improve the clarity and understanding of the paper.
2. The writing quality of the paper is poor, with numerous grammatical errors and typos. This makes the paper difficult to read and understand.
3. The paper does not provide sufficient details about the dataset. The authors should provide more information about the number of samples, the diversity of the dataset, and the data collection process.

### Suggestions

The paper needs a more rigorous definition of the problem being addressed. Currently, the description of the task is somewhat vague, lacking a formal specification of the input space, output space, and the transformation function that the models are expected to learn. For instance, the authors should explicitly define what constitutes a 'photograph of an apartment' (e.g., resolution, perspective, lighting conditions) and what constitutes a '2D floor plan' (e.g., scale, level of detail, coordinate system). Furthermore, the mapping function, which transforms the input photograph into the output floor plan, should be formally defined, even if it is a black-box model. This would involve specifying the domain and codomain of the function, as well as any constraints or assumptions that are imposed on it. Without a clear problem formulation, it is difficult to assess the validity of the benchmark and the significance of the results.

To improve the writing quality, the authors should thoroughly proofread the manuscript to eliminate grammatical errors and typos. The presence of such errors significantly detracts from the credibility of the work and makes it difficult to follow the authors' arguments. Furthermore, the authors should consider using more precise and technical language to describe the methods and results. For example, instead of using vague terms like 'spatial reasoning,' they should specify the particular spatial abilities that are being tested, such as 'depth perception,' 'object recognition,' 'scene understanding,' or 'geometric reasoning.' This would allow for a more nuanced and detailed analysis of the models' performance. The authors should also ensure that the figures and tables are clearly labeled and easy to understand, with sufficient captions and explanations.

Regarding the dataset, the authors should provide a more detailed description of the data collection process, including the source of the photographs, the method used to generate the ground truth floor plans, and any data augmentation techniques that were applied. The authors should also provide a more detailed analysis of the dataset's diversity, including the range of apartment layouts, the number of rooms, the types of furniture, and the lighting conditions. This would allow for a better understanding of the dataset's limitations and the generalizability of the results. Furthermore, the authors should consider releasing a sample of the dataset to allow other researchers to validate the data quality and reproduce the results. The lack of detailed dataset information makes it difficult to assess the benchmark's robustness and fairness.

### Questions

1. Can the authors provide more details about the dataset, including the number of samples, the diversity of the dataset, and the data collection process?
2. Can the authors provide a more detailed analysis of the results, including the performance of different models and the factors that affect their performance?
3. How do the authors plan to address the limitations of the current models and improve their performance on the Blueprint-Bench?

### Rating

5

### Confidence

4

**********
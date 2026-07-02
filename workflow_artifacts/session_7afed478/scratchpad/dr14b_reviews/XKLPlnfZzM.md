### Summary

This paper proposes a diffusion model that first learns to generate spatial marginal distributions over geographical occupancy and then deaggregates them into trajectories. This approach allows for the generation of synthetic trajectories without relying on sample-specific conditions, enabling transferability to new regions.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The proposed Temporal Deaggregation Diffusion Model (TDDM) introduces a novel hierarchical framework that separates spatial occupancy priors from temporal dynamics in trajectory generation. This factorization allows for more scalable and generalizable trajectory generation, which is a significant advancement over existing methods that often require strong sample-specific conditioning.

2. The paper establishes a comprehensive benchmarking framework across three major cities (Beijing, Porto, and San Francisco), providing standardized metrics for fidelity and distributional coverage.

3. The paper is well-written and clearly explains the methodology, experiments, and results.

### Weaknesses

#### Some Related Works


#### comment

1. The model does not explicitly account for temporal dynamics, such as time of day, day of the week, or seasonal variations. This could limit the model's ability to capture real-world variations in mobility patterns.

2. The generalization experiments are limited to the three cities in the study. Testing the model on a more diverse set of cities would provide a stronger validation of its generalization capabilities.

3. The paper does not discuss the computational requirements of TDDM in detail, which could be a barrier to adoption for some users.

### Suggestions

The paper's primary weakness lies in its limited consideration of temporal dynamics. While the model captures spatial occupancy and temporal movement, it overlooks crucial temporal patterns such as time of day, day of the week, and seasonal variations. These patterns significantly influence human mobility, and their absence could lead to unrealistic trajectory generation. For instance, the model might generate similar traffic patterns during peak hours and off-peak hours, which is not representative of real-world scenarios. To address this, the authors should explore incorporating temporal embeddings or conditioning variables that capture these variations. This could involve adding time-based features to the input of the diffusion model or using a conditional diffusion model that generates trajectories based on specific time indicators. Furthermore, the evaluation metrics should be expanded to include measures that specifically assess the model's ability to capture these temporal patterns, such as comparing the distribution of trajectories generated at different times of the day with the real data.

Another area for improvement is the generalization capability of the model. While the authors demonstrate generalization across three cities, this is insufficient to validate the model's robustness across diverse urban environments. The three cities might share similar urban characteristics, and the model's performance might degrade in cities with different road network structures, population densities, or mobility patterns. To address this, the authors should evaluate the model on a more diverse set of cities, including cities with different geographical locations, sizes, and urban planning styles. This would provide a more comprehensive understanding of the model's generalization capabilities and identify potential limitations. Additionally, the authors should investigate the impact of city-specific factors on the model's performance and explore techniques to mitigate these effects, such as domain adaptation or meta-learning.

Finally, the paper lacks a detailed discussion of the computational requirements of TDDM. This is a critical aspect for practical adoption, as the computational cost of training and inference can be a significant barrier for users with limited resources. The authors should provide a detailed analysis of the model's computational complexity, including the number of parameters, training time, and inference time. They should also investigate techniques to reduce the computational cost, such as model compression or quantization. Furthermore, the authors should provide guidelines on the hardware requirements for training and inference, such as the recommended GPU memory and CPU specifications. This would enable potential users to assess the feasibility of using TDDM in their specific contexts and facilitate the practical adoption of the model.

### Questions

1. Could the authors provide more details on the computational requirements for training and using TDDM? This information would be valuable for potential users with limited computational resources.

2. How does TDDM handle variations in data quality or availability across different regions? Could the authors provide more insights into the model's robustness in such scenarios?

3. Are there plans to extend the model to incorporate additional temporal dynamics, such as time of day, day of the week, or seasonal variations? This could significantly enhance the model's applicability to real-world scenarios.

### Rating

6

### Confidence

3

**********
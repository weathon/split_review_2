### Summary

This paper addresses the task of online map-based motion prediction for autonomous driving. The authors identify several issues with the current protocol, including inappropriate dataset splits, different ranges for online mapping and motion prediction, and non-discriminative metrics. To address these issues, they propose a new benchmark called OMMP-Bench, which includes a new data partition, refined metrics, and a boundary-free baseline. The authors evaluate several existing methods on OMMP-Bench and provide insights into the effect of map element selection on motion prediction models.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper identifies several critical issues with the existing online map-based motion prediction protocol, which have been overlooked in previous work.
2. The proposed new data partition and evaluation metrics are reasonable and can provide a more accurate assessment of model performance.
3. The analysis of different map element selections provides valuable insights for the design of online mapping and motion prediction models.

### Weaknesses

#### Some Related Works


#### comment

1. The proposed boundary-free baseline is relatively simple and may not be competitive with more sophisticated methods. The baseline's simplicity, while useful for establishing a lower bound, might not fully explore the potential of integrating image features with map data. Specifically, the method of aggregating image features around agents could be improved by incorporating more advanced techniques such as attention mechanisms or graph neural networks to better capture spatial relationships and contextual information. This could lead to a more robust and competitive baseline.
2. The analysis of map element selection is limited to a few types and could be expanded to include more types and combinations. The current analysis focuses on a limited set of map elements, such as lane boundaries and centerlines. However, other crucial map elements like pedestrian crossings, traffic signs, and road markings could significantly impact motion prediction. A more comprehensive analysis should explore the influence of these additional elements, both individually and in combination, to provide a more complete understanding of their contribution to the motion prediction task. Furthermore, the interaction between different map elements should also be considered.

### Suggestions

To address the limitations of the boundary-free baseline, future work should explore more sophisticated methods for integrating image features with map data. Instead of simply aggregating image features around agents, techniques like attention mechanisms could be employed to allow the model to focus on the most relevant visual information. For instance, a transformer-based architecture could be used to process image features and map elements jointly, enabling the model to learn complex relationships between them. Additionally, graph neural networks could be utilized to model the spatial relationships between agents and map elements, allowing for a more nuanced understanding of the scene. This would not only improve the performance of the baseline but also provide a more robust comparison point for evaluating more complex models. Furthermore, the baseline should be evaluated on a wider range of scenarios, including those with occlusions and varying lighting conditions, to ensure its robustness.

Expanding the analysis of map element selection is crucial for a more comprehensive understanding of their impact on motion prediction. Future studies should include a broader range of map elements, such as pedestrian crossings, traffic lights, stop signs, and different types of road markings. The analysis should not only consider the individual impact of each element but also explore their interactions. For example, the combination of lane boundaries and traffic lights might provide more informative context than either element alone. This could be achieved by systematically adding or removing different map elements and evaluating the resulting performance. Furthermore, the analysis should consider the impact of map element accuracy and completeness on motion prediction. This could involve introducing noise or missing elements in the map data and observing the effect on the prediction performance. Such an analysis would provide valuable insights into the robustness of motion prediction models to map imperfections.

Finally, the evaluation metrics should be further refined to better capture the nuances of motion prediction. While the current metrics provide a reasonable assessment of performance, they could be augmented with metrics that specifically measure the accuracy of predicted trajectories in different scenarios. For example, metrics that focus on the prediction of sharp turns or interactions with other agents could be included. Additionally, the evaluation should consider the uncertainty of the predictions, providing a more complete picture of the model's capabilities. This could involve using probabilistic prediction models and evaluating the quality of the predicted probability distributions. By incorporating these more sophisticated metrics, the benchmark can provide a more comprehensive and informative assessment of motion prediction models.

### Questions

Please refer to the weakness part.

### Rating

6

### Confidence

3

**********
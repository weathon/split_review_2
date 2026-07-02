### Summary

This paper introduces SpookyBench, a benchmark designed to evaluate the temporal reasoning capabilities of video-language models (VLMs). The authors highlight that while VLMs have made significant progress in understanding spatio-temporal relationships in videos, they struggle when spatial information is obscured, relying heavily on frame-level spatial features. SpookyBench presents a unique challenge by encoding information solely in temporal sequences of noise-like frames, mirroring natural phenomena where temporal patterns carry crucial information. The benchmark reveals a significant performance gap between humans and state-of-the-art VLMs, with humans achieving over 98% accuracy while VLMs score 0%. This underscores the need for novel architectures or training paradigms that decouple spatial dependencies from temporal processing to enhance temporal pattern recognition in VLMs.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper introduces SpookyBench, a novel benchmark designed to evaluate the temporal reasoning capabilities of video-language models (VLMs) by isolating temporal information from spatial cues. This is a significant contribution as it addresses a critical gap in existing benchmarks, which often evaluate spatio-temporal understanding together. The benchmark's focus on purely temporal patterns is innovative and highlights a previously underexplored aspect of VLM performance.

2. The paper provides a thorough analysis of the performance gap between humans and state-of-the-art VLMs on SpookyBench. The authors demonstrate that this gap persists across various model architectures, scales, and training strategies, indicating a fundamental limitation in current approaches. This systematic analysis is valuable for the research community as it clearly identifies the need for new methods to address temporal reasoning.

3. The paper is well-structured and clearly written, making it accessible to a broad audience. The introduction effectively sets the stage by discussing the limitations of current VLMs in temporal reasoning. The methodology section provides a detailed explanation of the benchmark design, and the results are presented in a clear and concise manner. The discussion section offers insightful interpretations of the findings and suggests potential directions for future research.

4. The paper's findings have significant implications for the development of VLMs. By highlighting the "time blindness" of current models, the authors underscore the need for novel architectures or training paradigms that can effectively process temporal information independently of spatial cues. This could inspire a new wave of research focused on improving temporal pattern recognition in VLMs, potentially leading to more robust and versatile models.

### Weaknesses

#### Some Related Works


#### comment

1. The paper identifies a critical limitation in current VLMs' ability to process temporal information independently of spatial cues but does not propose any concrete solutions or directions for addressing this issue. While the benchmark is valuable for highlighting the problem, the lack of constructive insights or potential solutions limits the paper's impact on advancing the field. The paper would be significantly strengthened by including a discussion of potential architectural changes, training strategies, or data augmentation techniques that could improve temporal reasoning capabilities in VLMs. For example, the authors could explore the use of recurrent neural networks or temporal convolutional networks, which are specifically designed to capture temporal dependencies, or discuss the potential of incorporating attention mechanisms that focus on temporal relationships rather than spatial features.

2. The paper lacks a detailed analysis of why current models fail on SpookyBench. While the authors demonstrate the failure modes (e.g., attempting to extract information from individual frames), they do not provide a deep dive into the underlying mechanisms that cause this failure. A more thorough investigation into the model architectures and training processes could reveal specific bottlenecks or biases that contribute to the observed time blindness. For instance, the authors could analyze the activation patterns of different layers in the VLMs when processing SpookyBench videos to identify which parts of the network are most active and whether they are capturing any temporal information. Furthermore, an analysis of the gradients during training could reveal if the models are even learning to attend to temporal information, or if the training process is primarily focused on spatial features.

3. The paper does not explore the potential trade-offs between spatial and temporal processing in VLMs. It is possible that the current architectures are optimized for spatial understanding at the expense of temporal reasoning, or vice versa. A discussion of this trade-off and potential ways to balance spatial and temporal processing would provide a more nuanced understanding of the problem. The authors could investigate whether models trained with a greater emphasis on temporal information, perhaps through a modified loss function or data augmentation, would perform better on SpookyBench, even if it comes at a slight cost to spatial reasoning performance. This would help to understand the inherent limitations of current architectures and the potential for improvement.

### Suggestions

To enhance the paper's contribution, the authors should explore potential solutions to the identified limitations. This could involve proposing modifications to existing VLM architectures, such as incorporating recurrent layers or temporal attention mechanisms, to better capture temporal dependencies. Furthermore, the authors could investigate novel training strategies, such as curriculum learning or adversarial training, that specifically target temporal reasoning abilities. For example, they could design a curriculum that gradually increases the complexity of temporal patterns in the training data, or use adversarial examples to force the model to learn more robust temporal representations. Additionally, exploring data augmentation techniques that emphasize temporal variations, such as time warping or frame shuffling, could help improve the model's ability to generalize to unseen temporal patterns. These explorations would provide valuable insights into how to overcome the current limitations of VLMs and move towards more robust temporal understanding.

In addition to proposing solutions, the authors should conduct a more in-depth analysis of why current models fail on SpookyBench. This could involve analyzing the internal representations of the models when processing SpookyBench videos, using techniques such as activation visualization or feature attribution. This would help to identify which parts of the network are most active and whether they are capturing any temporal information. Furthermore, the authors could investigate the impact of different architectural choices on temporal reasoning performance, such as the type of temporal pooling or the use of attention mechanisms. A detailed analysis of the model's failure modes could reveal specific bottlenecks or biases that contribute to the observed time blindness. For example, the authors could analyze the gradients during training to see if the models are even learning to attend to temporal information, or if the training process is primarily focused on spatial features. This deeper understanding of the underlying mechanisms would be crucial for developing effective solutions.

Finally, the authors should explore the potential trade-offs between spatial and temporal processing in VLMs. This could involve training models with different emphases on spatial and temporal information and evaluating their performance on both SpookyBench and traditional benchmarks. This would help to understand whether the current architectures are inherently biased towards spatial understanding and whether it is possible to achieve a better balance between spatial and temporal processing. The authors could also investigate whether models trained with a greater emphasis on temporal information, perhaps through a modified loss function or data augmentation, would perform better on SpookyBench, even if it comes at a slight cost to spatial reasoning performance. This would provide a more nuanced understanding of the problem and help to guide the development of more robust and versatile VLMs.

### Questions

1. Can the authors provide more insights into why current models fail on SpookyBench? What specific aspects of the architectures or training processes contribute to this limitation?
2. Are there any preliminary ideas or suggestions for addressing the identified limitations in temporal reasoning? What potential directions could future research take to overcome this challenge?

### Rating

6

### Confidence

3

**********
### Summary

This paper proposes a new framework for text-to-motion generation that focuses on generating physically consistent motions. The authors introduce a new dataset, Motion2Motion, which contains text-motion pairs with latent intent annotations. They also propose a new optimization method, ERA-CoT, to improve the reasoning capabilities of the model. The authors demonstrate that their method outperforms several baselines on a variety of metrics.

### Soundness

2

### Presentation

2

### Contribution

2

### Strengths

1. The authors propose a new dataset, Motion2Motion, which is a valuable contribution to the field of text-to-motion generation. The dataset contains text-motion pairs with latent intent annotations, which can be used to train models that generate physically consistent motions.

2. The authors propose a new optimization method, ERA-CoT, which improves the reasoning capabilities of the model. The method is based on reinforcement learning and uses a combination of rewards to encourage the model to generate motions that are physically consistent and semantically coherent.

### Weaknesses

#### Some Related Works


#### comment

1. The authors claim that their method generates physically consistent motions, but they do not provide any quantitative evaluation of the physical plausibility of the generated motions. It is important to evaluate the physical plausibility of the generated motions using metrics such as joint angle limits, ground contact forces, and center of mass stability. Without such evaluation, the claim of physical consistency cannot be fully substantiated.

2. The authors compare their method to several baselines, but they do not compare it to any state-of-the-art text-to-motion generation methods. It is important to compare the proposed method to the most recent and advanced methods in the field to demonstrate its superiority. The lack of comparison to methods that explicitly model physics or use similar reasoning approaches makes it difficult to assess the true advancement of this work.

3. The authors do not provide any qualitative evaluation of the generated motions. It is important to provide visualizations of the generated motions to allow readers to assess the quality of the motions. The absence of visual examples makes it hard to judge the practical relevance of the generated motions and their adherence to the text descriptions.

### Suggestions

To strengthen the evaluation of physical plausibility, the authors should incorporate metrics that directly assess the biomechanical feasibility of the generated motions. Specifically, they should measure joint angle velocities and accelerations to ensure that the generated motions are not only within joint limits but also dynamically realistic. Furthermore, analyzing the ground reaction forces and their distribution can provide insights into the stability and balance of the generated motions. These metrics should be compared against established thresholds or empirical data from real human motion capture to provide a clear benchmark for physical plausibility. Additionally, the authors could consider using a physics engine to simulate the generated motions and evaluate the resulting forces and torques on the joints, which would provide a more comprehensive assessment of the physical consistency of the motions.

To better contextualize the performance of the proposed method, the authors should compare it against state-of-the-art text-to-motion generation methods that explicitly model physics or use similar reasoning approaches. This would involve not only comparing the quantitative metrics but also analyzing the qualitative aspects of the generated motions. For example, the authors could compare their method to approaches that use physics-based simulators or those that incorporate explicit constraints on joint angles and velocities. This comparison should highlight the specific advantages and disadvantages of the proposed method in relation to existing techniques. Furthermore, the authors should consider comparing their method to approaches that use different types of motion representations, such as those based on quaternions or rotation matrices, to assess the impact of the motion representation on the quality of the generated motions.

Finally, the authors should provide a more thorough qualitative evaluation of the generated motions. This should include visualizations of the motions from multiple viewpoints, as well as comparisons to the ground truth motions (if available). The visualizations should clearly demonstrate the diversity and naturalness of the generated motions, as well as their adherence to the text descriptions. The authors should also provide a detailed analysis of the failure cases of their method, highlighting the types of motions that are difficult to generate and the reasons for these failures. This analysis should provide insights into the limitations of the proposed method and suggest directions for future research. Furthermore, the authors could consider conducting a user study to assess the perceived quality and realism of the generated motions, which would provide a more subjective evaluation of the method's performance.

### Questions

1. How does the proposed method compare to state-of-the-art text-to-motion generation methods in terms of physical plausibility and semantic coherence?

2. What are the limitations of the proposed method, and what are the directions for future research?

### Rating

3

### Confidence

4

**********
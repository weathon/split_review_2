### Summary

This paper presents a method for generating grasps for dexterous hands with a single demonstration. The method formulates this task as a single-step MDP and uses RL to optimize a policy for editing the action spaces (wrist pose and hand joint angles) of the demonstration. The policy can be trained in a matter of hours and can be used to grasp an object in novel configurations, using a simple reward function. The method is also extended to a vision-based policy using imitation learning. The proposed method achieves SOTA performance in simulation and real-world experiments.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

- The paper is well written and easy to follow
- The proposed method is simple but effective. It achieves SOTA performance in simulation and real-world experiments
- The authors provide thorough implementation details and the code is available for reproducibility
- The authors perform thorough experiments to evaluate the method in simulation and the real-world, including different embodiments, different objects, different camera configurations, etc.

### Weaknesses

#### Some Related Works


#### comment

 - The method assumes that the object model is available. This assumption might be problematic in real-world applications, where object models are not always accessible. The reliance on a full object point cloud, even with a RGBD camera, limits the method's applicability in scenarios with complex occlusions or highly reflective surfaces, which can degrade point cloud quality. Furthermore, the method does not address how it would handle partial observations or noisy point clouds, which are common in real-world settings.
- The method is limited to grasping objects that are already known by the robot. It would be interesting to see how this method can be extended to grasp novel objects without requiring to train the policy. The method's reliance on a pre-trained policy limits its ability to generalize to objects with significantly different geometries or material properties than those seen during training. The lack of a mechanism for adapting to new object characteristics is a significant limitation for real-world deployment where a vast array of objects may be encountered.

### Suggestions

The paper could benefit from a more detailed discussion on how the method would handle situations where the object model is not perfectly captured, which is a common occurrence in real-world scenarios. For example, the authors could explore the impact of noisy or incomplete point clouds on the performance of the grasp policy. This could involve experiments where the input point cloud is corrupted by adding noise or by removing parts of the object model. Furthermore, the authors could investigate methods for robustifying the policy to handle such uncertainties, such as incorporating techniques from robust perception or learning-based approaches that can handle partial observations. This would significantly improve the practical applicability of the proposed method.

To address the limitation of grasping only known objects, the authors could explore incorporating techniques that allow for better generalization to novel objects. This could involve using a more expressive representation of the object's geometry, such as a learned latent space, that can capture a wider range of object shapes. Additionally, the authors could investigate methods for adapting the policy to new objects, such as using meta-learning or few-shot learning techniques. This would allow the policy to quickly learn how to grasp new objects with minimal training data. Another approach could be to incorporate a module that can predict suitable grasp points based on the object's geometry, which could then be used to guide the grasp policy. This would allow the method to handle objects that are significantly different from those seen during training.

Finally, the paper should include a more thorough analysis of the computational cost of the method, particularly the time required to generate a grasp for a new object. While the method is presented as being fast, a more detailed breakdown of the computational steps would be beneficial. This should include the time required for processing the object point cloud, computing the editing parameters, and executing the grasp. Furthermore, the authors should discuss how the computational cost scales with the complexity of the object model and the number of fingers on the dexterous hand. This analysis would provide a better understanding of the method's limitations and its suitability for real-time applications.

### Questions

- What is the runtime of the method? How long does it take to grasp a new object?

### Rating

6

### Confidence

4

**********
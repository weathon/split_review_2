### Summary

This paper introduces a 3D multi-modal representation learning framework for robot manipulation. The authors enhance the DROID dataset with high-quality depth maps and point clouds, constructing DROID-3D as a valuable supplement for 3D embodied vision research. The proposed EmbodiedMAE model learns representations across RGB, depth, and point cloud modalities through stochastic masking and cross-modal fusion. The model is evaluated on 70 simulation tasks and 20 real-world robot manipulation tasks, demonstrating superior performance compared to state-of-the-art vision foundation models.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper is well-written and easy to follow.
2. The proposed method is technically sound and innovative.
3. The experiments are comprehensive and convincing.

### Weaknesses

#### Some Related Works


#### comment

1. The proposed method is evaluated only on one real-world robot. It would be better to evaluate the proposed method on more robots to show the generalization of the proposed method.
2. The proposed method is evaluated only on the RDT policy. It would be better to evaluate the proposed method on different policies to show the generalization of the proposed method.
3. The proposed method is evaluated only on the LIBERO and MetaWorld benchmarks. It would be better to evaluate the proposed method on more benchmarks to show the generalization of the proposed method.

### Suggestions

The paper would benefit from a more thorough evaluation of the proposed method's generalization capabilities. Specifically, the current real-world experiments are limited to a single robot platform. To demonstrate the robustness of the approach, it is crucial to evaluate the method on a diverse set of robotic systems, including robots with different kinematic structures, sensor configurations, and actuation capabilities. This would provide a more comprehensive understanding of the method's ability to adapt to varying real-world scenarios. For example, testing on both arm and mobile robots, or robots with different end-effectors, would be valuable. Furthermore, the evaluation should include a detailed analysis of the performance variations across these different platforms, highlighting any specific challenges or limitations encountered.

In addition to expanding the range of robots, the evaluation should also consider a wider variety of policy learning algorithms. The current evaluation focuses solely on the RDT policy, which may not be representative of all policy learning approaches. To ensure the general applicability of the proposed method, it is important to evaluate its performance with other policy learning algorithms, such as those based on reinforcement learning or imitation learning. This would help to determine whether the method's benefits are specific to the RDT policy or if they generalize to other policy learning paradigms. For instance, evaluating the method with a model-based RL algorithm or a different imitation learning algorithm could reveal potential interactions between the representation learning and the policy learning process. This would provide a more complete picture of the method's strengths and weaknesses.

Finally, the evaluation should be extended to include a broader range of manipulation benchmarks. While LIBERO and MetaWorld are valuable benchmarks, they do not cover the full spectrum of manipulation tasks. To further validate the generalization capabilities of the proposed method, it should be evaluated on additional benchmarks that include more complex and diverse tasks, such as those involving deformable objects, multi-step manipulation, or tasks that require more intricate reasoning about object affordances. This would provide a more comprehensive assessment of the method's ability to handle a wide range of manipulation challenges. For example, including benchmarks that involve tasks like tool use or collaborative manipulation could further demonstrate the method's versatility and potential for real-world applications.

### Questions

1. How does the proposed method perform on other types of robots, such as mobile robots or robots with different kinematic structures?
2. How does the proposed method perform with different policy learning algorithms, such as reinforcement learning or imitation learning?
3. How does the proposed method perform on other manipulation benchmarks that involve more complex and diverse tasks?

### Rating

6

### Confidence

3

**********
### Summary

This paper introduces FEDSGM, a unified framework for federated constrained optimization that addresses four major challenges in federated learning (FL): functional constraints, communication bottlenecks, local updates, and partial client participation. FEDSGM extends the projection-free, primal-only concept of the switching gradient method (SGM) to FL with convex functional constraints, avoids dual-variable tuning and inner solves. FEDSGM incorporates bidirectional error feedback to correct bias introduced by compression. FEDSGM allows multiple local steps and partial client participation. Additionally, FEDSGM employs soft switching to stabilize updates near the feasibility boundary. The authors validate the theoretical guarantees of FEDSGM via experimentation on Neyman–Pearson classification and constrained Markov decision process (CMDP) tasks.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

- The paper is well-written and easy to follow.
- The paper presents a unified framework that addresses multiple challenges in federated learning, which is a significant contribution to the field.
- The convergence guarantees provided in the paper are theoretically sound and well-supported.

### Weaknesses

#### Some Related Works


#### comment

 - The experiments could be more comprehensive, including comparisons with a wider range of existing methods and more diverse datasets.

### Suggestions

The paper would benefit from a more thorough experimental evaluation. Specifically, the authors should compare their method against a broader range of state-of-the-art federated learning algorithms, particularly those designed for constrained optimization. For instance, methods that utilize projection-based approaches or those that incorporate dual variable updates should be included as baselines. Furthermore, the current experiments are limited to two specific tasks: Neyman-Pearson classification and constrained Markov decision processes. While these are relevant, the authors should expand their evaluation to include other datasets and tasks that are commonly used in the federated learning literature, such as federated image classification or natural language processing tasks. This would provide a more robust assessment of the proposed method's performance and generalizability. The experimental section should also include a more detailed analysis of the impact of different hyperparameter settings on the performance of FEDSGM, such as the local update frequency, the compression ratio, and the partial client participation rate. This analysis would help in understanding the sensitivity of the method to these parameters and provide practical guidance for users.

Furthermore, the paper should provide more details on the implementation of the soft switching mechanism. While the authors mention that it helps stabilize updates near the feasibility boundary, a more in-depth explanation of how this mechanism works and its impact on the convergence behavior would be beneficial. For example, it would be useful to see a visualization of how the switching parameter changes over time and how it affects the objective and constraint violation. The authors should also discuss the computational overhead of the soft switching mechanism and how it compares to other methods. In addition, the paper should include a more detailed discussion of the limitations of the proposed method. For example, the authors should discuss the assumptions made in the theoretical analysis and how they might affect the practical performance of the method. The authors should also discuss the potential challenges in applying FEDSGM to real-world federated learning scenarios, such as dealing with heterogeneous data distributions and communication delays.

Finally, the paper should provide a more detailed analysis of the convergence behavior of FEDSGM under different conditions. For example, the authors should investigate how the convergence rate is affected by the choice of the local update frequency, the compression ratio, and the partial client participation rate. The authors should also provide a more detailed comparison of the convergence behavior of FEDSGM with other methods, particularly in terms of the trade-off between convergence speed and constraint satisfaction. The paper should also include a more detailed discussion of the practical implications of the theoretical results. For example, the authors should discuss how the theoretical convergence guarantees translate into practical performance and how they can be used to guide the design of federated learning systems. The authors should also provide a more detailed discussion of the potential benefits and drawbacks of using FEDSGM in different federated learning scenarios.

### Questions

- Can the authors provide more details on how FEDSGM compares to other state-of-the-art methods in constrained federated learning?
- How sensitive is FEDSGM to the choice of hyperparameters, such as the local update frequency, the compression ratio, and the partial client participation rate?

### Rating

6

### Confidence

3

**********
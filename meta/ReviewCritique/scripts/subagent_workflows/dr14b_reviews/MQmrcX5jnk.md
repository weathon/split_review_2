### Summary

The paper proposes a new method for training normalizing flows to sample Boltzmann distributions. The method works by defining a sequence of intermediate distributions that interpolate between a tractable initial distribution and the target distribution. The paper considers three types of annealing paths: geometric, tempered, and geometric-tempered. The geometric-tempered path combines the benefits of both geometric and tempered paths, avoiding mode collapse and mass teleportation. The paper demonstrates the effectiveness of the proposed method on several molecular systems, including alanine dipeptide, alanine tetrapeptide, alanine hexapeptide, and ELIL tetrapeptide.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

- The paper is well-written and easy to follow.
- The proposed method is well-motivated and theoretically sound.
- The paper provides a comprehensive experimental evaluation of the proposed method on several molecular systems.
- The paper compares the proposed method to several baselines, including forward KL, reverse KL, FAB, and TA-BG.
- The paper introduces a new benchmark, the ELIL tetrapeptide, which is the largest system studied to date without access to samples from molecular dynamics.

### Weaknesses

#### Some Related Works


#### comment

 - The paper does not provide a detailed analysis of the computational cost of the proposed method. It would be helpful to compare the computational cost of the proposed method to the baselines, especially for larger systems.


### Suggestions

The paper would benefit from a more thorough investigation into the computational demands of the proposed method, particularly in comparison to existing approaches. While the paper mentions the number of target evaluations, a more detailed breakdown of the computational time spent on different stages of the algorithm would be valuable. For instance, the time required for sampling from intermediate distributions, computing the loss function, and updating the model parameters should be analyzed. This analysis should also consider the scaling of computational cost with the size of the system, as the overhead of the constrained mass transport framework might become more significant for larger molecules. Furthermore, it would be beneficial to compare the computational cost of the proposed method with the baselines, not only in terms of total time but also in terms of memory usage and the number of gradient updates required. This would provide a more complete picture of the practical efficiency of the proposed method.

To further strengthen the paper, a more detailed discussion of the limitations of the proposed method would be beneficial. While the paper demonstrates the effectiveness of the method on several molecular systems, it would be valuable to explore the scenarios where the method might struggle. For example, it would be interesting to investigate the performance of the method on systems with highly complex energy landscapes or with a large number of degrees of freedom. Additionally, the paper could discuss the sensitivity of the method to the choice of hyperparameters, such as the number of intermediate distributions and the learning rate. A more thorough analysis of these limitations would provide a more balanced view of the proposed method and help guide future research.

Finally, the paper could benefit from a more in-depth analysis of the impact of the trust-region bound on the performance of the method. While the paper mentions that the trust-region bound controls the variance of the importance weights, it would be helpful to provide a more detailed analysis of how this bound affects the convergence of the algorithm and the quality of the generated samples. For example, the paper could investigate the effect of different trust-region bounds on the effective sample size and the total variation distance to the target distribution. This analysis could provide valuable insights into the optimal choice of the trust-region bound and help improve the performance of the method.

### Questions

- How does the computational cost of the proposed method compare to the baselines, especially for larger systems?
- What are the limitations of the proposed method?
- How does the choice of the trust-region bound affect the performance of the method?

### Rating

6

### Confidence

3

**********
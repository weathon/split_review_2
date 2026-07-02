### Summary

This paper proposes a plug-and-play alternating direction method of multipliers (ADMM-PnP) framework for solving inverse problems with score-based generative models. The key contribution is a novel denoiser called AC-DC, which addresses the mismatch between the geometry of ADMM iterates and the noisy data manifolds used to train score functions. The AC-DC denoiser consists of three stages: auto-correction (AC) via additive Gaussian noise, directional correction (DC) using conditional Langevin dynamics, and score-based denoising. The authors provide theoretical convergence guarantees for the proposed method under certain conditions and demonstrate its effectiveness on various inverse problems, including inpainting, deblurring, and phase retrieval.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper introduces a novel AC-DC denoiser that effectively addresses the manifold mismatch issue in score-based PnP methods. The combination of auto-correction, directional correction, and score-based denoising is a creative solution that balances efficiency and accuracy.
2. The authors provide rigorous theoretical analysis of the convergence properties of the proposed method. They establish conditions under which the ADMM-PnP algorithm with the AC-DC denoiser converges to a fixed point or a ball neighborhood. The theoretical results are well-supported by mathematical proofs and provide valuable insights into the behavior of the proposed method.
3. The paper is well-written and clearly structured. The authors provide detailed explanations of the proposed method, the theoretical analysis, and the experimental results. The use of figures and tables effectively illustrates the key concepts and findings.

### Weaknesses

#### Some Related Works


#### comment

1. The paper's convergence analysis relies on certain assumptions (Assumptions 2 and 3) that may not always hold in practice. The assumption that the log data density is M-smooth and the coercivity assumption for -log p_data might be restrictive. Specifically, the M-smoothness assumption requires that the gradient of the log data density does not change too rapidly, which may not be true for complex data distributions. The coercivity assumption, while ensuring that the score function does not vanish at infinity, might be difficult to verify for real-world data manifolds. Providing more discussion or relaxations of these assumptions would be beneficial. It is unclear how the proposed method would behave if these assumptions are violated, and what the practical implications would be.

2. The paper lacks a detailed discussion of the computational complexity and runtime of the proposed method compared to other baselines. The three-stage denoising process, involving auto-correction, directional correction, and score-based denoising, could be computationally expensive, especially the Langevin dynamics step. A comparison of the computational cost with other state-of-the-art methods would be valuable for practical applications. The authors should provide a breakdown of the computational cost of each stage and discuss how the number of Langevin steps affects the overall runtime and performance.

3. While the paper demonstrates the effectiveness of the proposed method on various inverse problems, it would be beneficial to explore its performance on a wider range of applications and datasets. The current experiments, while demonstrating the method's potential, are limited in scope. Testing on more diverse datasets and problem settings would provide a more comprehensive evaluation of the method's robustness and generalizability. For example, it would be interesting to see how the method performs on color images, or on datasets with different characteristics than those used in the current experiments.

### Suggestions

The paper would benefit from a more in-depth discussion of the limitations imposed by Assumptions 2 and 3. Specifically, the authors should provide examples of data distributions where these assumptions might fail and discuss the potential consequences for the convergence of their algorithm. For instance, they could analyze the behavior of the score function near the boundaries of the data manifold or in regions of low data density. Furthermore, it would be helpful to explore alternative assumptions or regularization techniques that could mitigate the impact of violating these conditions. A more robust theoretical analysis that considers the possibility of non-smooth or poorly behaved score functions would significantly strengthen the paper. The authors could also consider providing empirical evidence to support the validity of these assumptions for the datasets used in their experiments.

To address the lack of computational analysis, the authors should include a detailed breakdown of the computational cost of each stage of the AC-DC denoiser. This should include the number of floating-point operations, memory usage, and runtime for each step, as well as how these scale with the size of the input and the number of Langevin steps. A comparison with other state-of-the-art methods, such as DiffPIR and RED-diff, should be provided, highlighting the trade-offs between computational cost and performance. The authors should also investigate the impact of the number of Langevin steps on the convergence and quality of the results. It would be beneficial to show how the performance changes as the number of Langevin steps is varied, and to provide guidelines for selecting an appropriate number of steps for different applications. This analysis should be presented in a clear and concise manner, possibly using tables and graphs to illustrate the key findings.

Finally, the authors should expand their experimental evaluation to include a wider range of applications and datasets. This could include testing on color images, different types of noise, and more complex inverse problems. It would also be valuable to explore the performance of the method on datasets with different characteristics than those used in the current experiments. For example, the authors could consider using datasets with higher resolution images or datasets from different domains. This would provide a more comprehensive evaluation of the method's robustness and generalizability. The authors should also discuss any limitations or challenges they encounter when applying the method to new datasets or problem settings. This would help to identify areas for future research and development.

### Questions

1. Assumptions 2 and 3 are critical for the convergence analysis. Can the authors provide more discussion or relaxations of these assumptions? How do they affect the convergence in practice?
2. The paper mentions that the AC-DC denoiser is effective in aligning ADMM iterates with the data manifold. Can the authors provide more insights or visualizations on how this alignment is achieved?
3. The paper compares the proposed method with several baselines but does not include a comparison with methods like DiffPIR and RED-diff in terms of runtime and computational complexity. How does the proposed method compare to these baselines in terms of computational efficiency?
4. The paper uses a linear schedule for sigma(k) in the experiments. How does the choice of sigma(k) affect the performance and convergence of the proposed method? Can the authors provide more details on how to choose an appropriate schedule for sigma(k)?

### Rating

6

### Confidence

3

**********
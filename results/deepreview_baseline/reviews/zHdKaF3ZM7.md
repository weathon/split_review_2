## Summary

This paper introduces WARP (Weight-space Adaptive Recurrent Prediction), a novel sequence modeling framework that unifies weight-space learning with linear recurrence. Instead of maintaining a fixed-dimensional hidden state, WARP parametrizes its hidden state as the weights and biases of an auxiliary neural network, updating these weights via a linear recurrence driven by input differences. The model enables gradient-free test-time adaptation, in-context learning, and seamless integration of physical priors. Empirical results show competitive or state-of-the-art performance across diverse tasks including image completion, time series forecasting, dynamical system reconstruction, and multivariate time series classification.

## Strengths

- **Novel and conceptually elegant framework**: The idea of treating the weights of an auxiliary network as the hidden state of a recurrent model is genuinely novel and well-motivated. The paper clearly articulates how this bridges weight-space learning and linear recurrence, offering a fresh perspective on sequence modeling that differs meaningfully from existing approaches.

- **Strong empirical results across diverse domains**: WARP demonstrates competitive performance on a wide range of tasks. The results on PEMS08 traffic forecasting (reducing MAE by over 50% compared to SOTA), the physics-informed variant achieving order-of-magnitude improvements on dynamical systems, and top-three performance on 4 out of 6 UEA classification datasets are impressive and well-documented.

- **Gradient-free adaptation and in-context learning capabilities**: The paper convincingly demonstrates that WARP can perform test-time adaptation without gradient computation, and shows in-context learning on a linear regression task. This is a practically valuable property that distinguishes WARP from many competing approaches.

- **Physics-informed modeling**: The ability to seamlessly incorporate domain-specific physical priors into the root network is a significant advantage, as demonstrated by the WARP-Phys variant's dramatic improvements on dynamical system reconstruction tasks.

## Weaknesses

### Fatal
None.

### Major

- **Scalability concerns are insufficiently addressed**: The paper acknowledges that the size of matrix A limits scaling to large root networks, but this is a fundamental limitation that affects the practical utility of the approach. With experiments limited to a 16GB GPU, it remains unclear whether WARP can scale to problems requiring larger hidden states. The proposed solutions (low-rank diagonal parametrizations, block-diagonal decompositions) are mentioned only as future work, leaving a significant gap in the current contribution.

- **Missing critical baselines and comparisons**: The paper does not compare against modern efficient sequence models like Mamba-2, RWKV, or recent linear attention Transformers on several key benchmarks. For the UEA classification tasks, the baselines are taken from a single prior work [96], and it's unclear whether these represent the current state-of-the-art. The image completion experiments lack comparisons with more recent SSM variants (e.g., Mamba, S6) that have shown strong performance on such tasks.

- **Computational efficiency analysis is insufficient**: While the paper claims computational efficiency, the analysis in Appendix E.3 is not presented in the main text. Given that WARP requires materializing high-dimensional hidden states θ_t (which are the size of the entire root network), the computational and memory costs could be substantial. The paper would benefit from a clear comparison of FLOPs, memory usage, and wall-clock time against baselines for representative tasks.

- **The in-context learning experiment is limited**: The ICL demonstration is restricted to a simple linear regression task with random keys. This is far from the sophisticated in-context learning capabilities demonstrated by large language models or even simpler meta-learning approaches. The paper would benefit from more challenging ICL benchmarks or a clearer articulation of what "in-context learning" means in this context.

### Minor

- **The paper overclaims in several places**: Statements like "transformative paradigm for adaptive machine intelligence" and "human-level artificial intelligence" in the conclusion are hyperbolic and not supported by the evidence presented. The claim of "infinite-dimensional" RNN hidden states is misleading—while the weight space is high-dimensional, it is finite.

- **The relationship to prior work on fast weights and test-time training is underdeveloped**: The paper mentions connections to fast weights [7, 83] and test-time training [101] but does not clearly differentiate WARP from these approaches or explain what new capabilities WARP enables beyond what these prior methods could achieve.

- **Ablation studies are relegated to the appendix**: The main text mentions ablation studies but does not present them. Key architectural choices (e.g., the use of input differences vs. direct inputs, the importance of the identity initialization of A, the effect of different coordinate systems) should be ablated in the main paper to build confidence in the design decisions.

### Trivial
- The paper uses "weight-space" inconsistently—sometimes referring to the space of the root network's weights, sometimes to the space of the RNN's parameters.

## Nice-to-Haves

- A theoretical analysis of the expressivity of weight-space linear RNNs compared to standard RNNs and SSMs would strengthen the paper significantly.
- Experiments on language modeling or other discrete sequence tasks would broaden the impact.
- A more detailed analysis of when the gradient-free adaptation property is beneficial compared to fine-tuning would help practitioners understand when to use WARP.

## Novel Insights

The paper's core insight—that the weights of an auxiliary network can serve as a high-resolution hidden state for a linear recurrent model, updated via input differences rather than gradient descent—is genuinely novel and opens up a new direction for sequence modeling. The connection to synaptic plasticity (STDP) provides an interesting biological motivation, though this is more suggestive than rigorous. The demonstration that this architecture naturally supports physics-informed modeling and gradient-free adaptation is a valuable synthesis of ideas from weight-space learning, linear recurrence, and scientific machine learning.

## Suggestions

1. Provide a clear computational complexity analysis (FLOPs, memory) comparing WARP to standard RNNs, SSMs, and Transformers for representative sequence lengths and hidden dimensions.
2. Add experiments with larger root networks (if possible with more GPU memory) or demonstrate the effectiveness of the proposed scaling solutions (low-rank A, block-diagonal decompositions).
3. Include comparisons with more recent baselines (Mamba-2, RWKV, recent linear attention models) on at least a subset of benchmarks.
4. Move key ablation studies (input differences vs. direct inputs, identity initialization, coordinate system choices) to the main paper.
5. Tone down the claims about "human-level AI" and "transformative paradigm" to better match the empirical scope of the work.
6. Clarify the relationship to fast weights and test-time training, and provide a more nuanced discussion of what WARP adds beyond these prior approaches.

## Score and Decision

The paper presents a genuinely novel and well-motivated framework with strong empirical results across diverse domains. However, the scalability concerns, missing comparisons with recent baselines, and insufficient computational efficiency analysis are significant issues that prevent a higher score. The work is clearly above the acceptance threshold but has room for improvement.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>
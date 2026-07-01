## Summary

The paper introduces WARP (Weight-space Adaptive Recurrent Prediction), a sequence model that treats the hidden state of a linear RNN as the flattened weights of an auxiliary MLP. The recurrence uses input differences and a linear transition, while the output is produced by decoding the weight-state through the non-linear MLP. The authors claim this framework enables gradient-free adaptation, in-context learning, and seamless integration of physical priors, and they present extensive experiments on forecasting, classification, dynamical system reconstruction, and in-context learning tasks.

## Strengths

- **Novel formulation.** Combining weight-space learning with linear recurrence is a genuinely new idea. Using the weights of an auxiliary network as the hidden state of an RNN, while keeping the recurrence linear, allows non-linear decoding without sacrificing the parallelizability of linear RNNs.
- **Broad and competitive empirical evaluation.** The paper evaluates WARP on a wide range of tasks (image completion, energy/traffic forecasting, dynamical system reconstruction, multivariate time series classification, in-context learning) and shows that it often matches or outperforms strong baselines including GRU, LSTM, S4, Mamba, and Transformer-based models.
- **Demonstrated flexibility.** The ability to inject physical priors into the root network (WARP-Phys) leads to dramatic improvements (e.g., >10× on MSD), and the in-context learning experiment shows that the final weight-state can be extracted and reused, offering computational savings.
- **Clear exposition of the architecture and training modes.** The paper explains the convolutional and recurrent training modes, the use of input differences, and the initialization scheme, making the method reproducible.

## Weaknesses

### Fatal
None.

### Major
1. **Scalability of the state transition matrix.** The matrix \(A\) has size \(D_\theta \times D_\theta\), where \(D_\theta\) is the flattened weight dimension of the root MLP. For even a modest MLP (e.g., two hidden layers of width 256), \(D_\theta\) can be millions, making \(A\) prohibitively large. The paper acknowledges this limitation but does not quantify the practical \(D_\theta\) used in experiments or provide a solution (e.g., low-rank or diagonal parametrizations). This fundamentally limits the model’s applicability to small root networks and raises questions about its scalability to more complex tasks.
2. **Suspiciously large improvement on PEMS08.** WARP achieves MAE 6.59 vs. the best baseline 13.45 (a >50% reduction) without using graph structure, while baselines are graph-based methods designed for traffic data. The paper mentions a non-causal convolution preprocessing step but does not sufficiently justify why this does not constitute an unfair advantage or data leakage. A more detailed ablation and fair comparison (e.g., training baselines with the same preprocessing) is needed.
3. **In-context learning experiment is too simple.** The ICL task is linear regression with random keys, which is a toy problem. The claim of “sub-quadratic in-context learning” is not supported by experiments on more challenging ICL benchmarks (e.g., few-shot classification). The novelty of the ICL capability is therefore not convincingly demonstrated.
4. **Overclaimed “gradient-free adaptation.”** While the root network weights \(\theta_t\) are updated without gradients at test time, the overall model parameters (\(A, B, \phi\)) are trained with gradients. This is standard for any recurrent model whose hidden state update is deterministic. The term “gradient-free adaptation” is misleading if not carefully contextualized; the paper does clarify this, but the emphasis in the abstract and introduction overstates the novelty.

### Minor
- The paper uses strong language (“transformative paradigm,” “outstanding results”) that is not fully justified given the scalability limitations and the simplicity of some experiments.
- The connection to biological learning (STDP) is superficial and adds little to the technical contribution.
- The main text does not report computational cost (FLOPs, memory) relative to baselines; the appendix mentions wall-clock time and GPU usage, but a direct comparison in the main paper would strengthen the efficiency claims.

### Trivial
None.

## Nice-to-Haves
- An analysis of the trade-off between \(D_\theta\) and performance, with experiments using low-rank or diagonal approximations of \(A\).
- Additional ICL experiments on standard few-shot learning benchmarks (e.g., Omniglot, miniImageNet) to substantiate the ICL claims.
- An ablation study comparing input differences \(\Delta x_t\) vs. direct inputs \(x_t\) to justify the design choice.

## Novel Insights

The paper’s core insight is that the weight space of a neural network can serve as a high-resolution hidden state in a linear recurrence, enabling non-linear decoding without breaking the parallelizability of linear RNNs. This perspective bridges weight-space learning and sequence modeling, and the empirical results suggest that such models can be competitive with or outperform established architectures on several tasks. The ability to incorporate physical priors directly into the root network is a particularly elegant demonstration of the framework’s flexibility.

## Suggestions
1. Address the scalability concern by either (a) providing experiments with larger root networks and reporting the resulting \(D_\theta\) and memory usage, or (b) proposing and evaluating a low-rank or diagonal parametrization of \(A\).
2. For the PEMS08 experiment, include a fair comparison by training the baselines with the same non-causal convolution preprocessing, or provide a clear justification that the preprocessing does not leak future information.
3. Tone down the claims of “transformative” and “outstanding” to better match the current limitations of the approach.
4. Add a complexity analysis (FLOPs and memory) for WARP vs. baselines in the main paper.

## Score and Decision

The paper presents a novel and interesting idea, supported by extensive experiments across diverse tasks. However, the major scalability issue and the questionable fairness of the PEMS08 comparison prevent a stronger recommendation. The contribution is solid but not yet transformative.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>
## Summary

The paper introduces WARP (Weight-space Adaptive Recurrent Prediction), a novel sequence model that treats the flattened weights of an auxiliary MLP as the hidden state of a linear recurrence, driven by input differences. The model decodes outputs by applying the reconstituted MLP to coordinate inputs, combining the parallelization advantages of linear recurrence with the expressivity of non-linear decoding. Extensive experiments across image completion, time series forecasting, dynamical system reconstruction, and classification demonstrate competitive or superior performance, with particularly striking results in physics-informed modeling and traffic forecasting.

## Strengths

- **Genuinely novel architecture**: The combination of weight-space learning and linear recurrence to create "self-decoding" hidden states is a creative and well-motivated contribution. The formulation θ_t = Aθ_{t-1} + BΔx_t with y_t = MLP_{θ_t}(τ) is elegant, and the conceptual diagram in Figure 1 clearly positions this relative to standard and linear RNNs.

- **Comprehensive and diverse evaluation**: The paper evaluates across six distinct task categories (image completion, energy forecasting, traffic forecasting, dynamical system reconstruction, classification, and in-context learning) spanning multiple data modalities. This breadth convincingly demonstrates the framework's versatility.

- **WARP-Phys demonstrates a compelling practical advantage**: Embedding domain-specific physics into the root network (e.g., the sinusoidal prior on SINE, the known ODE structure for MSD) yields order-of-magnitude improvements over the black-box variant, concretely demonstrating that the weight-space formulation naturally accommodates domain knowledge — something standard RNNs cannot easily achieve.

- **Clean dual-mode training**: The parallelization via convolutional mode and the recurrent mode (with/without auto-regression) follows established SSM methodology and is technically sound. The connection to fast weights and test-time training is well-articulated.

- **Strong in-context learning demonstration**: The cumulative-sum trick for the linear regression ICL task is clever, and the ability to extract the final root network θ_{T-1} for subsequent queries without reprocessing the full sequence is a practical advantage.

## Weaknesses

### Fatal
None.

### Major

- **Fundamental scalability constraint of matrix A**: The transition matrix A has dimensions D_θ × D_θ, where D_θ is the number of parameters in the root MLP. Even for a modest 10K-parameter root network, A contains 100M parameters. The paper's experiments appear to use very small root networks (consistent with ~1.68M total parameters for MNIST), which limits the expressiveness argument. This is not merely a limitation — it constrains the core claim that "the weights of an auxiliary function approximator can serve as high-resolution hidden states." If the root network must be small to keep A tractable, the "high-resolution" argument weakens substantially. Low-rank or diagonal parameterizations of A are mentioned in the limitations but not explored, leaving the reader uncertain about practical viability beyond small-scale settings.

- **PEMS08 traffic forecasting comparison is narrow**: The dramatic improvement (6.59 vs 13.45 MAE) is compared against only three baselines (GMAN, D²STGNN, STDCN) drawn from a single prior paper [62]. The PEMS08 benchmark has many other published results (e.g., DCRNN, Graph WaveNet, STGCN, ASTGCN, and numerous others), and the paper does not contextualize against them. Additionally, WARP uses non-causal convolution preprocessing and processes all 170 sensor nodes jointly through the weight space, which is a substantially different setup from the graph-based baselines that rely on explicit spatial adjacency. Without careful ablation isolating the contribution of each design choice, the "50%+ improvement over SOTA" claim is difficult to evaluate.

- **CelebA baseline BPD values appear anomalous**: LSTM achieves BPD of 3869 at L=100, and ConvCNP reaches 248.1 at L=600, while WARP achieves values near zero or negative. These extreme baseline values suggest potential training instabilities or implementation issues in the baselines rather than exclusively reflecting WARP's strength. Without verification that baselines were properly tuned, these comparisons may overstate WARP's advantage.

### Minor

- **Classification results are mixed**: WARP achieves best accuracy on only 2 of 6 UEA datasets (Ethanol and Heartbeat) and performs notably poorly on EigenWorms (70.93 vs LinOSS's 95.0). The paper's framing of "top three on 4 out of 6" is accurate but somewhat selective. The weak EigenWorms performance — a dataset with nearly 18K-length sequences — somewhat undermines claims about long-range dependency handling.

- **Lack of comparison to modern linear RNN variants on forecasting**: The forecasting experiments compare against GRU, LSTM, S4, and ConvCNP, but do not include more recent models like Mamba, S5, RetNet, or Griffin on the forecasting tasks, even though these are included in the classification benchmarks. This inconsistency makes it harder to assess relative performance.

- **Limited analysis of what weight-space states learn**: The paper would benefit from visualization or analysis of the evolved weight vectors θ_t across time steps. Understanding whether the weights encode interpretable features or capture meaningful temporal structure would strengthen the scientific contribution beyond the empirical performance gains.

### Trivial

- The claim in the conclusion of "infinite-dimensional" hidden states is an overstatement — D_θ is finite, just potentially large.

## Nice-to-Haves

- An experiment varying root network size (e.g., small/medium/large) to empirically characterize the tradeoff between A-matrix cost and expressivity would be valuable.
- Ablation comparing input differences Δx_t vs. direct inputs x_t across multiple tasks to validate the universal benefit of the difference-based formulation.
- A wall-clock comparison against Mamba/S5 on the classification benchmarks to contextualize computational efficiency.

## Novel Insights

The paper's central insight — that the weights of an auxiliary network can serve as a high-resolution hidden state in a linear recurrence, with non-linearity entering through the decoding rather than the state transition — is genuinely novel. This creates a clean separation between the hardware-friendly linear recurrence (enabling parallelization) and the expressive non-linear output mapping, sidestepping the well-known expressivity limitations of purely linear sequence models. The observation that input differences naturally implement a form of synaptic plasticity-like adaptation, enabling gradient-free test-time updates through the recurrence alone, is a compelling conceptual contribution that connects machine learning architecture design to neuroscience principles.

## Suggestions

- Add experiments on the PEMS08 benchmark with a broader set of recent graph-based and non-graph baselines, and include ablations isolating the contribution of non-causal preprocessing, joint multi-node processing, and the weight-space formulation itself.
- Explore practical parameterizations of A (e.g., block-diagonal, Kronecker-factored, or low-rank complex diagonal as mentioned in the limitations) with empirical validation, since this is the primary barrier to scaling.
- Verify baseline implementations for CelebA experiments, particularly LSTM and ConvCNP BPD values, to ensure fair comparison.

## Score and Decision

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>
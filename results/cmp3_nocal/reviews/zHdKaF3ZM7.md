Now I'll write the final consolidated review.

## Summary

This paper introduces WARP (Weight-space Adaptive Recurrent Prediction), which treats the flattened weights of a root MLP as the hidden state of a linear RNN. The recurrence is driven by input differences (Δxₜ = xₜ − xₜ₋₁), and the hidden state θₜ is decoded by unflattening it back into the MLP and applying it to a coordinate system τ. This is a genuinely novel synthesis of weight-space learning and linear recurrence, enabling gradient-free updating of the root network's parameters at test time, in-context learning via the linear recurrence, and integration of physical priors into the root MLP architecture. Experiments span image completion, traffic forecasting, time series classification, dynamical system reconstruction, and in-context learning.

## Strengths

1. **Conceptually novel framework.** Treating MLP weights as the hidden state of a linear RNN (θₜ = Aθₜ₋₁ + BΔxₜ) is a creative and, to my knowledge, original synthesis of weight-space learning and linear recurrence. The self-decoding property — where θₜ plays both the role of hidden state and decoder parameters — is a clean design that saves on parameter count while introducing nonlinear expressivity through the root MLP.

2. **Input-difference driving mechanism.** Using Δxₜ rather than direct inputs is theoretically principled (connected to Neural CDE theory) and provides a natural inductive bias: constant inputs produce no weight change, making the recurrence sensitive to change rather than absolute values, which is appropriate for continual learning and adaptation settings.

3. **Honest limitations section.** Section 4.2 explicitly acknowledges the scaling bottleneck of the dense A matrix, the lack of theoretical depth, and the model's poor performance on long sequences and untested language modalities. This candor is commendable and rare.

4. **Competitive time series classification results.** On the UEA MTSCA benchmark (Table 4), WARP achieves top-three placement on 4 out of 6 datasets, including state-of-the-art on EthanolConcentration (36.49%) and Heartbeat (80.65%), with ablations against a strong and diverse set of 11 baselines including Mamba, S5, Griffin, and FACTS.

## Weaknesses

### Fatal
None.

### Major

1. **PEMS08 comparison compromised by non-causal preprocessing.** The paper reports a >50% MAE reduction over SOTA on PEMS08 (MAE 6.59 vs. 13.45). However, line 180 states: *"we preprocess the input sequence with a non-causal convolution, as detailed in Appendix D."* The baselines (GMAN, D²STGNN, STDCN) are cited from published results and there is no indication they used equivalent preprocessing. Since this is a 12-step-input → 12-step-forecast task, a non-causal convolution on the input uses information from all input positions to transform each one, providing richer input representations than a causal model would see. This is the paper's most dramatic quantitative result, and without an apples-to-apples comparison, the claim of "reducing MAE by over 50%" is not supported as evidence of architectural superiority. The authors should either rerun without non-causal preprocessing, apply the same preprocessing to baselines, or clearly frame this as a different pipeline rather than a direct comparison.

2. **The "10x improvement" claim rests on a result whose noise exceeds its signal.** The abstract claims *"outperforms the next best model by more than 10x,"* supported by Table 3 (MSD: WARP-Phys MSE 0.03±0.04 vs. Transformer 0.34±0.12). The standard deviation (0.04) exceeds the mean (0.03), meaning the point estimate is statistically unreliable — the true MSE could plausibly be near zero or as high as ~0.11, making the precise倍数 factor ambiguous. On SINE* (the other dataset where WARP-Phys strongly outperforms baselines), the improvement over the next-best model (WARP) is ~4.5×, not 10×. The "more than 10x" claim in the abstract is selectively based on the one dataset where error bars undermine the estimate.

3. **Anomalous BPD values on CelebA suggest metric computation issues.** In Table 1 (CelebA): WARP achieves a negative BPD (−0.162 at L=600), which is unusual — bits-per-dimension should be positive for any reasonable continuous density model; a negative value implies the assigned probability density exceeds 1 per dimension, which is theoretically possible with badly calibrated variance estimates but would indicate the NLL loss is not being computed or calibrated correctly. Separately, the LSTM BPD of 3869 at L=100 (dropping to ~7 at longer contexts) and ConvCNP BPD monotonically increasing with context (1.498→39.91→248.1) are anomalous. These values are not discussed, yet BPD is used as a key evaluation metric. The authors should explain or correct these numbers.

4. **Root MLP architecture is critically underspecified for reproducibility.** The paper states only that the root network is a "fixed-width MLP" with Dₓ-dimensional input and either D_y or 2×D_y output (line 84). The number of hidden layers, hidden width, activation function, and resulting total hidden state dimension D_θ are never reported for any experiment. Since A ∈ ℝ^{D_θ×D_θ} dominates the parameter count, this omission makes it impossible for readers to assess model capacity, the true parameter count breakdown, or whether the method is computationally practical. The claim of "~1.68M parameters" for MNIST implies D_θ ≈ 1300 (since A alone would be D_θ²), but this is never verified.

### Minor

1. **The ICL experiment modifies the standard task in a way that is not sufficiently contextualized.** The paper adapts the task from von Oswald et al. by transforming the input sequence into its cumulative sum (line 247). This is transparently described, but the significance of the modification is understated — the cumulative sum turns the ICL problem into one where the model can exploit aggregate statistics rather than needing to infer the key-value mapping from individual pairs. The demonstration uses only T=32 tokens with D_s ∈ {2, 8}, which is at a much smaller scale than typical ICL evaluations. The paper would benefit from either running an ablation without cumulative-sum preprocessing or more clearly scoping what claim is being made.

2. **ETT forecasting evaluation omits key baselines.** The ETT heatmap (Figure 3b) compares only GRU, LSTM, and WARP, while S4, ConvCNP, and Transformer — baselines used in other experiments in the same section — are absent. Given that S4 is a state-of-the-art linear RNN/SSM that is a direct conceptual competitor, its omission from this task leaves the evaluation incomplete.

3. **Several claims are overstated relative to the evidence.** (a) The conclusion calls θₜ an *"infinite-dimensional"* hidden state (line 283), but D_θ is finite and bounded by GPU memory. (b) The abstract claim of *"surpasses state-of-the-art"* is too broad given mixed results (e.g., WARP at 70.93% on EigenWorms vs. LinOSS at 95.0%, Table 4). (c) The claim that the parallel scan enables efficient precomputation (line 80) is technically true but would be O(T·D_θ²) for dense A, not the logarithmic cost associated with structured linear RNNs used in SSMs.

4. **WARP-Phys is incompatible with discontinuous dynamics.** The paper acknowledges (line 237) that WARP-Phys cannot handle the Lotka-Volterra repeat-copy task due to artificial discontinuities. This is an honest admission, but it means the physics-informed variant — which produces the most dramatic results — is only applicable to smooth continuous dynamics, substantially limiting its scope.

### Trivial
None.

## Nice-to-Haves

- Report D_θ, the root MLP architecture (layers, width, activation), and the parameter count breakdown (A vs. B vs. φ vs. others) for every experiment. This is the single most important piece of missing information.
- Include wall-clock timing and memory usage in the main paper rather than deferring entirely to the appendix. For a method whose practical question is "does the expressivity gain justify the O(D_θ²) recurrence cost?", this evidence belongs in the main text.
- Add uncertainty calibration evaluation (e.g., coverage plots) for the probabilistic forecasting experiments, especially given the anomalous BPD values.
- Analyze the spectral properties of the learned A matrix (rank, eigenvalue distribution) to understand whether the dense parameterization is necessary or whether a structured approximation would suffice.

## Removed Points

These points from the input reviews were flagged for removal; treat them with caution:

- **"Gradient-free adaptation is standard RNN forward-pass dynamics."** Removed. This criticism is factually inaccurate. In a standard RNN, the hidden state hₜ is a latent vector; the decoder weights remain fixed. In WARP, θₜ IS the decoder weights — the root MLP's parameters change at test time without gradient descent. This IS genuinely different. The mechanism (a linear recurrence) is simple, but the target of the update (the decoder weights) is novel. The paper correctly distinguishes this from approaches requiring gradient-based test-time optimization (e.g., MAML).
- **"The 10x claim is based on WARP vs WARP-Phys rather than next best model."** Removed. On MSD-Zero, WARP (0.32±0.02) IS the next best model after WARP-Phys (0.04±0.01) — the comparison is correctly stated against "the next best model."
- **"Missing comparison to LSTM on sequential MNIST."** Removed. The paper does not claim SOTA on sequential MNIST; the 93% figure is presented as an additional result in the appendix.
- **"No analysis of A's structure."** Removed. This is a nice-to-have, not a weakness.
- **"Wall-clock comparison relegated to appendix."** Removed per instructions: appendix sections are stripped by the parser and exist in the original submission.
- **"Uncertainty calibration not evaluated."** Removed. This is a nice-to-have, not a necessary evaluation for every probabilistic forecasting paper.
- Formatting, style, and reproducibility nitpicks removed per filtering rules.

## Novel Insights

Beyond the paper's own contributions, one observation from the review process stands out: the tension between the framework's theoretical appeal and the empirical evaluation. The core idea — that the linear recurrence's hidden state can be the weights of a decoder — elegantly sidesteps the expressivity limitations of standard linear RNNs by offloading nonlinearity to the decoding step, while retaining the parallelizability of linear recurrence. This architectural insight is the paper's genuine contribution, and it is strong enough that the paper would remain interesting even with more modest empirical claims. The review process surfaced that many of the paper's most dramatic empirical claims (PEMS08 >50% reduction, 10× improvement) are not necessary to establish the value of the framework, and their brittleness weakens rather than strengthens the paper.

## Suggestions

1. **Clean up the PEMS08 evaluation.** Either remove the non-causal convolution, apply equivalent preprocessing to baselines, or explicitly frame the result as "with additional non-causal preprocessing" to avoid misleading comparisons. This single change would make the paper's strongest quantitative claim credible.

2. **Recompute or explain the BPD values on CelebA.** Negative BPD and extreme jumps (LSTM: 3869→7.3) need explanation. If the metric computation has issues, correct them; if the values are correct under an unconventional BPD definition, state this clearly.

3. **Tone down the "10x" claim** to something like "up to an order of magnitude on some datasets" and acknowledge the high variance on MSD.

4. **Specify D_θ and root MLP architecture** for every experiment in a table. Without this, the results are not reproducible and the model's capacity cannot be assessed.

5. **Scope the ICL results more carefully.** Either add an ablation without cumulative-sum preprocessing or clearly distinguish what WARP's ICL demonstration shows vs. the standard ICL setup.

## Score and Decision

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Accept</decision>
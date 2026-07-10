Now let me finalize the review with my assessment.

## Summary

This paper introduces WARP (Weight-space Adaptive Recurrent Prediction), a novel sequence modeling architecture that treats the weights and biases of an auxiliary MLP as the hidden state of a linear RNN. The hidden state θ_t evolves via θ_t = Aθ_{t-1} + BΔx_t, and outputs are produced by running the MLP (with weights θ_t) on a coordinate input τ. This combines linear recurrence (enabling parallel scans) with nonlinear decoding through the root MLP. The paper evaluates WARP across image completion, time series forecasting, dynamical system reconstruction, time series classification, and in-context learning.

## Strengths

- **Genuinely novel architectural concept.** Treating the weights of an auxiliary MLP as the recurrent hidden state of a linear RNN, then decoding by running that MLP on a coordinate input, is creative and distinct from prior work. Weight-space learning has been used to analyze trained models, but using weight-space features as *intermediate recurrent hidden states* is original (Section 2.2, Figure 1).

- **The physics-informed variant (WARP-Phys) demonstrates meaningful gains.** The order-of-magnitude improvement over vanilla WARP on MSD (Table 3: MSE 0.03 vs 0.94) convincingly shows that the weight-space formulation can productively incorporate domain-specific physical priors.

- **Input differences as recurrence drivers.** The choice to use Δx_t rather than x_t (Eq. 1) is well-motivated by neural ODE theory [54] and draws an interesting neuromorphic parallel to STDP (Section 4.1). This is a thoughtful design choice that distinguishes WARP from standard RNN formulations.

- **Broad evaluation across multiple domains** — image completion, time series forecasting, dynamical system reconstruction, time series classification, and in-context learning — providing a comprehensive empirical picture of the method's capabilities.

## Weaknesses

### Major

- **D_θ × D_θ scalability bottleneck undercuts the "high-resolution" framing.** The recurrence requires A ∈ ℝ^{D_θ × D_θ}, which grows quadratically in the root MLP's parameter count. With ~1.68M total parameters for MNIST (line 149), D_θ is bounded by roughly sqrt(1.68M) ≈ 1,300, making the root MLP a very small network. This directly conflicts with claims of "high-resolution hidden states" (line 31) and "infinite-dimensional RNN hidden states" (line 283). While the paper acknowledges this limitation in Section 4.2, the framing throughout the abstract and introduction is substantially overstated given the practical constraint.

- **ETT experiment (Figure 3b) compares only GRU and LSTM.** The paper claims superiority on energy forecasting yet omits standard baselines: Transformers (Informer, Autoformer), SSMs (S4, Mamba), and MLP-based models (N-BEATS, TSMixer). The comparison is too thin to support the claimed results.

- **CelebA BPD values indicate a computation or evaluation issue.** LSTM BPD = 3869 at L=100 is nonsensical (astronomically worse than random). GRU and ConvCNP BPD values anomalously *increase* with context length (GRU: 24.14 at L=100 → 71.51 at L=600). WARP itself reports negative BPD values (-0.043, -0.162), which are impossible for correctly computed discrete likelihoods. If pixel values are continuous (normalized to [0,1]), this requires explicit justification; if discrete, it signals a bug. The baseline anomalies suggest an evaluation inconsistency; without clarification the BPD results in Table 1 are uninterpretable.

- **S4 is absent from the CelebA portion of Table 1** without explanation. S4 is included for MNIST and described as a SOTA SSM baseline (line 149), yet omitted from CelebA, making the comparison incomplete.

- **The "gradient-free adaptation" framing is misleading.** The paper emphasizes that θ_t is updated "without requiring gradients" (abstract, lines 35-36, line 108) and connects this to test-time training literature [101]. However, every RNN updates its hidden state without gradient descent during forward propagation — this is simply how a forward pass works. What WARP does differently is that the hidden state is the decoder weights, but this is not a form of test-time adaptation in the sense used in that literature. The framing overstates what is fundamentally a normal forward-pass computation.

### Minor

- **The in-context learning experiment (Section 3.4) does not clearly demonstrate per-sequence adaptation.** The paper describes "finding a shared vector w" (line 247), which suggests a single w across all sequences rather than the standard ICL setup where each sequence has a different underlying function. If w is global, the task reduces to meta-learning a single linear map — a simpler problem that does not require ICL. The paper should clarify whether w varies per sequence.

- **The physics-informed comparison (Table 3) lacks a control.** WARP-Phys vs vanilla WARP shows physical priors improve performance, but does not isolate whether the weight-space formulation provides advantages over, say, a physically-informed GRU or Neural ODE with the same prior.

## Nice-to-Haves

- Adopt a structured parameterization of A (low-rank, diagonal, block-diagonal) to remove the O(D_θ²) bottleneck.
- Add S4 and other SSM/Transformer baselines to the ETT and CelebA comparisons.
- Provide controlled re-implementation of PEMS08 baselines and clarify the non-causal convolution preprocessing.
- Add a controlled experiment comparing WARP-Phys against a standard RNN with the same physical prior.

## Removed Points

These points are flagged to be removed; treat them with caution:
- Formatting and style nitpicks about paper presentation (parser artifacts, not author errors).
- Speculative claims about missing appendix content or unreleased code/models — the parser strips appendices from all papers; cited references are assumed to exist.
- The "PEMS08 result is too good, therefore suspicious" speculation without concrete evidence of an error — kept as a call for scrutiny rather than an assertion of wrongdoing.
- Generic "the paper should include more datasets" type requests unmoored from specific experiments.

## Novel Insights

The most useful synthetic insight from the reviews is that a pattern of evaluation anomalies (PEMS08 being dramatically better than graph-aware SOTA, CelebA BPD being nonsensical for both baselines and WARP, S4 omitted from CelebA, missing ETT baselines) collectively points toward evaluation-level issues that go beyond any single table. A second insight is that the D_θ² cost is not merely a "limitation" but actively contradicts the paper's central rhetorical framing ("high-resolution," "infinite-dimensional"), making the paper's claims and its actual architecture misaligned.

## Suggestions

1. Add Transformer, SSM, and MLP baselines to the ETT comparison and add S4 to the CelebA table.
2. Explain the CelebA BPD computation (discrete vs continuous likelihood, normalization) and resolve baseline anomalies.
3. Clarify whether w varies per sequence in the ICL experiment, or reframe it.
4. Add a controlled experiment comparing WARP-Phys against a standard RNN with the same physical prior.
5. Temper the "gradient-free adaptation" and "infinite-dimensional" framing.
6. Consider adopting a structured A to address the scalability bottleneck.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>
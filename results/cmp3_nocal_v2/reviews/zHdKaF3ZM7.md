## Summary

This paper introduces WARP (Weight-space Adaptive Recurrent Prediction), a sequence model whose hidden state is the *flattened weight vector* of an auxiliary MLP decoder. The recurrence is linear: θₜ = Aθₜ₋₁ + BΔxₜ, and the output is produced by decoding θₜ itself. The architecture enables gradient-free test-time adaptation (the fast weights θₜ are updated via linear recurrence, not backprop), injection of physical priors into the root network, and parallel training via a convolutional mode. Experiments span image completion, energy/traffic forecasting, dynamical system reconstruction, multivariate classification, and in-context learning.

## Strengths

1. **Genuinely novel architectural idea.** Treating the hidden state as the *parameters of the decoder* — so the decoder "reads itself" — is architecturally distinct from standard RNNs (separate hidden state and decoder) and SSMs (compressed linear state). This is clearly communicated in Figure 1 and Section 2.2 (Eq. 1). The self-decoding property means representational capacity grows with D_θ in a way that standard compressed states cannot match.

2. **Input differences (Δxₜ) are a well-motivated design choice.** The paper draws a clear connection to continuous-time RNNs (Kidger et al.) and notes the practical benefit that weight updates slow when inputs change slowly, aiding continual learning and test-time adaptation. This is a non-trivial architectural decision that distinguishes WARP from most linear RNNs.

3. **WARP-Phys on the MSD dataset shows a striking empirical result.** MSE of 0.03×10⁻² (vs. next-best Transformer at 0.34×10⁻², and WARP itself at 0.94×10⁻²) is a genuine order-of-magnitude improvement (Table 3). This demonstrates the value of the prior-injection mechanism even if the comparison is not apples-to-apples against black-box baselines.

4. **Broad evaluation scope.** The paper tests across image completion (Table 1), energy/traffic forecasting (Fig. 3b, Table 2), dynamical systems (Table 3), multivariate classification (Table 4), and in-context learning (Fig. 5). This breadth is a genuine strength.

## Weaknesses

### Major

1. **The O(D_θ²) cost of the dense A matrix is a structural limitation that restricts the practical operating regime.** A ∈ ℝ^{D_θ × D_θ} means storing and multiplying A costs both O(D_θ²) parameters and O(D_θ²) FLOPs per timestep. For the reported ~1.68M total parameters on MNIST, A alone accounts for roughly 1M parameters (implying D_θ ≈ 1000 and a root MLP of only ~1000 weights). This directly limits the "high-resolution weight-space" claim — D_θ ≈ 1000 is higher-dimensional than typical SSM states (16–256), but it is a far cry from the sort of scale where dense O(D_θ²) matrices are tractable. The paper acknowledges this in Section 4.2 ("the size of the matrix A limits scaling to huge root neural networks") and defers structured A to future work, but the issue is more central than acknowledged: the very mechanism that makes the state high-resolution (weight-space parameterization) also makes the transition matrix prohibitively large for dense parameterization. This creates a built-in tension between the paper's main claimed advantage (high-resolution states) and computational practicality.

2. **The PEMS08 traffic forecasting result (MAE 6.59 vs. next-best 13.45, a >50% reduction) is stated without adequate explanation, and this undermines credibility.** Table 2 shows WARP, a general-purpose sequence model using no graph structure, beating GMAN, D²STGNN, and STDCN — all graph-aware spatiotemporal architectures — by more than 50% on MAE. The paper mentions only a "non-causal convolution" preprocessing step (referenced to Appendix D) and cites published baseline numbers from [62] rather than re-running them. An improvement of this magnitude from a generic model over specialized architectures is extraordinary and demands a mechanistic explanation in the main text (e.g., ablation of the convolution, discussion of evaluation protocol alignment). Without it, readers cannot assess whether this result reflects genuine architecture advantage, preprocessing artifacts, or evaluation discrepancies.

### Minor

3. **The WARP-Phys comparison conflates the advantage of having the correct physical prior with the advantage of the WARP architecture.** WARP-Phys on SINE* embeds the exact functional form τ ↦ sin(2πτ + φ̂) in its forward pass, so it only needs to estimate a single scalar (the phase). The comparison to black-box GRU/LSTM/Transformer that must learn the functional form from data is fundamentally uneven: the "10× improvement" claim in the abstract combines the prior-injection capability (a genuine contribution) with the architecture's inductive bias in a way that makes it impossible to disentangle their contributions. The paper should compare against grey-box versions of the baselines that also receive the parametric form.

4. **The classification results are weaker than the "top three" framing suggests.** Table 4 shows WARP achieves SOTA on 2/6 datasets (Ethanol, Heartbeat) and is third on 2 more, but on EigenWorms (the longest sequence at 17,984 steps) it scores 70.93% vs. LinOSS at 95.0% — a 24-point gap. The claim of "outperform[ing] established models such as Mamba" is selective: WARP (70.93%) beats Mamba (70.9%) by <0.03% while trailing LinOSS by 24 points. The paper should be more transparent about where WARP excels and where it falls short.

5. **The in-context learning experiment (Section 3.4) is underspecified.** No baselines are reported, the task (learning a linear mapping from random keys to values) is the simplest ICL benchmark, and the cumulative-sum input transformation is non-standard. The paper cites [102] but provides no comparison to their Transformer ICL results, making it impossible to gauge whether WARP's ICL performance is competitive or simply adequate.

6. **Several BPD values in Table 1 are anomalous and unexplained.** LSTM achieves BPD=3869 on CelebA (L=100) while all other entries are O(10⁰–10²), and WARP achieves negative BPD values on CelebA (−0.043, −0.162). Negative BPD is unusual and the 3869 outlier suggests a potential unit/scale mismatch. These need clarification.

7. **The "infinite-dimensional" RNN hidden state claim in the conclusion (Section 4.3) is hyperbolic.** θₜ is finite-dimensional (D_θ). The argument that it is "infinite-dimensional" because it parametrizes a function would apply to any parametric model. This should be removed.

### Trivial

None.

## Nice-to-Haves

- **Wall-clock/FLOPs comparison in the main text.** The paper states that Appendix E.3 contains computational efficiency metrics; given the O(D_θ²) cost of A, a main-text comparison would directly address the most important practical concern.
- **Ablation of the input-difference mechanism** (Δx vs. direct x). This is presented as a key design choice (Section 2.2) but not empirically isolated in the main paper.
- **Standard deviations for Table 1** (which reports only the best of 3 runs without variance).
- **Grey-box versions of baselines** for the WARP-Phys experiments, to isolate the contribution of the architecture from the contribution of the prior.

## Removed Points

These points from the input review were removed, with justification:

- **"The 'brain-inspired' reference (signal differences as synaptic plasticity) is speculative and adds little"** — Subjective presentation judgment, not a substantive weakness. The paper makes a minor connection to STDP in the discussion; this is a speculative motivation, not a core claim.
- **"Missing strongest modern SSMs (Mamba, S5) in Table 1"** — Mamba is included in the classification table (Table 4), and S4 is the standard baseline for the image completion benchmark used. Scope creep to demand all possible baselines for every experiment.
- **"The ETT figure reports mean MSE without variance"** — The paper states "mean MSE across three runs." Adding variance would strengthen the evaluation but is not a core flaw; the evaluation is standard for this setting.
- **"No complexity comparison to support the sub-quadratic ICL claim"** — WARP's O(T) recurrence is inherently sub-quadratic; this is architecturally guaranteed, not an empirical claim needing separate verification. The claim is valid without an additional experiment.
- **"The paper should report what fraction of the variance WARP captures relative to the best model"** — A methodological suggestion, not a weakness. The "top three" framing is unconventional but factually correct.
- **"The quadratic scaling is fatal / the method is not ready for practical deployment"** — Overstated. The paper demonstrates working results at D_θ ≈ 1000 with total params ~1.7M, which is a practical regime. The limitation is real and major, but not fatal — the paper achieves competitive results despite it, and structured-A approaches are a natural future direction.

## Novel Insights

The harsh reviewer's most valuable observation is that the A-matrix scaling is not just a "scaling limitation" but a direct structural consequence of the weight-space-as-state design. The high-dimensional weight-space representation that is WARP's main claimed advantage *creates* the quadratic cost of the transition matrix. This tension is deeper than the paper acknowledges: it is not a matter of more GPU memory, but a design-level conflict between state resolution and transition cost. This insight sharpens the paper's limitations section and points to the most important direction for future work (structured, low-rank, or diagonal A).

## Suggestions

1. **Address the PEMS08 result directly in the main text.** Add an ablation showing performance with and without the non-causal convolution, and discuss whether the evaluation protocol aligns with the published baselines. A 50%+ improvement over specialized architectures requires a clear mechanistic explanation.
2. **Clarify the A-matrix scaling tradeoff quantitatively.** Add a small controlled experiment (e.g., varying root MLP size on a simple task) with wall-clock time, memory usage, and accuracy, to show the practical operating regime readers can expect.
3. **Add grey-box baseline comparisons** for the WARP-Phys experiments (e.g., a GRU or Transformer that receives the known functional form and only needs to predict φ̂).
4. **Report standard deviations for Table 1** and clarify the anomalous BPD values (LSTM 3869, WARP negative).
5. **Tone down overclaims:** remove "transformative paradigm," "infinite-dimensional hidden states," and "human-level artificial intelligence." The paper's genuine contribution is strong enough without these.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>
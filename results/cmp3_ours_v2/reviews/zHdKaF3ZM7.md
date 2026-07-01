Now I have sufficient calibration context. Let me write the final review.

**Calibration Summary:**

| Anchor | Avg Score | Decision | Similarity | Comparison |
|--------|-----------|----------|------------|------------|
| Linear RNNs FST (I1484gDBr4) | 2.50 | Reject | 0.71 | Much less novel than WARP |
| RotRNN (z6qmomJW91) | 4.00 | Reject | 0.71 | WARP has more novel core idea but messier eval |
| Mimetic Init (iVy7aRMb0K) | 4.50 | Reject | 0.71 | Incremental (init only), WARP much more novel |
| Were RNNs All We Needed? (GrmFFxGnOR) | 5.00 | Reject | 0.72 | Similar novelty level but cleaner experiments |
| Gated RNNs discover attention (rfSfDSFrRL) | 5.50 | Reject | 0.71 | Novel theory paper, comparable quality level |
| Deep Linear Probe Gen (XoYdD3m0mv) | 6.00 | Accept | 0.72 | Cleaner but less ambitious, narrower scope |
| LinOSS (GRMfXcAAFh) | 8.00 | Accept | 0.69 | Strong theory + experiments, WARP doesn't reach this |

**Round 1 Bracket**: 4.0 – 6.0

**Narrowing**: The WARP paper has a genuinely novel core idea (weight-space as hidden state) that is more creative than the incremental anchors at 2.5-4.5, but its evaluation has more significant issues than the cleaner papers at 6.0-8.0. Its closest comparator in novelty-plus-problematic-evaluation is "Were RNNs All We Needed?" (5.00) and "Gated RNNs discover attention" (5.50). However, WARP has more extensive experiments across more domains. **Final score: 5.5**.

---

## Summary

This paper introduces WARP (Weight-space Adaptive Recurrent Prediction), a novel sequence modeling architecture that treats the flattened weights of an auxiliary MLP as the hidden state of a linear RNN. The recurrence `θ_t = A θ_{t-1} + B Δx_t` updates these weights in response to input differences, and the output is decoded by the same weights acting as an MLP ("self-decoding"). The paper evaluates WARP across image completion, time series forecasting, dynamical system reconstruction, multivariate classification, and in-context learning.

## Strengths

- **Genuinely novel architectural concept.** Using the weights of an auxiliary network as the hidden state of a linear RNN, with the self-decoding property, is creative and clearly distinct from existing sequence models (SSMs, linear attention, standard RNNs). This is the paper's strongest contribution.
- **Input-difference-driven recurrence** (Δx_t rather than x_t), motivated by Kidger et al.'s theoretical work on NCDEs, is a thoughtful design choice that creates a natural connection to synaptic plasticity and gradient-free test-time adaptation.
- **Extensive empirical scope.** The paper evaluates across many domains (images, traffic, energy, dynamical systems, UEA classification, in-context learning) with diverse baselines, demonstrating the architecture's versatility.
- **Strong results on several benchmarks.** WARP achieves best or near-best performance on multiple UEA classification datasets (Ethanol, Heartbeat, Motor), the ETT energy forecasting task, and the MSD/MSD-Zero dynamical system reconstruction tasks, with WARP-Phys showing order-of-magnitude improvements.

## Weaknesses

### Fatal

None.

### Major

- **Quadratic scaling of the transition matrix A is a structural bottleneck that is understated.** The recurrence involves `A ∈ ℝ^{D_θ × D_θ}`, meaning ~D_θ² parameters go into A alone. For the claimed ~1.68M total parameters on MNIST, D_θ ≈ 1,300, which constrains the root MLP to a single hidden layer of modest width (~400). This is not merely a hardware limitation ("experiments on an RTX 4080... could only support moderate D_θ values") — it is a structural O(D_θ²) vs. O(D_θ) ratio between the transition matrix and the root network's parameters. The paper acknowledges this in Section 4.2 but frames it as a scale-up issue rather than a fundamental capacity trade-off. Reporting D_θ and the full root MLP architecture for every experiment is essential for the reader to assess expressivity claims.

- **The PEMS08 result (>50% improvement over SOTA) lacks sufficient support for such an extraordinary claim.** The paper acknowledges that PEMS08 uses "chunk-wise forecasting which significantly differs from the setting in Fig. 2" and employs non-AR mode with non-causal convolution preprocessing. The baselines' numbers (GMAN, D²STGNN, STDCN, 2020–2022) are taken from a prior paper [62] rather than evaluated under the same protocol. No error bars or variance estimates are reported for WARP's PEMS08 result (Table 2 shows bare numbers), and the baselines may not represent the current SOTA. A result of this magnitude requires either comparison under the identical protocol or substantially more validation.

- **Root MLP architecture and D_θ values are not reported for any experiment.** The paper discusses "high-resolution" weight-space hidden states but never states what the root MLP actually is (depth, width, number of layers, activation functions) or the corresponding D_θ for any of the benchmarks. This makes it impossible to assess whether the hidden state truly provides a high-capacity representation or whether the decoder is too small to matter. This information is standard to report for any architecture paper and should be in the main text or a clearly referenced appendix.

### Minor

- **The WARP-Phys "physics-informed" claim is partially inflated.** For the SINE* dataset, WARP-Phys hardcodes the exact closed-form solution `τ ↦ sin(2πτ + φ̂)` into the root network, reducing the problem to learning a single phase parameter. While incorporating domain knowledge is a legitimate capability, the comparison against black-box RNNs/Transformers that must learn the structure from data is not informative about the weight-space recurrence mechanism itself — it demonstrates that a model with the answer's parametric form baked in outperforms models without it. The paper should clarify what physical knowledge is injected for each dataset and distinguish this from more general physics-informed learning (e.g., embedding differential equation structure).

- **The in-context learning experiment (Section 3.4) is not informative as presented.** The paper modifies the standard Von Oswald et al. ICL benchmark by taking cumulative sums of the input sequence without justifying why this modification is needed or what effect it has. No ICL baselines (not even the original Transformer from Von Oswald et al.) are compared against, and the task is small (N=31 key-value pairs with scalar output). The claim of "sub-quadratic in-context learning" is unsupported without such comparisons.

- **CelebA BPD values are anomalous.** In Table 1, BPD values across methods vary wildly: GRU (24.14–71.51), LSTM (3869–7.9), ConvCNP (1.498–248.1), WARP (0.052 to -0.162). These magnitudes suggest incompatible evaluation procedures (different likelihood parameterizations, preprocessing, or metric computation). The paper should explain the BPD computation and why WARP achieves negative BPD while other methods differ by orders of magnitude.

- **PEMS08 baselines date from 2020–2022.** The cited SOTA (STDCN, 2022) may not reflect current best results on this benchmark.

### Trivial

- Wall-clock speed and memory benchmarks are relegated to the stripped appendix (Appendix E.3). A brief summary in the main paper would help.
- PEMS08 result lacks error bars (though UEA results in Table 4 do include ± std).

## Nice-to-Haves

- Analysis of the learned θ_t trajectories (e.g., PCA/t-SNE visualization) would strengthen the claim that the weight-space hidden state encodes meaningful representations.
- Comparison against Neural ODEs / NCDEs as additional continuous-time baselines, given the theoretical motivation from Kidger et al.
- Ablation of the cumulative sum in the ICL task, showing whether WARP can also solve the standard (non-cumulative) version.

## Removed Points

The following points from the Harsh Critic input were removed for the reasons stated:

- **"Abstract 'top three' framing is misleading"** — Removed because it is factually accurate: WARP places top-3 on 4 of 6 UEA datasets (SCP2: 2nd, Ethanol: 1st, Heartbeat: 1st, Motor: 3rd).
- **"Section 1 expressivity claim is too strong"** — Removed because this is a reasonable motivational claim supported by citations; the paper is not making a formal claim.
- **"No Neural ODE baseline comparison"** — Moved to Nice-to-Have; the paper already has extensive baselines (11 methods for UEA).
- **"No analysis of learned θ_t dynamics"** — Moved to Nice-to-Have; interesting but not a core flaw.
- **"Parallel scan memory cost tension"** — The paper already acknowledges this in footnote 4. Removed as already addressed.
- **"BPD should be non-negative"** — For continuous data modeled with a Gaussian likelihood, BPD can be negative. Restated the concern as anomalous variation across methods rather than the sign of WARP's BPD.

## Novel Insights

The harsh and strength reviewers both independently identify the same key tension: the paper's core idea (weight-space linear RNNs) is genuinely creative and potentially impactful, but the empirical evaluation is uneven, with some of the most striking results (PEMS08, WARP-Phys, ICL) resting on evaluation choices that either differ from standard protocols or lack proper baselines. Neither reviewer noticed that the CelebA BPD anomalies and the missing root MLP specifications compound into a single meta-problem: the reader cannot tell whether the architecture's success comes from the weight-space mechanism itself or from favorable experimental design choices. This suggests the paper's main weakness is not any single flaw but a pattern of insufficiently rigorous evaluation of the most exciting results.

## Suggestions

1. Report D_θ and the full root MLP architecture (width, depth, activation) for every experiment in the main paper.
2. For PEMS08: either reproduce at least one baseline under the same chunk-wise protocol, or report results only on standard-format benchmarks and tone down the "over 50%" claim.
3. Replace the ICL experiment with the standard Von Oswald et al. setup (without cumulative sum) and compare against at least a Transformer baseline, or remove the ICL claims entirely.
4. Clarify what "physical constraints" are injected for each WARP-Phys dataset and explicitly distinguish "embedding the known closed-form solution" from "physics-informed learning" in the general sense.
5. Explain the BPD computation for CelebA — particularly why variance across methods is so large.
6. Fix the scaling discussion: explicitly state that |A| ≈ D_θ² while root network capacity ≈ O(D_θ), making this a structural ratio issue, not just a hardware limitation.

## Score and Decision

**Calibration anchors (all rounds):**
1. `I1484gDBr4` — Linear RNNs FST (avg 2.50, Reject). Much less novel idea.
2. `z6qmomJW91` — RotRNN (avg 4.00, Reject). Comparable novelty but weaker results.
3. `iVy7aRMb0K` — Mimetic Init (avg 4.50, Reject). Incremental contribution.
4. `GrmFFxGnOR` — Were RNNs All We Needed? (avg 5.00, Reject). Similar novelty level, cleaner experiments.
5. `rfSfDSFrRL` — Gated RNNs discover attention (avg 5.50, Reject). Comparable quality, novel theory.
6. `XoYdD3m0mv` — Deep Linear Probe Gen (avg 6.00, Accept). Cleaner but narrower scope.
7. `GRMfXcAAFh` — LinOSS (avg 8.00, Accept). Strong theory + experiments.

**Bracket**: Round 1 → 4.0–6.0. **Narrowing**: Closest anchors at 5.00–5.50.

**Final score**: 5.5 — The core architectural idea is novel and creative, and the experiments are extensive in scope. However, several headline results rest on evaluation choices that are insufficiently supported or compared under non-standard protocols, and the structural scaling limitation (quadratic A matrix) is understated. These issues prevent the paper from being a clear accept but also do not invalidate the core contribution.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Accept</decision>
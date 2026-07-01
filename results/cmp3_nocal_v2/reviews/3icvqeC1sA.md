## Summary

ChaosNexus introduces ScaleFormer, a U-Net-inspired multi-scale Transformer architecture for zero-shot/few-shot forecasting of chaotic dynamical systems. The model uses hierarchical patch merging/expansion to capture dynamics at multiple temporal resolutions, Mixture-of-Experts layers for cross-system specialization, and a wavelet-based frequency fingerprint for system identification. Pretrained on 20K synthetic chaotic ODE systems, it reports ~7% sMAPE improvement over the leading baseline (Panda) on a 9.3K held-out test set and demonstrates competitive zero-shot performance on global weather forecasting.

## Strengths

1. **Well-motivated architectural design (Section 3.2).** The paper correctly identifies that chaotic dynamics exhibit multi-scale temporal structure — fast oscillations and slow trends coexist, and single-resolution architectures (Panda, DynaMix) may truncate long-range dependencies or oversmooth fast oscillations. The U-Net encoder-decoder with hierarchical patch merging/expansion is a natural and principled fit for this property. This is a genuine architectural insight, not an arbitrary design choice.

2. **Clean methodological description (Sections 3.1–3.4).** The architecture is described with sufficient detail: dual axial attention with O(S²+V²) complexity, RoPE embeddings, the MoE formulation with a shared expert plus top-K specialist experts (Eqs. 1–4), patch merging/expansion (Eqs. 5–6), wavelet scattering for the frequency fingerprint, and the MMD-based attractor regularization (Eq. 10). The paper is upfront about adopting the Koopman-theoretic patch embedding from Panda.

3. **Large-scale synthetic evaluation (Section 4.1).** Zero-shot evaluation on 9.3K held-out chaotic systems provides a statistically meaningful testbed. The use of multiple attractor-statistic metrics (correlation dimension, KL divergence of attractors, Lyapunov exponent, weighted mean energy) beyond point-wise accuracy is appropriate for chaotic systems and goes beyond common practice.

4. **Qualitative attention analysis (Section 4.4, Figure 5).** The visualization of shallow vs. deep layer attention patterns across systems with varying regularity offers genuine interpretability, confirming that the model learns multi-scale representations — shallow layers capture high-frequency local patterns while deep layers attend to global structure. This is the strongest mechanistic evidence in the paper that the architectural design functions as intended.

## Weaknesses

### Fatal

None.

### Major

1. **The paper overstates its attractor-statistics results (Section 4.1, Figure 2).** The abstract and Section 4.1 claim "notable improvements in the fidelity of long-term attractor statistics" and "superior fidelity." The data in Figure 2 tells a more nuanced story. On the correlation dimension error (D_frac), the paper reports the value 0.203 — but the figure caption clarifies this is the **median**, while ChaosNexus's **mean** D_frac is ~0.225. Panda's mean D_frac is ~0.200, meaning **Panda achieves better average performance on this primary attractor-geometry metric**. On D_step (KL divergence of attractors), the models are essentially tied (~1.2). The paper text (line 164) uses the ambiguous term "average" when reporting the median value (0.203) and frames this as evidence of "superior fidelity," but a fair mean-to-mean comparison does not support this conclusion for the attractor metrics. The actual advantage over Panda is limited to point-wise sMAPE (~7% relative improvement, ~70 vs. ~75), which is real but narrower than the headline claim. The paper should report both mean and median transparently and qualify the "superior fidelity" claim.

2. **The weather evaluation does not isolate the architectural contribution (Section 4.2, Figure 3).** The main weather experiment compares ChaosNexus (pretrained on 20K synthetic systems + fine-tuned on WEATHER-5K) against baselines (CrossFormer, FEDFormer, Koopa, PatchTST, Transformer) that are **trained from scratch** on WEATHER-5K alone. This conflates two factors: (a) the benefit of large-scale pretraining on synthetic chaos data, and (b) the benefit of the multi-scale architecture. Any pretrained model would be expected to outperform from-scratch training in low-data regimes, so this comparison cannot support the paper's claim that the *architecture* drives the improvement. The critical controlled comparison — ChaosNexus vs. Panda (same pretraining corpus, similar parameter count) on the same fine-tuning protocol — is mentioned only in a single sentence (line 217) with details relegated to the appendix. Controlled results against Panda on weather should be featured prominently in the main text, not deferred to the appendix.

### Minor

3. **Scaling "insight" largely corroborates prior work (Section 4.3, Figure 4).** The paper frames the finding that "generalization stems from system diversity rather than data volume" as a key contribution (abstract, conclusion). However, the paper explicitly acknowledges (line 237) that "prior work, such as (Lai et al., 2025), establishes the scaling law for system diversity, which our Figure 4(c) corroborates." The complementary finding in Figure 4(b) — that increasing per-system trajectories yields negligible gains — is a logical corollary of the same principle, not an independent discovery. The framing as a novel "key insight" overstates the contribution.

4. **No ablation summary in the main text (Section 4).** The paper's novelty rests on three architectural components: the multi-scale U-Net (ScaleFormer), per-scale MoE layers, and the wavelet-based frequency fingerprint. All ablation studies are deferred to the appendix (line 146). While deferring ablations to the appendix is common practice, the paper would benefit from at least a summary table in the main text showing the contribution of each component (e.g., comparing the full model against a single-resolution variant with matched parameters). Without this, readers cannot assess which design choices drive the reported improvements.

5. **Imprecise weather results in Figure 3.** The values in Figure 3 are reported as approximate (~0.8, ~3.5) rather than exact numbers with confidence intervals or standard deviations. The text claims "mean error strictly below 1°C" — but ~0.8 with no error bars is insufficiently precise. Exact figures should appear in the main text.

### Trivial

None.

## Nice-to-Haves

- The MMD regularization (Eq. 10) uses "a mixture of rational quadratic kernels" but does not specify kernel parameters or how they were chosen. These could be summarized in the main text.
- The loss weights λ₁ and λ₂ are mentioned but not given numerical values in the main text.
- Direct comparison against Panda on WEATHER-5K with identical fine-tuning protocols would substantially strengthen the real-world claims.

## Removed Points

These points are flagged to be removed; treat them with caution.

- *"The comparison against general-purpose time-series foundation models (TimesFM, Chronos, Moirai-MoE, etc.) is informative but predictable — these models were not designed for chaotic dynamics, so their poor performance is expected."* — This is a judgment about experimental design choices, not a verifiable weakness of the paper. The baselines are reasonable for a zero-shot evaluation and the paper includes Chronos-S-SFT (fine-tuned on the chaos corpus) to partially address domain mismatch.
- *"Loss weight and kernel parameter specification... should be stated in the main text, not only in the appendix."* — Demoted to Nice-to-Haves.
- *"Requesting confidence intervals for large-scale benchmarks where single-run evaluation is the norm"* — Variants of this appeared in the input; confidence intervals are partially addressed via the Figure 2 inset plots. The Figure 3 precision issue (imprecise ~0.8 values) is retained as Minor #5 since it's about exactness, not about CI methodology.

## Novel Insights

The main meta-insight from synthesizing the reviews is that the paper's central claim — "superior fidelity of long-term attractor statistics" — is undermined by the paper's own data when means (rather than medians) are compared: Panda achieves a better mean correlation dimension error (0.200 vs. 0.225). The paper's text obscures this by reporting the median (0.203) and using the ambiguous term "average." Additionally, the weather evaluation is fundamentally set up to conflate the benefit of pretraining with the benefit of the proposed architecture, making the real-world claims difficult to evaluate. These two issues together mean the paper's headline contributions are narrower than advertised.

## Suggestions

1. **Clarify the attractor-statistics reporting.** Report both mean and median for D_frac in the main text. Qualify the claim of "superior fidelity" to accurately reflect that: (a) sMAPE shows a ~7% improvement over Panda, (b) D_step is comparable, and (c) D_frac mean is slightly worse than Panda while the median is competitive.

2. **Restructure the weather evaluation.** Replace the main weather comparison (pretrained ChaosNexus vs. from-scratch baselines) with a controlled comparison against Panda under identical fine-tuning protocols. The from-scratch baselines can remain as a secondary reference but should not be the headline result.

3. **Add a single-resolution ablation to the main text.** The cleanest test of the core thesis is to compare ChaosNexus against a variant without patch merging/expansion (same params, same pretraining data). A summary table in Section 4 showing this would directly address the paper's central claim.

## Score and Decision

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>
Now I have strong calibration anchors. Let me produce the final consolidated review.

## Summary

PI-CCA proposes a replay-free continual learning method for vision-language models that preserves cross-modal alignment by storing a compact "CCA certificate" (canonical correlations and sketched subspaces) and enforcing consistency via spectral and subspace losses computed from mini-batch statistics. The method achieves SOTA results across four VL-CL benchmarks (MTIL, X-TAIL, VLCL, ConStruct-VL) among replay-free approaches, and ablation studies confirm the contribution of each component.

## Strengths

- **Principled problem framing.** The paper identifies that prior VL-CL methods regularize proxy signals (logits, similarities, parameters) rather than the alignment geometry itself, and designs the method around this insight (Section 1). The CCA certificate captures canonical correlations and subspaces of the whitened cross-covariance—the natural invariants of cross-modal alignment. This is a conceptually clean departure from prior work.

- **Consistent SOTA across all four tracks.** Tables 1–2 show PI-CCA outperforming a broad set of contemporary baselines (ZSCL, Mod-X, C-CLIP, MG-CLIP, Proxy-FDA, etc.) on classification (MTIL, X-TAIL), retrieval (VLCL), and structured concepts (ConStruct-VL). The gains over the next-best replay-free method are meaningful (e.g., 76.8 vs 75.2 Avg on MTIL; 48.6 vs 46.1 I2T R@1 on VLCL). The empirical case is strong.

- **Thorough component ablation.** Table 3 systematically ablates each loss term, EMA mechanism, spectral moment, pairing strategy, and sketch type. Degradation patterns are coherent and interpretable: removing the spectral term (−2.5 pt on MTIL Avg) or subspace term (−2.2 pt) causes the largest damage, consistent with the method's motivation. The fact that the sorted surrogate and exact Hungarian pairing yield nearly identical accuracy (76.7 vs 76.8) is a practical validation.

- **Efficiency-conscious design.** The Pareto analysis over certificate capacity (k, h) in Figure 2 shows genuine engineering consideration, identifying a broad efficient ridge near (k, h) = (64, 256). The constant-memory property (O(kh) storage) is backed by the method design.

## Weaknesses

### Fatal
None.

### Major

- **Figure 3 reports correlation values that are not credible as descriptions of real experimental data.** The caption states Pearson r = 1.00 and Spearman ρ = 1.00 for three of four panels, and 0.99/1.00 for the fourth. The paper describes this as coming from a sweep over "realistic perturbations (certificate size, EMAs, invariance strength, whitening, pairing, LoRA capacity/LR, sketch type)" — which should yield many independent data points. A Pearson correlation of 1.00 means points lie *exactly* on a line with zero residual; a Spearman ρ of 1.00 means *every single pair* has ranks in perfect agreement. With any realistic number of data points from distinct experimental conditions involving stochastic optimization, this is essentially impossible. Possible explanations (very small N, deterministically confounded metrics, or computational error) are each damaging to the claim that "stability of the canonical subspace/spectrum reliably predicts downstream performance" (Conclusion). **This does not invalidate the method itself** — the benchmark results (Tables 1–2) and ablations (Table 3) stand independently — but the correlation evidence as reported is not credible and must be corrected or removed. The paper's core contribution survives, but this secondary thesis is unsupported as presented.

### Minor

- **Streaming EMA dynamics under task shifts are unanalyzed.** Equations 12–13 define separate EMA rates β (covariance) and α (certificate), but the paper does not analyze how their interaction behaves across domain transitions. When the model moves from one domain (e.g., "Location") to another (e.g., "Count"), the EMA covariance will gradually reflect the new domain's distribution while still containing decayed signal from prior domains. The whitened cross-covariance M^(t) computed from these EMAs may not represent the current task's alignment geometry well, potentially creating a mismatch with the certificate. The ablation (Table 3) shows that disabling either EMA degrades performance, but this does not characterize the joint dynamics over long task sequences. This is a depth-of-analysis gap, not an error.

- **Sketch-based subspace loss approximation guarantees are not established.** The paper claims (Section 3.3) that the Frobenius distance between sketched projectors "preserves order/angles under near-isometric sketches (e.g., Gaussian/SRHT)." However, standard Johnson–Lindenstrauss bounds apply to distances between individual points, not directly to ‖RᵀP₁R − RᵀP₂R‖_F (a quadratic form in the sketch matrix). The paper calls this a "surrogate" but provides neither formal bounds nor experiments quantifying how sketch dimension h affects the fidelity of this approximation. Given that L_sub is one of the two key regularization terms, this gap warrants attention.

- **No direct computational cost comparison against baselines.** The Pareto analysis (Figure 2) shows internal tradeoffs for PI-CCA's hyperparameters, but the paper does not report per-step wall-clock time or peak memory for baseline methods (C-CLIP, ZSCL, etc.) on the same hardware. Since PI-CCA requires an SVD per step (even with block power iteration), a reader cannot assess its practical computational overhead relative to existing methods.

### Trivial
None.

## Nice-to-Haves

- A controlled experiment where the certificate is intentionally corrupted (random spectra/subspaces or a certificate from a different domain) to directly test whether it is the *correct* alignment geometry that produces the benefit, rather than just any regularization.
- An analysis showing that geometry drift predicts retention even after controlling for total parameter change (‖Δϕ‖), to rule out the possibility that geometry drift is merely a proxy for overall model change.
- Locating baseline methods on the same memory-performance plane (Figure 2) for direct practical cost comparison.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **Code not released during review** (Harsh Critic): "Code is not released during review... regrettable given the correlation concern." — The paper explicitly states the reason (ongoing commercial use) and commits to release upon acceptance. The hard rules state that criticism questioning availability of cited entities should be removed; while the authors' own code is a slightly different case, this point is more about policy than scientific validity and does not belong in a technical review.

- **"The correlation analysis in Figure 3 reports correlations that are effectively impossible"** — This IS kept as a Major weakness above. The removed version here is just the framing from the "Missing Parts" section that said "Figure 3 must be corrected," which is redundant with the already-captured Major weakness.

- **"Section-by-Section Notes" general observations** (e.g., "Introduction is clearly stated," "Related Work is comprehensive") — These are area-of-concern sweep notes from the harsh critic, not specific weaknesses. They are either neutral observations already reflected in the strengths or not actionable.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Fix Figure 3.** Clarify the number of data points, verify the correlation computation, and report honest statistics. Even correlations of r ≈ 0.85–0.95 with clear trends would support the claim. If the data genuinely lie perfectly on a line, explain why (e.g., deterministic relationship between the metrics or very small N). If the evidence is insufficient, downgrade the claim appropriately.

2. **Add baseline computational costs.** Report per-step wall-clock time and peak GPU memory for at least the top-3 replay-free baselines on the same A100-80GB hardware used in the Pareto analysis.

3. **Acknowledge the EMA interaction dynamics** as a limitation or provide analysis in the appendix, particularly for long task sequences.

4. **Characterize the sketch approximation error** empirically by showing how L_sub's Frobenius distance correlates with the true subspace angle as a function of sketch dimension h.

---

**Calibration.** I retrieved 24 anchor papers across 6 score bands. Key anchors: C-CLIP (avg 6.50, accepted) — comparable scope but PI-CCA has stronger results and more principled method; TiC-CLIP (avg 6.25, accepted) — benchmark-heavy contribution with different focus; Adapting MLLM to Concept Drift (avg 7.00, accepted) — similar strength with novel theoretical framing; Learning without Forgetting for VLMs (avg 5.67, rejected) — fundamental concerns about method effectiveness; Continual LLaVA (avg 4.75, rejected) — benchmark contributions weakened by insufficient evaluation. PI-CCA is stronger than all sub-6.5 anchors due to its principled method, consistent SOTA across four benchmarks, and thorough ablations. It is comparable to the 7.0 anchor but has a distinctive data-quality blemish (Figure 3). **Round-1 bracket:** 6.0–7.5. **Final score:** 7.0 — a solid accept with a fixable evidential issue in the secondary analysis.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>
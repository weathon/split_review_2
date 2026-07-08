I have all the information needed. Let me write the final review.

## Summary

The paper proposes Augmented Intermediate Representations (AIR), a method to inject instruction hierarchy (IH) signals into every decoder layer of a transformer via layer-specific trainable embedding tables — rather than only at the input layer as prior work does. The aim is to prevent the IH signal from attenuating through depth. Evaluated on multiple models (3B, 7B, 8B) and training methods (SFT, DPO) against gradient-based prompt injection attacks, AIR achieves 1.6× to 9.2× reductions in ASR compared to the ISE and Delimiter baselines, with negligible parameter overhead (~0.4M for an 8B model).

## Strengths

- **The method is clean, simple, and parameter-efficient**: adding ~0.4M parameters to an 8B model (0.005% increase) by inserting layer-specific trainable embedding tables into each decoder block. The analogy to RoPE distributing positional information across layers provides good intuition for the design. **[weight=9.79]**

- **Consistent and large improvements on gradient-based attacks** across 3 model families (3B, 7B, 8B) and both training regimes (SFT, DPO). Table 1 shows AIR reduces ASR substantially vs Delim and ISE in nearly all configurations, with differences often being orders of magnitude (e.g., Llama-3.2-3B Astra SFT: AIR=0.1% vs Delim=14.5%; Qwen-2.5-7B Astra SFT: AIR=2.4% vs ISE=39.2%). **[weight=10.72]**

- **Broad evaluation by the standards of the sub-area**: 3 model scales, 2 training methods (SFT, DPO), 4 static + 2 gradient-based attack types, plus the SEP benchmark, and two utility metrics (AlpacaEval 2.0 win rate, SEP utility score). The GCG loss curves (Figure 7) include standard deviation bands. **[weight=9.95]**

## Weaknesses

### Fatal
None.

### Major

- **The motivating experiment (Figure 3) contains an anomalous and unexplained result for the Delimiter baseline**, which shows cos-sim=1.0 across all decoder layers. This is problematic because Delim demonstrably reduces ASR in Table 1 (e.g., Llama-3.2-3B GCG: 77.5%→38%), so the metric used to support the claim that "IH signals degrade with depth" appears insensitive to how Delim actually works (its mechanism operates through attention modulation via special tokens, not through representation modification). The paper uses Figure 3 as primary motivation but does not explain this discrepancy. The ISE curve (0.55→0.92) alone still supports the degradation claim, so this weakens rather than invalidates the motivation. **[weight=4.30 — MAJOR severity]**

### Minor

- **The comparison between AIR and ISE is confounded by a difference in IH-related parameter count.** AIR adds (32+1)×3×4096 = ~0.4M parameters while ISE adds 3×4096 = ~12K, a roughly 33× difference. Although 0.4M is tiny relative to the 8B model (0.005%), an ablation controlling for capacity (e.g., AIR injecting at a subset of layers, or ISE with proportionally larger embeddings) would strengthen the mechanistic claim that multi-layer injection per se is responsible for the improvement. **[weight=7.68]**

- **No statistical uncertainty is reported for any ASR result in Table 1** — all are point estimates without confidence intervals, error bars, or mention of multiple runs or random seeds. While the main AIR improvements are large enough (orders of magnitude) that this doesn't threaten the core conclusions, for configurations where numbers are close (e.g., SEP scores of 3.1 vs 3.1 for Llama-3.1-8B) the lack of variance reporting limits assessment. **[weight=5.16]**

- **The utility analysis frames the comparison as "AIR does not significantly degrade utility compared to None"** (line 198), but the "None" baseline underwent only non-adversarial instruction tuning while AIR went through an additional adversarial robustness stage. The within-pipeline comparisons visible in Figure 6 (AIR vs Delim vs ISE, all trained identically) are more informative and actually favor AIR, so this is primarily a framing issue rather than an evidential one. **[weight=6.38]**

- **The paper does not discuss why SFT+None (adversarial training without any IH mechanism) sometimes matches or outperforms SFT+Delim and SFT+ISE** on some configurations (e.g., Llama-3.2-3B GCG: SFT-None=38, SFT-Delim=38, SFT-ISE=48.1). This observation is visible in Table 1 but not acknowledged or analyzed, and it raises questions about whether IH injection always helps over adversarial training alone. **[weight=4.32]**

- **The paper does not discuss adaptive attacks** — whether an attacker aware of AIR could design adversarial prefixes that target or bypass the layer-specific embeddings. This is a standard consideration in security papers. **[weight=4.55]**

### Trivial
- The formal alignment function A(O,I) defined in Section 2 is not used in the evaluation (which uses literal string match or logit-based likelihood for ASR measurement). **[weight=1.00]**

## Nice-to-Haves
- Analysis/visualization of what the learned IH embeddings encode across different layers (e.g., do early layers encode coarse distinctions that later layers refine?).
- An ablation testing whether sharing the same embedding table across all layers (instead of separate per-layer tables) would perform similarly — this would help isolate the multi-layer distribution mechanism from total capacity.
- Adaptive attack discussion.

## Removed Points
- The critic's claim that the Figure 3 Delim anomaly "undermines the core premise" — downgraded from Fatal to Major because the ISE curve alone (0.55→0.92) provides sufficient evidence of IH signal degradation, and AIR's empirical advantage over ISE in Table 1 independently supports the contribution regardless of the Delim artifact.
- "Missing detail about privilege level assignment" — the paper specifies this clearly in Section 5.3 ("P0 is assigned to system and user instruction tokens...").
- The critic's claim that improvement should be qualified as "gradient-based only" — the abstract explicitly says "on gradient-based prompt injection attacks."
- Section-by-section observations about different LR and GCG steps for SFT vs DPO — these are standard procedural differences, not confounds.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. **Resolve the Figure 3 anomaly**: explain why cos-sim=1.0 for Delim is expected given its mechanism, or use a metric that captures attention-mediated IH effects.
2. **Add a capacity-controlled ablation**: compare full-layer AIR against AIR at a subset of layers (e.g., layers 0, 8, 16, 24) with matched total IH parameter budget, to isolate the effect of multi-layer distribution.
3. **Report statistical uncertainty**: at minimum state number of random seeds used; add confidence intervals for near-tic configurations.
4. **Discuss the SFT+None observation**: why does adversarial training without IH sometimes match or exceed Delim/ISE?
5. **Add adaptive attack discussion**: what happens when the attacker knows about layer-specific embeddings?

## Score and Decision

**Round 1 bracket**: [5.5, 7.5] — paper is clearly above the reject-range anchors (PFT=4.25, AutoHijacker=4.25) and comparable to or above borderline-accept anchors (ISE=6.0, SEP=6.67). Not in the top tier (8.0+).

**Anchors consulted**:
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/sjWG7B8dvt.md` (ISE paper) — avg 6.0, Round 1, itemized. ISE is the direct baseline that AIR improves upon; its strengths avg ~8.1 vs our ~10.15. Our weaknesses slightly heavier (avg 4.77 vs 4.4) but none threaten the core empirical contribution.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/0VZP2Dr9KX.md` (Baseline Defenses paper) — avg 5.25, Round 2, itemized. Had fundamental issues (single-attack study, inconsistent evaluation) that our paper does not share.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/8EtSBX41mt.md` (SEP paper) — avg 6.67, Round 2, itemized. A benchmark paper in the same problem area; our strengths are substantially stronger (10.15 vs 8.08 avg) while our weaknesses are heavier (4.77 vs 3.22).

**Weighted-item comparison**: The paper shares with the ISE anchor the high-weight positives of a clean, effective method backed by broad evaluation; it lacks the ISE paper's negative-weight criticisms about clarity and novelty. The highest-weight weakness (capacity confound at 7.68) is not a validity threat — it calls for an ablation to strengthen the mechanistic claim, but the empirical results (orders-of-magnitude ASR reductions) stand regardless of whether the advantage comes from multi-layer injection or slightly more IH capacity. On balance, the paper's strengths (avg 10.15 vs ISE's 8.1) substantially exceed those of the nearest anchor, placing it clearly above 6.0 and in the upper half of the bracket.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>
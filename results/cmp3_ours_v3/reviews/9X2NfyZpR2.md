Now let me synthesize my final review.

**Calibration Summary:**

**Round 1 bracket search:**
- Strong reject range (<1.5): No relevant matches found (unrelated topics)
- Reject range (1.5–3.5): Unrelated papers (object-centric learning, anomaly detection)
- Low-to-mid range (3.5–5.5): Actions-to-Action (4.40, Reject) — had fundamental ablation flaws; Adaptive Memory (4.60, Reject) — limited baselines; Weakly Supervised Skilled Activity (4.75, Reject) — overclaimed results, no confidence intervals
- Mid-to-high range (5.5–7.5): AntGPT (6.25, Accept) — SOTA LTA, minor weaknesses; Action Sequence Augmentation (6.50, Accept) — solid but limited novelty; Weakly Supervised VidSGG (6.00, Accept) — solid contribution with minor gaps
- High range (7.5–8.5): Unrelated (novel view synthesis, video generation)
- Very high range (>8.5): No matches

**Round 2 narrow (4.5–6.5):** Confirmed: AntGPT (6.25), Weakly Supervised VidSGG (6.00), Weakly Supervised Skilled Activity (4.75), Interaction-based Segmentation (5.00)

**Initial bracket:** The paper sits between 4.5 and 6.0. It has stronger novelty than the 4.4–4.75 papers but weaker evaluation rigor than the 6.0–6.5 papers.

**Narrowing:** The paper's contribution (first transcript-only LTA) is genuinely novel and better-motivated than the 4.4–4.75 papers. However, the ablation methodology issue (using stochastic Top-1 instead of deterministic) and missing variance are more significant than the minor weaknesses in the 6.0–6.5 papers. Final score: **5.0**.

---

## Summary

This paper proposes TbLTA, the first framework for dense long-term action anticipation (LTA) trained exclusively from video transcripts — ordered action lists without timing, duration, or boundary annotations. It uses a temporal alignment module (ATBA) to generate pseudo-labels, cross-modal attention to ground video features semantically, CTC loss for alignment, and CRF for prediction coherence. On Breakfast at 30% observation, the deterministic variant achieves 40.28 MoC (10% horizon), outperforming all supervised baselines. This is a novel and well-motivated contribution to reducing annotation cost for LTA.

## Strengths

- **First transcript-only LTA framework.** The paper genuinely pioneers transcript-level supervision for dense LTA, where all prior work required at least some frame-level labels. The only prior weakly-supervised LTA work (Zhang et al., 2021) still uses frame-level labels on the observed segment. This is clearly stated and defensible (lines 31–35, 69–76).

- **Strong deterministic result on Breakfast at 30% observation.** The deterministic TbLTA achieves 40.28 MoC (10% horizon, Obs 30%), outperforming every supervised baseline including ActFusion (35.79), FUTR (32.37), and Cycle Cons. (29.66) (Table 1). This is genuinely surprising and the paper's most compelling evidence that transcript-level supervision can capture procedural structure that frame-level supervision misses, given Breakfast's strong procedural regularities.

- **Coherent architectural design.** The integration of ATBA-based temporal alignment, CTC loss, cross-modal attention with gated residual update (Eqs. 1–2), and CRF-based coherence into a single training pipeline is well-engineered. The cross-modal attention module with local masking and gated residual update is the most novel architectural piece, and the full pipeline is clearly motivated (Section 3).

## Weaknesses

### Fatal
None.

### Major

- **Ablation study confounds representation quality with sampling breadth.** The ablations in Table 4 are performed on the stochastic Top-1 variant (line 231: "we report results using the Top-1 MoC metric"), not the deterministic one. The "TbLTA" values in Table 4 match the stochastic Top-1 column in Table 1, not the deterministic column — e.g., 50Salads Obs 20%/10%: Table 4 shows 33.8, matching the stochastic Top-1 value 33.76, while the deterministic is 24.90. Ablating components (CRF, cross-attention, duration) on the best-of-N metric conflates the quality of the learned representation with the breadth of the sampling procedure. We learn about each component's contribution to the *best possible sample*, not to the *single deterministic output* at inference. The paper should report ablations on the deterministic variant (or both), since that is what the paper proposes as its primary contribution.

- **No variance or uncertainty reported for any result.** Results are averaged over multiple dataset splits (line 194), but no standard deviations, confidence intervals, or per-split numbers are given. This undermines assessment of the headline claim. On Breakfast Obs 30%/10%, TbLTA (40.28) beats ActFusion (35.79) by 4.5 points, but on Breakfast Obs 20%/10%, ActFusion (28.25) beats TbLTA (27.47). On 50Salads, TbLTA deterministic is substantially behind supervised methods across the board (e.g., 24.90 vs 39.55 at Obs 20%/10%). Without error bars, the reader cannot assess whether the positive results are significant or whether the weaker results indicate genuine limitations. This is the single highest-leverage improvement the authors could make.

### Minor

- **WS-DA baseline comparison is too sparse to be informative.** WS-DA (Zhang et al., 2021), the only prior weakly-supervised LTA method, is reported with a single number per dataset at what appears to be only the Obs 30%/10% setting (Table 1). All other cells are marked "-". Since the paper's framing treats WS-DA as the closest baseline, this sparse comparison weakens the benchmarking. The paper should at minimum discuss what settings WS-DA originally reported and acknowledge this limitation.

- **Stochastic variant mechanism is deferred to appendix.** The main paper says "we also report the stochastic protocol of Abu Farha & Gall (2019) in the supp. mat." (line 223), but the method section (Section 3) describes only the deterministic architecture. The number of samples, sampling mechanism, and temperature are not stated in the main paper. While deferring implementation details to supplementary material is standard, the stochastic variant is used for key results (Table 1 ablations, Table 4), so a brief description in the main text would improve stand-alone readability.

### Trivial
- The EGTEA results show that TbLTA (65.37 All-class mAP) trails supervised methods by ~9–11 points (Anticipatr 76.80, Timeception 74.10) — the paper's claim of being "competitive on rare classes" is accurate (60.11 vs 59.70 and 55.10) and "supervised models retain a clear edge overall" is appropriately measured. No factual overstatement.

## Nice-to-Haves

- A sensitivity analysis for loss weights (γ₁, γ₂, γ₃) would strengthen the methodological presentation.
- The large architectural differences between Breakfast (4 layers, hidden 128) and 50Salads (8 layers, hidden 512) could be briefly justified as dataset-specific tuning rather than presented without comment.
- Clarifying whether the same dataset splits are used as the supervised baselines would increase confidence in cross-table comparisons.

## Removed Points

These points from the harsh critic review were removed or downgraded:

1. **"EGTEA claims overstated"** — Removed. The paper says "supervised models retain a clear edge overall, but our method proves to be competitive on rare classes." This is factually accurate (60.11 vs 59.70 on Rare classes) and appropriately measured.
2. **"Dual claim framing blurs contribution"** — Removed. The paper clearly separates deterministic (Ours TbLTA) and stochastic (Ours TbLTA*) in Table 1 with distinct labels and captions. There is no blurring.
3. **"Stochastic variant not described in main paper"** — Downgraded from Critical to Minor. The paper states details are in supplementary material (line 223); the parser strips the appendix. Deferring implementation details to supplementary is standard practice for conference papers.
4. **"Architecture differences across datasets as confound"** — Removed. Dataset-specific architectural tuning is standard and the differences are reported transparently (line 196).
5. **"Loss weights not specified"** — Removed. Deferred to supplementary material, which is standard. Original criticism was more about completeness.

## Novel Insights

The harsh critic's most valuable observation is that the ablation study's use of the stochastic Top-1 metric creates an unrecognized confound between representation quality and sampling breadth. This is a genuine methodological concern: the paper ablates components to understand what makes TbLTA work, but the metric mixes two effects (learned representations + stochastic sampling). Addressing this by also reporting deterministic ablations would substantially strengthen the experimental story and clarify which architectural choices drive the core transcript-only contribution vs. benefit primarily from sampling diversity.

## Suggestions

1. **Report ablations on the deterministic variant** (or on both deterministic and stochastic). This is essential for cleanly attributing component contributions to the paper's primary contribution.
2. **Add standard deviations or per-split results** to all tables. This is especially important for the Breakfast 30% result, which is the paper's headline finding.
3. **Expand the WS-DA comparison or discuss its limitations** — even a paragraph explaining what settings are available from the original work would help readers calibrate the comparison.
4. **Briefly describe the stochastic mechanism in the main text** (number of samples, sampling procedure) rather than deferring entirely to the appendix.

## Score and Decision

**Score:** 5.0 — The paper has a genuinely novel and well-motivated contribution (first transcript-only LTA), with one compelling result (Breakfast 30%) and a coherent architecture. However, the ablation methodology conflates two distinct sources of performance, and the lack of variance reporting prevents assessment of significance. These issues are fixable but currently weaken the experimental evidence.

**Decision:** Reject (borderline — the core contribution is sound but the experimental presentation needs improvement before acceptance)

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>
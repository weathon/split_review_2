Now I have a clear picture. Let me write the final calibrated review.

## Summary

Pi-CCA proposes a replay-free continual learning framework for vision-language models that preserves cross-modal alignment by directly constraining the canonical correlation spectrum and subspaces via a compact, sketched CCA certificate. The method combines spectral matching, subspace-angle preservation, and prompt-invariance losses. Across MTIL, X-TAIL, VLCL, and ConStruct-VL benchmarks, it achieves SOTA among replay-free methods with consistent (1–3 point) gains.

## Strengths

- **Principled conceptual reframing (Section 3, throughout).** The insight that forgetting in VL-CL corresponds to drift in the geometry of cross-modal alignment, and that preserving this geometry via CCA spectrum and subspaces is more direct than regularizing proxy signals (logits, similarities, routing weights), is genuinely novel and well-articulated. This is not an incremental modification of existing regularization — it targets a different object entirely.

- **Methodological soundness and careful execution (Section 3.1–3.4).** The CCA certificate construction is sound: random orthonormal sketches ($h \ll d_v, d_t$) of the top-$k$ canonical subspaces plus canonical correlations give a constant-memory summary. The three loss terms (sorted spectral pairing + Ky-Fan-$k$ sum, subspace-angle Frobenius distance on sketched projectors, prompt invariance via averaged projectors) each correspond directly to specific geometric quantities. The EMA-based streaming estimation is a reasonable practical solution for the replay-free constraint.

- **Consistent empirical strength across diverse benchmarks (Tables 1, 2).** Pi-CCA achieves SOTA among replay-free methods on all four evaluation tracks — MTIL (76.8 Avg vs. 75.2 C-CLIP), X-TAIL (68.1 Avg vs. 67.4 RAIL), VLCL I2T R@1 (48.6 vs. 47.3 GIFT), and ConStruct-VL (75.2 FA / 2.7 AF). Gains are modest in absolute terms (~1–3 points) but consistent across tasks and metrics, which is more convincing than a single large gain.

- **Thorough diagnostic analysis (Section 4.3, Figures 2–5).** The paper goes beyond top-line numbers with component ablation (Table 3), certificate capacity Pareto analysis (Fig. 2), geometry-to-performance correlation (Fig. 3), prompt invariance stress test (Fig. 4), and task-order sensitivity (Fig. 5). The ablation cleanly shows both spectral and subspace terms are necessary, and prompt invariance contributes specifically to robustness.

- **Replay-free with constant memory.** The certificate is $O((d_v + d_t)h + k)$ and does not grow with data, unlike replay buffers, generators, or stored reference statistics used by many competitors.

## Weaknesses

### Fatal
None.

### Major

- **Figure 3: The reported perfect correlations (r=1.00, ρ=1.00 for two of four panels) are not credible as empirical evidence.** The scatter plots show Pearson r=1.00 and Spearman ρ=1.00 for two panels and r=0.99, ρ=1.00 for the other two. Real experimental data across diverse independent hyperparameter configurations does not produce perfect rank and linear correlation simultaneously. The paper states these points come from "sweeping realistic perturbations" — if the drift measures and performance drops are both computed relative to the same reference configuration, a near-perfect correlation may be a measurement tautology rather than an empirical discovery. The paper claims this as evidence that "preserving CCA geometry predicts retention," but the current presentation undermines rather than supports this claim. The authors should clarify what each data point represents, how many independent measurements underlie each panel, and report correlation statistics with confidence intervals rather than rounded-to-perfect values. *This issue does not threaten the paper's core contribution (which is supported by ablations and main results), but the figure as presented is misleading and must be corrected.*

### Minor

- **Backbone CLIP variant and LoRA rank are not stated in the main paper (§4.1).** The experimental setup never specifies which CLIP model is used (ViT-B/16, ViT-B/32, ViT-L/14) or the LoRA rank and which layers are adapted. These details affect the embedding dimensions ($d_v$, $d_t$), the sketch dimension $h$, and the zero-shot performance ceiling against which baselines are compared. The reproducibility statement promises this information in the appendix (which exists in the original submission but is stripped by the parser), but a single sentence in §4.1 would make the main paper self-contained on a design decision consequential for baseline fairness assessment.

- **VLCL comparison vs. GIFT (Table 2): statistical significance is unclear.** Pi-CCA reports 48.6±1.0 vs. GIFT 47.3±1.2 for I2T R@1 — a 1.3 point margin with overlapping standard deviations. Without knowing whether these are standard deviations or standard errors, or the number of seeds, it is unclear if this difference is significant. The claim of "surpassing a synthetic-replay method" should be qualified accordingly. The overall trend is clear, so this does not undermine the paper, but precision would strengthen the claim.

- **Prompt-invariance computational overhead is not analyzed.** The method computes $M+1$ SVDs per batch ($M=4$ by default, so 5× the SVD cost). The ablation (Table 3) shows removing prompt invariance costs ~1.5 points on MTIL Avg. A breakdown of wall-clock time by component would help readers evaluate whether the 5× SVD overhead is justified.

### Trivial

- **Table 1 lacks variance estimates** while Table 2 reports standard deviations. The number of seeds for MTIL/X-TAIL is not stated.

## Nice-to-Haves

- A temporal trace of certificate drift (canonical correlations and subspaces) over the full task sequence would clarify whether the certificate truly preserves the original pre-training geometry or maintains internal consistency as it drifts via EMA. The paper acknowledges the EMA refresh provides "controlled plasticity," but visualizing the drift trajectory would sharpen the narrative.
- An apples-to-apples comparison where a proxy-based method (e.g., ZSCL or Mod-X) is configured with the same LoRA rank and backbone as Pi-CCA, isolating the effect of the constraint target (CCA geometry vs. proxy signals).

## Removed Points

*These points were flagged for removal during filtering. Treat them with caution — they may reflect reviewer misunderstandings, parser artifacts, or category-driven noise rather than genuine problems.*

- **"Backbone/LoRA missing from main paper"** downgraded from Critical Issue to Minor. The information exists in the original submission's appendix (stripped by the parser). Missing from the main paper is a presentation concern, not a verification gap.
- **"Certificate EMA contradicts preservation framing"** removed. The paper explicitly acknowledges the EMA provides "controlled plasticity" (line 133) — the authors are transparent about this design choice, and the tension between "preserving" and "adapting" is openly discussed rather than concealed.
- **"Unfair comparison framing vs. C-CLIP"** removed. The claim that prior methods "regularize outcomes" is a conceptual framing choice, not a factual error about C-CLIP.
- **"w/o certificate EMA ablation still does well"** removed. This is an honest ablation result, not a weakness. The paper does not overclaim dependence on this component.
- **"Missing hyperparameters (β, γ, etc.)"** removed per hard rules — these details are in the appendix of the original submission.
- **"Missing related works"** removed per hard rules — I cannot verify the existence or absence of specific works.
- **"Unfair comparison with baselines"** removed. The asymmetry (if any) favors the baselines, not Pi-CCA, so this is not a valid complaint against the paper.

## Novel Insights

The harsh critic's key insight — that Figure 3's perfect correlations (r=1.00, ρ=1.00) likely reflect a measurement artifact rather than an empirical discovery — is valuable and should be addressed by the authors. The drift measures and performance drops are both computed relative to the same reference configuration; if they are both functions of the same underlying hyperparameter changes, the "correlation" may be closer to a mathematical identity than a discovery about generalization. This does not invalidate the method's core contribution but does mean the paper should not use this figure as independent evidence for its central thesis. The remaining diagnostic evidence (ablations, Pareto analysis, stress tests) already provides strong support without relying on this figure.

## Suggestions

1. **Correct Figure 3.** Report the actual number of distinct data points per panel, clarify what each point represents, and provide correlation statistics with proper confidence intervals. If the near-perfect values arise from a small number of unique measurements, say so explicitly.
2. **Add one sentence to §4.1** stating the CLIP backbone variant and LoRA rank/configuration.
3. **Clarify error bar conventions** for all tables, and report the number of seeds used in Table 1.
4. **Provide a computational cost breakdown** (wall-clock time per step by component) to help readers evaluate the prompt-invariance trade-off.
5. **Add a certificate drift trajectory plot** (optional but recommended) showing how $\|\rho_{1:k}^{(t)} - \rho_{1:k}^{(0)}\|$ evolves over the task sequence.

---

**Calibration.** Round 1 bracketed this paper across six score bands. Key anchors:
- C-CLIP (sb7qHFYwBc, avg 6.50, Accept): A direct baseline that our paper outperforms on all metrics. C-CLIP had weaknesses including missing related works, unclear benchmark definition, no code, and insufficient hyperparameter analysis — issues of similar or greater severity than those in our paper.
- TiC-CLIP (TLADT8Wrhn, avg 6.25, Accept): A benchmark-focused CL continual training paper.
- Vision & Language Synergy (9aZ2ixiYGd, avg 5.00, mixed 8/6/3/3): Rehearsal-free prompt-based CL, less directly related.
- Strong reject anchors (avg 1.00): Not comparable — these are clearly flawed papers.
- High-scoring anchors (avg 8.00): These are exceptional papers with unanimous accept reviews; our paper's methodological concerns (Fig. 3) and minor omissions place it below this tier.

Round 1 bracket: 6.0–7.5. Narrowing to 7.0 based on (a) the paper's stronger novel contribution and evaluation relative to C-CLIP (6.50), (b) the contained nature of the Figure 3 issue (does not threaten core claims), and (c) consistency with the Accept decision. The paper's weaknesses are all addressable in revision.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>
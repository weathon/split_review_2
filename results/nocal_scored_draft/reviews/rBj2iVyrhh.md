Now let me write the final consolidated review.

## Summary

This paper identifies a genuine limitation of existing alternating training methods for multimodal learning: while they reduce encoder-level gradient interference, the shared classifier remains vulnerable to bias from faster-converging modalities, creating an "entrenched preference" that suppresses weaker modalities. The authors propose Classifier-Constrained Alternating Training (CCAT), a two-stage framework that (1) pretrains a shared classifier with bidirectional cross-attention and a contribution-regularization term, then (2) freezes this classifier during alternating training while using modality-specific LoRA adapters to compensate for the distribution shift. A sample-level secondary update mechanism further targets severely imbalanced samples. CCAT achieves consistent improvements over baselines on CREMA-D, Kinetic-Sound, and MVSA, with particularly large gains on KS (+6.76 pp).

## Strengths

1. **Well-motivated problem framing (Section 1, Figure 1).** The paper correctly identifies that existing alternating training methods (MLA) reduce encoder-level gradient interference but leave the shared classifier vulnerable to bias from faster-converging modalities. The empirical tracking of contribution values (Figure 1) provides direct evidence that classifier bias persists even under alternating training — a genuine and previously underappreciated problem that reframes modality imbalance from an encoder-centric to a classifier-centric perspective.

2. **Classifier-freezing + LoRA strategy is architecturally sensible (Section 3.3, Eq. 9-10).** Freezing a pretrained classifier as a "decision anchor" while using modality-specific LoRA adapters to compensate for the fused→unimodal distribution shift is a clean, lightweight design. The low-rank correction mechanism preserves the frozen classifier's parameters while enabling modality-specific adaptation.

3. **Large and consistent gains on Kinetic-Sound (Table 1).** The +6.76 pp improvement over LFM on KS is substantial. Unimodal audio accuracy also improves significantly (61.65 vs. 56.40 for MMPareto), suggesting the method genuinely helps weaker modalities rather than just improving fusion.

4. **Consistent improvements across all three benchmarks (Table 1).** CCAT achieves the best multimodal accuracy on CREMA-D (85.89), KS (79.29), and MVSA (80.73), with ablations (Table 2) confirming each component contributes positively.

5. **Ablation study systematically validates the design (Table 2).** The ablation removes each component individually (Fix, Alt, Sec, LoRA), and all result in performance degradation across all three datasets, confirming that each component serves a purpose.

## Weaknesses

### Major

- **Unvalidated "mutual information" estimator (Eq. 5) is central to the method but lacks justification.** The paper relies on a quantity labeled as "mutual information" for three purposes: (i) the regularization term that penalizes contribution disparity during pretraining, (ii) the imbalance detection threshold (β), and (iii) identifying samples for secondary updates (Algorithm 1, lines 10-14). The formula MI(z_i^m, f_i) = log(N) + E_D[ log( exp(¯f_i, ¯z_i^m) / Σ_l exp(¯f_i, ¯z_i^l) ) ] does not correspond to any standard MI estimator (InfoNCE, MINE, Donsker-Varadhan) — it computes a softmax-normalized cosine similarity averaged over the dataset. The paper cites Zhou et al. (2025b) but provides no analysis of why this quantity approximates MI, what assumptions it relies on, or any validation that it correctly tracks modality contribution. This matters because all downstream components (regularization, imbalance detection, secondary updates) depend on this measurement. A controlled experiment (e.g., artificially degrading one modality and checking whether the estimator correctly identifies it) would be straightforward and informative. Without such validation, the mechanism rests on an unexamined foundation. **(This is the most significant issue; the paper's results suggest the overall approach works, but the theoretical grounding of a core component is not established.)**

### Minor

- **Abstract contains a numerical error on the CREMA-D improvement.** The abstract claims "+1.35% on CREMA-D," but Table 1 shows CCAT at 85.89% and the best baseline (LFM) at 83.62% — a difference of +2.27 pp. The other two claimed values (+6.76% on KS, +1.92% on MVSA) match the table correctly. This inconsistency must be corrected.

- **Overclaimed theoretical contribution.** Contribution (i) claims "a new theoretical framework" and "a proof" of similarity between class and modality imbalance. Section 3.1 provides gradient derivations (Eq. 1-3) showing that both class and modality imbalance involve a dominance-suppression feedback loop at the classifier-weight level. This is a reasonable observation and motivation, but it does not constitute a theoretical framework or formal proof. The analysis operates at the classifier-weight level, not at the encoder-parameter level where modality-specific gradients actually interact. Reframing this as a motivating analogy rather than a theory would better match what the section delivers.

- **No measures of variance or statistical significance.** The paper reports average accuracy over three random seeds (Table 1 caption) but no standard deviations, confidence intervals, or significance tests. Without variance information, it is impossible to assess whether the smaller gains (+2.27% on CREMA-D, +1.92% on MVSA) are reliable relative to noise. Given that many ablation differences in Table 2 are in the 1-4 pp range, variance reporting is essential for interpretation.

- **t-SNE clustering metrics computed on t-SNE embeddings (Figure 5).** The quantitative clustering metrics (Calinski-Harabasz, Silhouette, Davies-Bouldin) are computed on t-SNE projections rather than the original feature representations. Since t-SNE is a nonlinear, stochastic embedding that distorts distances non-preservingly, these metrics do not provide valid quantitative evidence about the discriminability of the learned feature space. Metrics should be computed on the original features.

- **The fused→unimodal distribution mismatch is acknowledged but not analyzed.** Section 3.3 correctly identifies that P(z^m|y) ≠ P(f|y) and proposes LoRA modules as a corrective. However, a low-rank logit-level correction cannot recover the cross-modal interactive information that the pretrained classifier was trained on (from bidirectional cross-attention fusion). The paper does not analyze whether this limitation is material, nor does it compare against training the classifier directly on unimodal inputs during alternating training (which would avoid the mismatch entirely). The ablation shows LoRA helps (removal drops 0.38-1.21 pp), but this is the smallest contribution among all components.

### Trivial

- No sensitivity analysis shown for the regularization coefficient λ (set to 0.001).
- The abstract's "over state-of-the-art methods" is vague — the best baseline varies by dataset (LFM for CREMA-D/KS, MMPareto for MVSA).

## Nice-to-Haves

- Computational cost/FLOPs comparison with baselines.
- Analysis of the secondary update frequency (what fraction of samples trigger it at the chosen β thresholds?).
- Discussion of failure cases: e.g., on MVSA, CCAT's Image accuracy (55.30) is lower than MMPareto's (59.54) — does this mean CCAT over-suppresses the image modality on this dataset?

## Removed Points

These points are flagged to be removed; treat them with caution:
- The observation that "LoRA contributes the least among all components" (Section 4.3) is a descriptive finding, not a weakness — all components contribute positively.
- The "secondary update mechanism has a potential circularity issue" is speculative without evidence.
- Several "Section-by-Section" notes (computational cost, secondary update frequency, failure cases) are nice-to-haves, not weaknesses.
- Missing related works / formatting nitpicks are excluded per filtering rules.

## Novel Insights

None beyond the paper's own contributions. The key insight — that alternating training alleviates encoder-level interference but leaves a persistent classifier bias — is the paper's genuine contribution and is well-evidenced by Figure 1.

## Suggestions

1. **Validate the contribution estimator.** Either (a) show that Eq. 5 behaves like mutual information on synthetic data where ground-truth modality importance is known, or (b) replace it with a simpler, interpretable measure (e.g., gradient norms, attention weights) and drop the MI claim.
2. **Report standard deviations** for all main results (Tables 1-2).
3. **Correct the CREMA-D number** in the abstract from +1.35% to +2.27%.
4. **Tone down Contribution (i)** — reframe the gradient analysis as a motivating analogy rather than a "theoretical framework" or "proof."
5. **Recompute clustering metrics** on the original feature space rather than on t-SNE embeddings.

## Score and Decision

The paper identifies a genuine, previously underappreciated problem (classifier bias in alternating training) and proposes a well-motivated, architecturally clean solution that achieves consistently positive results across three benchmarks. The core idea is sound and the experimental evidence (especially the large gains on KS) is compelling. However, the paper has one significant unresolved issue: the "mutual information" estimator that drives the regularization, imbalance detection, and secondary updates is not validated as a measure of modality contribution. Combined with an abstract error, overclaimed theoretical framing, and missing variance reporting, these issues prevent the paper from being fully ready in its current form. All concerns are addressable, and the method itself has clear promise.

**Score: 6** (borderline accept)

**Decision: Accept**

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>
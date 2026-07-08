## Summary

This paper introduces TD-JEPA, a zero-shot unsupervised RL method that replaces the standard one-step, on-policy, single-policy latent-predictive loss with a multi-step, policy-conditioned, off-policy temporal-difference loss. The core algorithmic insight — using TD learning to make latent prediction work across multiple policies from offline reward-free data — is cleanly motivated and correctly derived. The paper provides theoretical analysis connecting TD-JEPA to successor-measure factorization via gradient-matching arguments (Theorems 1, 3) and a policy evaluation bound (Theorem 4). Empirically, the method is evaluated on 65 tasks across 13 datasets (DMC, OGBench) covering locomotion, navigation, and manipulation with both proprioceptive and pixel observations, matching or outperforming state-of-the-art zero-shot baselines.

## Strengths

- **A clean algorithmic idea, well-executed.** The progression from one-step latent prediction (Eq. 3) through multi-policy Monte-Carlo loss (Eq. 5) to the TD variant (Eq. 7) and asymmetric encoders (Eq. 9) is clearly motivated and correctly derived. This is a genuine improvement over prior latent-predictive work that was restricted to one-step, single-policy, or on-policy settings.

- **Theoretical framework that connects latent-predictive learning to successor-measure factorization.** The gradient-matching argument (Theorems 1 and 3) generalizes prior results that were restricted to one-step or single-policy settings. Theorem 4 bridges representation quality to zero-shot RL performance. This provides a principled understanding of why the TD-JEPA objective is appropriate for zero-shot RL.

- **Extensive and well-structured empirical evaluation.** 65 tasks across 13 datasets (DMC, OGBench) covering locomotion, navigation, and manipulation with both proprioceptive and pixel observations. This is substantially larger than most prior zero-shot RL evaluations. The three-part structure (main comparison → ablations on dynamics modeling → ablation on symmetric vs. asymmetric encoders) is sensible.

- **Honest reporting of uncertainty.** The paper reports standard errors, uses a principled bolding criterion based on overlapping confidence intervals, and supplements aggregate means with a probability-of-improvement analysis (Fig. 2). This avoids the common pitfall of declaring victory based on a single aggregate number.

- **Fine-tuning results (Fig. 4) demonstrating practical value.** Showing that learned representations can be frozen for downstream offline/online RL, achieving faster adaptation than training from scratch, is a useful finding that goes beyond the zero-shot framing.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **OGBench proprioception results are more mixed than a blanket "state-of-the-art" reading might suggest.** On OGBench proprioception (Table 1), TD-JEPA (37.98±0.77) is statistically tied with HILP (37.98±1.11) and lower in mean than FB (39.04±0.66). On specific sub-tasks, the gaps are dramatic: on antmaze-me, FB achieves 51.60±2.65 while TD-JEPA achieves 20.20±2.39. The paper's own Fig. 2 confirms TD-JEPA is "only slightly preferable to FB and HILP from proprioception." The paper's claims are appropriately qualified overall, but this context is important for readers evaluating the method.

2. **The theoretical analysis relies on strong idealized assumptions (A1–A3) that are acknowledged but create a gap between theory and practice.** Assumption A3 — requiring P^{π_z} to be symmetric for all z — is essentially never satisfied in realistic environments. The paper states these can be relaxed "at the price of more involved proofs and notation" (line 157) but does not demonstrate the relaxation in the main text. The practical algorithm relies on an orthonormality regularization heuristic (Algorithm 1) that is motivated by but not derived from the theory. This is a standard limitation for this line of work, and the paper is transparent about it, but readers should be aware that the theorems serve as motivation and analytical connection rather than guarantees for the practical method.

3. **The BC regularization applied in OGBench is not fully specified in the main text.** Footnote 4 states "We additionally apply BC regularization in OGBench based on Park et al. (2025b), as detailed in App. E.6." Without the appendix, it is unclear whether this regularization was applied uniformly across all baselines or only to TD-JEPA. If applied differently, this could affect the comparison on low-coverage OGBench datasets. The authors should clarify this explicitly.

### Trivial
None.

## Nice-to-Haves

- A computational cost comparison (wall-clock time or parameter counts) would help practitioners evaluate the trade-off, as TD-JEPA trains four networks plus policies with target networks.
- Reporting sensitivity to the orthonormality regularization coefficient λ would strengthen the empirical contribution.
- Reporting d_φ and d_ψ dimensionalities and number of seeds in the main text would improve completeness.

## Removed Points

These points are flagged to be removed, treat them with caution:

- **BYOL*/BYOL-γ* comparison presentation**: The harsh critic raised concern that these methods are placed alongside standard baselines in Table 1 in a way that could mislead. However, the paper explicitly marks them with asterisks and Footnote 5 (lines 251–252) clearly states they are representation learning methods whose zero-shot instantiation is novel. This concern is adequately addressed by the paper itself.
- **Computational cost comparison request, sensitivity to λ, missing related work**: These are nice-to-haves or scope suggestions, not weaknesses.

## Novel Insights

None beyond the paper's own contributions. The key insight — that gradient descent on the latent-predictive losses matches gradient descent on explicit successor-measure approximation losses — is the paper's own contribution. The input reviews do not surface genuinely novel observations that extend beyond what the paper already states.

## Suggestions

1. Explicitly state in the main text whether BC regularization in OGBench was applied uniformly to all baselines or only to TD-JEPA.
2. Add a brief computational cost comparison (wall-clock time or parameter counts).
3. Consider reporting sensitivity to the orthonormality regularization coefficient λ.
4. Report d_φ, d_ψ dimensionalities and number of seeds in the main text.

---

**Calibration Report**

**Round 1 (Bracketing):** The paper was compared against anchors across all score bands. No topically similar papers were found in the strong-reject (score<1.5) or strong-accept (score>8.5) bands. The most relevant anchors were in the 5.5–7.5 range.

**Anchors retrieved and compared:**

| Path | Avg Score | Round | Itemized? | Comparison |
|------|-----------|-------|-----------|------------|
| `Uj0h13lVrR.md` | 1.00 | R1 | No | GFlowNets paper, not topically comparable |
| `gwZ90hFSL2.md` | 1.00 | R1 | No | Humanoid robot NLP, not comparable |
| `fnO5h1CFyh.md` | 3.00 | R1 | No | Successor representations topic but low score |
| `473sH8qki8.md` | 2.00 | R1 | No | Reward-based policy, low score |
| `o5Bqa4o5Mi.md` | 5.25 | R1 | Yes | Policy representation (π2vec) — TD-JEPA has stronger theory and wider eval |
| `X5qi6fnnw7.md` | 4.75 | R1 | Yes | Conservative World Models — TD-JEPA is more novel with better experiments |
| `s9SVlWOcLt.md` | 6.75 | R1 | Yes | Proto Successor Measure — TD-JEPA has similarly strong theory but vastly more extensive experiments (65 tasks vs 2) |
| `ms0VgzSGF2.md` | 6.75 | R1 | Yes | Self-Predictive RL — TD-JEPA has similarly strong theory but cleaner empirical support |
| `9sOR0nYLtz.md` | 6.50 | R2 | Yes | FB-CPR (humanoid zero-shot RL) — TD-JEPA has more novelty and broader evaluation |
| `rvUq3cxpDF.md` | 7.50 | R2 | Yes | Learning to Act without Actions — TD-JEPA has broader experiments and stronger theory |

**Weighted-item comparison:** TD-JEPA's strengths all carry high weights (8–11), comparable to the best anchors. Its weaknesses carry moderate weights (4–8), with none in the very low (< 2) range that drag down lower-scoring papers. The closest anchors in topic and quality (Proto Successor Measure at 6.75, Bridging Self-Predictive RL at 6.75, FB-CPR at 6.50) all have at least one major weakness — either a severe negative-weight criticism, very limited experiments, or restricted evaluation domains — that TD-JEPA does not share. "Learning to Act without Actions" (7.50) has similarly high-strength weights but several very-low-weight weaknesses (< 3) that TD-JEPA lacks.

**Final bracket:** 6.5–7.5 → 7.0.

## Score and Decision

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>
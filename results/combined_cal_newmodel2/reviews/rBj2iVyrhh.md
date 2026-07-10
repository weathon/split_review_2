Now I'll compile the final review with all the analysis.

---

## Summary

This paper identifies a genuine gap in multimodal learning: existing alternating training methods (MLA, Reconboost) solve encoder-level gradient interference but do not prevent the classifier from developing a structural preference for the dominant modality. To address this, CCAT proposes a two-stage framework: (1) pretrain a shared classifier with bidirectional cross-attention and a regularization term penalizing modality contribution disparity, then (2) freeze this classifier during modality-alternating training while using lightweight modality-specific LoRA adapters and sample-level secondary updates for severely imbalanced samples. Experiments on CREMA-D, Kinetic-Sound, and MVSA show consistent improvements over state-of-the-art baselines.

## Strengths

- **Well-motivated problem diagnosis.** The core observation — that alternating training methods solve encoder-level interference but allow the *classifier* to develop structural preference for the dominant modality — is precise and supported by empirical tracking in Figure 1. This identifies a genuine and previously under-explored gap in prior work.

- **Clean and coherent design.** The two-stage framework is internally consistent: the pretraining stage produces a balanced classifier, the frozen classifier provides a stable decision anchor during alternating training, LoRA modules bridge the distribution mismatch between fused and unimodal feature spaces, and sample-level secondary updates target the most imbalanced instances. Each component addresses a specific link in the chain of modality imbalance.

- **Consistent and meaningful gains across benchmarks.** Table 1 shows CCAT outperforms all baselines on all three datasets, with gains of +6.76% (Kinetic-Sound), +1.92% (MVSA), and +1.27% (CREMA-D) over the next-best method. These are practically significant improvements.

- **Clean ablation structure.** Table 2 systematically ablates all four components (classifier freezing, alternating training, secondary updates, LoRA), showing that the full combination produces the best result and each component contributes non-trivially.

## Weaknesses

### Fatal
None.

### Major

- **Overclaimed theoretical grounding in Section 3.1.** The paper claims a "profound theoretical isomorphism" and "proof" connecting class imbalance and modality imbalance, but the derivation is heuristic. Equation (3) decomposes the fused feature as `f = γ₁ f⁽¹⁾ + γ₂ f⁽²⁾` with "implicitly learned modality utilization coefficients" — a simplified linear representation that does not correspond to the paper's actual bidirectional cross-attention fusion mechanism. The gradient analysis offers useful conceptual intuition but is presented as a rigorous theoretical framework. This overclaim affects Contribution (i). The paper's practical value does not depend on this isomorphism being formally proven; the empirical motivation from Figure 1 is sufficient. The authors should significantly tone down this section.

### Minor

- **No variance or significance reporting.** The paper reports average test accuracy over three random seeds (Table 1) but provides no standard deviations, confidence intervals, or per-seed results. Given the magnitude of the claimed improvements (especially +6.76% on Kinetic-Sound), the reader cannot assess statistical significance. Standard deviations from three seeds are minimal to report and should be added.

- **Missing critical ablation baseline.** Table 2 always includes at least one of the four CCAT components. A baseline with none of CCAT's components (standard end-to-end jointly trained model with no classifier freezing, no LoRA, no alternating training, no secondary updates) would help establish the additive contribution of the full framework beyond what the SOTA comparison (Table 1) provides indirectly.

- **Sensitivity analysis for λ is absent.** The regularization coefficient λ (for the modality contribution disparity penalty) is fixed at 0.001 with no exploration of its impact. If this regularization term is important to the method's success, its sensitivity should be documented.

### Trivial

- **Dataset-dependent β threshold.** The imbalance threshold β is tuned per dataset (0.15 for CREMA-D, 0.30 for KS, 0.05 for MVSA) via validation grid search. While this is standard practice, it adds a tuned parameter beyond what baselines use. The paper provides a full grid search (Figure 4) showing moderate sensitivity, but a brief discussion of robustness would be helpful.

## Nice-to-Haves

- Computational cost comparison (training time of CCAT vs. MLA) would help contextualize the practical trade-offs.
- Analysis of the frozen classifier's output distribution on unimodal inputs before LoRA correction would clarify how much of the distribution mismatch LoRA needs to bridge.
- Extending the sample-level imbalance detection beyond the current threshold-based approach could improve generality.

## Removed Points

These points from the input review were removed after verification against the paper. Treat them with caution.

1. **"MI estimator is not valid"** — REMOVED. The formula in Equation (5) is an InfoNCE-style lower bound on mutual information: log(N) + E[log(exp(⟨f̄_i, z̄_i^m⟩) / Σ_l exp(⟨f̄_i, z̄_i^l⟩))], which is a standard and well-known estimator (lower bound) of mutual information from contrastive representation learning. The reviewer's claim that "this is not mutual information" is factually incorrect.

2. **"Experimental results are implausibly large"** — REMOVED. This is speculative with no evidence the results are impossible. The +6.76% gain on Kinetic-Sound comes from a multi-component method specifically designed for modality imbalance. The CREMA-D video improvement (+5.78%) is the method's stated purpose: helping weaker modalities. No evidence of unfair comparison or data leakage is provided.

3. **"Comparison fairness for unimodal evaluation"** — REMOVED. Lines 275-277 state that for MLA, MMPareto, LFM, and CCAT, unimodal results are "directly acquired from decision-level fusion outputs" — the same protocol for all. MLA also uses alternating training (same paradigm as CCAT), so the comparison between CCAT and MLA on unimodal performance is fair. The claim that CCAT has an "inherent advantage" ignores that its closest baseline (MLA) uses the same alternating training approach.

4. **"Two-stage coherence gap is insufficiently analyzed"** — REMOVED. The paper explicitly acknowledges the distribution mismatch (line 133: P(z^m|y) ≠ P(f|y)), introduces LoRA specifically to address it, and provides an ablation (Table 2 row 4) showing the impact of removing LoRA. The paper does address this gap.

5. **"t-SNE does not show modality balancing"** — REMOVED. Section 4.4 is titled "Enhancing Discriminative Space via Fixed Classifier Design" and claims improved class separability, not modality balancing. The clustering metrics (CH, SH, DB) are appropriate for this claim.

## Novel Insights

The most useful observation from synthesizing the reviews is that the paper's theoretical framing in Section 3.1 is presented as a rigorous proof/isomorphism but is actually a heuristic conceptual analogy. Importantly, the paper's practical contribution (the CCAT framework and its empirical validation) does not depend on this isomorphism being formally proven — the empirical motivation from Figure 1 is entirely sufficient. The paper would be stronger if it dropped the pretense of a formal theoretical framework and presented the class-imbalance analogy as the useful intuition it is.

## Suggestions

1. **Retitle Section 3.1.** Change from "proof"/"theoretical framework" to "conceptual motivation" or "intuitive analogy." Remove claims of "profound theoretical isomorphism." The class-imbalance analogy is genuinely useful intuition and does not need inflated framing.
2. **Report standard deviations** for all results in Table 1 (three seeds is sufficient).
3. **Add a "none of CCAT" ablation** baseline (standard end-to-end joint training) to Table 2.
4. **Include λ sensitivity analysis** (e.g., {0.0001, 0.001, 0.01}) to substantiate the regularization term's role.
5. **Comment on β robustness** — the grid search in Figure 4 suggests reasonable stability, but a brief statement would help.

## Score and Decision

**Anchors retrieved across rounds:**

| Anchor | Score | Round | Itemized | Comparison |
|--------|-------|-------|----------|------------|
| ul1cjLB98Y.md — "A Theory of Unimodal Bias..." | 5.25 | R1 | Yes | More rigorous theory but limited to linear networks; rejected for scope limitations |
| TPZRq4FALB.md — "Test-time Adaptation against Multi-modal Reliability Bias" | 8.00 | R1 | Yes | Stronger experiments and clearer framing; upper bound on CCAT comparison |
| gNoqEdT2wO.md — "A Multimodal Class-Incremental Learning benchmark" | 2.33 | R1 | Yes | Much weaker contribution; benchmark-only paper |
| 5BXWhVbHAK.md — "Can One Modality Model Synergize..." | 6.33 | R2 | Yes | Comparable: strong theory + empirical, but more severe weaknesses (-2.45 missing related work) |
| 19ufhreGTj.md — "Understanding Dimensional Collapse..." | 5.80 | R2 | Yes | Comparable scope; rejected for limited novelty despite strong experiments |

**Round-1 bracket:** 5.5–7.5. **Round-2 narrowing:** CCAT's lowest-favorability items (-0.42, 0.69) are much milder than those of the 5.80 anchor (-3.08, -3.07) and comparable to the 6.33 anchor (-2.45). Its high-favorability items (13.11, 12.72) are close to both. CCAT's weaknesses are all fixable and none threaten the core empirical contribution. The overclaimed theory is the most significant issue but can be corrected in revision without touching the method.

**Final score:** 6.0. The paper addresses a clear gap with a well-designed framework and obtains consistent SOTA results. The main weakness (overclaimed theoretical framing) is presentation-level and separable from the empirical contribution. The missing variance reporting is a concrete but easily fixable omission. With revisions addressing the theoretical overclaims and experimental reporting gaps, this would be a solid contribution.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>
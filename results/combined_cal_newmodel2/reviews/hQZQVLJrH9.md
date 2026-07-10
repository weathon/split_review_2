Now I have all the calibration information I need. Let me produce the final consolidated review.

## Summary

This paper proves that activation steering and influence-function-based data re-weighting are, to first order, equivalent — connected by a primal–dual relationship between two Jacobian subspaces. The paper derives a constructive mapping (Influence-Aligned Steering / IAS) from steering vectors to training-data influence weights and vice versa, introduces a principal-angle diagnostic $\gamma$ that characterizes when steering can substitute for influence, and provides generalization bounds. The theoretical contribution is genuinely novel and well-presented, but the experimental validation is severely mismatched to the practical claims the paper makes.

## Strengths

- **Novel and well-executed theoretical contribution.** The core insight — that activation steering and influence functions are first-order duals connected via a primal–dual relationship between $\mathcal{S}_h(x)$ and $\mathcal{S}_\theta(x)$ — is conceptually novel. The mathematical machinery (primal program P, dual derivation, spectral optimality, alignment bounds) is internally consistent and presented at the right level of formality. (favorability: 18.75)

- **The $\gamma$ diagnostic is a genuinely useful and cheap-to-compute idea.** The principal-angle scalar tells practitioners upfront whether steering can succeed, and the no-free-lunch theorem (Theorem 6.2) formalizes what was previously empirical folk intuition. (favorability: 12.45)

- **Clean identification and unification of two disconnected literatures.** The paper correctly identifies that activation steering and influence analysis have operated in parallel despite both pursuing model controllability, and offers a clean geometric unification that is well-motivated and clearly presented. (favorability: 15.71)

## Weaknesses

### Fatal
None.

### Major

- **The headline applied contribution is not demonstrated.** The paper's steering→data mapping (Corollary 1 / $\rho_{\mathbf{s}}$) is listed as a core contribution ("identify the responsible training examples," line 29; "pinpoints the fewest training examples," line 130) but is never empirically validated. No experiment computes $\rho_{\mathbf{s}}$ and shows that the top-weighted training examples are causally related to the targeted behavior. This gap between claimed and demonstrated practical payoff is the paper's most significant weakness. (favorability: -1.47)

- **Experimental scope mismatched to the practical claims.** The paper advertises tools that "scale to billion-parameter models" (line 25), yet experiments use only GPT-2 Medium (345M parameters) and ResNet-50 — neither at billion-parameter scale. No evidence of scaling is provided. (favorability: -1.36)

- **The slope = 1.50 in Figure 1 is unexplained.** The predicted vs. actual logit shift has a slope of 1.50 (not 1.0), meaning the actual effect is systematically 50% larger than the first-order prediction. The paper says this is "consistent with the expected linear regime" without any justification. A cosine of 0.978 confirms directional alignment, but the systematic magnitude bias undermines confidence in the first-order approximation and requires explanation. (favorability: 1.19)

- **Influence function fragility is cited but not addressed.** The paper references Basu et al. (2021) ("Influence functions in deep learning are fragile") but does not engage with this concern. Influence functions are known to be unstable in overparameterized models due to ill-conditioned Hessians and non-convexity. Since the duality takes influence functions as one of its two pillars, this instability is a structural concern for practical reliability that goes unaddressed. (favorability: 0.24)

- **No statistical variability reported.** Table 1 reports single numbers with no error bars, confidence intervals, or multiple runs. The toxicity differences (0.0150 vs 0.0164) are tiny absolute values that could easily be within noise range. (favorability: -2.10)

- **IAS underperforms CAA without explanation.** In Table 1, IAS (0.0164 toxicity, 13701 PPL) is worse than CAA (0.0150, 13291) on both metrics. The paper does not explain why a theoretically principled method underperforms a simpler heuristic, nor does it articulate what compensating advantage IAS offers. (favorability: -0.75)

### Minor

- **The no-free-lunch theorem (Theorem 6.2) is not directly tested.** There is no controlled experiment where $\gamma$ is small and steering is shown to fail as predicted. The paper shows $\gamma$ increases with depth (Figure 2), which is consistent but indirect evidence. (favorability: 4.48)

- **The generalization bounds (Theorem 6.1) are not empirically tested.** (favorability: 5.09)

- **The spectral optimality experiment tests only one class (horse) of one model (ResNet-50).** While the statistical significance test is appropriate (p=0.00498), this single data point provides limited validation of Theorem 5.3. (favorability: 2.31)

- **Only one baseline (CAA) is compared against for detoxification.** (favorability: -1.15)

- **The baseline perplexity of 14,333 is extraordinarily high for GPT-2 Medium on WikiText** (typical values are ~20–30), suggesting a non-standard evaluation setup that is not explained. (favorability: -0.05)

- **Equation (2) in Section 3 is mathematically inconsistent.** It writes $\Delta h^* = \mathbf{J}_{h \rightarrow y}^\top \mathbf{J}_{\theta \rightarrow y} \Delta\theta$, but the dual derivation gives $\Delta h^* = \mathbf{J}_{h \rightarrow y}^\dagger \mathbf{J}_{\theta \rightarrow y} \Delta\theta$ (Moore-Penrose pseudoinverse, not transpose). Theorem 5.2 gives the correct formula, so this is a correctable inconsistency, but it should be fixed. (favorability: 2.68)

- **No analysis of the damping parameter $\lambda$ sensitivity and no wall-clock computational cost measurements** to support the claimed efficiency. (favorability: 1.02)

### Trivial
None.

## Nice-to-Haves

- Demonstrate the $\rho_{\mathbf{s}}$ data-attribution pipeline with a concrete example.
- Directly test the no-free-lunch theorem by comparing steering outcomes at layers with high vs. low $\gamma$.
- Investigate the slope = 1.50: is it due to the damping $\lambda$, finite step size, or higher-order terms?
- Add error bars / confidence intervals to Table 1.
- Compare against additional steering methods beyond CAA.
- Include wall-clock timing measurements.
- Analyze sensitivity to the damping parameter $\lambda$.
- Characterize how large $\alpha$ can be before the first-order approximation degrades.

## Removed Points

- Various formatting/style nitpicks — these are parser artifacts, not author errors.
- Criticisms about missing appendix content — the appendix is stripped by the parser; the original submission contains it.
- The claim that "the experiments validate almost none of the applied claims" — kept substantively but reorganized as specific Major weaknesses rather than a general statement.

## Novel Insights

The reviews' most valuable insight is that the paper's theoretical contribution is strong and self-contained, but the experiments test almost none of the applied claims the paper advertises. This gap between theoretical ambition and empirical validation is the central issue. The slope = 1.50 in Figure 1 stands out as a specific unresolved anomaly that, if explained, could either strengthen or weaken the theory. The influence function fragility concern (Basu et al., 2021) is a structurally important issue that the paper should address rather than merely cite.

## Suggestions

1. **Validate the central applied claim**: Demonstrate the steering→data mapping (Corollary 1) with at least one concrete example where $\rho_{\mathbf{s}}$ surfaces causally relevant training documents.
2. **Add error bars to all quantitative results** and report multiple runs.
3. **Either provide evidence for the billion-parameter scalability claim or downscope it** to match what is demonstrated.
4. **Engage with the influence-function fragility literature** (Basu et al., 2021) and discuss how the framework mitigates or inherits these concerns.
5. **Investigate and explain the slope = 1.50** in Figure 1 — characterize when the first-order approximation is reliable and when it breaks down.
6. **Directly test the no-free-lunch theorem** by comparing steering fidelity at layers with high vs. low $\gamma$.

## Score and Decision

**Calibration summary.** All anchors retrieved across rounds:

| Anchor Path | Avg Human Score | Round | Itemized | Comparison |
|---|---|---|---|---|
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/9wjGUN65tY.md` (Conceptors steering) | 5.00 | R1 | Yes | Most similar paper (theoretical steering framework + experiments). Our theory is stronger, but conceptor paper had more thorough experiments (5 tasks). Conceptor was rejected. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/2XBPdPIcFK.md` (ActAdd steering) | 5.00 | R1 | Yes | Empirical steering paper with mixed reviews (8,3,6,3). Stronger experiments than our paper, rejected. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/z1yI8uoVU3.md` (Measuring steering effects) | 3.00 | R1 | Yes | Empirical evaluation; limited novelty. Rejected. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/Ebt7JgMHv1.md` (Subspace illusion) | 6.33 | R1 | Yes | Strong theoretical+empirical paper with broad experimental validation. Better experiments than our paper. Accepted. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/EwAGztBkJ6.md` (Gradient interpretations) | 4.00 | R2 | Yes | Theoretical paper; questionable significance. Rejected. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/dwademPdV1.md` (Concept influence) | 5.33 | R2 | Yes | Influence functions application; incremental. Rejected. |
| Various band-1 and band-6 anchors | — | R1 | No | Not sufficiently similar for close comparison. |

**Round-1 bracket (initial):** 3.5–5.5, based on comparison with conceptor (5.0, Reject) and subspace illusion (6.33, Accept) papers.

**Round-2 narrowing:** The paper's strongest items (theoretical novelty, favorability 18.75) are comparable to the strongest items in the conceptor paper (favorability ~10–13) and better. However, its weakest items (ρₛ untested at -1.47, no error bars at -2.10, underperforming CAA at -0.75) are more negative than the weakest items in the conceptor paper (-3 to -4 range). The subspace illusion paper (6.33) had both strong theory AND broad experiments, setting a higher bar our paper does not meet. This places the paper below 5.0 but above 3.0, settling at **4.0**.

**Final score rationale.** The theoretical contribution (steering↔influence duality, γ diagnostic, no-free-lunch theorem) is genuinely novel and publishable. However, the paper makes strong applied claims (scalability to billion-parameter models, practical workflow for data attribution) that are not supported by the evidence. The only downstream comparison shows IAS underperforming CAA. The slope anomaly, missing error bars, unaddressed influence-function fragility, and untested central applied claim collectively widen the gap between what the paper promises and what it demonstrates. The theory alone could justify a borderline score in a theory-friendly venue, but the claim–evidence mismatch prevents acceptance.

**Final score: 4.0 / Decision: Reject**

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>
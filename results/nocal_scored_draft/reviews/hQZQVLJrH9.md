Now I have all signals. The four Major weaknesses all score 0.00 (extremely damaging) while the strengths score 1.00 (extremely favorable). This confirms the paper has a strong theoretical core but substantially overclaims on the practical side. Let me write the final review.

---

## Summary

This paper establishes a first-order theoretical equivalence between activation steering and influence functions, showing that both are projections of the same underlying sensitivity tensor. The core contributions are: (1) a closed-form duality mapping steering vectors to signed influence measures over training data and vice versa (Theorem 4.2), (2) an alignment diagnostic γ(x) (Theorem 5.1) that quantifies when activation steering can faithfully approximate an influence-based perturbation, (3) a spectral optimality result for choosing steering directions under a norm budget (Theorem 5.3), and (4) a proposed practical workflow combining steering, data provenance, and diagnostic-driven decisions about when to switch to weight-space editing.

## Strengths

- **Theoretical unification is genuinely novel and clean.** The paper identifies a deep structural connection between activation steering and influence functions — two areas that have developed independently — and formalizes it through Jacobian subspaces and principal angles. The core idea (Section 3) that both techniques are projections of the same underlying sensitivity tensor, differing only in whether one perturbs activations or parameters, is conceptually elegant and well-supported by the chain-rule factorization (Lemma 4.1).

- **The alignment diagnostic γ(x) (Theorem 5.1) is simple, cheap, and impactful.** The observation that a single scalar — the cosine of the smallest principal angle between the activation→logit and parameter→logit Jacobian subspaces — determines whether steering can faithfully approximate an influence-based perturbation is the kind of result that could change practice. The cost (two SVDs) is negligible, and the no-free-lunch bound (Theorem 6.2) gives it formal teeth.

- **The paper is internally coherent.** The theoretical framework (primal-dual programs in Section 3, equivalence in Theorem 4.2, bounds in Section 5) is developed in a logically consistent way. Each theoretical result feeds into the next, and the practical consequences (Section 6.1: when to skip steering) follow naturally from the math.

## Weaknesses

### Fatal
None.

### Major

- **The headline data-provenance claim is not empirically demonstrated.** The paper lists "identify the responsible training examples" as its first contribution and states "one inspects the top-weighted examples to debug bias or privacy leaks" (Section 4, line 118). Corollary 1 explicitly says "see Section 7" (line 130), yet Section 7 contains no experiment showing any mapping from steering vectors back to training examples — no examples, no case study, no anecdotal trace. This is a central practical claim with zero supporting evidence. For a paper whose abstract promises "a constructive algorithm for mapping undesired behaviors back to causal training examples," this omission is severe.

- **The first-order linearity plot (Figure 1) shows slope 1.50, not the theoretically-predicted 1.0 — a 50% systematic overshoot that is neither explained nor acknowledged as a limitation.** The paper calls this "consistent with the expected linear regime" (line 239), but a slope of 1.5 means the actual logit shift is 50% larger than the first-order prediction. While the cosine (0.978) confirms directional alignment, the magnitude discrepancy undermines quantitative uses of the framework (e.g., norm budgets from Theorem 5.3). No mechanistic explanation is offered.

- **IAS underperforms CAA on both metrics in the only head-to-head comparison (Table 1) without discussion.** CAA achieves lower toxicity (0.0150 vs 0.0164) AND lower perplexity (13291 vs 13701) than the paper's own IAS method. The paper reports these numbers neutrally (line 228-235) without acknowledging or explaining the gap. If the practical value of IAS lies elsewhere (e.g., data provenance), the paper should state this explicitly.

- **Influence function fragility (Basu et al., 2021) is cited in the references but never addressed as a threat to the framework.** The entire duality rests on influence functions being meaningful — the steering vector is built from an influence-based parameter update, and the mapping from steering back to data is expressed in terms of influence scores. The damped inverse (H+λI)^{-1} is mentioned (line 52) but the damping parameter λ is never justified or ablated, and the conditions under which influence scores are trustworthy are not discussed. This matters because influence functions are known to be unstable in precisely the deep network regime the paper targets.

### Minor

- **No statistical reporting appears in any experiment.** Table 1 reports single numbers without confidence intervals or standard errors; Figure 1 shows a scatter plot without confidence bands; Figure 2 shows a single median curve without quartile ranges. For a paper making quantitative claims, this is a meaningful deficit.

- **The spectral optimality experiment (Section 7.4, Figure 3) shows that the spectral direction is statistically distinguishable from random directions (p=0.00498), but does not actually demonstrate that using this direction improves steering outcomes** (e.g., increases the target class logit more than alternative directions). The connection between the spectral significance test and practical steering quality is not made.

- **The paper claims the framework "scale[s] to billion-parameter models" (line 25) but experiments are limited to GPT-2 Medium (355M parameters) and ResNet-50 (~25M parameters).** Broader validation is needed to support the scaling claim.

### Trivial
None.

## Nice-to-Haves

- **Validate that high-γ layers (Figure 2) actually produce better steering outcomes than low-γ layers.** The paper shows γ increases with depth but never tests whether steering at L11 (γ≈0.94) outperforms steering at L4 (γ≈0.75).
- **Clarify the proof sketch for Corollary 1 (line 128).** The argument that if a measure ν with smaller ℓ₁ norm existed, one could "scale ρ_s down and still match the shift" is not self-contained or logically clear as stated.
- **Report the specific λ value used for Hessian damping and show sensitivity to this choice.**

## Removed Points

These points from the input review are flagged to be removed; treat them with caution:
- **Abstract "equivalent" too strong:** REMOVED because the paper qualifies with "to first order" and discusses the subspace inclusion condition in Section 2 assumptions. The criticism ignores this qualification.
- **Missing ROME/MEMIT empirical comparison:** REMOVED as scope creep. These are parameter-space editing methods (complementary regime, per Section 8), not activation-steering methods.
- **Perplexity numbers "abnormally high":** REMOVED as speculative — the reviewer admits it's "hard to verify" without the appendix.
- **Compute cost unclear:** REMOVED. The paper explicitly states "two backward passes per input" (line 32) and discusses the cost model (line 56).

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Either add a concrete data-provenance experiment or drop it as a headline contribution.** A qualitative case study with 3-5 examples showing that top-weighted training examples are causally related to the steered behavior would suffice. Without this, the paper's first-listed contribution is unsupported.

2. **Explain the slope 1.5 discrepancy in Figure 1.** Is it a layer-choice artifact, a nonlinearity in later layers, or a truncation effect from the pseudoinverse? If it cannot be explained, honestly bound this as a limitation of the first-order approximation rather than calling it "consistent with the expected linear regime."

3. **Acknowledge the CAA comparison transparently.** Either state what IAS offers that CAA does not (data provenance, γ diagnostic, spectral direction), or provide evidence that IAS has compensating advantages that justify the slight performance gap.

4. **Include confidence intervals or variance estimates** for the main results in Table 1 and the slope in Figure 1.

## Score and Decision

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>
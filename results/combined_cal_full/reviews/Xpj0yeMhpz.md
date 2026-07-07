Now I have all the calibration data I need. Let me compile the final review.

**Calibration Summary:**

Rounding 1 bracket: **5.5 – 7.5**. The paper's own human review (OHOmpkGiYK.md, avg 5.75 with scores 6,6,3,8) is the closest anchor. Comparing my draft's weighted items against it: my positive weights (empirical gains +5.41, scaling +5.28, principled design +4.22) exceed those of the anchor's most positive items (+3.83, +3.50, +3.26). My heaviest negatives (-3.88 for theorem overselling, -3.16 for TOFU) are considerably milder than the anchor's heaviest negative (-7.42 for model mismatch concern, which my verification shows is at least partly debatable since TARF's UA in model mismatch [91.11] is much closer to Retrained [87.76] than GA's [5.76] which overshoots). The anchor had more severe weaknesses overall (motivation -2.15, artificial problems -2.88, appendix length -2.06).

Other anchors: TLBPjECC5D (avg 5.25, heavily criticized for incremental novelty -7.90), CGfWyU28Pd (avg 4.50, criticized for insufficient contribution -7.48 and -8.08), bKQJzuBSRJ (avg 6.00, criticized for lack of technical depth -8.49 but praised for experimental evidence +6.54). This paper fares better than all of them in novelty and is comparable on empirical evidence.

Final score: **6.5** — between "borderline accept" and "accept", reflecting a genuine novel contribution with strong empirical support but some overclaiming in theory and uneven depth in downstream experiments.

---

## Summary

This paper decouples the class label from the target concept in machine unlearning, introducing a formal taxonomy of four scenarios (all matched, target mismatch, model mismatch, data mismatch) based on whether the label domains of the forgetting data (L_D), model output (L_M), and target concept (L_T) coincide. The authors diagnose why existing class-wise unlearning methods fail in the mismatch settings and propose TARF (TARget-aware Forgetting), a three-phase framework combining annealed gradient ascent on forgetting data with target-aware gradient descent on selected retaining data. Empirically, TARF achieves near-perfect Gap scores (within ~1% of the retrained reference) in the target mismatch and data mismatch settings where all baselines fail by a large margin.

## Strengths

- **Novel and well-motivated problem formulation.** The paper identifies an important gap: existing class-wise unlearning assumes the target concept coincides exactly with a pre-training class label, but real unlearning requests (privacy, copyright, fairness) involve semantic subsets or supersets. The formal taxonomy based on L_D, L_M, L_T (Section 3.1, Figure 1) is clean, intuitive, and genuinely expands the scope of the field.

- **Dramatic empirical gains in the hardest settings.** In target mismatch and data mismatch — where baselines fail — TARF achieves Gap scores an order of magnitude better than the best baseline. For CIFAR-100 target mismatch: TARF Gap=0.21% vs. best baseline (GA) at 8.86%. For CIFAR-10 data mismatch: TARF Gap=0.96% vs. GA at 5.89%. These are not incremental improvements; they make these problems practically feasible.

- **Systematic diagnostic experiments motivate the method.** Figure 2 and Figure 3 convincingly demonstrate *why* existing methods fail: (a) in model mismatch, entangled representations cause forgetting to spill over; (b) in target/data mismatch, the forgetting data under-represents the full target concept. This analysis directly motivates TARF's design.

- **Principled three-phase design.** TARF's phases (target identification via representation gravity, target separation via joint ascent/descent, retraining approximation) each address a specific challenge from Section 3.2. The framework is unified (Eq. 3-5) rather than an ad-hoc pipeline.

- **Strong scaling results.** The method maintains its advantages on ImageNet-1k (Table 4), demonstrating generalization to large-scale settings.

## Weaknesses

### Fatal
None.

### Major
- **Potential numerical discrepancy in Gap computation.** For SCRUB on CIFAR-10 model mismatch, computing Gap = (1/4)∑|Retained − Method| from the displayed table values yields ~3.62, not the reported 2.60. FT's Gap (5.33) and TARF's Gap (2.90) compute correctly from the same table. A similar discrepancy appears for SCRUB on CIFAR-100 model mismatch (table implies ~1.70 but reported as 2.45). Since Gap is the main aggregate metric in Table 3, the authors must verify these values and clarify whether Gap is computed from exact (unrounded) numbers or if a different formula is used.

### Minor
- **Theorem 3.2 is formally correct but its framing oversells it.** The bound follows straightforwardly from Lipschitz smoothness and the chain rule — it is not a deep theoretical insight. The paper never estimates the bound's terms (λ_max(J_θ), C_ℓ, E[d_h]) from data, nor uses it quantitatively. The real contribution is the *operationalization* via representation gravity (Definition 3.3) and the three-phase algorithm, not the bound itself. The authors should reframe Theorem 3.2 as a formal intuition.

- **The target identification phase assumes practically important information.** The paper states "we assume that the number of classes in D_un belonging to the target concept is known in target mismatch forgetting" (Section 2). In real-world unlearning, the developer may not know how many classes the reported examples span. The paper does not explore robustness to misspecifying this number, nor whether the top-k heuristic from Phase I can work without knowing k.

- **The LLM/TOFU experiment (Table 5) is too underdeveloped for convincing evidence of generality.** The metrics ("QA Prob on F.", values like 0.0009) are opaque, with no task construction or setup description in the main text. Def erring entirely to the appendix weakens what is meant to demonstrate generality. This does not undermine the core vision contribution, but it reads as an afterthought.

- **The Gap metric conflates distinct behaviors.** For example, in CIFAR-10 model mismatch, TARF (Gap=2.90) has UA diff=3.35 vs. Retrained, while SCRUB (Gap=2.60 reported) has UA diff=7.38 — a much larger deviation that the aggregate hides. Presenting per-metric absolute differences alongside the aggregate would improve interpretability.

- **MIA values below the Retrained reference go unremarked.** In several settings (e.g., model mismatch), TARF and baselines achieve MIA values *better* (lower) than the gold-standard Retrained model. This may indicate over-forgetting beyond the reference — the Gap metric would not capture this, and it deserves comment.

### Trivial
None.

## Nice-to-Haves

- Run a robustness experiment where the number of target-concept classes is *not* known, using a simple heuristic (e.g., fixed percentile threshold on accuracy drop in Phase I).
- Add a supplementary column or figure showing per-metric absolute differences (|UA_Retained − UA_Method|, etc.) alongside the aggregate Gap.
- Briefly comment in the main text on why TARF sometimes achieves MIA below the Retrained reference.

## Removed Points

These points are flagged to be removed, treat them with caution:
- "The stable diffusion experiment is purely qualitative" — case studies in concept removal are standardly qualitative; this does not weaken the paper.
- "Single-run results without error bars in main text" — the paper states means and stds are in Appendix F.7, which is standard practice for this type of paper.
- "No analysis of when TARF fails" — the Conclusion (Section 5) discusses open challenges and regimes where representation gravity weakens, partially addressing this.
- "Missing related works" — cannot verify without external sources.
- Hyperparameter sensitivity criticisms — the paper notes these are in the appendix, which is reasonable given space constraints.
- All formatting/style/typo nitpicks — these are parser artifacts, not author errors.
- Generic or speculative criticisms without concrete paper anchor.

## Novel Insights

None beyond the paper's own contributions. The harsh critic's key insight — that the Gap discrepancy for SCRUB is a verifiable numerical issue affecting the main comparison table — is a concrete finding that the human reviewers of this paper did not surface. This is worth raising but does not fundamentally change the evaluation, since TARF's own Gap values compute correctly and its advantages in target/data mismatch are far too large to be explained by a rounding issue.

## Suggestions

1. **Verify and correct the Gap values** in Table 3, particularly for SCRUB in model mismatch. Clarify whether Gap is computed from exact (unrounded) metrics or from displayed rounded values.
2. **Reframe Theorem 3.2** explicitly as a formal intuition rather than a novel analytical result. The paper's real contribution is the operationalization via representation gravity.
3. **Run robustness experiment** for the assumption about knowing the number of target-concept classes — or disclose its sensitivity as a limitation.
4. **Either develop the TOFU/SD experiments properly** with clear task descriptions and interpretable metrics in the main text, or remove them to avoid distracting from the core contribution.
5. **Add per-metric breakdowns** alongside the aggregate Gap to improve interpretability.

## Score and Decision

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>
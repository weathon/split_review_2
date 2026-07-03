Now I have all the information I need. Let me write the final consolidated review.

## Summary

This paper introduces Dig-DEC (Dual Information Gain Decision-Estimation Coefficient), a model-free complexity measure that replaces the optimism mechanism of prior work (FGQ⁺23) with an information-gain-driven exploration principle. The key technical contributions are: (i) a generalized AIR framework using an arbitrary convex divergence D, enabling mirror-descent-style analysis; (ii) removal of optimism, which allows the framework to handle hybrid MDPs (stochastic transitions, adversarial rewards) with bandit feedback without explicit reward estimators; and (iii) refined online estimation procedures that tighten regret bounds for both average and squared estimation error settings. The paper demonstrates applications to bilinear classes, Bellman-Eluder dimension, coverability, and their hybrid counterparts.

## Strengths

1. **Dig-DEC ≤ optimistic DEC + η (Theorem 13).** This is a clean theoretical result (verified in Section 6, Eq. 8-9, Theorem 13) showing that the new complexity measure never exceeds the prior optimistic DEC from FGQ⁺23 up to an additive η, establishing that Dig-DEC is at least as good as the state of the art in all stochastic settings where optimistic DEC applies.

2. **Concrete strict improvement (Theorem 14).** The paper constructs a 3-armed bandit instance (Section 6, Theorem 14) where Dig-DEC achieves constant regret while optimistic E2D suffers Ω(√T), demonstrating strict improvement can be arbitrarily large in a specific case.

3. **Generalized AIR framework with flexible divergence.** Replacing the pure-KL divergence in the AIR objective with a convex divergence D (Eq. 2, Section 4) and connecting the analysis to mirror descent (Section 4, lines 153-161) is a genuine technical contribution that simplifies and generalizes the constructive minimax theorem used in prior work. The paper demonstrates this flexibility by recovering prior model-based results with a simpler single-level algorithm.

4. **Improved estimation procedures.** The unbiased estimator construction (Section 4.2.1, line 213) using sample-splitting to obtain an unbiased product estimator is a concrete innovation. For the squared-error case (Theorem 11), the paper proves Est ≤ log²|Φ| (constant), leading to √T regret for Bellman-complete MDPs — matching optimism-based approaches for the first time with a DEC-based method.

5. **Addresses an open problem.** The paper tackles the open problem from LWZ25 of obtaining model-free regret bounds for hybrid (stochastic transition, adversarial reward) MDPs with bandit feedback.

## Weaknesses

### Fatal
None. The core technical framework is sound and the theoretical contributions are genuine. The presentation issues, while significant, are fixable and do not invalidate the underlying approach.

### Major

1. **Numerical exponent inconsistencies across abstract, introduction, and Table 1.** The abstract (line 13) claims the average-error regret bounds improve to T^{3/5} (on-policy) and T^{7/8} (off-policy). The introduction (line 33) gives T^{3/2}/T^{5/6} — using completely different exponents with a superlinear T^{3/2} that cannot be a regret exponent. Table 1 (lines 262-265) shows the average-error bounds are uniformly T^{2/3}, disagreeing with both the abstract and introduction. A reader cannot determine from the main text what the paper's actual regret exponents are. These are not parser artifacts (the fractions are clearly different LaTeX expressions) and affect the paper's headline quantitative claims.

2. **Hybrid Table 2 shows primarily superlinear T-exponents that contradict the "first sublinear regret" claim.** Table 2 (lines 291-295) lists regret bounds with T-exponents: T^{3/2} (bilinear on-policy), T^{13/8} (bilinear off-policy), T^{3/2} (bilinear star on-policy), T^{1/2} (bilinear star off-policy), T^{3/2} (coverable). Four out of five entries have exponents >1, meaning these regret bounds grow faster than T. The introduction (line 32) claims "the first sublinear regret for model-free learning in hybrid bilinear classes and Bellman-complete coverable MDPs." These are directly contradictory. Even if the derivation in the appendix (which is unavailable) would show these exponents actually yield sublinear regret after η optimization, the table as presented cannot be taken at face value.

### Minor

3. **Self-contradictory Est improvement claim (line 213).** The paper states: "our construction of the estimator improves their rate of Est from √T to T^{1/2}." Since √T = T^{1/2}, this claims an improvement from a quantity to itself. The surrounding text describing the unbiased estimator construction is technically interesting, but the claimed T-exponent improvement is nonsensical as written. The improvement may be in the bias removal or the N/log|Φ| dependence, but this is not stated clearly.

4. **Computational tractability of Algorithm 1 unaddressed.** The minimax optimization in Eq. (3) requires solving min_{p∈Δ(Π)} max_{ν∈Δ(Ψ)} AIR(p,ν;ρ_t) at each round over simplices whose dimensions scale with |Φ|×|Π| and |Π|, both of which can be huge or infinite. The paper does not discuss whether this can be solved efficiently, even approximately. This is a known limitation of the AIR/DEC literature, but the paper frames its contribution as providing a "more flexible" analysis that "nicely connects to the standard analysis of mirror descent" without providing any mirror-descent algorithm for Eq. (3). A brief discussion of approximations or FTRL-based dynamics would significantly improve the paper.

### Trivial
None.

## Nice-to-Haves

- The KL decomposition in Section 6 (lines 305-306) separating the KL term into regularization and information-gain components is insightful. A brief illustrative calculation showing why this matters for a specific MDP — beyond the 3-armed bandit — would strengthen the argument.
- A brief note acknowledging the gap between the analysis technique and practical instantiation of Eq. (3), even if pointing to standard approaches like Follow-the-Regularized-Leader or no-regret dynamics.

## Removed Points

- **Criticism about the hybrid table being "meaningless."** The critic's strong language (T^{3/2} entries being "meaningless as regret bounds") is kept as Major Weakness #2 but the severity is moderated — the bounds contradict the paper's claims but are not "meaningless" per se; they may result from an error in the table or a misunderstood derivation.
- **All reproducibility concerns about missing appendix sections.** The appendix is stripped by the parser; this is not the authors' fault.
- **Requests for experimental validation.** Not standard for pure theory papers in this line of work.
- **Formatting/typo nitpicks.** Parser artifacts, not author errors.
- **The critic's claim about the intro's T^{3/2} being a "completely different number."** While this is factually correct as a criticism, the intro exponent is included under Major Weakness #1 as part of the broader inconsistency, not as a standalone point.
- **Generic strengths about "filling a gap" or "addressing an important problem."** Too generic to be useful; only concrete, evidence-backed strengths are retained.

## Novel Insights

None beyond the paper's own contributions. The reviews do not surface an observation that the paper itself does not already make.

## Suggestions

1. **Harmonize all numerical exponents across abstract, introduction, and tables.** Decide on one consistent set of regret exponents for each setting and ensure they appear identically everywhere. This is the single most important improvement the paper needs.
2. **Clarify the hybrid table.** Either correct the superlinear T-exponents to their intended sublinear values, or explain the η optimization that renders these bounds sublinear. If the table entries are wrong, fix them. If they are correct, the "sublinear" claim in the introduction must be qualified.
3. **Fix the Est improvement claim (line 213).** State explicitly what the improvement actually is (e.g., removing bias that improves constants or log factors) rather than claiming an impossible √T → T^{1/2} improvement.
4. **Add a brief discussion of computational aspects** of solving Eq. (3), even if only to point to standard approximations.
5. **Consider adding the hybrid table derivation** to the main text or a prominently placed appendix reference, since the hybrid results are the paper's most novel contribution.

## Score and Decision

Given the novel technical framework, the concrete theoretical results (Theorems 13, 14), and the refined estimation procedures, the paper has genuine value. However, the numerical presentation is sufficiently inconsistent — with three different sets of exponents for the same settings across the abstract, introduction, and Table 1, and a Table 2 whose superlinear entries contradict the claimed "sublinear" result — that a reader cannot evaluate the paper's core quantitative claims from the main text alone. These are fixable issues but prevent acceptance in the current form.

MY FINAL SCORE: <score>5</score>
MY FINAL DECISION: <decision>Reject</decision>
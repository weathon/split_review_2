## Summary

This paper introduces Dig-DEC, a new model-free Decision-Estimation Coefficient that replaces the optimism principle used in prior work (FGQ+23) with a KL information-gain term. This conceptual change enables the first model-free regret bounds for hybrid MDPs (stochastic transitions, adversarial rewards) under bandit feedback, resolving an open problem from LWZ25. The paper also refines the online function-estimation procedure to obtain improved regret rates in both the average and squared estimation error settings.

## Strengths

1. **Principled conceptual advance.** Replacing optimism with an information-gain term in the DEC framework is well-motivated and technically non-trivial. The KL decomposition into regularization and information-gain components is clearly explained (§6, lines 303–306), and the result that Dig-DEC ≤ optimistic DEC + η (Theorem 13) provides a clean sanity check that the new measure is never substantially larger.

2. **Open problem resolved.** The paper delivers the first model-free regret bounds for hybrid MDPs with bandit feedback (bilinear classes and Bellman-complete coverable MDPs), which LWZ25 left as an open problem. This is a genuine advance in the theory of learning in hybrid MDPs.

3. **Squared-error results are strong and internally consistent.** Theorem 11 bounds Est by a constant (log²|Φ|, independent of T) under Bellman completeness. The D_sq entries in Table 1 (e.g., bilinear star on-policy: H√(dT) log|Φ|) are consistent with the formula T·dig-dec + Est/η when η is optimized, matching the best optimism-based bounds (JLM21, XFB+23). These results check out.

4. **General divergence framework.** Algorithm 1 operates with a general divergence D, and the mirror-descent style analysis (§4) avoids the restrictive "constructive minimax theorem" of prior work. The framework subsumes prior AIR frameworks and simplifies analysis.

5. **Theorem 14 (3-armed bandit).** This explicit construction showing O(1) vs Ω(√T) regret (Dig-DEC vs optimistic DEC) is valuable for grounding the abstract comparison.

## Weaknesses

### Major

1. **Headline T-exponent claims are internally inconsistent and some are mathematically incorrect.** This is a serious communication problem that prevents a reader from determining what regret rates the paper actually proves.

   - **Abstract (line 13):** The off-policy "improvement" from $T^{5/6}$ to $T^{7/8}$ is a regression: $5/6 \approx 0.833$ versus $7/8 = 0.875$. A larger exponent means *worse* regret. As written, this claims an improvement that is actually a degradation.
   - **Bullet in introduction (line 33):** The $T^{5/8} \to T^{5/6}$ transition ($0.625 \to 0.833$) is similarly a regression.
   - **Abstract vs. Table 1:** The abstract claims an on-policy rate of $T^{3/5}$ ($T^{0.60}$), but Table 1 reports $T^{2/3}$ ($T^{0.667}$) for the same setting. These are different values.
   - **Line 213:** "improves their rate of Est from $\sqrt{T}$ to $T^{\frac{1}{2}}$" — these are identical ($T^{0.5}$). The statement is vacuous.

   These are not formatting artifacts; the T-exponents are well-formed and inconsistent by design. The paper's arithmetic needs to be verified and corrected throughout.

2. **Regret exponents in Tables 1 and 2 do not match the paper's own formulas.** Using the formulas provided in the paper (Theorem 6: Regret ≲ T·dig-dec + Est/η, with Est from Theorem 7 or 11, optimized over η):

   - **Table 1 (D_av entries, stochastic):** For on-policy bilinear class (dig-dec = $H^2 d\eta$, Est ≲ $\log|\Phi|\,T^{1/2}$), optimizing η gives regret $\propto T^{3/4}$, but the table reports $T^{2/3}$. For off-policy, the formula yields $T^{5/6}$ but the table again reports $T^{2/3}$.
   - **Table 2 (hybrid entries):** Most entries show super-linear T-exponents ($T^{3/2}$, $T^{13/8}$), which contradicts the paper's own claim of "the first sublinear regret for model-free learning in hybrid MDPs" (line 11). Computing with the stated formulas (e.g., for bilinear on-policy D_av: dig-dec = $(H^5 d^3 \eta)^{1/2}$, Est ≲ $d\log|\Phi|\,T^{1/2}$) yields regret $\propto T^{5/6}$, which is sublinear. This suggests the table entries were computed incorrectly rather than the method being flawed, but the paper must be self-consistent.

   The D_sq entries in Table 1 are internally consistent (they check out against the formula), but the D_av entries in Table 1 and nearly all entries in Table 2 are inconsistent with what the formulas predict. These discrepancies must be resolved.

### Minor

3. **Abstract's claimed on-policy improvement is inconsistent with Table 1.** The abstract says the on-policy average-error regret improves from $T^{3/4}$ to $T^{3/5}$, while Table 1 shows $T^{2/3}$ for all D_av on-policy settings. Even ignoring the arithmetic issues above, the abstract and table disagree on the same claimed result. This makes it impossible for a reader to know what rate is actually proved.

### Trivial

None.

## Nice-to-Haves

- **Computational complexity.** Algorithm 1 involves solving a saddle-point problem over Δ(Π) × Δ(Ψ) in every round, which may be intractable for large policy or function classes. The paper positions itself as a theory paper, so this is acceptable, but a brief acknowledgment would be helpful.
- **Lower bounds.** The paper does not provide matching lower bounds for Dig-DEC, so the tightness of the regret bounds is unknown. The comparison with optimistic DEC (Theorem 13) is an upper bound on Dig-DEC, not a lower bound. This is natural for a paper introducing a new complexity measure and is not a weakness, but noting it as future work would strengthen the conclusion.

## Removed Points

These points were raised in the input review but are removed as they are either factually incorrect, speculative, or not weaknesses:

1. **Concern about the step from $\sum_t \min_p \max_\nu \text{AIR}$ to $T\cdot\text{dig-dec}$:** The reviewer claimed this "skips a non-trivial step" because $\rho_t$ is algorithm-dependent. But by definition $\text{dig-dec} = \max_\rho \min_p \max_\nu \text{AIR}(\cdot;\rho)$, so for *any* $\rho_t$, the per-round min-max is bounded by dig-dec. The inequality is immediate from the definition. Removed.

2. **Missing appendix/proof concerns:** The reviewer noted that proofs in the appendix could not be checked. Since the appendix is stripped by the parser for all papers, this would apply to every submission and is not a valid weakness. Removed.

## Novel Insights

The review process surfaces one observation beyond the paper's own claims: the paper has two distinct contributions that should be decoupled in evaluation. The conceptual contribution (Dig-DEC replacing optimism with information gain) is clean, well-motivated, and appears sound. The numerical/numerical-reporting contribution (the specific regret exponents, the claimed improvements over FGQ+23) is where the inconsistencies lie. These two layers should not be conflated: the former is strong, while the latter needs substantial correction. A reader should evaluate the paper on its conceptual framework rather than the specific T-exponent claims, which the authors need to fix.

## Suggestions

1. **Verify and harmonize all T-exponent arithmetic.** Recompute every entry in Tables 1 and 2 from the formulas in Theorems 6, 7, and 11, using the optimal η. Ensure the abstract, introduction bullets, and tables all report the same numbers. Pay special attention to the D_av entries, which are inconsistent with the formulas.

2. **Fix the off-policy improvement claim.** If $T^{7/8}$ is correct, state it honestly without calling it an improvement over $T^{5/6}$. If it was meant to be a different exponent (e.g., $T^{5/8}$), correct it. Similarly fix the introduction's $T^{5/8}\to T^{5/6}$ claim.

3. **Fix the vacuous Est claim.** If the Est improvement is in the hidden constants or in the N factor (e.g., reducing dependence on the number of estimation functions), say so explicitly. The current phrasing "√T to T^{1/2}" says nothing.

4. **Clarify which Table 2 entries are sublinear.** Since the claim of "first sublinear regret for hybrid MDPs" is a headline contribution, it should be immediately verifiable from the table. Currently most entries show super-linear T-exponents, which directly contradicts this claim.

## Score and Decision

The paper makes a genuine conceptual contribution — Dig-DEC is a principled and well-motivated advance over optimistic DEC, and the ability to handle hybrid MDPs with bandit feedback resolves an open problem. The squared-error results (D_sq) are sound and consistent. However, the paper has serious self-consistency problems in its headline numerical claims. Multiple T-exponents in the abstract and introduction are mathematically incorrect (stating regressions as improvements), the abstract and table report different rates for the same setting, and most table entries disagree with the paper's own formulas. These are presentation and verification errors, not fatal flaws in the method itself, but they are severe enough that the paper cannot be accepted in its current form.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>
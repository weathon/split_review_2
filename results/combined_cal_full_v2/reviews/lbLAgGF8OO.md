Now I have all the information needed. Let me produce the final consolidated review.

**Round 1 Bracket:** The most topically similar papers (RL theory with regret bounds) fall in the 5.5–7.5 range. The strongest anchor — "Model-based RL as a Minimalist Approach" (avg 7.00, Accept) — has comparable strength weights (9.21–12.21) but no numerical inconsistencies. "On Bits and Bandits" (avg 6.50, Accept) has similar strength weights (8.42–12.18) and presentation weaknesses with weights -0.50 to 7.25. Our paper's strengths (9.30–10.24) are competitive with both anchors, but the presence of verifiable mathematical inconsistencies in Tables 1–2 (weights 2.39–2.60) that the 7.00 anchor does not share places this paper below that anchor. The weaknesses are all positively weighted (0.46–2.91), meaning they are real but not fatal. Final score: 6.0 — borderline accept, contingent on resolving numerical inconsistencies.

---

## Summary

This paper introduces Dig-DEC, a new model-free complexity measure for the decision-estimation coefficient (DEC) framework that replaces the optimism principle with pure information-gain-driven exploration via two KL-based terms (regularization + policy-dependent information gain). It provides a general algorithmic framework with a Bregman-divergence-based analysis that simplifies prior work, and applies it to derive regret bounds for several MDP classes in both stochastic and hybrid (stochastic transitions + adversarial rewards) settings. The paper also refines the online function-estimation procedure for both average and squared estimation error.

## Strengths

- **Conceptual departure from optimism.** The Dig-DEC objective replaces the optimism principle (used in prior work FGQ+23) with pure information-gain-driven exploration, incorporating two KL-based terms (regularization + policy-dependent information gain) instead of an optimistic value bonus. This is a clean and principled conceptual advance.
- **Cleaner analysis framework.** The paper generalizes the AIR objective to handle arbitrary divergences via Bregman divergences (Eqs. 5–6), connecting the analysis to standard mirror descent. This is a genuine technical simplification over the "constructive minimax theorem" used in prior work (XZ23, LWZ25) and enhances algorithmic flexibility.
- **Separation result (Theorem 14).** The explicit construction of a 3-armed bandit where optimistic DEC suffers Ω(√T) regret while Dig-DEC achieves O(1) regret provides strong evidence that the new complexity measure can be strictly better, not just equal.
- **First model-free framework for hybrid MDPs with bandit feedback.** The paper addresses a genuine open problem from LWZ25—achieving model-free regret bounds for hybrid bilinear classes and Bellman-complete coverable MDPs under bandit feedback, under specific structural assumptions. The removal of optimism is what enables avoiding explicit reward estimators in this setting.

## Weaknesses

### Fatal
None.

### Major

- **Numerical inconsistencies between abstract and introduction.** The abstract (line 13) claims "improving... from T^{5/6} to T^{7/8} (off-policy)." Since 5/6 ≈ 0.833 < 0.875 = 7/8, the exponent increases, meaning the claimed "improvement" is actually a regression. Meanwhile, the introduction (line 33) gives entirely different numbers: "improve the T^{3/2}/T^{5/8} regret... to T^{3/2}/T^{5/6}" — neither the specific exponents nor the claimed direction of improvement match the abstract. These are headline quantitative claims that are internally contradictory and, in the abstract's off-policy case, arithmetically wrong. The introduction's numbers also describe a regression (5/8→5/6 is an increase in exponent).

- **Regret exponents in Table 1 (stochastic, non-completeness rows) inconsistent with stated theorems.** Using the stated formula (line 251) Reg ≤ T·dig-dec_η + Est/η, the dig-dec values from Table 1, and Est ≲ N log|Φ| T^{1/2} from Theorem 7: for bilinear on-policy (dig-dec = H²dη, N=1), optimizing η gives regret ∝ T^{3/4}, but the table reports T^{2/3}. For bilinear off-policy (dig-dec = √(H³d|A|²η), N=1), optimization gives ∝ T^{5/6}, but the table reports T^{2/3}. A verifiable algebraic calculation from the main text shows these do not match. Either the dig-dec bounds, the Est bound, the formula, or the table entries are incorrect.

- **Table 2 (hybrid setting) contains superlinear regret bounds conflicting with the "sublinear regret" claim.** The introduction (line 32) explicitly claims "the first sublinear regret for model-free learning in hybrid... MDPs." However, multiple entries in Table 2 report T^{3/2} (e.g., hybrid bilinear on-policy: $d(H^5 \log |\Phi|)^{1/2} T^{3/2}$), which grows faster than T and is superlinear — average per-round regret diverges. Other rows in the same table report T^{1/2} (sublinear) and T^{13/8} (superlinear), creating internal inconsistency about what rates are actually achieved.

### Minor

- **Line 213 states: "our construction of the estimator improves their rate of Est from √T to T^{1/2}."** Since √T = T^{1/2}, this is a tautology and the claimed improvement is unverifiable from the main text. This is almost certainly a LaTeX/parsing artifact, but it obscures a meaningful quantitative claim.

### Trivial
None.

## Nice-to-Haves

- The hybrid setting assumptions (Assumptions 3 and 4) are restrictive: the paper acknowledges (lines 115–117) that Assumption 3 does not capture all learnable hybrid MDPs. A more extended discussion of which settings remain open would help readers understand the scope of the contribution.
- A concrete worked example showing how Dig-DEC handles a simple hybrid MDP (e.g., a 2-state linear MDP with adversarial rewards) would help illustrate the mechanism by which removing optimism enables bandit-feedback hybrid learning.

## Removed Points

These points are flagged to be removed, treat them with caution:
- **Harsh Critic weakness 5 (assumptions restrict scope)**: The paper explicitly acknowledges this limitation on lines 115–121, stating it does not capture all learnable hybrid MDPs and that this is left as future work. This is transparent, not a hidden flaw.
- **POSTERIORUPDATE is a black box**: Deferring algorithmic details to the appendix is standard for theoretical papers of this length. The appendix is stripped by the parsing pipeline, so this cannot be assessed.
- **Missing related work**: Cannot verify without external sources.
- **Pure formatting/style nitpicks**: Removed per instructions.
- **Harsh Critic strength 2 (first model-free results for hybrid)**: PARTIALLY DEMOTED — the conceptual framing is a strength, but the numerical inconsistencies in the hybrid table cast doubt on the specific quantitative claims. The strength is retained in qualified form.

## Novel Insights

None beyond the paper's own contributions. The key insight — replacing optimism with two information-gain terms (regularization via KL(ν_φ, ρ) and policy-dependent KL information gain) in the DEC objective, enabling both strict improvement in stochastic settings and handling of adversarial rewards without explicit estimators — is clearly articulated by the authors.

## Suggestions

1. **Reconcile the abstract and introduction.** Ensure all numerical improvement claims are arithmetically correct (the exponent should decrease when the bound improves) and that both sections agree on the same numbers.
2. **Verify and correct Tables 1 and 2.** Every regret exponent in the tables should be derivable from the dig-dec bound, the Est bound, and the formula Reg ≤ T·dig-dec + Est/η after optimizing η. Provide a worked derivation for at least one representative row (e.g., bilinear on-policy) in the main text.
3. **Clarify the hybrid setting regret scaling.** If some entries in Table 2 are genuinely superlinear (T^{3/2}), either correct them, explain why a superlinear bound is meaningful for this setting, or adjust the "sublinear regret" claim in the introduction accordingly. If the table contains typesetting errors, correct them explicitly.
4. **Fix the √T = T^{1/2} tautology** on line 213 to state the actual improvement explicitly.

## Score and Decision

**Score: 6.0**  
**Decision: Accept**

The paper presents a genuinely interesting conceptual contribution (Dig-DEC replacing optimism with information-gain-driven exploration) and a technically clean analysis framework (general AIR with Bregman divergences). The separation result (Theorem 14) convincingly demonstrates strict improvement over prior work. However, the numerical inconsistencies across the abstract, introduction, and Tables 1–2 are real and must be resolved before the paper can be fully trusted. The core framework is not called into question by these issues, but the quantitative claims that exemplify its value are unreliable as presented. The paper should be accepted contingent on the authors correcting these numerical problems in the final version.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>
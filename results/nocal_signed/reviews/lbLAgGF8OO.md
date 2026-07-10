Now I have all the evidence I need. Let me produce the final consolidated review.

---

## Summary

This paper introduces Dig-DEC, a model-free decision-estimation coefficient that replaces the optimism principle in prior work [FGQ+23] with a pure-information-gain mechanism. The framework generalizes the Algorithmic Information Ratio (AIR) to handle general divergence measures, and connects to mirror descent via a new analysis. The paper claims improved regret bounds in the stochastic setting and the first model-free regret bounds for hybrid MDPs (stochastic transitions, adversarial rewards) with bandit feedback.

## Strengths

- **Conceptual contribution — removing optimism from DEC.** The central idea is well-motivated: optimism-based exploration in [FGQ+23] is problematic in adversarial settings, and replacing it with pure information gain produces a more principled and more general framework. This is clearly articulated in Section 1 (lines 19–25) and carried through the whole paper. *[impact: +6.6]*

- **Generalization of the AIR framework.** The paper shows how to replace the KL-only divergence in the AIR objective with a general divergence D (Eq. 2, line 127), with a new analysis connecting to mirror descent (Section 4, lines 153–171). This recovers prior results more flexibly and opens the door to further extensions. *[impact: +7.7]*

- **Addresses an important open problem.** The paper tackles the open problem from [LWZ25] of model-free learning in hybrid MDPs with bandit feedback, providing a unified Dig-DEC framework that covers both stochastic and hybrid settings. The framing is coherent and the algorithmic design is principled. *[impact: +9.9]*

## Weaknesses

### Fatal
None.

### Major

- **Internal inconsistency in claimed regret improvements between abstract and introduction.** The abstract (line 13) claims improving bounds from T^{3/4} to T^{3/5} (on-policy) and T^{5/6} to T^{7/8} (off-policy) for average estimation error. The introduction (line 33) claims improving from T^{3/2}/T^{5/8} to T^{3/2}/T^{5/6} for the same case. These are different fractions describing the same comparison, and neither set of numbers matches the T^{2/3} and √T rates actually reported in Table 1. Furthermore, the "improvements" T^{5/6}→T^{7/8} (0.833→0.875) and T^{5/8}→T^{5/6} (0.625→0.833) are numerically *worse* (larger exponents). The reader cannot determine which bounds are actually being claimed or how they relate to the results in the tables. *[impact: -8.1]*

- **Table 2 entries appear to show super-linear regret, contradicting the paper's central claim of sublinear regret.** In Table 2 (lines 291–295), four of five regret entries show T^{3/2} or T^{13/8} — both super-linear. Since per-episode reward is bounded in [0,1] and total regret is at most T, a T^{3/2} bound is vacuous. Only one entry (bilinear\*, off-policy, complete) shows √T. The paper claims "sublinear regret" for hybrid settings (line 32), but its own table does not support this. This could be a rendering artifact (e.g., inverted fractions like T^{3/2} for intended T^{2/3}), but as presented it prevents verification of the paper's central contribution. *[impact: -7.3]*

### Minor

- **Theorem 14 claims constant (≤1) regret on a 3-armed bandit instance** — an extraordinarily strong claim — but offers no intuition in the main text about the mechanism. The proof is deferred to the appendix. While the proof exists in the original submission, a result this strong deserves at least a paragraph of explanation in the main body. *[impact: -0.6]*

### Trivial
None.

## Nice-to-Haves

- Expand Section 5.2 (hybrid setting results) beyond its current three lines to give some intuition for how the framework extends to the bandit setting.
- Discuss computational considerations for the minimax optimization (Eq. 3) over Δ(Π) × Δ(Ψ), or acknowledge that the paper focuses on statistical rates and leaves computation for future work.
- Elaborate on why optimism caused difficulty specifically in the bandit setting (Section 6 touches on this but would benefit from more explanation).

## Removed Points

These points from the input review were removed, but are documented here for completeness:

1. **Missing appendix / Algorithm 2/3/4 pseudocode not in main text** — REMOVED per rule: parser strips appendices from all papers; they exist in the original submission.
2. **Proof in missing Appendix J** — REMOVED per rule: the appendix exists in the original submission.
3. **Section 5.2 brevity** — MOVED to Nice-to-Haves; the technical content resides in the appendix, not a core flaw.
4. **Computational tractability concern** — MOVED to Nice-to-Haves; the paper focuses on statistical rates and this is not a standard expectation for this line of work.
5. **Generic "estimator description too brief"** — MOVED to Nice-to-Haves; the detail is in the appendix.

## Novel Insights

The review surfaces a tension not directly discussed in the paper: the abstract and introduction present mutually inconsistent numeric improvement claims (different fractions, and in some directions the "improvement" corresponds to a larger exponent), and Table 2's regret rates in the hybrid setting are at odds with the paper's stated claim of "sublinear regret." The review cannot determine whether these are rendering artifacts (e.g., inverted fractions T^{3/2} → T^{2/3}) or genuine errors, but either way the paper as presented does not allow a reader to verify its central numeric claims from the main text. This is a presentation failure that does not necessarily indicate flawed mathematics — the conceptual framework appears coherent — but it severely undermines the paper's ability to communicate its contribution.

## Suggestions

1. **Reconcile all numeric claims.** Ensure the abstract, introduction, and Tables 1–2 present identical or clearly traceable regret rates. Any disparity (e.g., abstract says T^{3/4} while introduction says T^{3/2}) must be explained or corrected. If the fractions in Table 2 are rendering artifacts (inverted numerators/denominators), replace them with the intended values.
2. **Verify Table 2 entries explicitly state sublinear rates.** If the regret expressions are indeed O(T^{3/2}), the paper must explain how this constitutes "sublinear regret" or withdraw the claim. If they are artifacts, correct them.
3. **Add a brief main-text intuition for Theorem 14's constant-regret construction** so the reader can assess plausibility without consulting the appendix.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>
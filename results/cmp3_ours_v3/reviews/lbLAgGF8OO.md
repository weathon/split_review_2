Now let me write the final review with calibration information.

## Summary

This paper introduces Dig-DEC (dual information gain decision-estimation coefficient), a new complexity measure for model-free RL that replaces the optimism principle used in prior work (FGQ+23) with information-gain-driven exploration via KL regularization. The framework provides a unified treatment of stochastic and hybrid (stochastic transitions, adversarial rewards) MDPs, yields the first model-free regret bounds for hybrid MDPs with bandit feedback, and refines the online function estimation procedure for improved estimation error bounds. Key results include a 3-armed bandit construction where Dig-DEC achieves O(1) regret while optimistic DEC suffers Ω(√T), and improved Est bounds for Bellman-complete MDPs.

## Strengths

- **Principled removal of optimism.** The paper correctly identifies that optimism (used in FGQ+23's optimistic DEC) is an obstacle to handling adversarial/hybrid environments. The Dig-DEC framework replaces optimism with a KL regularization term and an information-gain term, which is a cleaner conceptual approach. (Section 4, Eq. 7–8; Section 6.)

- **Theorem 14 (3-armed bandit separation).** This is a concrete, clean construction where optimistic DEC provably suffers Ω(√T) regret while Dig-DEC achieves O(1) regret. This demonstrates that the improvement is not just incremental — it can be arbitrarily large in some settings. (Section 6.)

- **Improved Est bound for Bellman-complete MDPs.** Reducing the Est term from O(T^{1/2}) to O(log²|Φ|) in the squared-error case (Theorem 11) is a substantial technical contribution, enabling √T overall regret for Bellman-complete MDPs with bounded eluder dimension or coverability.

- **Theorem 13 shows Dig-DEC ≤ optimistic DEC + η**, so it is never substantially worse than optimistic DEC, while offering the additional flexibility of handling adversarial/hybrid settings.

- **Unified framework across stochastic and hybrid settings.** The paper embeds both settings into the Φ-restricted environment framework (Definition 2) and provides a single Algorithm 1 that covers both, with the divergence measure D as the only varying component. This is a genuine theoretical unification. (Sections 3–4.)

## Weaknesses

### Fatal

None.

### Major

1. **Inconsistent numerical claims across abstract, introduction, and Table 1.** 
   - **Abstract (line 13):** Reports improvement for average estimation error from T^{3/4}→T^{3/5} (on-policy) and T^{5/6}→T^{7/8} (off-policy).
   - **Introduction (line 33):** Reports improvement from T^{3/2}/T^{5/8}→T^{3/2}/T^{5/6}.
   - **Table 1:** All average estimation error entries report T^{2/3}.
   
   These three sets of numbers are not consistent with each other. Some are not even improvements on their own terms (T^{7/8} > T^{5/6} would be a regression; T^{3/2} in the introduction is superlinear). The paper must present a single consistent set of verified regret exponents across all sections.

2. **Conflict between "sublinear" claim for hybrid MDPs and Table 2 entries.** 
   The introduction (line 32) claims "the first sublinear regret for *model-free* learning in *hybrid* bilinear classes and Bellman-complete coverable MDPs." However, Table 2 reports T^{3/2} and T^{13/8} for most hybrid entries — these are superlinear. Only one entry (bilinear★ off-policy with D_sq) gives T^{1/2}. If the exponents result from fraction corruption during PDF parsing (e.g., T^{2/3} rendered as T^{3/2}), they must be corrected in the manuscript. If the exponents as presented are correct, the "sublinear" claim is unsupported for most hybrid cases.

### Minor

3. **Line 213 claims Est improvement "from √T to T^{1/2}"** — these are the same rate (T^{0.5}→T^{0.5}). This is clearly a typo (likely intended to read from a worse rate such as T^{2/3} or T^{3/4} to T^{1/2}). Trivially fixable but occurs in a central location describing a key contribution.

4. **No side-by-side comparison with FGQ+23's rates.** The paper claims improvement over FGQ+23 across several settings but never provides a single table or paragraph showing prior rates vs. new rates per setting. The reader must piece this together from scattered and inconsistent mentions in the abstract, introduction, and footnotes, making it difficult to verify the claimed improvements.

### Trivial

None.

## Nice-to-Haves

- Add a dedicated comparison table showing FGQ+23's rates vs. this paper's rates for each setting.
- Clarify how the abstract's T^{3/5} on-policy bound relates to Table 1's T^{2/3}.
- Provide a brief worked derivation of the regret rate for one hybrid case to help readers verify sublinearity.

## Removed Points

These points are flagged to be removed, treat them with caution:

1. **"The abstract and introduction need to be harmonized"** — Merged into Major Weakness 1 rather than kept as a separate point.
2. **"Section 3.2 limitation should be mentioned in abstract"** — The limitation is explicitly stated at line 115: "it does not capture all learnable hybrid MDPs we are aware of." The abstract appropriately scopes the contribution without repeating all limitations.
3. **"No worked example of sublinearity for hybrid"** — Moved to Nice-to-Haves; detailed derivations are likely in the appendix (stripped by parser).
4. **"The 'model-free' caveat is easy to miss"** — The caveat is stated explicitly at line 37: "the term 'model-free' learning in our work does not mean that the learner has no access to the model class M."
5. **"Criticism that T^{3/2} and T^{13/8} in Table 2 are definitively superlinear"** — This is retained in Major Weakness 2, but it should be noted that fraction corruption (e.g., 2/3↔3/2) is a known PDF parsing artifact that could explain the discrepancy; the paper needs to verify its intended exponents.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Harmonize all numerical claims: decide on one consistent set of regret exponents and use them uniformly in the abstract, introduction, and tables.
2. Fix the "√T to T^{1/2}" claim on line 213.
3. Resolve the conflict between the "sublinear" claim for hybrid MDPs and the superlinear entries in Table 2; if these are fraction-rendering errors, correct the fractions throughout.
4. Add a direct comparison table with FGQ+23's regret rates per setting.

## Calibration Report

**Round 1 bracket:** 5.5–7.5 (after comparing the paper against anchors across all score bands).

**Anchor papers considered:**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| /home/.../Uj0h13lVrR.md | 1.00 | R1 | Unrelated GFlowNets paper; not comparable |
| /home/.../5lUdTogEL3.md | 1.00 | R1 | Person re-ID paper; not comparable |
| /home/.../Zi1QNJKXAD.md | 3.20 | R1 | Robust MDP paper; less novel contributions |
| /home/.../lFzUHGebeb.md | 2.00 | R1 | Online linear regression; unrelated |
| /home/.../2h3m61LFWL.md | 4.25 | R1 | Value-biased MLE for linear MDPs; less ambitious |
| /home/.../w8Zo7jACq7.md | 5.20 | R1 | Model-free CMDP; solid but narrower scope |
| /home/.../G1DoOVM3xZ.md | 5.25 | R1 | RL with general function approx; similar level of contribution but rejected on presentation |
| /home/.../6HfNB34x9I.md | 5.25 | R1 | Online MDP with predictions; similar tier |
| /home/.../GvsCOOPxoI.md | 6.17 | R1 | DEC-POMDP; different subfield |
| /home/.../txD9llAYn9.md | 7.00 | R1 | Model-based RL, horizon-free bounds; cleaner presentation |
| /home/.../op19LjpHkH.md | 5.75 | R1 | Actor-critic; empirical, not directly comparable |
| /home/.../nIEjY4a2Lf.md | 6.00 | R1 | Misspecified Q-learning; similar theoretical depth |
| /home/.../aPNwsJgnZJ.md | 6.00 | R2 | Horizon-free adversarial RL; closest topical match, accepted |
| /home/.../i3KSorBQxF.md | 4.00 | R2 | Adversarial MDP with revealed transitions; narrower scope |
| /home/.../3k6raldhEd.md | 5.00 | R2 | CMDP with long-term constraints; similar level |

**Narrowing:** The paper's contributions (Dig-DEC framework, first hybrid model-free bounds, separation result) are substantively stronger than the 4.0–5.25 papers. Its closest topical anchor (aPNwsJgnZJ, avg 6.0) was accepted and has a similar theoretical style. However, the numerical inconsistencies in the presentation are more severe than those in the accepted 6.0–7.0 anchors, justifying a score at the lower end of the 5.5–7.5 bracket.

## Score and Decision

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>
## Summary

This paper introduces Dig-DEC, a model-free Decision-Estimation Coefficient that removes the optimism principle from prior work (optimistic DEC [FGQ+23]) and drives exploration purely through information-gain (KL) regularization. The key contributions are: (1) a conceptual advance showing optimism can be replaced by KL regularization without sacrificing performance, with Theorem 13 proving Dig-DEC is never substantially larger than optimistic DEC and Theorem 14 giving a separation where Dig-DEC achieves O(1) regret versus Ω(√T); (2) the first model-free regret bounds for hybrid MDPs with bandit feedback, resolving an open problem from [LWZ25]; (3) a Bregman-divergence-based analysis framework that unifies prior AIR approaches with simpler arguments; and (4) improved online estimation procedures (unbiased estimator for average estimation error, constant Est bound for squared estimation error via a refined two-timescale method).

## Strengths

- **Conceptual advance: removing optimism from DEC.** The paper correctly identifies that optimistic DEC's reliance on an optimism principle is a barrier to adversarial/hybrid settings. Replacing it with KL regularization is a clean conceptual step, formally supported by Theorem 13 (Dig-DEC ≤ optimistic DEC + η) and Theorem 14 (a 3-armed bandit separation where Dig-DEC achieves O(1) regret vs Ω(√T)).

- **Resolves an open problem.** Provides the first model-free regret bounds for hybrid MDPs with bandit feedback under linear reward and several transition structures, resolving the main open question from [LWZ25]. The paper correctly explains why optimism prevents bandit feedback (requiring an explicit reward estimator that Dig-DEC avoids).

- **Generalized analysis framework.** The Bregman-divergence-based analysis (Section 4, Eqs. 5–6, Theorem 6) unifies prior AIR frameworks [XZ23, LWZ25] under a single, simpler argument, recovering prior results with less complexity (e.g., avoiding a two-level algorithm to prevent log|Φ| scaling).

- **Improved estimation procedures.** The sample-splitting construction (Section 4.2.1) provides an unbiased estimator of average estimation error, improving over the biased estimator of [FGQ+23]. For squared estimation error in Bellman-complete MDPs, the refined two-timescale procedure achieves Est = O(log²|Φ|), a constant improvement over [FGQ+23]'s T^{1/2} bound.

## Weaknesses

### Major

- **Numerical inconsistencies across abstract, introduction, and tables.** The paper's central quantitative claims disagree across multiple locations, preventing a reader from determining which rates are correct.
  - Abstract (line 13): claims improvement from T^{3/4} to T^{3/5} (on-policy) and from T^{5/6} to T^{7/8} (off-policy) for average estimation error. Notably, T^{7/8} > T^{5/6}, so the off-policy "improvement" is actually a *worsening*.
  - Introduction (line 33): states different numbers — T^{3/2}/T^{5/8} → T^{3/2}/T^{5/6} — where T^{3/2} (superlinear) appears in both and cannot be correct as stated.
  - Table 1 (lines 262–270): shows the actual regret bounds for average estimation error are T^{2/3}, matching neither the abstract (T^{3/5}, T^{7/8}) nor the introduction (T^{3/2}/T^{5/6}).
  These are not minor typos; they involve different polynomial exponents. For a paper whose main deliverables are regret bounds, this is a significant presentation failure.

- **The claim of "sublinear regret" for hybrid settings is inconsistent with Table 2.** The introduction (line 32) states: "We establish the first sublinear regret for model-free learning in hybrid bilinear classes and Bellman-complete coverable MDPs with linear reward and bandit feedback." However, Table 2 shows that 4 of 5 hybrid entries have superlinear regret bounds: T^{3/2} (bilinear on-policy with/without completeness, coverable) and T^{13/8} (bilinear off-policy without completeness). Only the bilinear★ off-policy with completeness entry achieves a sublinear T^{1/2} rate. The coverable MDP entry, specifically claimed in the introduction as achieving sublinear regret, shows T^{3/2} (ω(T)). This is a genuine contradiction between the stated claim and the reported results.

### Minor

- **Table 1 lacks explicit baseline comparisons.** The primary results table shows only the authors' Dig-DEC bounds without including the corresponding [FGQ+23] bounds that are the claimed baseline for improvement. The paper states (line 35) that comparison tables are in Appendix A, which is unavailable. While the appendix stripping is a known parser issue, the main text should ideally include baseline values for verifiability.

### Trivial

- **Line 213:** states "improves their rate of Est from √T to T^{1/2}" — these two expressions are mathematically identical. This appears to be a writing error; the intended comparison likely involves different quantities.
- **Lines 27, 41:** minor grammatical issues ("is the that of hybrid MDPs", "we $|\Pi|$ is finite").

## Nice-to-Haves

- Include a worked example in the main text showing how the generic bound T·dig-dec + Est/η reduces to a concrete rate for one setting, to help readers verify the arithmetic.
- Add a brief derivation (or explicit reference to an appendix equation) showing how the optimal η choice yields each claimed T-exponent.

## Removed Points

These points are flagged to be removed, treat them with caution:

- **"Missing baseline comparison as a critical/evidential issue"**: Downgraded from "Critical Issue" to Minor. The paper states the comparison tables are in Appendix A. Since appendix stripping is a known parser issue, this is not a fatal omission from the submission's perspective, though including baseline numbers in the main text would still be beneficial.
- **"Superlinear hybrid rates as possibly fatal / contradicting sublinear claim"**: Kept as Major (not Fatal) because the paper's primary contribution of being the *first* model-free hybrid bounds is still valid even if some rates are superlinear. One entry (T^{1/2}) does achieve sublinear regret. The "sublinear" claim in the introduction may need revision to be more precise about which settings achieve it.
- **Table formatting complaints**: Removed as parser artifacts.
- **Grammar/style nitpicks**: Removed per formatting guidelines.

## Novel Insights

None beyond the paper's own contributions. The reviewers' observations surface the numerical inconsistencies and presentation gaps but do not reveal additional technical insights beyond what the paper itself states.

## Suggestions

- **Harmonize the numerical claims.** Ensure the exponents in the abstract, introduction, and Tables 1–2 are mutually consistent. If different settings yield different rates, the text must clearly delineate which applies where.
- **Clarify the hybrid "sublinear" claim.** Either correct the introduction to accurately reflect which hybrid settings achieve sublinear (o(T)) regret, or explain why T^{3/2} is considered "sublinear" in context. Add a brief derivation showing how each hybrid bound emerges from T·dig-dec + Est/η.
- **Add baseline bounds to Table 1.** Include [FGQ+23]'s regret bounds as a column so readers can verify the claimed improvements from the main text directly.
- **Fix the abstract's off-policy rate (T^{5/6} → T^{7/8})**, which is numerically a worsening, and the introduction's T^{3/2} entries, which are superlinear.
- **Correct line 213** where √T = T^{1/2} are claimed as an improvement.

## Score and Decision

**Calibration anchors used (all rounds):**

| File | Avg Score | Round | Itemized? | Comparison |
|------|-----------|-------|-----------|------------|
| `Uj0h13lVrR.md` | 1.00 | R1 | No | Unrelated (GFlowNets) — not topically relevant |
| `5lUdTogEL3.md` | 1.00 | R1 | No | Unrelated (person re-identification) |
| `2h3m61LFWL.md` | 4.25 | R1 | Yes | VBMLE for linear MDPs. Had major novelty concerns (-10.28 weight). My paper has stronger novelty. |
| `6HfNB34x9I.md` | 5.25 | R1 | Yes | DOOMD for online MDPs. Had unclear assumptions (-11.43 weight). My paper is more technically sound. |
| `aPNwsJgnZJ.md` | 6.00 | R1 | Yes | Horizon-free adversarial RL. Clean presentation, few weaknesses. My paper's presentation issues disqualify it from this tier. |
| `RMgqvQGTwH.md` | 7.00 | R1 | Yes | Hybrid RL with offline data. Strong empirical+theory. My paper is pure theory with presentation issues. |
| `U0c2IaQhHk.md` | 5.00 | R2 | Yes | RKHS-RL. Had algorithm similarity concerns (-8.81), empirical gap (-6.56). My paper's negatives are smaller (-3.28, -3.05) but presentation issues are more evident. |
| `lF2aip4Scn.md` | 6.50 | R2 | Yes | Demonstration-regularized RL. Strong theoretical contributions with minor presentation issues. My paper's presentation issues are more significant. |

**Round 1 bracket:** [4.25, 6.0]  
**Round 2 refinement:** My paper's largest negative weights (-3.28, -3.05) are substantially smaller than the major negatives of the 4.25 anchor (-10.28) and 5.00 anchor (-8.81), but the 6.00 anchors had minimal weaknesses. My paper lacks the cleanliness to enter the 6.0+ tier. Final score: 5.0.

The paper presents genuine, novel contributions — particularly the clean conceptual shift from optimism to information-gain regularization and the first model-free hybrid bounds with bandit feedback. However, the numerical claims in the abstract, introduction, and tables are internally inconsistent to a degree that prevents proper evaluation. The abstract claims an "improvement" from T^{5/6} to T^{7/8} (which is a worsening), the introduction uses superlinear T^{3/2} rates, and Table 1 shows T^{2/3}. The "sublinear regret" claim for hybrid settings is contradicted by most entries in Table 2. These are fixable presentation issues, but they must be resolved before the paper can be accepted.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>
## Summary

This paper provides the first absolute (non-relative) utility guarantees for differentially private set union under a missing-mass objective, using the Weighted Gaussian Mechanism (WGM). It proves near-matching lower bounds, a distribution-free ℓ∞ missing-mass bound, and extends these results to unknown-domain variants of private top-k and k-hitting set via a meta-algorithm that uses WGM as a domain-discovery precursor. Experiments on six datasets show the WGM-based methods are competitive with or outperform existing baselines.

## Strengths

1. **First absolute utility guarantees for DP set union.** The paper provides concrete, provable bounds on missing mass for the Weighted Gaussian Mechanism (Theorems 3.3, 3.6). Prior work only gave relative/comparative guarantees or analyzed restricted special cases (e.g., one item per user). This is a genuine theoretical advance for a fundamental DP primitive used in multiple industrial frameworks.

2. **Near-matching lower bound (Theorem 3.5).** The lower bound matches the upper bound's dependence on ε and N up to polylog factors on Zipfian data. This degree of tightness is noteworthy and gives confidence that the analysis is not loose on the key resource parameters.

3. **Distribution-free ℓ∞ bound (Theorem 3.6).** The paper shows that the ℓ∞ missing mass guarantee does not require Zipfian assumptions, which is a clean theoretical contribution that directly enables the downstream applications in Section 4.

4. **Empirical demonstration that WGM is competitive or superior.** Figure 1 shows WGM matching or beating more complex sequential methods (Policy Gaussian, Policy Greedy) on missing mass, and Figure 2 shows it consistently outperforming the Durfee & Rogers limited-domain top-k baseline.

## Weaknesses

### Fatal

None.

### Major

1. **Figure 3 / text mismatch in the k-hitting set experiments (Section 5.3).** The text (lines 309–310) states the baselines are *"the non-private greedy algorithm and the private non-domain algorithm from Mitrovic et al. (2017) after taking ∪W_i to be a public known-domain."* However, the figure description (lines 319–323) lists the methods as *"Ours," "DP-Top-k," "DP-Top-k with Pay-What-You-Get,"* and *"Random Selection."* These label sets are disjoint — the described baselines (non-private greedy, Mitrovic et al. private variant) do not match the plotted ones (DP-Top-k, DP-Top-k with Pay-What-You-Get, Random Selection). Additionally, the text says *"average number of users hit"* while the figure y-axis is labeled *"Number of Missed Users"* (the complement). This internal inconsistency makes the k-hitting set experimental results uninterpretable as presented. The core theory (Theorems 4.5, 4.6) is unaffected, but this is a significant evidential problem in the empirical evaluation.

### Minor

1. **Theorem 3.6 references a Zipfian parameter s in its threshold choice despite claiming to be distribution-free.** The theorem statement (line 157) says *"Let W be any dataset"* (no Zipfian assumption), yet specifies *"T = \hat{Θ}_{Δ_0, s}(max{σ, 1})"* where s is only defined as the Zipfian exponent. The final bound does not depend on s, so this is likely a carryover notation error, but it needs clarification or correction.

2. **"Within 5%" claim undersells WGM's performance (line 281).** The paper states WGM *"obtains MM within 5% of that of the policy mechanisms."* However, the Figure 1 description shows WGM substantially outperforming the policy mechanisms on Movie Reviews (WGM ≈ 0.00 vs. baselines ≈ 0.10) and Reddit (WGM ≈ 0.17 vs. baselines ≈ 0.20–0.25). On two of three datasets WGM is strictly better, not merely close. The framing is misleadingly modest.

3. **Missing error bars.** Standard errors or confidence intervals are reported only for the k-hitting set experiment (line 311). The set union (line 281) and top-k (line 297) results report averages across only 5 trials without any measure of variance.

4. **No runtime or scalability measurements.** The paper claims the WGM is more scalable than sequential methods (lines 29, 281) but provides no runtime, round-count, or other scalability data to substantiate this.

### Trivial

None.

## Nice-to-Haves

- An empirical check of the ℓ∞ missing mass bound (Theorem 3.6) would connect theory and experiment more directly.
- Clarifying Theorem 4.3's log(M) dependence in terms of the discovered domain size |D| would improve self-containedness.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **"(1 - 1/ϵ) vs (1 - 1/e)" notation issue:** The text shows "(1 - 1/ϵ)" (line 253), which is a parser-generated formatting artifact confusing ϵ with e. This is not an author error.
- **Suggestion that baselines are unfair because not fully private:** The paper explicitly acknowledges the baselines are *"not a valid private algorithm in the unknown domain setting"* (line 309). The authors already address this limitation, and removing the baseline comparison would weaken rather than strengthen the paper.
- **Speculation about the figure/text mismatch being a "pattern of results not being reported straightforwardly":** This unsupported extrapolation is removed. Only the verified mismatch itself is retained.
- **Criticism that log(M) appears in Theorem 4.3 where M is unknown:** This is a presentation issue the authors could clarify, but the bound can be expressed in terms of |D| (the discovered domain). It does not undermine the theorem.

## Novel Insights

The harsh review makes a useful distinction that the harsh review itself does not fully articulate: the paper's experimental presentation has a concrete, localized flaw (the k-hitting set figure/text mismatch), but this flaw does not cascade into the theoretical sections. The review correctly separates the theory (which is sound and represents a genuine contribution) from the experiment (which is partially broken). This separation prevents an overly harsh judgment of the paper's core contributions while still holding the empirical claims to a high standard. Beyond this, no genuinely novel insight emerges from the reviews beyond the paper's own contributions.

## Suggestions

1. **Resolve the Figure 3 mismatch.** Either update the text to describe the baselines that actually appear in the figure, or replace the figure to match the textual description of baselines. The y-axis label ("users hit" vs. "missed users") must also be reconciled.

2. **Clarify the s subscript in Theorem 3.6.** If it is a notation error, remove it. If the threshold choice depends on Zipfian properties even for the distribution-free bound, explain why this does not contradict the distribution-free claim.

3. **Provide error bars for all three experiments** and, if feasible, add basic runtime/scalability data to support the claimed advantage.

4. **Re-frame the set union results** to accurately reflect that WGM is competitive-to-better rather than "within 5%."

## Score and Decision

**Score:** 6.0  
**Decision:** Accept  

The paper's core theoretical contributions — first absolute utility guarantees for DP set union under missing mass, near-matching lower bounds, and a distribution-free ℓ∞ bound — are novel, rigorous, and represent a genuine advance. The extensions to unknown-domain top-k and k-hitting set are well-structured applications. However, the k-hitting set experimental section (Section 5.3) has an internal inconsistency between the text and figure that makes this experiment uninterpretable as presented. This is a significant but localized presentation flaw that does not undermine the theoretical contributions. The paper is acceptable conditional on resolving the figure/text mismatch; the theoretical value alone justifies acceptance, and the empirical issue is fixable without changing the core science.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>
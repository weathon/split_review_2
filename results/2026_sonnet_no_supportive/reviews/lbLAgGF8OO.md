Now I have enough to write the review. Let me draft it and call calibration search.Based on my review of the paper and calibration results, I can now produce the final consolidated review.

**Round 1 Bracket:** The calibration shows papers at 5.5–7.5 are borderline accept/reject theory papers with incremental RL theory contributions. Papers at 7.5–8.5 are clean, impactful accepted theory papers that solve concrete problems with principled approaches. This paper: (1) closes an explicit open problem from [LWZ25], (2) improves multiple existing bounds in the stochastic setting, (3) provides a strict separation theorem, and (4) contributes a cleaner unifying framework. No major or fatal weaknesses exist. **Initial bracket: 7.5–8.5.**

The paper's contributions are stronger than the score-6 borderline papers in calibration (which offered incremental improvements or had methodological gaps). It aligns with the score-8.0 anchors (confounded POMDPs paper, tractable MARL paper) — principled theory papers that solve specific problems with rigorous new techniques. Score: **8.0**.

---

## Summary

This paper introduces Dig-DEC (Dual Information Gain Decision-Estimation Coefficient), a model-free complexity measure for reinforcement learning that replaces the optimism mechanism of prior work [FGQ+23] with dual information-gain terms (KL-divergence + a divergence $\bar{D}$ over infosets). The framework is instantiated via a generalized mirror-descent analysis (Algorithm 1) that subsumes the prior AIR framework [XZ23, LWZ25]. Key results include: (1) improved regret bounds in stochastic MDPs (e.g., $\sqrt{T}$ for Bellman-complete MDPs, matching optimism-based approaches); (2) the first model-free bandit regret bounds for hybrid MDPs (stochastic transitions, adversarial rewards), resolving an open problem from [LWZ25]; and (3) a strict separation example (Theorem 14) where optimistic E2D suffers $\Omega(\sqrt{T})$ while Dig-DEC achieves $O(1)$ total regret.

---

## Strengths

- **Conceptual cleanness of Dig-DEC (Eq. 8, Section 4.1).** The paper precisely diagnoses why optimism fails for bandit hybrid MDPs — the optimistic update requires an explicit reward estimator unavailable under bandit feedback (Section 2.2) — and the dual information-gain formulation sidesteps this directly. The design is well-motivated from first principles.

- **Bregman/mirror-descent analysis (Eqs. 5–6, Section 4).** The prior AIR framework [XZ23, LWZ25] relied on a "constructive minimax theorem" restricted to strictly convex divergences. The new analysis based on standard Bregman divergence inequalities is strictly more general, enabling Algorithm 1 to handle divergences the prior framework could not; prior results are recovered as special cases (Appendix C, noted in Section 4).

- **First model-free bandit bounds for hybrid MDPs (Table 2, Section 5.2).** [LWZ25] explicitly left the model-free bandit hybrid case open ("Extension to the bandit setting is challenging under this framework as the optimistic update requires an explicit construction of the reward estimator," Section 2.2). This paper closes the gap under Assumptions 2–4 for hybrid bilinear classes and coverable MDPs.

- **Strict separation result (Theorem 14).** A 3-armed bandit construction where optimistic E2D suffers $\Omega(\sqrt{T})$ while Dig-DEC achieves $\leq 1$ total regret shows the improvement is categorical in certain regimes — not merely a constant-factor gain. This goes beyond the standard "ours $\leq$ theirs" comparison typical in complexity-measure papers.

- **Improved unbiased estimator (Section 4.2.1).** Replacing [FGQ+23]'s biased squared-mean estimator with a product-of-means sample-splitting estimator yields an unbiased estimate of the squared Bellman error, enabling improved regret bounds including $\sqrt{T}$ for Bellman-complete MDPs (Table 1), matching optimism-based approaches [JLM21, XFB+23] for the first time in the DEC framework.

- **Clean conceptual decomposition (Section 6).** The decomposition of Dig-DEC's extra KL term into a *regularization* component ($\text{KL}(\nu_\phi, \rho)$, enabling removal of optimism) and an *information gain* component ($\mathbb{E}[\text{KL}(\nu_\phi(\cdot|\pi,o), \nu_\phi)]$, enabling strict improvement) is a genuine expository contribution explaining mechanistically when and why the new approach succeeds.

---

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

- **Assumption 4 (known linear features) restricts hybrid results.** The paper's new hybrid bandit bounds (Section 5.2) require a known linear reward feature (Assumption 4, Section 3.2). The paper is transparent about this limitation ("in this work, for the hybrid setting, we consider linear reward with known features," Section 3.2) and explicitly acknowledges the unknown-feature case (e.g., hybrid low-rank MDPs with unknown reward features, [LMWZ24]) as future work. The restriction rules out an important class of problems, though it matches the same reward assumption as [LWZ25]'s model-based result in the full-information case.

- **Quantitative claims in abstract and introduction are difficult to parse.** The abstract states the off-policy bound improves "from $T^{5/6}$ to $T^{7/8}$" — but $7/8 > 5/6$, which is numerically a regression, not an improvement. Likewise, Introduction bullet 3 states improvements "from $T^{3/2}/T^{5/8}$ to $T^{3/2}/T^{5/6}$" where $T^{3/2}$ appears on both sides and $T^{5/6} > T^{5/8}$. These are PDF-parsing artifacts (fractions are garbled throughout), but they make the abstract appear inconsistent and the claimed improvements unverifiable without reading Table 1 carefully. The detailed comparison table is deferred to Appendix A; including even a simplified version in the main body would help.

- **Theorem 14 separation: no intuition in main body.** The strict separation result is stated as a "there exists" result (Section 6) with all supporting detail deferred to Appendix J. For a result that constitutes the primary evidence that Dig-DEC is *categorically* better than optimistic DEC in the stochastic setting, a brief sketch of the mechanism — specifically, why optimism forces over-exploration on a provably bad arm in this bandit construction — would substantially increase the persuasiveness of the claim within the main text.

### Trivial

- Table 2 contains entries with exponents such as "$T^{3/2}$" (superlinear, hence vacuous for large $T$) and "$T^{13/8}$", which are evidently parser artifacts from corrupted fraction notation. The original fractions are sublinear as required for valid regret bounds.

---

## Nice-to-Haves

- A compact comparison table (setting / prior regret / our regret / assumption) in the main body, rather than relying on Appendix A, so the specific T-exponent improvements are legible without appendix access.
- A brief discussion (even a conjecture) of whether Assumption 4 (known features) is *necessary* for the hybrid bandit results or an artifact of the current technique; this would better situate the result in the open landscape.
- Brief discussion of computational tractability of the minimax problem Eq. (3); while this is a standard omission in DEC-framework theory papers, noting which concrete settings admit efficient solutions would benefit practitioners.

---

## Removed Points

*These points are flagged to be removed, treat them with caution.*

- **"$T^{7/8}$ improvement is numerically worse" as an author error.** The harsh critic correctly identified this as a parser artifact. Per hard rules, parser/formatting issues must not be attributed as paper errors. Retained only as a minor presentation note about abstract clarity.
- **Theorem 14 proof inaccessibility.** The critic flags "inaccessibility of Appendix J" as a review limitation. Per hard rules, weaknesses about missing appendix content must be removed — the appendix exists in the original submission. Only the absence of main-body intuition is retained as a minor weakness.
- **Computational complexity of minimax Eq. (3) as a weakness.** This is a standard omission in DEC-framework theory papers; it does not invalidate any theorem. Moved to Nice-to-Haves.
- **General observation that Dig-DEC subsumes prior work as a strength.** This is concrete and specific, so it was kept. No removal needed here.

---

## Novel Insights

The decomposition of Dig-DEC's extra KL term (Section 6) into a *regularization* component (which alone recovers all stochastic bounds of optimistic DEC, by avoiding the explicit optimism term) and an *information gain* component (which enables strict improvement in special stochastic cases and is the key enabler in hybrid/adversarial ones) is a conceptually sharp insight not found in prior DEC/AIR work. It suggests a broader principle: in adversarial and hybrid settings, the reward-estimator cost imposed by optimism can always be replaced by a purely distributional information-gain term, with no asymptotic loss in stochastic settings and concrete gain in hybrid ones. The Bregman divergence analysis technique (Eqs. 5–6) that replaces the "constructive minimax theorem" of [XZ23] may also prove reusable in future extensions of the DEC/AIR framework.

---

## Suggestions

1. Add a 4–5 column comparison table (setting / prior regret / our regret / assumption) to the main body to make the quantitative improvements immediately legible.
2. Include a 2–3 sentence intuitive explanation in Section 6 of why optimism misfire on the Theorem 14 bandit instance (what specific mechanism forces $\Omega(\sqrt{T})$ exploration of a bad arm).
3. Clarify in Section 3.2 or Section 7 whether the known-feature Assumption 4 is conjectured necessary or merely a proof artifact, to guide future work.

---

## Score and Decision

**Anchor papers retrieved:**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| Zi1QNJKXAD | 3.20 | R1 | Robust MDP paper, incremental, no open problem resolved |
| A1WwYw5u8m | 3.00 | R1 | Actor-critic convergence, incremental sample complexity |
| mBJF0p9yRR | 3.25 | R1 | Average-reward TD convergence, narrow contribution |
| ByW9j60mvV | 5.25 | R1 | Bayes-adaptive MDP theory, interesting but no concrete gap closed |
| 2jzhImk4br | 5.00 | R1 | Inverse constraint inference, methodological gaps |
| GvsCOOPxoI | 6.17 | R1 | DEC-POMDP learning theory, comparable niche but limited separation |
| op19LjpHkH | 5.75 | R1 | Actor-critic decoupling, empirical, less rigorous |
| TeeyHEi25C | 6.25 | R1 | Diffusion models for value estimation, different domain |
| 5t57omGVMw | 8.00 | R1 | Clean bandit theory paper, resolves specific problem with rigorous analysis |
| 8BAkNCqpGW | 8.00 | R1 | Policy gradient for confounded POMDPs, rigorous theory, finite-sample bounds |
| stUKwWBuBm | 8.00 | R1 | Tractable MARL via behavioral economics, principled theory |
| A3YUPeJTNR | 8.00 | R1 | Prediction-driven allocation theory, clean contribution |

**Round 1 bracket:** 7.5–8.5. No papers in the 8.5+ band were found in the calibration corpus.

**Narrowing:** The paper closes an explicit open problem ([LWZ25]'s hybrid bandit case), improves multiple prior bounds, provides a strict separation theorem, and contributes a clean unifying framework — all characteristics matching the score-8.0 anchors. The minor weaknesses (Assumption 4, presentation clarity) do not approach the level needed to pull below 8.0. The paper is a solid, clear theoretical contribution without fatal or major flaws. It does not rise to "strong accept" (which would typically require more surprising or broadly impactful results), but clearly clears the accept threshold.

**Final score: 8.0**

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>
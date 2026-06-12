Now I have a good picture. Let me write the final review.

**Round 1 bracket: 6.0–7.5.** The paper is clearly stronger than the 5.5–6.0 watermarking anchors (LdIlnsePNt at 6.00, which had proof errors and weak theory-practice connection; ll2nz6qwRG at 5.83; DEJIDCmWOz at 6.00). It's comparable to E4LAVLXAHW at 7.00 (accepted, strong empirical black-box detection paper). The paper's theoretical novelty is higher but the theory-practice gap for SynthID limits it slightly.

**Round 2 narrowing: 6.5–7.5.** The paper is clearly above 6.0 anchors (which were rejected or had serious rigor issues) and sits alongside the 7.0 accepted papers. The question is whether the theory-practice gap and temperature issues pull it down to 6.5 or it stays at 7.0.

**Final assessment: 7.0.** The paper constructively resolves an impossibility result with a genuinely novel insight, provides a clean theoretical framework with rigorous proofs, and has reasonable (if limited) empirical validation. The main limitations (SynthID m=30 vs. m=∞, suboptimal temperatures) are real but not fatal — the paper acknowledges the gap and the empirical results still show improvement.

---

## Summary

This paper revisits the trade-off between LLM watermark strength and speculative sampling efficiency, previously shown to be fundamental under a binary definition (Hu & Huang, 2024). The authors introduce a quantitative KL-divergence-based measure of watermark strength (connected to p-value decay via Theorem 3.1), fully characterize the Pareto trade-off curve as a constrained optimization problem, and propose pseudorandom draft-token acceptance (Algorithm 1) that provably achieves maximum watermark strength and maximum sampling efficiency simultaneously. Experiments on Gumbel-max and SynthID watermarks demonstrate improved detection without sacrificing inference speed.

## Strengths

- **Novel central insight that constructively resolves an impossibility result (Section 4.1, Theorem 4.1):** The observation that replacing the truly random acceptance coin flip with a pseudorandom one makes the entire generation deterministic in the seed ζ is simple but non-obvious. Theorem 4.1 cleanly proves this achieves unbiasedness, maximum SE = 1 − TV(Q,P), and maximum WS = Ent(P) simultaneously — constructively breaking a previously stated impossibility result from Hu & Huang (2024).
- **Quantitative watermark strength with operational meaning (Def. 3.1, Theorem 3.1):** The KL-based measure WS(P_ζ) = E_ζ[D_KL(P_ζ ‖ P)] is directly connected to the p-value decay rate of the likelihood ratio test, providing a concrete sample complexity bound n ≥ (1/D̄) log(1/α). This cleanly extends the binary definition and gives the measure clear statistical interpretation.
- **Elegant decomposition and unification (Theorem 3.2, Theorem 3.3):** The identity WS = Ent(P) − E[Ent(P_ζ)] immediately shows degenerate watermarks maximize strength, and both Gumbel-max and SynthID (as m→∞) achieve this maximum — a satisfying unification.
- **Clean trade-off formulation via constrained optimization (Eq. 8, Eq. 10):** The Pareto frontier is formulated as a plug-and-play convex optimization with concrete visualizations for multiple decoder classes (Figure 1), showing Google's class outperforms Hu's at matched efficiency — insights unavailable from prior binary analysis.
- **Well-designed experiments with correctly isolated comparisons (Figure 2):** Comparing Ars-τ vs. Ars-Prior and Bayes-MLP vs. Bayes-Prior cleanly isolates the contribution of ζ^R to detection. The inclusion of an oracle detector provides a meaningful upper bound. Both AATPS matching and TPR@FPR=1% improvement are demonstrated across two watermarking schemes and two model pairs.

## Weaknesses

### Fatal
None.

### Major

- **Theory-practice gap for SynthID experiments.** Theorem 4.1 explicitly assumes the decoder S is degenerate (line 217: "Assume the decoder S is unbiased and achieves the largest watermark strength, hence it is degenerate by Thm. 3.2"). However, the experiments use SynthID with m = 30 (line 259), which is non-degenerate — the paper acknowledges that "the watermark strength drops below that of Gumbel-max" for m = 30 (line 172), consistent with Theorem 3.3. The conclusion (line 275-276) identifies extending to non-degenerate watermarks as "an open and interesting direction." While the empirical improvement is real, the main theorem does not explain *why* the pseudorandom acceptance mechanism should improve detection for finite m. Even a brief discussion or partial result bridging this gap would substantially strengthen the paper.

### Minor

- **Suboptimal temperature choices undermine generality claims.** The paper uses temperatures of 0.5 for Gumbel-max and 0.7 for SynthID, justified as making "results more pronounced" (line 259). Lower temperatures produce more peaked distributions, making watermarking and detection inherently easier. Including at least one experiment at temperature 1.0 — even if absolute detection rates are lower — would strengthen confidence in the practical applicability of the results.
- **Detection improvement relies on specific strategies not theoretically guaranteed.** Remark 3.1 correctly distinguishes watermark strength from detection efficiency (line 93-94). The practical improvement depends on specific detection strategies (threshold calibration via grid search, trained MLP classifiers) whose performance is not bounded by the watermark strength theorem. An asymptotic argument connecting Theorem 3.1's p-value decay to the practical detection setup would make the framework more actionable.

### Trivial

- **Limited main-text experimental scope.** Gemma model pair results and C4 dataset results are deferred to the appendix. Including these in the main text would broaden the empirical evidence base, particularly if results are consistent across settings.

## Nice-to-Haves

- Discuss adversarial robustness implications: if an adversary knows the PRNG, the deterministic acceptance mechanism might allow them to predict draft vs. target tokens, potentially enabling targeted watermark removal. (Acknowledged as future work in the conclusion.)
- Report sensitivity of detection performance to the grid-searched threshold τ and validation set size.
- Provide a partial theoretical extension to non-degenerate watermarks (finite m) to bridge Theorem 4.1 with the SynthID experiments.

## Removed Points
These points are flagged to be removed, treat them with caution:
- Harsh critic's concern about Figure 1 being on "simulated (Q, P) pairs" without appendix verification — theoretical results hold for arbitrary valid pairs, and the paper references Appendix C.1 for details.
- Harsh critic's point about "more model pairs / datasets in main text" — moved to Trivial tier as it's a presentation choice, not a fundamental issue.

## Novel Insights

The paper's most genuinely novel insight is that the residual randomness in the acceptance coin flip of speculative sampling is the precise source of the watermark-efficiency trade-off, and that making this coin flip pseudorandom converts the entire generation pipeline into a deterministic function of the seed. This simple but non-obvious observation constructively resolves an impossibility result and yields a practical algorithm with formal guarantees. The quantitative watermark strength framework connecting KL divergence to sample complexity via p-value decay also provides a useful formalization that moves well beyond prior binary definitions.

## Suggestions

- Add a discussion paragraph explaining why pseudorandom acceptance is expected to improve detection for non-degenerate watermarks (finite m), even though Theorem 4.1 formally requires degeneracy. Even a heuristic argument would strengthen the paper.
- Include at least one experiment at temperature 1.0 for both watermarking schemes to validate generality beyond the "more pronounced" regime.
- Consider moving the Gemma and C4 results into the main text to broaden the empirical evidence.

## Calibration Anchors

| Anchor | Avg Score | Round | Comparison |
|--------|-----------|-------|------------|
| LdIlnsePNt (Watermarking w/ Speculative Sampling) | 6.00 (Reject) | R1 | Topically closest, but had proof errors and weak theory-practice connection; paper under review is much stronger |
| DEJIDCmWOz (Reliability of Watermarks) | 6.00 (Accept) | R1 | Purely empirical, no theoretical novelty; paper under review is stronger |
| 9k0krNzvlV (Learnability of Watermarks) | 5.75 (Accept) | R1 | Interesting but less theoretically rigorous; paper under review is stronger |
| E4LAVLXAHW (Black-Box Detection of Watermarks) | 7.00 (Accept) | R1 | Strong empirical paper; comparable quality, paper under review has stronger theory |
| 0koPj0cJV6 (Watermark for Black-Box LMs) | 4.60 (Reject) | R1 | Weaker contribution; paper under review clearly above |
| eKGEsFdpin (Sampling Based Watermarking) | 3.67 (Reject) | R1 | Weak watermarking paper; paper under review clearly above |
| n7iwmPacDt (Polybasic Speculative Decoding) | 3.00 (Reject) | R1 | Speculative decoding paper with weak theory; paper under review clearly above |
| jlhBFm7T2J (Undetectable Watermark for Images) | 6.50 (Accept) | R2 | Similar theoretical depth in watermarking; paper under review slightly stronger |
| VgtpRXhxli (Pareto Front Computation) | 6.00 (Reject) | R2 | Pareto optimization paper; paper under review has stronger contribution |
| fDaLmkdSKU (Constrained Learning) | 5.80 (Accept) | R2 | Optimization paper; comparable rigor but less novel |
| ujpAYpFDEA (Watermarked LLMs via Crafted Prompts) | 7.50 (Accept) | R2 | Strong watermarking paper; paper under review is comparable |

**Round 1 bracket: 6.0–7.5.** The paper is clearly stronger than the 6.0 anchors (some rejected, some accepted but with fewer contributions). It sits alongside the 7.0 accepted papers.

**Round 2 narrowing: 6.5–7.5.** The paper's theoretical novelty is strong enough to be above 6.5, but the theory-practice gap and temperature issues prevent a 7.5.

**Final score: 7.0.** The paper constructively resolves an impossibility result with a genuinely novel insight, provides a clean theoretical framework with rigorous proofs, and has reasonable empirical validation. The limitations (SynthID m=30, suboptimal temperatures) are acknowledged and do not undermine the core theoretical contribution.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>
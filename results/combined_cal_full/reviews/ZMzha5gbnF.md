Now let me produce the final review with the calibrated score.

## Summary

This paper identifies and characterizes a novel "priming vulnerability" in Masked Diffusion Language Models (MDLMs): because MDLMs are only trained from fully masked initial states, they have never learned to recover from partially contaminated intermediate states containing affirmative tokens. The paper demonstrates this vulnerability via (1) an anchoring attack that directly injects tokens during denoising (raising ASR from ~2% to ~20%+ with a single token), and (2) First-Step GCG, an optimization-based attack enabled by a theoretical lower bound (Theorem 4.1) that achieves 20× speedup over Monte Carlo GCG. To mitigate the vulnerability, the paper proposes Recovery Alignment (RA), which trains models via RLHF on contaminated intermediate states. Experiments across three MDLMs show RA reduces ASR from 22.0% to 1.3% at t_inter=4 while preserving general capability across 11 benchmarks.

## Strengths

- **Novel vulnerability discovery specific to MDLMs.** The core observation — that MDLMs are trained only from fully masked initial states and fail to recover from partially contaminated intermediate states — is clean, architecture-specific, and distinct from ARM safety concerns. (Sections 1, 4, 5)
- **Clean operationalization via anchoring attack.** The monotonic increase in ASR with later intervention steps (Figure 2) is exactly what the vulnerability story predicts; a single affirmative token at step 1 raises ASR from ~2% to ~20%. (Section 4.1)
- **Controlled ablation (RA vs. RA w/o inter) is the paper's strongest evidence.** For LLaDA Instruct at t_inter=4, RA w/o inter gives 22.0% ASR while RA gives 1.3% — a 17× reduction attributable solely to contamination training. (Table 2)
- **General capability preserved across 11 benchmarks.** RA shows essentially identical average performance to the original models (LLaDA: 52.2 vs 52.6; LLaDA 1.5: 52.7 vs 52.8), a practically important result. (Section 6.3, Table 4)
- **First-Step GCG (Theorem 4.1) is a genuine algorithmic contribution.** The 20× speedup and up to 4× ASR improvement over Monte Carlo GCG is practically meaningful; the theoretical derivation is sound given its monotonicity assumption. (Section 4.2, Table 1)

## Weaknesses

### Fatal
None.

### Major
None.

### Minor
- **Capability benchmarks lack variance estimates.** Table 4 reports only point estimates. Given the small absolute differences (often <1 percentage point), the claim of "no substantial degradation" would be stronger with variance or a statistical test. (Section 6.3)
- **MMaDA results partially conflate general alignment with vulnerability-specific mitigation.** MMaDA starts at 79.7% No Attack ASR (it is essentially unaligned). RA w/o inter (standard RLHF) reduces No Attack ASR to 2.0%, nearly matching RA's 3.3%. The specific benefit of contamination training on MMaDA is visible mainly at t_inter>0, but the paper's framing somewhat broadly claims "mitigates the vulnerability" across all models. (Table 2)
- **The claimed mechanism for general jailbreak robustness lacks direct evidence.** Section 6.2 offers a plausible explanation (RA models re-detect harmfulness at intermediate steps and course-correct), but the paper provides no trajectory-level analysis showing this actually occurs. The authors appropriately hedge ("A plausible mechanism"), but the claim remains speculative. (Section 6.2)

### Trivial
None.

## Nice-to-Haves
- Trajectory-level generation analysis showing RA models pivoting from harmful to safe trajectories would directly substantiate the claimed mechanism for general jailbreak robustness.
- Finer-grained analysis of which token types (e.g., "Sure" vs. domain-specific terms) have the strongest priming effect would deepen understanding of the vulnerability.
- A brief discussion of how to construct harmful query-response pairs when such data is not available (the Limitations section already notes a DPO-style alternative as future work).

## Removed Points
These points were flagged for removal but are preserved here for completeness:
1. **"Two threat models are loosely coupled"** — the paper explicitly distinguishes a "hypothetical attacker" (Section 4.1) and a "more realistic attacker" (Section 4.2) in lines 35, 84, and 88. The narrative connection (both exploit the priming effect) is interpretively sound and the paper does not claim equivalence.
2. **"Baseline comparison fairness"** — the paper's primary controlled comparison is RA vs RA w/o inter (identically trained except for contamination). Baselines are standard methods with configurations deferred to Appendix D.6, which is standard practice.
3. **"No analysis of what affirmative tokens are most dangerous"** — beyond the paper's stated scope.
4. **"No direct comparison with PAD/DiJA as baselines for measuring vulnerability"** — the anchoring attack is by design a different (simpler, more controlled) method for evaluating the vulnerability itself.
5. Generic strengths about "addressing an important problem" — not paper-specific.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. Add variance estimates or significance tests for the capability benchmarks (Table 4).
2. Include trajectory-level analysis showing an RA model detecting harmfulness at intermediate steps and pivoting to safety, to substantiate the recovery mechanism.
3. Verify consistency between the text claim of "2% to 21%" for LLaDA Instruct at t_inter=1 (line 35, 110) and the figure data — if the figure's 40% is correct, correct the text; if the text's 21% is correct, correct the figure transcription.
4. Discuss the effective regime of RA (t_inter ≤ 16) more prominently in the conclusion, since ASR climbs to 50.7% at t_inter=32.

## Score and Decision

**Score calibration against anchors:** My draft's weighted items exhibit strong positives (+3.53 to +5.64) and no weakness with meaningful negative weight (worst: -0.43). Comparing to relevant anchors:
- *"Backtracking Improves Generation Safety"* (8.00): strengths +2.37 to +6.79, worst weakness -3.22. Comparable strength profile.
- *"Booster"* (8.00): strengths +3.21 to +4.66 (weaker than mine), but had severe weaknesses (-7.52, -7.28). My negatives are much milder.
- *"Jailbreaking Safety-Aligned LLMs"* (6.14): severely criticized (-9.78, -9.30 weaknesses). My paper is clearly stronger.
- *"Safety Alignment Should be Made More Than Just a Few Tokens Deep"* (9.50): stronger exposition but also had severe negatives.

Round-1 bracket: [7.0, 8.0]. Based on weighted-item comparison — my strongest positives (+5.64, +5.26) match the upper anchors' range, while my weakest negatives are far milder than the 6-range anchor — the paper sits comfortably in the upper half of this bracket.

MY FINAL SCORE: <score>7.5</score>
MY FINAL DECISION: <decision>Accept</decision>
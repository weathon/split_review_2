The model scores are informative. Let me note that the "honest treatment" strength was fragmented into 4 low-impact items by the model — I'll re-merge it into one coherent strength in my final write-up. The strongest negatives (limited scope at -7.5, no significance tests at -7.6) relate to the experimental section, which is secondary to the paper's core theoretical contribution. The three core theoretical strengths are rated very highly (+7.9, +9.2, +8.6).

Let me now produce the final consolidated review.

---

## Summary

This paper re-examines the trade-off between watermark strength and speculative sampling efficiency in LLMs. Its core contributions are threefold: (1) a continuous, information-theoretically grounded measure of watermark strength (expected KL divergence) that replaces the binary definition in prior work; (2) a characterization of the trade-off as a Pareto frontier through constrained optimization; and (3) a pseudorandom acceptance mechanism (Alg. 1) that provably achieves both maximal watermark strength and maximal sampling efficiency simultaneously under a degenerate decoder. The paper is primarily theoretical, with supporting experiments showing improved detectability.

## Strengths

1. **Principled continuous definition of watermark strength (Def. 3.1, Theorem 3.1-3.2).** The core theoretical move — replacing Hu & Huang's binary "preserved vs. lost" notion with expected KL divergence between watermarked and original distributions — is well-motivated and productive. Theorem 3.1 connects this quantity to the exponential p-value decay rate under the LRT, and Theorem 3.2 establishes Ent(P) as the upper bound, attained iff the decoder is degenerate (deterministic in ζ). The equivalence to mutual information under unbiasedness further grounds the definition information-theoretically.

2. **Clean characterization of the trade-off as a Pareto frontier (Def. 3.2, Eq. 8, Lemma 3.1).** Reformulating the problem as maximizing WS subject to a lower bound on SE is natural and general. Lemma 3.1 shows that speculative sampling is the optimal transition kernel for any fixed P_ζ, reducing the problem to studying induced distributions (Q_ζ, P_ζ) without loss of generality. This framing enables the derivation of explicit trade-off curves and the identification of the theoretical optimum.

3. **Elegant pseudorandom-acceptance insight (Section 4.1, Alg. 1 line 8, Theorem 4.1).** The observation that residual randomness in the acceptance coin flip prevents the final token distribution from being degenerate — and hence prevents maximal WS — is precise. Making acceptance pseudorandom so the entire generation is a deterministic function of ζ is a clever, tight fix. Theorem 4.1 provides a clean proof that this simultaneously achieves unbiasedness, maximal SE (1 - TV(Q,P)), and maximal WS (Ent(P)) under a degenerate decoder.

4. **Practical detection schemes (Section 4.2).** The Ars-τ and Bayes-MLP methods that leverage ζ^R are well-motivated extensions of the theoretical insight. The paper is honest about the gap between these methods and the oracle detector, and the empirical results show meaningful improvement over prior-based baselines.

5. **Honest treatment of limitations.** The paper consistently flags where its theoretical guarantees do and do not apply: Remark 3.1 distinguishes WS from detection efficiency; Theorem 3.3 notes SynthID achieves max WS only as m→∞; Figure 1 explicitly shows the m=30 performance drop; and Footnote 3 acknowledges the bonus-step issue.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

- **Theoretical guarantees only partially cover the SynthID setting:** Theorem 4.1 assumes a degenerate decoder, but the SynthID experiments use m=30 (non-degenerate; max WS requires m→∞ per Theorem 3.3). While the paper acknowledges this in Figure 1 and the discussion of trade-off curves, the abstract and conclusion claim maximal WS without restating this scope condition. This creates a gap between the strongest theoretical claim and a significant portion of the experimental evidence. The paper would benefit from either (a) running Gumbel-max as the primary test of Theorem 4.1 and treating SynthID as a secondary practical case, or (b) explicitly conditioning the "maximal WS" claim in the abstract and conclusion.

- **Experiments measure detectability (TPR@FPR) rather than watermark strength (WS) directly.** The paper acknowledges this conceptual distinction (Remark 3.1) but does not empirically verify that Alg. 1 achieves the claimed maximal WS — e.g., by estimating E_ζ[KL(P_ζ∥P)] from samples for the Gumbel-max case (where the theory applies cleanly). The observed improvement could be attributed to better utilization of the ζ^R signal even if WS is unchanged. Direct measurement of WS would close the gap between theory and evidence.

- **Limited experimental scope.** Primary results use one dataset (EL15) and one model pair (Llama-68M/7B) in the main text, with lower-than-standard temperatures (0.5/0.7) described as making results "more pronounced." While the contribution is primarily theoretical and Gemma/C4 results appear in the appendix, the generality of the empirical findings for practical deployment at standard temperatures (T≈1) is not established.

- **Efficiency baseline choice.** The comparison (Std. SpecSAMPL) is standard speculative sampling without any watermark, rather than prior watermarked speculative sampling (Hu & Huang). This shows efficiency is maintained relative to no watermark, but does not isolate whether the method improves the efficiency-vs-strength trade-off specifically for watermarked generation.

- **Practical significance of the trade-off curves (Figure 1).** The paper does not discuss whether a practitioner could operate at interior points of the interpolated curves (e.g., "Hu's class" and "Google's class") or whether they are purely mathematical constructs.

### Trivial

- The Bayes-MLP training uses only 1,000 samples; the model architecture and training details could be specified more carefully.
- No statistical significance tests (e.g., bootstrap or McNemar) are reported for the detectability improvements.
- The abstract's framing ("show it is not absolute," "overcome" the trade-off) could mislead a casual reader into thinking the paper contradicts Hu & Huang's binary result, when it actually refines the definition — the paper does not falsify the binary impossibility, it replaces the definition with a continuous one.
- Bonus-step frequency is acknowledged as rare (Footnote 3) but no empirical data quantifies how often it occurs.

## Nice-to-Haves

- Run Alg. 1 with Gumbel-max at standard temperature (T=1) and report WS (KL divergence) empirically.
- Add an ablation distinguishing the contribution of ζ^R from the contribution of the degenerate decoder.
- Compare against prior watermarked speculative sampling (Hu & Huang) as an efficiency baseline.
- Report per-token acceptance rates alongside AATPS for a more direct connection to the per-token theory (Lemma 3.1).
- Provide bonus-step frequency data.

## Removed Points

These points from the input review were evaluated and removed after cross-checking against the paper:

- *"UMP test requires clarification about composite alternative"*: The reviewer acknowledged this is standard when conditioning on ζ (which is known to the detector in watermarking). This is a technical nuance, not a genuine weakness.
- *"Proof in appendix cannot be verified"*: Removed per rule — appendix content is parser-stripped, not an author error.
- *"Missing related works"*: Removed per rule — no external sources to verify existence of missing works.
- *"Conclusion mentions robustness to human editing as future work"*: This is a future direction acknowledgement, not a weakness.
- *"Rhetoric could be more precise in abstract/intro"*: Redistilled to the Trivial-level framing point above.

## Novel Insights

Beyond the paper's own contributions, the most striking synthesis from the review is how the reframing operates: Hu & Huang's binary "preserved vs. lost" framing of watermark strength was too coarse to capture the actual design space. Replacing it with a continuous information-theoretic measure (expected KL divergence ≡ mutual information under unbiasedness) reveals that the trade-off was never a fundamental barrier — it was an artifact of definitional granularity. The pseudorandom-acceptance trick (Alg. 1, line 8) follows naturally: if maximal WS requires degenerate token distributions, and the only remaining randomness in speculative sampling is the acceptance coin flip, then making that flip pseudorandom eliminates the last entropy source. This tight logical chain connects watermarking theory (degeneracy → max WS) with sampling practice (speculative acceptance) in a genuinely elegant way.

## Suggestions

- Empirically verify WS (KL divergence) for Gumbel-max to close the theory-evidence gap.
- Report results at standard temperature (T=1).
- Add a prior watermarked speculative sampling baseline for the efficiency comparison.
- Include an ablation isolating ζ^R's contribution from the degenerate decoder's contribution.
- Provide per-token acceptance rates and bonus-step frequency data.

## Score and Decision

The paper's theoretical contributions are substantial and well-supported: a continuous, information-theoretic measure of watermark strength; a principled Pareto-frontier characterization of the trade-off; and an algorithm (pseudorandom acceptance) elegantly proven to achieve the theoretical optimum. The weaknesses are real but evidential and scope-related — they pertain to the experiments, which are secondary to the theoretical core. The paper is clearly written, honestly addresses its limitations, and opens a productive new direction. The theoretical framework alone warrants a positive decision, and the empirical results (though limited in scope) are supportive. I recommend acceptance.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>
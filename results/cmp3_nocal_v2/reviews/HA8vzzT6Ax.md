## Summary

This paper introduces a theoretical framework for understanding the trade-off between watermark strength and speculative sampling efficiency in LLMs, and proposes a practical mechanism (pseudorandom acceptance) that simultaneously achieves maximal watermark strength and maximal sampling efficiency for degenerate decoders. The contributions span: (1) a quantitative definition of watermark strength via expected KL divergence (equivalently mutual information), (2) a Pareto frontier formulation of the watermark-efficiency trade-off, and (3) a pseudorandom acceptance algorithm (Alg. 1) with a proof (Theorem 4.1) that it achieves both maxima simultaneously.

## Strengths

1. **The pseudorandom acceptance mechanism (Alg. 1) is a genuinely novel and clever idea.** The key insight — that the residual randomness in prior speculative-sampling watermarking comes from the truly random acceptance coin flip, and replacing it with pseudorandomness restores determinism — is elegant. Theorem 4.1's proof that this achieves maximal WS and maximal efficiency simultaneously for degenerate decoders is the paper's strongest result and appears to be a genuinely new contribution not present in prior watermarking or speculative sampling literature.

2. **The quantitative definition of watermark strength (Def. 3.1) is well-motivated and connects to meaningful theory.** Using expected KL divergence (equivalently mutual information under unbiasedness) is a principled choice. Theorem 3.1's connection to the p-value decay rate under the UMP test gives this measure operational significance through sample complexity, and Theorem 3.2's characterization of maximal strength (degeneracy, WS = Ent(P)) is clean and intuitive.

3. **The trade-off curve formulation (Def. 3.2) is principled and appropriately general.** Casting the trade-off as a Pareto frontier between watermark strength and sampling efficiency, with Lemma 3.1 showing the speculative sampler is the optimal kernel, provides a solid theoretical framework that extends beyond the specific methods studied and gives the paper lasting value as a conceptual contribution.

## Weaknesses

### Fatal
None.

### Major

1. **Theorem 4.1's scope does not cover the SynthID experiments, and this limitation is not acknowledged in the experimental section.** Theorem 4.1(c) requires the decoder *S* to "achieve the largest watermark strength (hence it is degenerate by Thm. 3.2)" (line 217). Theorem 3.3 states that SynthID achieves maximal WS only "as *m* → ∞" (line 120). The SynthID experiments use *m* = 30 (line 257), which is finite and non-degenerate. While the paper acknowledges this gap in the theoretical section (Fig. 1, line 172: "the maximal watermark strength is attained only in the limit *m* → ∞"), the experimental section (Section 5) never restates this limitation or clarifies that Theorem 4.1(c) does not apply to these results. The reader cannot assess how much of the observed SynthID improvement is attributable to the mechanism versus the gap from non-degeneracy. This mismatch between theoretical scope and experimental scope substantially weakens the paper's central empirical claim for half of its experiments.

2. **Non-standard low temperatures are used throughout, with the explicit justification that they make results "more pronounced."** The paper states: "To make the results more pronounced, we use lower temperatures: 0.5 for Gumbel-max and 0.7 for SynthID" (line 259). Lower temperatures make distributions more peaked, which has two effects favorable to the proposed method: (a) acceptance rates increase (draft and target distributions become more similar), and (b) watermark detection becomes easier (the deterministic relationship between pseudorandomness and the chosen token is stronger when one token dominates). The paper provides no results at temperature 1.0 and no discussion of whether the improvements hold under this standard condition. If the method only shows meaningful gains at low temperatures, its practical value is substantially reduced.

### Minor

1. **The provenance of the detection baselines (Ars-Prior, Bayes-Prior) from prior work is not clearly established.** Ars-Prior selects between draft and target statistics based on the empirical acceptance rate (lines 233-237), and Bayes-Prior is described as "the prior approach" (line 247). It is not explicitly stated whether these exactly reproduce the detection methods from Hu & Huang (2024) and Dathathri et al. (2024), or whether they are new re-implementations by the authors. A table comparing baseline detection performance against published numbers from the original papers (on matched settings) would resolve this ambiguity.

2. **The theoretical WS metric and the experimental detection results remain conceptually disconnected.** Theorem 3.1 connects WS to the p-value decay rate of the *likelihood ratio test* (the UMP test), but the detectors evaluated (Ars-τ, Bayes-MLP) use different test statistics and detection rules. The paper acknowledges this gap in Remark 3.1 and Section 4.2, but does not bridge it empirically — for example, by measuring the empirical WS of Alg. 1's output distribution and showing that it *predicts* the observed detectability improvement. The experiments would be stronger if they connected the theoretical framework to the observed detection results.

### Trivial

1. **The "breaking the trade-off" framing slightly overstates the relationship to the prior impossibility result.** Hu & Huang (2024) proved an impossibility under a binary definition of watermark strength (preserved vs. not preserved). The paper replaces this with a continuous definition and shows the optimum is achievable under the new definition. This is a valid and interesting contribution, but it is a *reformulation* of the problem rather than a refutation. Phrasing such as "the trade-off is not absolute" (line 9) and "can be overcome" (line 24) could be more precise without diminishing the contribution.

## Nice-to-Haves

- Run the main experiments at temperature 1.0 (standard practice) to confirm the improvements are not artifacts of low-temperature settings.
- Establish approximate theoretical guarantees for SynthID with finite *m* (e.g., bound the gap between WS and Ent(P) as a function of *m*).
- Measure the empirical WS of Alg. 1's output distribution for both Gumbel-max and SynthID settings and plot it against the observed TPR to validate that the theoretical framework predicts experimental outcomes.
- Discuss the regime where draft and target distributions are very different (TV(Q,P) is large), where the acceptance rate is low and residual sampling is invoked frequently — the theoretical guarantees still hold, but the practical behavior may differ.

## Removed Points

These points from the original review were removed or demoted after cross-checking against the paper:

- **"Experimental evaluation is too narrow (one dataset, two small models)"** — Partially generic criticism. The paper includes C4 and Gemma results in the appendix (as explicitly noted at line 257), which is standard for page-limited submissions. The appendix results are referenced.
- **"No comparison against standard watermarking without speculative sampling"** — Scope creep. The paper is about watermarking *with* speculative sampling; comparing against non-speculative watermarking answers a different question.
- **"The connection between WS and experimental detection is asserted but not established"** — Already addressed in full by the paper's Remark 3.1 and Section 4.2, which explicitly acknowledge this gap. Retained above as a minor weakness (the paper doesn't bridge the gap empirically) rather than a major one.
- **Strengths about "important problem" framing** — Generic; removed. Only concrete, evidence-backed strengths are retained.

## Novel Insights

None beyond the paper's own contributions. The pseudorandom acceptance mechanism itself is the key insight, and the reviews do not surface additional novel perspectives beyond what the paper already provides.

## Suggestions

- In Section 5, explicitly state that Theorem 4.1(c)'s guarantee of maximal WS applies to Gumbel-max but not to SynthID with *m* = 30, and discuss how the observed SynthID improvement relates to the theoretical gap.
- Add at least one table or experiment at temperature 1.0 to demonstrate that the detection improvements are not artifacts of the low-temperature setting.
- Clarify whether Ars-Prior and Bayes-Prior are exact reproductions of detection methods from the cited prior work or new re-implementations, and if re-implemented, validate them against published numbers on matched settings.
- Consider adding an LRT-based detector (or measuring empirical WS from samples) to connect the theoretical framework more directly to the experimental outcomes.

## Score and Decision

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>
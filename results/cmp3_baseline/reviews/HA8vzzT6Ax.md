## Summary

This paper revisits the trade-off between watermark strength and speculative sampling efficiency in LLMs. It introduces a quantitative measure of watermark strength (expected KL divergence) that governs statistical detectability, formalizes the trade-off as a Pareto frontier via a constrained optimization, and proposes a mechanism that injects pseudorandomness into draft-token acceptance—proving it achieves maximal watermark strength while preserving speculative sampling efficiency. Experiments with Gumbel-max and SynthID watermarks demonstrate improved detectability without sacrificing efficiency.

## Strengths

- **Novel quantitative watermark-strength measure.** Moving beyond prior binary definitions, the expected KL divergence in Def. 3.1 is information-theoretically grounded (equivalent to mutual information under unbiasedness) and directly connected to sample complexity (Thm. 3.1). This provides a principled framework for analyzing the trade-off.
- **Clean theoretical characterization.** The paper proves that maximum watermark strength is attained iff the watermarked distribution is degenerate (Thm. 3.2), and that both Gumbel-max and limiting SynthID achieve this bound (Thm. 3.3). The Pareto formulation (Def. 3.2) and Lemma 3.1 (speculative sampling is optimal for a given P_ζ) are elegant and enable principled trade-off visualization.
- **Algorithm with provable guarantees.** The proposed pseudorandom acceptance (Alg. 1) is theoretically sound: Thm. 4.1 shows it simultaneously achieves unbiasedness, maximal sampling efficiency, and maximal watermark strength. This breaks the impossibility result of Hu & Huang (2024) in a rigorous manner.
- **Empirical validation of detectability improvement.** Experiments on ELI5 with Llama-68M/7B show that using the pseudorandom acceptance variable (Ars‑τ and Bayes‑MLP) yields higher TPR at fixed FPR compared to prior-based detection, under the same average accepted tokens per step. The gap to an oracle detector is modest.

## Weaknesses

### Fatal
None.

### Major

1. **Detection baseline may not be optimal.** The comparison against Ars‑Prior and Bayes‑Prior assumes these are the strongest available detectors without access to the acceptance variable. “Ars‑Prior” selects the test statistic by an estimated empirical acceptance rate, but a more sophisticated detector (e.g., a learned classifier that uses the acceptance rate as a feature rather than hard selection) could potentially perform better. The paper would benefit from a clearer justification that these baselines are indeed the state-of-the-art, or from a direct comparison to the original detection methods of Dathathri et al. (2024) as originally applied without the acceptance variable.

2. **Trade-off characterization is limited to specific decoder families.** While Eq. (8) defines a general optimization, the concrete Pareto curves in Fig. 1 are derived only for “linearly watermarked classes” (Eq. 9) and two other handcrafted classes. The paper claims to “complete the trade-off curve” (Section 3 title), but the completeness is only with respect to the proposed quantitative measure, not across all possible unbiased decoders. This overstatement could mislead readers about the generality of the derived curves.

### Minor

1. **Experimental temperature is lowered.** The main results use temperature 0.5 (Gumbel‑max) and 0.7 (SynthID), which amplify detectable signals. Standard practice often uses temperature 1.0. The paper should discuss whether the improvements persist at higher temperatures or provide additional results.
2. **SynthID theory vs. practice.** Thm. 3.3 states SynthID achieves maximal strength only as \(m\to\infty\), but experiments use \(m=30\) (a practical choice). The paper acknowledges the gap (Fig. 1 right panel, gray curve), yet the theoretical claim in the abstract and Section 4 may give an impression of full optimality in practical settings.
3. **Derivation of Eq. (10) is sketchy.** The transition from the optimization in (8) to the convex/non‑convex formulation (10) is presented without sufficient intermediate steps. A reader unfamiliar with the algebra may find it hard to verify the equivalence, especially the role of the entropy constraint and the reduction to \(\gamma \geq \gamma_0\).

### Trivial
None.

## Nice-to-Haves

- Include experiments at temperature \(T=1.0\) to confirm that the detectability improvement is not an artifact of low-temperature sharpening.
- Provide a more extensive comparison with alternative watermark+speculative sampling pipelines (e.g., the direct approach of Hu & Huang (2024) without the proposed mechanism).
- Discuss how the method can be extended to tree‑based speculative decoding, as hinted in the conclusion.

## Novel Insights

The paper’s core insight is that the “inevitable trade‑off” between watermark strength and speculative sampling efficiency is an artefact of binary strength definitions. By quantifying strength as expected KL divergence, the trade‑off becomes a continuous Pareto frontier that can be improved by making the acceptance decision itself pseudorandom. This reframes the problem from an impossibility to an optimization, and the proposed algorithm demonstrates that maximal strength and full efficiency can co‑exist when the watermarked distributions are degenerate.

## Suggestions

- Clarify the detection baseline: show that Ars‑τ and Bayes‑MLP outperform not only the simple prior‑based selection but also any reasonable detector that does not have access to the acceptance variable (e.g., a learned model that predicts the source from available features).
- Soften the claim of “complete characterization” in the title, abstract, and Section 3; instead state that the framework *enables* characterization for any given decoder families, and that concrete curves are provided for several important classes.
- Expand the derivation of Eq. (10) in the main text or appendix to make the step from (8) to (10) more transparent.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>
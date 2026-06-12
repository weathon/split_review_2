## Summary

This paper revisits the trade-off between watermark strength and speculative sampling efficiency for LLM inference. It introduces a quantitative measure of watermark strength based on expected KL divergence, characterizes the complete Pareto frontier between strength and efficiency as a constrained optimization problem, and proposes a pseudorandom acceptance mechanism that theoretically achieves both maximal watermark strength and maximal sampling efficiency simultaneously, effectively breaking the prior impossibility result of Hu & Huang (2024).

## Strengths

- **Genuine theoretical insight**: The core idea of making the acceptance decision itself pseudorandom (Algorithm 1, line 8) is clever and principled. By eliminating residual external randomness in the acceptance coin flip, the entire generation becomes a deterministic function of pseudorandom seeds, enabling Theorem 4.1 to simultaneously prove maximum watermark strength (WS = Ent(P)), maximum sampling efficiency (SE = 1 - TV(Q,P)), and unbiasedness. This constructively resolves the impossibility result of prior work.

- **Well-grounded quantification**: Defining watermark strength as expected KL divergence and connecting it to p-value decay rates via Theorem 3.1 (a Stein's lemma–type result) gives the measure concrete operational meaning in terms of sample complexity for detection. Theorem 3.2 cleanly characterizes the maximum as Ent(P), achieved by degenerate distributions, and Theorem 3.3 confirms Gumbel-max and SynthID (m→∞) attain it. This provides a unified analytical framework.

- **Clean trade-off characterization**: The constrained optimization formulation (Eq. 10) and the visualization of Pareto curves for multiple watermarking scheme classes (linear, Hu's, Google's) in Figure 1 offer a useful comparative landscape. Lemma 3.1 on the optimality of speculative sampling for fixed target distributions is a clean structural result.

- **Improved detection mechanisms**: The paper proposes concrete detection improvements (Ars-τ for Gumbel-max, Bayes-MLP for SynthID) that exploit the new pseudorandom acceptance variable rather than averaging candidate statistics, and validates the gains empirically.

## Weaknesses

### Fatal
None.

### Major

- **Limited experimental scope**: Experiments use relatively small model pairs (Llama-68M/7B, Gemma-2B/7B) on a single primary dataset (EL15) with lower temperatures (0.5 for Gumbel-max, 0.7 for SynthID) explicitly chosen to make results "more pronounced." This raises questions about generalizability to larger-scale models and standard operating temperatures. The paper acknowledges C4 results in the appendix, but the main text could better convey the sensitivity of gains to these choices.

- **Practical detection requires training data**: Both Ars-τ and Bayes-MLP require held-out watermarked texts (and unwatermarked texts for SynthID) for calibration/training (1,000 samples each). The paper does not discuss how many samples are needed in practice, how sensitive the calibration is, or how this interacts with deployment constraints where the detection threshold must be set before seeing watermarked samples.

### Minor

- **The KL divergence measure is natural but not deeply novel**: While the paper motivates the measure well through Theorem 3.1, using expected KL divergence between watermarked and original distributions as a "strength" measure is fairly standard in the watermarking literature. The contribution is more in the formal trade-off analysis built upon this measure than in the measure itself.

- **Degenerate watermarks only**: The framework and Theorem 4.1 require degenerate (point-mass) watermarks. The paper acknowledges this in the conclusion but does not quantify how much is lost for non-degenerate schemes, which are practically common.

- **Temperature sensitivity not explored**: Lower temperatures produce more peaked distributions, making watermarks stronger and acceptance rates higher naturally. The paper does not present results across a range of temperatures, leaving the practical significance of the improvements at standard generation temperatures unclear.

### Trivial
None.

## Nice-to-Haves

- Experiments across multiple temperature settings to characterize the robustness of the detection improvement.
- Analysis of how the number of calibration samples affects detection performance with Ars-τ and Bayes-MLP.
- Extension to tree-based speculative sampling methods, mentioned in the conclusion but not explored.

## Novel Insights

The paper's most novel observation is that the trade-off between watermark strength and speculative sampling efficiency is not fundamental—it was an artifact of residual external randomness in the acceptance decision. By replacing true random coin flips with pseudorandom ones tied to the same seed space, the entire speculative sampling pipeline becomes a deterministic function of pseudorandomness, collapsing the distinction between "accepted draft" and "target-sampled replacement" into a single watermarked distribution. This insight unites two previously conflicting goals and, if it scales to practical deployment settings, could meaningfully accelerate watermark adoption.

## Suggestions

- Add experiments at standard temperatures (e.g., 0.7–1.0) and on larger model pairs (e.g., 7B/70B) to strengthen the practical relevance claims.
- Provide ablations on calibration sample size for detection methods.
- Discuss the security implications of deterministic generation (e.g., what happens if the pseudorandom seed is known to an adversary).

## Score and Decision

The paper presents a well-executed theoretical framework with a genuinely novel mechanism (pseudorandom acceptance) that constructively resolves an established impossibility result. The theory is clean, the proofs appear rigorous, and the experiments support the core claims despite limited scope. The main reservation is the narrow experimental validation, which leaves practical impact somewhat uncertain.

MY FINAL SCORE: 7.0
MY FINAL DECISION: Accept
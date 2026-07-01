## Summary

This paper revisits the trade-off between watermark strength and speculative sampling efficiency in LLMs. It introduces a quantitative measure of watermark strength (expected KL divergence) that governs statistical detectability, characterizes the trade-off as a Pareto frontier via constrained optimization, and proposes a mechanism that makes draft-token acceptance pseudorandom. The authors prove that this mechanism achieves maximal watermark strength while preserving speculative sampling efficiency, and empirically demonstrate improved detectability at matched efficiency.

## Strengths

- **Novel quantitative framework for watermark strength.** Defining watermark strength as expected KL divergence (equivalently mutual information) is principled and connects directly to sample complexity via Theorem 3.1. This moves beyond the binary definition in prior work and enables a continuous trade-off analysis.
- **Clean characterization of the trade-off as a Pareto frontier.** Formulating the trade-off as a constrained optimization problem (Definition 3.2) and deriving explicit curves for Gumbel-max and SynthID watermarks provides a rigorous foundation for comparing schemes.
- **Theoretically grounded mechanism to break the trade-off.** Algorithm 1 and Theorem 4.1 show that pseudorandom acceptance can simultaneously achieve maximal watermark strength and maximal sampling efficiency, with proofs of unbiasedness, efficiency, and strength. The idea of making the acceptance decision deterministic in the pseudorandomness is elegant.
- **Empirical validation of improved detectability.** Experiments on two model pairs and two datasets show that the proposed detection methods (Ars-τ and Bayes-MLP) achieve higher TPR at fixed FPR while maintaining AATPS, confirming the practical benefit of the approach.

## Weaknesses

### Fatal
None.

### Major
- **Limited experimental scope.** The experiments use only two model pairs (Llama-68M/7B, Gemma-2B/7B) and two datasets (ELI5, C4). More diverse settings (different model sizes, domains, longer contexts) would strengthen the empirical claims. Additionally, the paper does not directly compare against the prior method of Hu & Huang (2024) in terms of the trade-off curve; only theoretical curves are shown.
- **Theoretical guarantee for SynthID is incomplete.** Theorem 4.1 assumes the decoder achieves maximal watermark strength (degenerate). SynthID with finite m (e.g., m=30 used in experiments) is not degenerate, so the theoretical guarantee does not directly apply. The empirical improvement for SynthID is still valuable, but the paper could discuss this gap more explicitly.
- **Detection methods require training/calibration.** Ars-τ requires a held-out validation set for threshold selection, and Bayes-MLP requires training data. This adds practical overhead and may limit deployment in some scenarios. The paper does not analyze sensitivity to the amount of training data.

### Minor
- **The trade-off curves in Figure 1 are for simulated (Q,P) pairs.** It would be more informative to see curves computed from real model distributions to assess practical relevance.
- **The paper claims to "break the trade-off" but the trade-off is defined in a specific binary sense from prior work.** The proposed method does not eliminate the trade-off for non-degenerate watermarks or biased watermarks, which the conclusion acknowledges. The framing could be slightly more measured.
- **Repeated context masking is mentioned but not explained.** A brief description in the main text would improve readability.

### Trivial
None.

## Nice-to-Haves
- Extend experiments to tree-based speculative decoding (e.g., Medusa, Eagle) to test generality.
- Analyze the impact of the lookahead K on the trade-off more systematically.
- Provide an ablation study on the amount of training data needed for Bayes-MLP.

## Novel Insights

Beyond the paper's own contributions, a genuinely novel insight is that the "inevitable" trade-off between watermark strength and speculative sampling efficiency arises from an overly restrictive definition of watermark strength. By recognizing that watermark strength is a continuous quantity (expected KL divergence) rather than a binary property, the paper reveals that the trade-off is not fundamental but rather a consequence of how the problem was framed. The key enabler is making the acceptance decision pseudorandom, which aligns the speculative sampling process with the deterministic nature of maximal-strength watermarks. This insight suggests that other seemingly fundamental trade-offs in LLM inference may be artifacts of binary or coarse-grained definitions, and that continuous measures can open up new design space.

## Suggestions
- Include a direct experimental comparison with the method of Hu & Huang (2024) on the same models and datasets to empirically demonstrate the improvement in the trade-off.
- Add a discussion of the computational overhead of the detection methods (Ars-τ, Bayes-MLP) relative to standard detection.
- Clarify in the main text how repeated context masking works and why it is needed for unbiasedness.

## Score and Decision

**Score:** 8

**Decision:** Accept

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>
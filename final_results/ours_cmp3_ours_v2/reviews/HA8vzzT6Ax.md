## Summary

This paper addresses the trade-off between watermark strength and speculative sampling efficiency in LLMs. It introduces a continuous KL-divergence-based measure of watermark strength (replacing the prior binary definition), formalizes the trade-off as a Pareto optimization problem, and proposes a pseudorandom acceptance mechanism (Algorithm 1) that provably achieves maximal watermark strength while preserving sampling efficiency. Experiments on Llama-68M/Llama-7B and Gemma pairs show improved detectability at matched efficiency.

## Strengths

1. **Principled continuous watermark strength measure (Def. 3.1).** Defining WS as expected KL divergence (equivalently mutual information under unbiasedness) is a genuine improvement over the binary "preserved vs. lost" definition in prior work. Theorem 3.1 connects this measure to p-value decay rate, giving it clear operational meaning for detection sample complexity.

2. **Clean pseudorandom acceptance mechanism (Algorithm 1, Theorem 4.1).** Making the acceptance decision deterministic in the pseudorandomness is simple and theoretically sound. Theorem 4.1 shows it simultaneously achieves maximal WS (= Ent(P)) and maximal sampling efficiency (= 1−TV(Q,P)), which directly addresses the practical bottleneck identified in the paper.

3. **Trade-off curve formulation (Definition 3.2, Lemma 3.1).** Casting the trade-off as a Pareto optimization problem provides a general framework that subsumes and extends prior binary impossibility results. The closed-form derivation for the linear watermarked class (equation 10) shows the machinery working concretely, and the framework is plug-and-play for different watermarking schemes.

## Weaknesses

### Fatal

None.

### Major

1. **Experiments use lower-than-standard temperatures without a temperature-1.0 control.** The paper explicitly states it uses temperatures of 0.5 (Gumbel-max) and 0.7 (SynthID) "to make the results more pronounced" (Section 5, line 259). Lower temperatures produce sharper distributions with lower entropy, which both reduces maximum watermark strength (Theorem 3.2: max WS = Ent(P)) and affects acceptance rates. While comparisons between methods at the same temperature are internally fair, the absence of temperature-1.0 results makes it unclear whether the observed improvements generalize to standard settings. For a paper claiming to "pave the way for efficient and practical deployment" (abstract, line 9), this is a significant omission that weakens the empirical claims.

### Minor

1. **Rhetorical framing overstates the relation to prior impossibility results.** The abstract states "we revisit this trade-off and show it is not absolute" and the introduction frames the contribution as overcoming a "seemingly unavoidable trade-off" (lines 22-24). The paper achieves this by replacing the binary definition of watermark strength with a continuous one. While the paper acknowledges this reframing (lines 24-25, 86-87), the contrast between the measured technical discussion and the stronger framing in the abstract could give readers the impression that prior impossibility theorems have been overturned rather than reframed under a different (more practical) definition.

2. **Bonus-step tokens in Algorithm 1 (lines 15-17) are not covered by Theorem 4.1's theoretical guarantee.** Footnote 3 (line 243) acknowledges that bonus-step tokens "are not controlled by the acceptance variable" and asserts their impact is "negligible" when K > 1. This means the theorem's claim of maximal watermark strength applies strictly only to a single-step version, not to the full multi-step algorithm with bonus tokens. The paper is transparent about this, but the headline claim is approximate for the practical algorithm, and the paper does not quantify the fraction of tokens generated via the bonus step in practice.

3. **SynthID detection pipeline (Bayes-MLP) requires training a neural network on labeled data.** The Bayes-MLP method (Section 4.2, lines 241-247) requires training a three-layer MLP on 1,000 labeled watermarked texts. The paper does not discuss sensitivity to training data distribution, whether the MLP generalizes across prompts, or what happens when the draft/target model pair changes. By contrast, the Gumbel-max Ars-T method uses a simple threshold on u_t, which is far more practical. The paper's conclusions group both methods together, but the practical deployability of the SynthID enhancement is less clear.

4. **Empirical evaluation is limited in scope.** The main text reports results for one model pair (Llama-68M/Llama-7B) on one dataset (EL15). Gemma results and C4 results are deferred to the appendix. For a paper with claimed practical relevance, a broader empirical base would strengthen the conclusions. Additionally, the number of independent runs used to compute the 95% confidence intervals (line 255) is not specified, making it hard to assess the reliability of the reported intervals.

### Trivial

- The phrase "fully characterize" in the abstract overstates what is done: the Pareto curves are derived for specific parametric subfamilies (linearly watermarked classes, equations 9-10), not the full space of all possible watermarking schemes.
- The derivation from Definition 3.2 to equation (10) is described in a single sentence without showing the algebra (line 164), making it harder to follow for a central contribution.

## Nice-to-Haves

- Run the main experiments at temperature 1.0 (and possibly 0.85) to confirm that the observed improvements generalize to standard settings.
- Quantify the fraction of tokens generated via the bonus step in practice (for K=2,3,4) and verify that detection performance is insensitive to including/excluding them.
- Estimate empirical WS (Def. 3.1) from the experiments to directly connect the theoretical guarantee (Theorem 4.1.c) to the observed TPR improvements.
- Discuss the computational cost of the detection methods (Ars-T requires computing two test statistics per token; Bayes-MLP requires training an MLP).

## Removed Points

These points were raised by reviewers but removed from the main review for the following reasons:

- **"No variance or error bars"**: The paper DOES show 95% confidence intervals (line 255: "Error bars mark the 95% confidence intervals," "Shaded regions indicate the 95% confidence intervals"). The unspecified number of runs is a minor detail, not a missing analysis.
- **"Oracle baseline is a significant gap"**: The paper compares against baselines (Ars-Prior, Bayes-Prior) throughout; the Oracle is an upper bound provided for reference, not a missing comparison.
- **"Theorem 3.1 assumptions may not hold for practical schemes"**: Speculative claim about uniform boundedness; not a demonstrated problem with the specific schemes studied in the paper.
- **"Missing related works"**: Removed per policy — the reviewer cannot definitively verify absent citations.
- **"No discussion of draft-target similarity effect"**: The paper's scope is the mechanism itself; regime dependence is a natural extension, not a core flaw.
- **Formatting/presentation nitpicks**: Removed per policy (parser artifacts).

## Novel Insights

The reviewer correctly observes that the "breaking the trade-off" framing could be read as overturning prior impossibility results when it actually replaces the definition of watermark strength. This is a valid rhetorical critique — the paper is transparent about the redefinition in the technical sections (lines 24-25, 86-87), but the abstract and introduction would benefit from clearer qualification. The reviewer also notes a disconnect between Theorem 4.1 (proving maximal WS) and the experiments (measuring TPR@FPR), which are related but not identical quantities — directly estimating empirical WS from the experiments would bridge this gap.

## Suggestions

1. **Most important**: Add experiments at temperature 1.0 to show the improvement pattern holds at standard settings. This is the single most impactful fix for the empirical concerns.
2. Quantify the bonus-step fraction and either (a) show empirically that detection is insensitive to it, or (b) modify Algorithm 1 to make the bonus step also pseudorandom.
3. Tighten the framing in the abstract to acknowledge more explicitly that the paper adopts a more nuanced definition of watermark strength rather than directly overturning prior impossibility results.
4. Add a direct empirical estimate of WS (Def. 3.1) from the experiments to connect the theoretical guarantee (Theorem 4.1.c) to the observed TPR improvements.

## Score and Decision

**Calibration.** Round 1 bracketing (5.5–7.5) using the following anchors:

| Anchor Paper | Avg Score | Comparison |
|-------------|-----------|------------|
| Watermarking using Semantic-aware Speculative Sampling | 6.00 (Reject) | Had proof errors and weak theory-practice connection; current paper is cleaner and better-integrated → higher |
| On the Learnability of Watermarks for Language Models | 5.75 (Accept) | More empirical, less theoretical depth; comparable quality |
| On the Reliability of Watermarks for Large Language Models | 6.00 (Accept) | Empirical robustness study; current paper has stronger theory |
| Black-Box Detection of Language Model Watermarks | 7.00 (Accept) | Strong empirical paper; current paper has stronger theory but weaker experiments |
| Sparse Watermarking in LLMs | 3.00 (Reject) | Lower quality, less relevant |
| WAPITI | 3.75 (Reject) | Lower quality |

The paper under review sits above the SEAL paper (avg 6.00) because its theory is cleaner and directly connected to the algorithm, but below Black-Box Detection (avg 7.00) because of the temperature issue and limited empirical scope. Its theoretical contributions are well-developed and clearly presented, making it a solid contribution to the ICLR community. The temperature concern prevents a higher score but is addressable.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>
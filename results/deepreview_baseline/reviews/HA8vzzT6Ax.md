## Summary

This paper revisits the trade-off between watermark strength and speculative sampling efficiency in LLMs. It introduces a quantitative measure of watermark strength (expected KL divergence), characterizes the trade-off as a Pareto frontier via constrained optimization, and proposes a mechanism—pseudorandom draft-token acceptance—that theoretically achieves maximal watermark strength while preserving maximal sampling efficiency. Experiments on ELI5 with Llama and Gemma model pairs show that the method maintains efficiency and improves detectability compared to prior approaches.

## Strengths

- **Novel quantitative measure of watermark strength.** Defining strength as expected KL divergence (equivalently mutual information under unbiasedness) is principled and directly connects to statistical detectability via p-value decay (Theorem 3.1). This moves beyond the binary definition in prior work and enables a continuous trade-off analysis.
- **Rigorous characterization of the trade-off.** The paper formalizes the trade-off as a Pareto frontier (Definition 3.2) and derives explicit curves for linear watermark classes and for Hu’s and Google’s schemes. The formulation is general and can be applied plug-and-play to other watermarking methods.
- **Clever mechanism to break the trade-off.** The key insight—making the acceptance decision pseudorandom so the entire generation is a deterministic function of pseudorandom variables—is elegant and theoretically sound. Theorem 4.1 proves unbiasedness, maximal sampling efficiency, and maximal watermark strength under the assumption of degenerate watermarks.
- **Improved detectability in practice.** The detection methods (Ars-τ for Gumbel-max, Bayes-MLP for SynthID) leverage the pseudorandom acceptance variable to select the correct test statistic, leading to higher TPR at fixed FPR compared to prior averaging-based detectors. Experiments confirm this improvement while maintaining efficiency (AATPS matches standard speculative sampling).
- **Clear writing and well-structured presentation.** The paper is easy to follow, with careful definitions, lemmas, and theorems that build logically toward the main contributions.

## Weaknesses

### Major

- **Trade-off is only broken for degenerate watermarks.** The theoretical guarantee of simultaneously achieving maximal strength and maximal efficiency (Theorem 4.1) relies on the assumption that the watermark decoder is degenerate (i.e., produces a deterministic function of pseudorandomness). While Gumbel-max and SynthID (in the limit) satisfy this, many practical watermarking schemes are not degenerate. The paper acknowledges this as an open direction, but the claim of “breaking the trade-off” is somewhat overstated—it applies to a specific class of watermarks. The trade-off for non-degenerate watermarks remains unresolved.

### Minor

- **Detection methods require training data.** Both Ars-τ (calibration on held-out set) and Bayes-MLP (training a three-layer MLP) need labeled watermarked and unwatermarked texts. In deployment scenarios where such data is scarce or expensive to obtain, this could be a practical limitation. The paper uses 1,000 training texts, which is reasonable but not always available.
- **Limited experimental scope.** The main experiments use only one dataset (ELI5) and two model pairs (Llama-68M/7B, Gemma-2B/7B). While additional results on C4 are in the appendix, the core claims would be strengthened by more diverse datasets and model sizes. The confidence intervals in Figure 2 are also somewhat wide, especially for SynthID.
- **Impact of bonus step on detection is glossed over.** The paper notes that bonus steps (when all K draft tokens are accepted) are not controlled by the acceptance variable and could affect detection, but argues the effect is negligible for K not too small. A more quantitative analysis (e.g., frequency of bonus steps in experiments) would be helpful.

### Trivial

- None.

## Nice-to-Haves

- Extend the framework to non-degenerate watermarks (e.g., biased watermarks or those with tunable strength) to see if similar improvements can be obtained.
- Investigate the robustness of the proposed detection methods to adversarial edits or paraphrasing, as mentioned in the conclusion.
- Provide a more detailed analysis of the computational overhead of generating pseudorandom acceptance variables (though likely negligible).

## Novel Insights

Beyond the paper’s own contributions, the key insight is that the “inevitable” trade-off between watermark strength and speculative sampling efficiency is not fundamental—it arises from the use of true randomness in the acceptance step. By replacing that randomness with pseudorandomness that is recoverable at detection time, the entire generation process becomes a deterministic function of shared pseudorandom variables, allowing both maximal strength and maximal efficiency to coexist. This principle unifies speculative sampling and watermarking in a way that was not previously recognized.

## Suggestions

- Clarify in the abstract and introduction that the trade-off is broken for degenerate watermarks, to avoid overclaiming.
- Include a table or figure showing the frequency of bonus steps in the experimental setup to justify the claim that their impact on detection is negligible.
- Consider evaluating on an additional dataset (e.g., XSum or CNN/DailyMail) to increase diversity of results.

## Score and Decision

**Score:** 8  
**Decision:** Accept

MY FINAL SCORE: <score>8</score>  
MY FINAL DECISION: <decision>Accept</decision>
## Summary

This paper introduces Insertion Language Models (ILMs), a new approach to sequence generation where tokens are inserted one at a time at arbitrary positions, using a denoising objective that drops tokens rather than masking them. ILMs overcome two key limitations: the fixed left-to-right ordering of autoregressive models and the fixed-length masking constraint of masked diffusion models. Experiments on planning tasks (star graphs, zebra puzzles) show ILMs achieve near-perfect accuracy where both ARMs and MDMs fail dramatically, while on text generation and infilling tasks ILMs are competitive with ARMs and outperform MDMs.

## Strengths

- **Novel training objective that enables stable insertion-based generation.** The paper identifies the high-variance problem of a naive insertion denoising objective and proposes a biased but tractable alternative that directly uses normalized counts of dropped tokens. This is a non-trivial technical contribution that makes ILMs trainable.
- **Compelling empirical demonstration of failure modes and their resolution.** On star graphs with variable arm lengths, MDMs drop to 21% accuracy while ILMs achieve 99.1%; on zebra puzzles, ILMs outperform ARMs (90% vs 81.2%) and MDMs (82.6%). These synthetic tasks are carefully designed to isolate the limitations the paper claims to address.
- **Clear and accessible exposition.** The paper provides intuitive examples (the chef/desert illustration in Figure 1), clean diagrams (Figure 2), and precise algorithms. The distinction between ILMs, ARMs, and MDMs is well-motivated and easy to follow.
- **Comprehensive evaluation spanning both constrained planning and open-ended language.** The paper does not limit itself to synthetic tasks—it validates on LM1B and TinyStories with multiple metrics (NLL, entropy, LLM judge) and infilling setups, showing ILMs are practical for text generation as well.
- **Flexibility that MDMs cannot match.** ILMs naturally support arbitrary-length infilling (both single-segment and multi-segment) while MDMs are fundamentally limited by their fixed mask count. The infilling results (Table 3) confirm this advantage.

## Weaknesses

### Major

- **The biased training objective is not fully analyzed.** The paper acknowledges the variance issue of a naive estimator and uses a biased approximation, but it provides no analysis of the bias-variance tradeoff, no bounds on the bias, and no empirical comparison to an unbiased estimator (even for small sequences where Monte Carlo might be feasible). This is a central component of the method and its properties deserve deeper scrutiny.
- **On text tasks, ILMs underperform ARMs in NLL and the gap is not satisfactorily explained.** The paper attributes this to "training token efficiency and scaling laws" but does not provide any evidence (e.g., scaling curves, token counts seen during training). Without analysis, readers cannot evaluate whether the gap is inherent or due to hyperparameter choices. The lower entropy of ILM generations on LM1B (2.80 vs ARM's 3.12 and dataset's 3.08) also suggests a diversity concern that is not addressed.

### Minor

- **Inference efficiency is mentioned as a limitation but not quantified.** ILMs cannot use KV caching, and the paper states this makes them slower than ARMs, but no wall-clock time comparison is provided beyond Figure 6 (which only shows MDM vs ILM vs ARM without KV cache). A fair comparison with cached ARMs would be informative.
- **Only small-scale experiments are conducted (85M parameter models, 1B token datasets).** While acceptable for a method paper, the paper's claims about ILMs' potential would be strengthened by at least a preliminary scaling study to show the method works at larger sizes.

### Trivial

- None beyond what the parser artifacts would normally produce.

## Nice-to-Haves

- An analysis of the bias introduced by the counting-based target insertion distribution, perhaps with a small-scale comparison to a Monte Carlo baseline.
- Scaling experiments (e.g., doubling model size or training tokens) to verify that ILMs continue to improve and remain competitive with ARMs.
- A quantitative comparison of inference speed: ILM vs ARM (with and without KV cache) on the same hardware.
- Exploration of data-dependent noising schedules, which the paper suggests as a way to close the text NLL gap.

## Novel Insights

The paper's central insight—that the failure of masked diffusion models on constrained tasks stems from simultaneous unmasking and fixed-length masks, and that inserting tokens one-at-a-time using relative positional information resolves both issues—is genuinely novel. The star graph experiments are particularly instructive: MDMs fail when arm lengths vary because their absolute position predictions break down, while ILMs succeed by iteratively inserting tokens using relative context. This suggests that generation order and positional encoding interact in ways that are underappreciated. The paper also reveals that a simple counting-based approximation of the denoising distribution (as opposed to learning a reverse process step-by-step) can be effective, which is a surprising finding for the diffusion community.

## Suggestions

1. Provide a theoretical or empirical analysis of the bias in the approximate training objective, perhaps by comparing to an unbiased estimator on short sequences.
2. Report the number of tokens seen during training for each model type, and show loss curves to verify that convergence is not the issue for the ARM-ILM gap on text.
3. Include a wall-clock speed comparison with an ARM that uses KV caching, to give practitioners a clear picture of the tradeoff.

## Score and Decision

Score: 8, Decision: Accept

MY FINAL SCORE: <score>8</score>  
MY FINAL DECISION: <decision>Accept</decision>
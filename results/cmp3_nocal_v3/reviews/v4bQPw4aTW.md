## Summary

AdaBoN proposes a simple, training-free two-stage method for adaptively allocating a Best-of-N inference budget across a batch of prompts. In the first stage, a fixed per-prompt exploration budget is used to estimate each prompt's reward distribution via Gaussian KDE. In the second stage, a greedy algorithm allocates the remaining budget to prompts with the highest estimated marginal gain. The method is evaluated across 12 LM-RM pairs, 3 datasets, and 50 batches per condition.

## Strengths

- **Practical, training-free method (Section 3, Algorithm 2).** AdaBoN requires no auxiliary model training, uses only KDE and a greedy allocation procedure, and works out-of-the-box with any LM-RM combination. This is a genuine advantage over the auxiliary-model approach of Damani et al. (2024).

- **Broad empirical scope.** The paper evaluates across 12 LM-RM pairs, 50 batches of prompts per condition, and 3 datasets (AlpacaEval, HH-RLHF, PKU-SafeRLHF). This is substantially broader than the prior work it builds on (Damani et al., 2024, which uses a single LM-RM pair and a single batch in its real-valued reward experiments).

- **Well-motivated latency-aware design (Section 2.3, page 4).** The two-stage (rather than fully sequential) policy is explicitly motivated by latency, enabling parallelization of LM calls in the exploration stage. The paper correctly identifies this as a practical consideration that prior adaptive methods overlook.

## Weaknesses

### Fatal

None.

### Major

- **Only one baseline (uniform allocation).** AdaBoN is compared only against uniform Best-of-N (Section 4.2, Equation 3). Uniform allocation is the minimax optimal non-adaptive baseline, but it is the weakest possible comparison for an adaptive method. The paper does not compare against any competing adaptive approach — not the closest prior work (Damani et al., 2024), nor even a simple adaptive heuristic such as "allocate remaining budget to prompts with highest empirical variance" or "allocate to prompts with lowest observed max reward." Without such a baseline, the reader cannot determine whether the observed gains are due to AdaBoN's specific allocation mechanism or simply to the fact that any non-uniform allocation introduces variation. The paper explains why it cannot compare with Damani et al. (2024) — lack of available implementation and prohibitive computational demands — but this does not excuse the absence of any sanity-check baseline.

### Minor

- **"Small exploration budget" is a mischaracterization.** The abstract and contribution list (lines 9, 28) describe the exploration phase as using a "small exploration budget," but the main experiments use d = 0.75B (line 215), meaning 90 out of 120 per-prompt queries (75%) are spent on uniform exploration, leaving only 30 (25%) for adaptive allocation. AdaBoN with d=0.75B is predominantly a uniform BoN method with a modest adaptive refinement. The paper is transparent about the actual value of d in the experimental section, but the high-level framing inflates the role of adaptivity. The paper also tunes d only over {0.60B, 0.70B, 0.75B, 0.80B} — never testing with genuinely small exploration budgets (e.g., d=0.1B) that would more convincingly demonstrate adaptive ability.

- **No formal statistical significance testing.** Median BWRs range from 0.54 to 0.62 (Table 1) — modest improvements over the 0.50 coin-flip baseline. The paper reports interquartile ranges and the percentage of batches with BWR > 0.50 (Table 2b, showing 76–100%), but does not report any formal significance test (e.g., bootstrap confidence intervals, one-sample Wilcoxon test, or permutation test). Given that some lower quartiles are at or near 0.51 (e.g., Qwen-Armo: [0.51, 0.56]; Gemma-Mistral: [0.51, 0.59]), the reader needs confidence that the improvements are not within the noise of the experimental setup.

- **On-device inference motivation is incongruent with the models used.** The paper motivates its small-K large-B regime with "personalized on-device inference" (line 25), but evaluates with 7–8B parameter LMs (Mistral-7B, Gemma-7B, Qwen2.5-7B, Llama-3-8B), which are not typical on-device models. This weakens the stated motivation, though it does not affect the validity of the experimental results (the method is model-agnostic).

### Trivial

None.

## Nice-to-Haves

- Testing with genuinely small exploration budgets (e.g., d = 0.1B or d = 0.25B) would provide a much stronger demonstration of the adaptive component's value.
- Adding a simple adaptive heuristic baseline (e.g., allocating remaining budget proportional to empirical reward variance) would help isolate whether the specific KDE+greedy mechanism matters or any adaptive scheme suffices.
- Reporting sensitivity to the Monte Carlo sample size (m=1024) for V_{i,j} estimation would improve reproducibility.

## Removed Points

These points were flagged in the input reviews but are removed (with justification):

1. **Figure 3 caption mismatch (Medical/Math/ArXiv).** The embedded image OCR text in the PDF extraction references "Medical, Math, ArXiv," but the paper's actual text caption (line 236) correctly reads "AlpacaEval dataset." The image OCR is a parser/formatting artifact, not an author error.

2. **Bernoulli example is unrealistic.** The paper presents this as a "simple example" (line 84) for illustrative purposes only; it is not claimed to represent real reward distributions.

3. **EST interpretation is unclear.** The paper's EST definition (Equation 5) is mathematically precise. An EST of ~150 is correctly interpreted as meaning AdaBoN with B=120 matches uniform allocations with ~20% larger budget on average.

4. **The 216,000 MLPs number is a straw-man argument.** The paper gives multiple independent reasons for not comparing with Damani et al. (2024): no available implementation, insufficient hyperparameter details, and computational cost. The exact count is secondary to the primary issue of unavailable implementation.

5. **Missing related works.** Removed per policy (no external sources to verify).

## Novel Insights

None beyond the paper's own contributions. The review surfaces a key observation not emphasized in the paper: with d=0.75B, AdaBoN is better characterized as "uniform BoN with 25% adaptive refinement" than as an adaptive allocation method, which reframes the significance of the results. Otherwise, the strengths and weaknesses identified align with the paper's own framing.

## Suggestions

1. **Add at least one simple adaptive baseline.** Even a heuristic like "allocate remaining budget to prompts with highest reward variance" would establish that AdaBoN's specific mechanism matters.
2. **Calibrate the "small exploration budget" language in the abstract.** Replace "small" with a precise description such as "a tunable exploration budget (defaulting to 75% of the total per-prompt budget)."
3. **Report formal statistical significance** for the primary BWR results against the 0.50 baseline.
4. **Consider testing with smaller d values** (e.g., d=0.25B or d=0.1B) to demonstrate adaptivity more convincingly.
5. **Tighten the on-device motivation** by either using smaller models or adjusting the framing to match the 7-8B models actually evaluated.

## Score and Decision

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>
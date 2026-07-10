Now let me write the final consolidated review.

## Summary

The paper proposes "Power Sampling," an MCMC-based inference-time method that samples from the sharpened power distribution p^α of a base LLM, without any training, datasets, or verifiers. The key contributions are: (1) a clear theoretical distinction between power distribution sampling and low-temperature sampling (Proposition 1), (2) a progressive-block MCMC algorithm (Algorithm 1) to approximate sampling from p^α, and (3) empirical results showing the method matches or exceeds GRPO on reasoning benchmarks while preserving generation diversity that RL post-training eliminates.

## Strengths

- **Clear theoretical distinction between power distribution and low-temperature sampling (Section 4.1, Proposition 1, Example 1).** The paper correctly identifies that low-temperature autoregressive sampling is NOT equivalent to sampling from p^α, with the "sum of exponents vs. exponent of sums" distinction (Eqs. 7–8) being pedagogically crisp. The two-token toy example cleanly illustrates why this difference matters for reasoning contexts. This is a genuinely useful clarification that the community has been sloppy about.

- **Training-free inference-time method with striking empirical results (Table 1).** Across three model families (Qwen2.5-Math-7B, Qwen2.5-7B, Phi-3.5-mini-instruct) and four benchmarks, the method produces large improvements over the base model (up to +51.9% on HumanEval with Phi-3.5) and is competitive with—sometimes exceeding—GRPO on single-shot tasks.

- **Diversity preservation demonstration (Figure 5).** The pass@k curves show that the proposed method maintains near-base-model pass@k for large k while achieving GRPO-level single-shot accuracy. This is a genuine differentiator from RL-posttraining, which is known to sacrifice generation diversity.

- **Elegant algorithmic design (Algorithm 1, Section 4.3).** The progressive-block MCMC strategy, using intermediate distributions π_k to avoid exponential mixing times in the high-dimensional token space, is methodologically sound and addresses a real concern with naive MCMC for LLMs.

## Weaknesses

### Major

- **N_{MCMC} is never reported (Section 5.1, Algorithm 1).** The paper lists N_{MCMC} as a hyperparameter in Algorithm 1 and provides the token-cost formula (Eq. 12: E[tokens] ≈ N_{MCMC}·T²/(4B) = N_{MCMC}·~12,288 with T=3072, B=192), but never states the actual value used. The only description is "relatively small values of N_{MCMC}" (line 231). Without this number, the computational cost (expected tokens per response ≈ N_{MCMC}·~12k vs. ~600–700 for a standard forward pass) cannot be assessed, making it impossible to evaluate whether the method achieves results through principled sampling or brute-force compute over orders-of-magnitude more tokens. This is a concrete evidential gap that undermines the practical significance claims in the abstract and conclusion.

### Minor

- **The GRPO baseline for Phi-3.5-mini-instruct appears poorly calibrated (Table 1).** On HumanEval, GRPO scores 0.134 vs. base 0.213 (a 37% *decrease*); on MATH500, GRPO improves the base by only 0.6pp (0.400→0.406). Hyperparameters were selected to "avoid training instabilities" rather than maximize performance, but the HumanEval regression is striking. This inflates the relative advantage of power sampling on Phi-3.5 (the model where the paper claims the strongest "outperformance"), though the core claims are still supported by the Qwen2.5 results where GRPO is properly tuned.

- **No variance or statistical significance reported (Table 1, Figures 4–5).** All results are single point estimates. Given the stochastic MCMC sampler (random resampling, acceptance/rejection), performance may vary across runs. Error bars or multiple-seed results would help assess whether the observed advantages (e.g., 57.3% vs. 53.7% on HumanEval for Qwen2.5-Math) are reliable.

- **The pass@k comparison (Figure 5) is compute-asymmetric.** Each power sampling sample costs orders of magnitude more than each GRPO sample (even for modest N_{MCMC}), but both methods are compared at equal sample count k without acknowledging this disparity. The diversity advantage is real, but its magnitude relative to cost is overstated when resource budgets are not equated.

- **Missing ablations.** (a) α sensitivity is not analyzed — the paper uses α=4.0 throughout for reasoning but provides no study of how performance varies with this key hyperparameter. (b) No acceptance rates are reported, so it is unclear how well the MCMC chain mixes in practice. (c) EOS handling is mentioned briefly ("termination can happen earlier with an EOS token") but the progressive blocking scheme (π_k) assumes fixed-length prefixes — how early termination interacts with the MCMC framework is not discussed.

### Trivial

None.

## Nice-to-Haves

- Include cost-matched comparisons to simpler inference-time methods (e.g., self-consistency, best-of-N at matched token budgets). Many of these methods share the "training-free, dataset-free, verifier-free" characteristic the paper highlights. Showing that power sampling outperforms them at equivalent compute would substantially strengthen the paper's claims.
- Add a brief discussion of how the acceptance ratio (Eq. 9) involves computing p^α for the full sequence at each MCMC iteration — this overhead is not discussed.

## Removed Points

- **"No comparison to other inference-time methods (self-consistency, best-of-N, tree-of-thoughts)"** — REMOVED. The paper's primary comparison target is RL training (GRPO), and it does compare against low-temperature sampling. Adding simpler inference-time baselines would strengthen the paper but their absence is not a flaw given the stated scope of matching RL. Moved to Nice-to-Haves.
- **"Abstract/Introduction framing over-extended"** — REMOVED. The paper frames its motivating question appropriately for the discussion it engages with; not a concrete weakness.
- **"Section 5.3 undermines distribution sharpening motivation"** — REMOVED. The observation that power sampling and GRPO achieve similar accuracy through different distributional mechanisms is a finding, not a weakness.
- **"Acceptance ratio computational overhead not discussed"** — REMOVED. The computational cost of log-likelihood computations is inherent to the MH acceptance step and the paper provides the token-cost formula. Moved to Nice-to-Haves.
- **"Pure formatting/style nitpicks"** — REMOVED per filtering rules.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- **Report N_{MCMC}** and provide a compute-accuracy Pareto curve (accuracy vs. total tokens generated) for different values of N_{MCMC} so readers can evaluate the cost-performance trade-off.
- Rerun or recalibrate the GRPO baseline for Phi-3.5-mini-instruct, or acknowledge the limitation and its effect on claims of "outperformance" more explicitly.
- Add variance estimates (multiple seeds or bootstrapped confidence intervals) for main results given the stochastic nature of the MCMC sampler.
- Include an ablation study for α and report acceptance rates from the MCMC chain.
- Add a compute-matched pass@k comparison (e.g., 1 power sample vs. N GRPO samples at equivalent token budget).

## Score and Decision

**Bracket analysis (Round 1):** I identified the plausible range as 5.5–7.5 by comparing against anchors spanning 8.0 (SMC paper, very clean evaluation), 6.60 (TSMC paper, similar MCMC-for-reasoning approach with missing compute details), 6.40 (ULTS, rejected on fundamental Bayesian issues), and 5.75 (Inference Scaling Laws, limited domain scope).

**Narrowing (Rounds 2–3):** The closest topical anchor is the TSMC paper (Ze4aPP0tIn, avg 6.60, Accept), which also uses Monte Carlo methods for LLM reasoning and also had missing inference-time compute statistics (weaknesses scored near-zero impact by the model) and a -10.00 "code not provided" weakness — yet still scored 6.60. The Compute-Optimal Sampling paper (3OyaXFQuDl, avg 7.00) similarly had a -10.00 weakness about limited dataset scale. The reviewed paper's missing N_{MCMC} is genuinely impactful but fixable, and the theoretical contribution (power distribution vs. low-temperature distinction) is stronger and more original than the TSMC paper's contribution.

**Final placement:** The paper has a genuinely strong theoretical contribution and impressive empirical results, but the missing N_{MCMC} parameter prevents full evaluation of practical significance. At 6.0, the paper sits slightly below the TSMC anchor (6.60) because the missing N_{MCMC} is more central to evaluating the method than the TSMC paper's missing details, but well above the ULTS paper (6.40, Rejected) and the MCMC extrapolative paper (4.75, Rejected) which had fundamental methodological flaws.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>
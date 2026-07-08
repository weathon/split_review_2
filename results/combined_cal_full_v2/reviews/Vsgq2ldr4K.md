Now I have all the information needed. Let me compose the final review.

## Summary

This paper proposes a training-free inference-time sampling method for LLMs that targets the "power distribution" p^α (the base model's distribution exponentiated) using a block-wise Metropolis-Hastings MCMC algorithm. The core theoretical contribution is clarifying that sampling from p^α is distinct from low-temperature sampling (Proposition 1), and the key empirical finding is that this method achieves reasoning accuracy comparable to or exceeding GRPO on several benchmarks while preserving generation diversity that RL collapses. The method requires no training, no curated datasets, and no verifier, making it applicable beyond verifiable domains.

## Strengths

- **Theoretical clarity on power distributions vs. low-temperature sampling (Section 4.1, Proposition 1, Example 1).** The paper proves that exponentiating the joint distribution (p^α) is not equivalent to low-temperature sampling, using the "sum of exponents" vs. "exponent of sums" contrast (Equations 7–8). The simple 2-token example cleanly demonstrates why the distinction matters. This is a genuine conceptual contribution that stands independently of the experimental results.

- **Training-free, dataset-free, and verifier-free method.** The proposed method requires no curated training data, reward design, hyperparameter sweeps for training stability, or verifier. This is a meaningful practical advantage over RL-based approaches and suggests applicability to non-verifiable domains where RL cannot be applied.

- **Diversity preservation is convincingly demonstrated (Figure 5).** The pass@k curves show GRPO plateauing around k=4–5 at ~90% while power sampling continues climbing to ~98%, matching the base model's asymptotic performance. This is a non-trivial empirical finding aligning with prior observations about RL-induced diversity collapse, and is consistent across the reported data.

- **Reasonable multi-model, multi-task evaluation breadth.** Testing on three model families (Qwen2.5-Math-7B, Qwen2.5-7B, Phi-3.5-mini-instruct) across four benchmarks (MATH500, HumanEval, GPQA, AlpacaEval 2.0) provides comparative breadth, and results are generally consistent across models.

## Weaknesses

### Major

- **N_MCMC — the hyperparameter controlling the method's entire compute budget — is not reported in the experimental setup.** Section 5.1 lists T=3072, B=192, α=4.0, and the proposal temperature, but N_MCMC (the number of MCMC steps) is never given a numerical value. Equation (12) shows the expected token budget is ≈ N_MCMC × T²/(4B) ≈ 12,288 × N_MCMC tokens per output sequence, meaning N_MCMC=10 would cost ~40× a standard forward pass and N_MCMC=100 would cost ~400×. Without this number, the comparisons in Table 1 are uninterpretable in terms of cost, the results are not reproducible, and a reader cannot assess whether the method offers a favorable accuracy-compute trade-off or merely spends more compute to get better accuracy. The paper mentions "relatively small values of N_MCMC" (line 231) but never states what those values are.

- **No MCMC convergence diagnostics are provided.** The paper acknowledges the risk of exponential mixing time in high-dimensional token spaces (Section 4.3) and proposes a block-wise sequential approach to mitigate it, but provides no empirical evidence that the chain actually converges to the target distribution p^α. Standard diagnostics — acceptance rates, trace plots, effective sample size, or Gelman-Rubin statistics — are absent. The only evidence offered is that resulting sequences have higher average likelihood under the base model, which is a necessary but not sufficient condition for convergence to p^α. Without these diagnostics, the paper's central methodological claim (that the algorithm approximately samples from p^α) remains unverified.

- **The Phi-3.5-mini GRPO baseline appears anomalously weak, inflating the apparent advantage of power sampling.** GRPO on Phi-3.5 achieves only 40.6% on MATH500 (barely above the base model's 40.0%) and 13.4% on HumanEval (below the base model's 21.3%). The paper states that the Phi-3.5 GRPO training used hyperparameters "selected from Abdin et al. (2024) that avoids training instabilities and converges to improvement over the base model over a large number of epochs" (line 268), but the near-zero improvement on MATH500 and degradation on HumanEval suggest the training may not have converged properly or used suboptimal settings. Power sampling then outperforms this weak baseline by large margins (73.2% vs. 13.4% on HumanEval), making the claimed "outperformance" less compelling.

### Minor

- **The "single-shot" framing obscures a large compute asymmetry between methods.** The paper presents all methods as "single-shot" (one final response string) in Table 1, but power sampling makes many sequential inference calls per output while GRPO generates one autoregressive chain in a single pass. The paper acknowledges this at line 203 ("even though multiple inference calls are made... We can interpret this as a new axis for inference-time scaling") but does not provide compute-controlled experiments (e.g., matching token budgets across methods). Without such controls, the reader cannot determine whether power sampling's improvements come from better use of compute or simply from spending more of it.

- **No ablation of key hyperparameters α and N_MCMC.** The paper reports using α=4.0 and mentions "relatively small" N_MCMC values, but provides no sensitivity analysis showing how performance varies with these parameters. This makes it difficult to assess how robust the method is or how to configure it in practice.

- **Low-temperature baseline temperature is not specified.** The paper reports a "Low-temperature" baseline in Table 1 but never states which temperature value was used. Given that the proposal distribution for power sampling uses τ=1/α=0.25, this control should use the same temperature for fair comparison, but the reader cannot verify this.

- **Compute cost formula (Equation 12) undercounts true cost.** The formula counts only tokens generated during the MCMC process but omits the forward passes needed to compute likelihoods for the Metropolis-Hastings acceptance ratio, which requires evaluating p(x)^α for at least the proposed sequence at each step. This adds a constant-factor overhead not captured by the token count estimate.

### Trivial

None.

## Nice-to-Haves

- A comparison against best-of-N sampling from the base model at matched compute budget would help isolate whether the MCMC structure itself provides benefit over naive compute scaling.
- Wall-clock time or FLOPs comparisons between methods would make the practical trade-off concrete.
- An ablation varying N_MCMC (e.g., 1, 5, 10, 50 steps) would clarify how much compute is needed and whether the method is sensitive to this parameter.

## Removed Points

These points are flagged to be removed; treat them with caution:

- **"Out-of-domain comparison stacks the deck against GRPO"** — The paper explicitly labels HumanEval and GPQA as "out-of-domain" and is transparent that GRPO was trained only on MATH. The claim that GRPO underperforms on out-of-domain tasks is an expected consequence of specialization, not a deceptive comparison. However, the Phi-3.5 baseline concern (retained above) is a separate issue about baseline quality, not domain mismatch.

- **"Single-shot comparison is misleading" (as a standalone criticism)** — The paper explicitly acknowledges at line 203 that "even though multiple inference calls are made" and frames this as inference-time scaling. The paper is transparent about the method using more compute. This concern is subsumed by the retained Minor weakness about the compute asymmetry not being quantified.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Report N_MCMC as used in all experiments**, and add a compute-controlled comparison where the total token budget (or wall-clock time) is matched across methods (e.g., compare power sampling against best-of-N from GRPO/base model at equal total tokens).
2. **Provide MCMC convergence diagnostics**: report acceptance rates, trace the evolution of sequence likelihoods over MCMC steps, or run a small-scale experiment where the true p^α can be exactly computed to verify chain convergence.
3. **Add ablations** showing sensitivity to α (e.g., α ∈ {2, 4, 8}) and N_MCMC (e.g., 1, 5, 10, 50).
4. **Re-evaluate the Phi-3.5 GRPO baseline** to ensure proper convergence, or acknowledge its weakness explicitly and restrict claims to the Qwen models where GRPO shows meaningful improvement.
5. **Specify the temperature** used for the low-temperature baseline.
6. **Update the compute cost analysis** (Equation 12) to account for likelihood evaluation passes.

## Score and Decision

**Calibration overview.** I retrieved 14 anchor papers across two rounds of calibration_search, spanning avg human scores from 0.50 to 8.00. Round 1 bracketed the candidate in [5.5, 7.5]. I itemized four anchors in this range for close comparison:

| Anchor | Path | Avg Score | Round | Itemized? | Comparison |
|--------|------|-----------|-------|-----------|------------|
| Twisted SMC for Math | Ze4aPP0tIn.md | 6.60 | R1 | Yes | MCMC for LLM reasoning; similar strengths (7.29–9.86) and weaknesses (0.37–6.23). Our paper has stronger theoretical novelty but weaker hyperparameter reporting. |
| Large Language Monkeys | 0xUEBQV54B.md | 5.00 | R1 | Yes | Inference compute scaling; core finding was seen as trivial/expected. Our paper has a non-trivial theoretical contribution, placing it above. |
| Smaller Weaker Yet Better | 3OyaXFQuDl.md | 7.00 | R2 | Yes | Compute-optimal sampling; thorough ablations and rigorous experiments. Our paper's strength weights are comparable (8.88–10.40 vs 5.17–9.67) but our critical weaknesses (compute transparency, missing ablations) are more impactful. |
| Flow of Reasoning | HHmnfVQagN.md | 5.75 | R2 | Yes | Diversity in reasoning; clarity/novelty concerns. Our paper is clearer and has stronger theoretical grounding, placing it above. |
| SMC Controlled Gen | xoXn62FzD0.md | 8.00 | R1 | Yes | SMC for constrained generation; thorough evaluation with ablations. Our paper lacks equivalent experimental rigor. |

**Weighted-item comparison.** The reviewed paper's strongest items — diversity preservation (weight 10.40), theoretical clarity (9.22), training-free nature (8.96) — are comparable to the Twisted SMC anchor's strongest items (9.86, 9.83, 9.45). However, the paper's most impactful weaknesses — compute cost formula undercount (7.84), compute asymmetry (5.62), missing ablations (5.20) — carry more negative weight than the Twisted SMC anchor's corresponding items (max weakness weight 6.23), placing it below that anchor. The Large Language Monkeys anchor (5.00) was downgraded for triviality of its core finding, which does not apply here. The paper sits between the Monkeys (5.00) and Smaller-Weaker (7.00) anchors, closer to Twisted SMC (6.60).

**Final score: 6.0.** The theoretical contribution (Proposition 1) and the diversity preservation finding (Figure 5) are genuinely valuable. The method's training-free nature is a real practical advantage. However, the paper's experimental evaluation is incomplete in ways that prevent a higher score: the missing N_MCMC value makes compute cost opaque, the lack of convergence diagnostics leaves the central methodological claim unverified, and the Phi-3.5 baseline is anomalously weak. These are addressable in revision but as presented they meaningfully limit the paper's contribution.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>
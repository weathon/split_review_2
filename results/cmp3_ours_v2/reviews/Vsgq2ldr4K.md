Now let me write the final review.

**Round 1 Bracket:** Based on calibration, the most directly relevant anchors are:
- TSMC for math reasoning (avg 6.60, accepted) — similar MCMC-for-reasoning approach, but requires training a value function; tested on fewer tasks
- SMC-controlled generation (avg 8.00, accepted) — stronger execution, broader evaluation, cleaner
- Inference Scaling Laws (avg 5.75, accepted) — empirical analysis with limited novelty concerns

The current paper's theoretical contribution (power distribution vs. low-temperature distinction, Proposition 1) is genuine and non-trivial, its empirical breadth (4 benchmarks × 3 model families) exceeds the TSMC paper, and it is fully training-free. However, it has the Phi-3.5 GRPO baseline issue and lacks compute-cost comparison. Based on these anchors, the plausible range is **5.75–7.0**.

## Summary

This paper proposes "Power Sampling," a training-free MCMC-based algorithm that samples from the sharpened power distribution p^α of a base LLM to elicit reasoning capabilities. The key insight is that sampling from p^α differs qualitatively from low-temperature sampling (sum-of-exponents vs. exponent-of-sums), and that doing so can produce single-shot reasoning performance approaching or exceeding RL-based posttraining (GRPO) without requiring any training data, verifiers, or reward models. Experiments across three model families and four benchmarks show Power Sampling approaches GRPO on in-domain MATH500 (74.8% vs. 78.5% on Qwen2.5-Math-7B), outperforms it on out-of-domain HumanEval (57.3% vs. 53.7%) and AlpacaEval 2.0, and preserves generation diversity where GRPO collapses.

## Strengths

1. **Theoretical insight in Proposition 1 and Observation 1 (Section 4.1).** The paper cleanly proves that low-temperature sampling does not sample from p^α and illustrates the qualitative difference with a simple 2-token example. The "sum of exponents vs. exponent of sums" distinction is a genuine, non-trivial observation that clarifies a commonly conflated distinction in the literature.

2. **Strong empirical results across multiple models (Table 1).** Power Sampling achieves 74.8% on MATH500 with Qwen2.5-Math-7B (vs. GRPO's 78.5%), outperforms GRPO on HumanEval (57.3% vs. 53.7%), and the pattern broadly holds across Qwen2.5-7B, Qwen2.5-Math-7B, and Phi-3.5-mini-instruct. Testing across three model families is more convincing than single-model demonstrations.

3. **Diversity preservation convincingly demonstrated (Figure 5).** The pass@k curves show Power Sampling maintaining the base model's diversity while achieving GRPO-level single-shot accuracy, directly addressing a known limitation of RL-posttraining. This is a meaningful practical advantage.

4. **Clean connection to the distribution sharpening literature.** The paper frames its contribution within the existing debate about whether RL-posttraining creates novel behaviors or merely sharpens the base distribution. This gives the work intellectual coherence beyond a sampling trick.

## Weaknesses

### Major

1. **GRPO baseline for Phi-3.5-mini-instruct appears to have largely failed, weakening the multi-model comparison.** In Table 1, GRPO on Phi-3.5 achieves: MATH500 0.406 (base: 0.400 — essentially no improvement), HumanEval 0.134 (base: 0.213 — worse than the base model), AlpacaEval 16.74 (base: 14.82 — modest). On two of four benchmarks, GRPO either fails to improve or degrades performance relative to the base model. This strongly suggests the GRPO training run for Phi-3.5 was not well-tuned. While the paper notes it "avoids training instabilities" (line 268), presenting a largely failed baseline as a valid comparison inflates Power Sampling's apparent advantage. The paper should either use a properly tuned GRPO baseline for Phi-3.5 or explicitly acknowledge the training was unsuccessful and limit claims to the models where GRPO was well-tuned.

2. **No compute-cost comparison with GRPO, which undermines the "training-free" advantage claim.** The paper estimates token cost (~N_MCMC × T²/(4B) tokens per sample, Eq. 12) but provides no wall-clock time, FLOP, or total compute comparison against the GRPO pipeline (training on 7,500 MATH problems + inference). Each MCMC step also requires forward passes for likelihood computation in the acceptance ratio, which the token estimate does not capture. Without this analysis, the practical significance of "training-free" cannot be assessed — Power Sampling could require more total compute than training an RL model. This is not a tangential addition; it is central to evaluating the paper's claimed advantage.

### Minor

1. **N_MCMC is not specified in the main experimental section.** Algorithm 1 lists N_MCMC as a hyperparameter, and line 231 states the paper "empirically finds a value for B that makes Algorithm 1 performant for relatively small values of N_MCMC," but no concrete value is given in the main paper body. While this may appear in the appendix (stripped by the parser), it should be in the main text for readers to assess computational cost and reproduce results.

2. **No ablation on the power parameter α.** The paper sets α = 4.0 throughout with no sensitivity analysis. The theoretical motivation directly involves α as a controlling parameter, but no experiment shows how performance varies with α (e.g., α ∈ {2, 4, 8, 16}). This would help clarify whether the advantage over low-temperature sampling is driven by the theoretical superiority of p^α or simply by the additional compute of MCMC.

3. **No MCMC convergence diagnostics.** The paper claims the MH chain approximately samples from p^α but provides no diagnostics — no acceptance rates, trace plots, effective sample sizes, or comparison of empirical output distributions across independent chains. Without such analysis, there is no evidence the algorithm actually reaches the claimed target distribution rather than some empirically effective but unrelated distribution.

4. **No comparison to simpler inference-time baselines.** Self-consistency (majority voting) and best-of-N sampling are standard inference-time methods that also improve reasoning without training. Including these would strengthen the paper by providing a more complete picture of the training-free landscape.

5. **Confidence intervals are absent from Table 1.** Given modest benchmark sizes (e.g., GPQA Diamond: 198 questions), reporting variance would help assess result reliability.

### Trivial

None.

## Nice-to-Haves

- A per-compute-equivalent comparison between Power Sampling and GRPO (e.g., at equal total FLOPs).
- A temperature sweep for the low-temperature baseline (beyond τ = 0.25).
- An analysis of the effect of proposal distribution temperature for AlpacaEval 2.0.

## Removed Points

These points are flagged to be removed, treat them with caution:
- "The value of N_MCMC is never specified — structural reproducibility failure" → Downgraded to Minor. N_MCMC may be in the appendix (stripped by parser). Still a valid point that it should be in the main text.
- "AlpacaEval 2.0 length bias concern" → Removed. The paper explicitly states (line 266) that AlpacaEval 2.0 scores are "normalized for the length of the model response," so the paper already addresses this.
- "Low-temperature baselines may be under-optimized" → Removed. τ = 0.25 is a standard low temperature; this is a speculative criticism without specific evidence.
- "cost of likelihood computation not accounted for" → Incorporated into Major weakness #2.
- Various generic concerns without concrete anchors → Removed.

## Novel Insights

The most valuable cross-review insight is that the paper's central claimed advantage ("training-free") is impossible to evaluate without a compute-cost comparison, yet none is provided. The Phi-3.5 GRPO baseline failure is a further blind spot that the paper acknowledges obliquely ("avoids training instabilities") but does not adequately address. These are structural issues, not minor presentation gaps: they directly affect whether the paper's headline claims are supported.

## Suggestions

1. Report the value of N_MCMC and provide a wall-clock time / FLOP comparison between Power Sampling and GRPO (training + inference across an entire benchmark).
2. Either fix the Phi-3.5 GRPO baseline or explicitly acknowledge its failure and limit multi-model claims to Qwen models where GRPO was properly tuned.
3. Run an α ablation study (e.g., α ∈ {2, 4, 8, 16}) on at least one benchmark.
4. Include MCMC diagnostics: acceptance rates or a comparison of empirical output distributions across independent chains.
5. Add confidence intervals to Table 1.
6. Add self-consistency and best-of-N as additional inference-time baselines.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>
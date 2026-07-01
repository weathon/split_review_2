Here is the final consolidated review.

---

## Summary

This paper proposes "Power Sampling," an MCMC-based inference-time algorithm that targets the power distribution p^α of a base LLM, aiming to extract reasoning capabilities comparable to RL-posttraining (GRPO) without any training. It makes a clean theoretical distinction (Proposition 1): low-temperature sampling ≠ sampling from p^α. Empirically, power sampling on Qwen2.5-Math-7B achieves 74.8% on MATH500 (GRPO: 78.5%), outperforms GRPO on HumanEval (57.3% vs. 53.7%), and preserves generation diversity that RL methods lose.

## Strengths

1. **Clean theoretical contribution (Proposition 1, Section 4.1).** The paper crisply proves that low-temperature sampling does not sample from p^α, using the "sum of exponents vs. exponent of sums" distinction. Example 1 with two-token sequences concretely illustrates the difference. This is precise and non-obvious.

2. **Genuinely striking empirical results (Table 1).** Power sampling on Qwen2.5-Math-7B improves MATH500 from 49.6% (base) to 74.8%, nearly matching GRPO's 78.5%. On Phi-3.5-mini-instruct HumanEval, it achieves 73.2% vs. GRPO's 13.4%. That a training-free sampling method can approach a full RL pipeline is notable.

3. **Diversity preservation (Figure 5, Section 5.3).** The pass@k curves convincingly show power sampling maintains multi-shot performance where GRPO plateaus. This directly addresses a known weakness of RL-posttraining, and the evidence is clear.

4. **Training-free, dataset-free, verifier-free framing is honest and significant.** If the method holds up, it broadens reasoning improvements to domains without verifiable rewards, a meaningful advantage over RL.

## Weaknesses

### Fatal

None.

### Major

1. **N_MCMC is not reported (Algorithm 1, Section 5.1).** The number of MCMC steps per block is a critical hyperparameter in Algorithm 1 but is never stated. The paper provides T=3072, B=192, and α=4.0, but N_MCMC is omitted. Since the compute cost scales as O(N_MCMC · T²/B) tokens generated per output (Equation 12), the total cost cannot be estimated. This makes the method irreproducible and its practical cost opaque. The paper must state N_MCMC and report the total inference cost.

2. **Sampling parameters for the "Base" and "Low-temperature" baselines are not specified (Table 1, Section 5.1).** The paper never states what temperature or decoding strategy the "Base" row uses (temperature=1 ancestral sampling? greedy decoding?), nor what temperature the "Low-temperature" row uses. Standard reasoning evaluation typically uses greedy decoding or low-temperature sampling. Without specification, the baselines are uninterpretable and the reported gains cannot be properly contextualized.

### Minor

3. **No variance or statistical significance (Table 1).** Every result is a point estimate with no error bars, confidence intervals, or multiple seeds. Given the stochasticity of MCMC and the modest size of some benchmarks (GPQA: 198 questions, HumanEval: 164), it is unclear whether observed differences (e.g., 57.3% vs. 53.7% on HumanEval) are meaningful.

4. **No ablation on α (Section 5.1).** Only α=4.0 is reported. The paper states this was found "most performant" but provides no data on sensitivity to this key hyperparameter.

5. **AlpacaEval 2.0 uses a different proposal temperature (τ=0.5 instead of τ=0.25), acknowledged but unexplained (line 271).** This means the method requires task-specific hyperparameter tuning, which tempers the "training-free, dataset-free" framing somewhat. The paper should explain why and how to select temperatures for new tasks.

6. **The Phi-3.5-mini-instruct GRPO HumanEval result (13.4%) is far below the base model (21.3%) and the low-temperature baseline (58.5%).** This strongly suggests the GRPO model underwent distributional collapse on coding from narrow MATH-only training. The paper presents 73.2% vs. 13.4% without discussing this likely specialization effect, which overstates the advantage.

7. **No convergence diagnostics for the MCMC chain (Section 4.3, Algorithm 1).** The paper assumes N_MCMC steps suffice for mixing but provides no evidence (acceptance rates, trace plots, autocorrelation) that the chain has converged to p^α. For an MCMC-based method, this is a meaningful gap.

### Trivial

None.

## Nice-to-Haves
- Comparison with other inference-time methods (best-of-N, self-consistency) would help contextualize the cost-performance tradeoff.
- The claim about "critical windows" / "pivotal tokens" (line 163) is suggestive but never empirically validated. Directly showing this connection would strengthen the narrative.
- Ablation on B (block size) would clarify the B vs. N_MCMC tradeoff discussed in Section 4.3.

## Removed Points

These points were flagged for removal; treat them with caution.

- **"GRPO comparison on OOD tasks is structurally unfair":** Removed because the paper transparently states GRPO was trained on MATH only and explicitly labels OOD results as out-of-domain. The OOD outperformance is a legitimate finding about generalization, not a misleading comparison.
- **"Missing comparison to self-consistency, best-of-N, CoT scaling":** Removed per the rule restricting criticism of missing related works/baselines. Moved to Nice-to-Haves.
- **Speculation about "published greedy decoding numbers being higher":** The factual point (baseline parameters unspecified) is retained in Major weakness #2. The speculative claim about external published numbers is removed as unverifiable from the paper.
- **Strength #4 ("Clean conceptual narrative"):** Removed as generic and superficial.
- **Compute cost multipliers (e.g., "200-400×"):** The critic's specific factors depended on the unknown N_MCMC. The core point that N_MCMC is missing is retained; speculative cost estimates are removed.

## Novel Insights

The most interesting observation emerging from the reviews is the tension between the paper's core theoretical result and its empirical evaluation. Proposition 1 rigorously shows low-temperature sampling ≠ p^α sampling, yet the low-temperature baseline already captures much of the gain (e.g., 69.0% vs. 74.8% on MATH500 for Qwen2.5-Math). This raises the question: is the advantage of power sampling primarily attributable to the true p^α target, or is it largely captured by the low-temperature proposal with MCMC refinement? The paper does not empirically isolate this. Separately, the pass@k finding — that power sampling matches the base model's multi-shot ceiling while GRPO saturates — is a genuinely non-obvious result suggesting the diversity loss from RL is not an inevitable tradeoff of single-shot gains.

## Suggestions

1. Report N_MCMC and the total token cost per output sequence; provide a cost-accuracy Pareto frontier if practical.
2. Explicitly state the sampling parameters (temperature/decoding strategy) for the "Base" and "Low-temperature" baselines in Table 1.
3. Add greedy decoding (temperature=0) as a baseline.
4. Add variance estimates (bootstrap confidence intervals or multiple seeds) to Table 1.
5. Include an ablation on α to show sensitivity to this hyperparameter.
6. Provide at minimum acceptance rates for the MCMC chain.
7. Isolate the effect of the p^α target vs. the low-temperature proposal by comparing power sampling against a low-temperature baseline at the same effective temperature.

## Score and Decision

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>
The calibration corpus appears to be unavailable. I'll proceed with my best judgment, applying the scoring rubric based on the paper and verified reviewer claims.

Let me finalize my review.

---

## Summary

This paper proposes *Power Sampling*, an MCMC-based inference-time algorithm that targets the power distribution \(p^\alpha\) of a base LLM, aiming to elicit reasoning capabilities comparable to RL-based posttraining (GRPO) without any training. The paper provides a formal proof that low-temperature sampling is not equivalent to power-distribution sampling (Proposition 1) and introduces a block-wise annealing Metropolis-Hastings algorithm for approximate sampling. Empirically, across Qwen2.5-Math-7B, Qwen2.5-7B, and Phi-3.5-mini-instruct on MATH500, HumanEval, GPQA, and AlpacaEval 2.0, power sampling matches or exceeds GRPO on several tasks while maintaining generation diversity.

## Strengths

1. **Clear theoretical motivation (Proposition 1, Section 4.1):** The paper formally proves that sampling from \(p^\alpha\) is distinct from low-temperature sampling — a common conflation in the literature. The "sum of exponents" vs. "exponent of sums" distinction (Eqs. 7–8) is cleanly presented and mathematically sound. The toy example (Example 1, Lines 135–161) concretely demonstrates that the two samplers can disagree on which token to prefer even when the base model assigns higher conditional likelihood to the other choice, making the distinction practically meaningful. This is a genuine conceptual contribution.

2. **Strong empirical results on multiple model families (Table 1, Lines 246–264):** On Qwen2.5-Math-7B, power sampling achieves 74.8% vs. GRPO's 78.5% on MATH500 (in-domain) and 57.3% vs. 53.7% on HumanEval (out-of-domain). On Qwen2.5-7B, it achieves 70.6% vs. 74.0% on MATH500 and 62.2% vs. 56.1% on HumanEval. These results substantiate the claim that training-free sampling can approach RL-level single-shot reasoning on models where the GRPO baseline is solid.

3. **Sustained diversity over multiple samples (Figure 5, Lines 311–338):** The pass@k analysis shows power sampling maintains near-perfect diversity (pass@16 = 0.98) where GRPO plateaus (pass@16 = 0.90). The tabulated numbers (Lines 317–334) show power sampling strictly dominates GRPO for all \(k > 1\). This is a concrete advantage over RL-posttraining and addresses a known weakness (diversity collapse, Song et al., 2025).

4. **Generalization to non-verifiable domains (Table 1, AlpacaEval 2.0 column, Lines 246–264):** On AlpacaEval 2.0, power sampling outperforms GRPO across all models (e.g., 2.88 vs. 2.38 for Qwen2.5-Math-7B and 8.59 vs. 7.62 for Qwen2.5-7B). Unlike RL methods that depend on a verifiable reward function, the training-free approach transfers to domains where no automated verifier exists — a meaningful practical advantage.

## Weaknesses

### Fatal
None.

### Major

1. **N_MCMC is not reported, making cost analysis and reproducibility impossible.** The paper defines N_MCMC in Algorithm 1 and gives a token-cost formula (Eq. 12: ≈ N_MCMC · T²/4B ≈ N_MCMC · 12,288 for the chosen T=3072, B=192), but **never states the actual value used**. This is the single parameter that determines both the computational cost and the quality of the approximation to \(p^\alpha\). Every other hyperparameter (T, B, α) is stated; this one is not. Without it, readers cannot estimate how expensive the procedure was or design replicable experiments. The paper mentions "relatively small values of N_MCMC" (Line 231) but this is not a number.

2. **No comparison against inference-time compute baselines.** The method trades substantial inference-time compute for accuracy (each output requires N_MCMC · ~12,288 tokens), but is only compared against one-pass sampling (base, low-temperature) and GRPO. Standard inference-time scaling baselines such as best-of-N sampling, self-consistency/majority voting, or beam search are absent. Since the paper's framing emphasizes inference-time compute as the key resource being traded, it is essential to show that MCMC is a good way to spend that compute compared to simpler alternatives at a comparable budget. Without this, the relative efficiency of the method is unknown.

3. **The GRPO baseline for Phi-3.5-mini-instruct is unreliable.** On HumanEval, GRPO achieves 13.4% — *worse* than the base model's 21.3%. On MATH500, GRPO achieves 40.6% vs. the base's 40.0%, essentially no improvement. While the paper states it used hyperparameters "selected from Abdin et al. (2024) that avoids training instabilities and converges to improvement" (Line 268), the results contradict this claim. The headline +59.8% over GRPO on Phi-3.5 HumanEval (73.2% vs. 13.4%) and several of the paper's strongest claims depend on this comparison. The paper's evidence would be better served by either obtaining a properly tuned GRPO checkpoint for Phi-3.5 or restricting the RL comparisons to the Qwen2.5 models where GRPO is known to work well.

### Minor

4. **No MCMC diagnostics reported.** The paper provides no acceptance rates, mixing diagnostics, or convergence checks for the MCMC chain. Given the paper's own acknowledgment of "[exponential] mixing time" in high-dimensional discrete token spaces (Lines 189–190), evidence that the chain actually converges to the claimed target distribution would substantially strengthen confidence in the method. An ablation showing accuracy as a function of N_MCMC would also help.

5. **The Phi-3.5 AlpacaEval 2.0 result is not discussed.** Low-temperature sampling achieves 18.15 on this task vs. power sampling's 17.65 (Table 1, Lines 258–262). This is the only case where the method underperforms its own proposal distribution. The paper presents its results as "consistent outperformance" but this counterexample is not acknowledged or analyzed.

6. **Hyperparameter selection is not stated to use a held-out validation set.** The paper says α=4.0 was "empirically found" (Line 270) without specifying whether this tuning was performed on the test benchmarks or a held-out set. Similarly, the claim that B=192 makes the algorithm "performant for relatively small values of N_MCMC" (Line 231) would benefit from the same clarification.

### Trivial
None.

## Nice-to-Haves
- Reporting acceptance rate statistics or showing that accuracy plateaus as N_MCMC increases would validate the MCMC procedure.
- A brief discussion of the method's limitations (computational cost, sensitivity to α, need for full sequence log-likelihood access) would improve completeness.

## Removed Points

These points from the input reviews were assessed and removed with justifications:

- **"Compute disparity is 100–500× more"** — REMOVED as speculative. N_MCMC is unreported, so the actual factor cannot be estimated with any precision. The underlying concern (undisclosed cost) is preserved in Major Weakness #1.
- **"No limitations section"** — REMOVED as a formatting/style nitpick.
- **"Variance/confidence intervals not reported"** — REMOVED. Single-run evaluation on standardized benchmarks is the norm in this community.
- **"Long-form reasoning claim is underdeveloped"** — REMOVED. The observation (Line 307) is presented as a finding, not a central claim, and is appropriately scoped.
- **Several generic strengths from the Strength Finder** — REMOVED. Generic framing such as "the paper addresses an important problem" adds no information. Only concrete, evidence-anchored strengths were retained.
- **"Critical windows / pivotal tokens speculation" (from Harsh Critic)** — REMOVED. The paper flags this as intuition ("this type of behavior is immensely valuable for reasoning tasks..."), not as evidence, so criticizing it as speculative is scope creep.

## Novel Insights

None beyond the paper's own contributions. The theoretical distinction between power distributions and low-temperature sampling (Proposition 1) is the paper's own insight, and the reviews do not surface an additional novel perspective beyond this.

## Suggestions

1. **Report N_MCMC and provide a compute-aware comparison.** State the value of N_MCMC used in all experiments and report the total token budget per output sequence. Then compare against best-of-N sampling from the base model at the same token budget. If power sampling outperforms best-of-N at equal compute, this is strong evidence for the method's value.
2. **Add inference-time compute baselines.** Include best-of-N (at several N), self-consistency, or beam search at comparable compute budgets.
3. **Fix or remove the Phi-3.5 GRPO comparison.** Either obtain a properly tuned GRPO checkpoint for Phi-3.5 or restrict the RL comparisons to Qwen2.5 models where the baseline is reliable.
4. **Provide MCMC diagnostics.** Report acceptance rates and an ablation over N_MCMC showing accuracy vs. compute.
5. **Address the AlpacaEval 2.0 Phi-3.5 result** where low-temperature outperforms power sampling.
6. **Clarify held-out validation.** State explicitly that α=4.0 was selected on a held-out validation set, not on the test benchmarks.

## Score and Decision

**Score:** 5.0

**Decision:** Reject (borderline)

**Rationale:** The paper makes a genuine theoretical contribution (Proposition 1 and the power-distribution formulation) and presents an interesting algorithm with promising results on Qwen2.5 models. However, three major issues prevent acceptance in the current form: (1) N_MCMC is unreported, making both cost analysis and reproducibility impossible; (2) no inference-time compute baselines are included, so the method's efficiency relative to simpler alternatives (best-of-N) is unknown; (3) the Phi-3.5 GRPO baseline is unreliable, with GRPO *degrading* performance below the base model on HumanEval, undermining some of the paper's strongest claimed advantages. These issues are addressable in revision. The theoretical contribution is solid, but the empirical evaluation requires substantial strengthening to support the paper's central claims.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>
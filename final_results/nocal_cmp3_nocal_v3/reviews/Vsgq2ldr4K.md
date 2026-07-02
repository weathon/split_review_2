## Summary

The paper proposes using MCMC to sample from a "power distribution" \(p^\alpha\) over token sequences defined by a base LLM, arguing that this mimics the distribution-sharpening effect of RL post-training without requiring any training, reward models, or curated datasets. The authors introduce a progressive block-wise Metropolis-Hastings algorithm that iteratively resamples token subsequences, and demonstrate that on MATH500, HumanEval, GPQA, and AlpacaEval 2.0, this sampling method yields single-shot accuracies that are competitive with GRPO-trained models while preserving generation diversity (pass@k) that RL collapses.

## Strengths

1. **Clear conceptual contribution distinguishing power distributions from low-temperature sampling.** Section 4.1's Proposition 1 and Example 1 cleanly demonstrate that the joint power distribution \(p^\alpha\) and per-token low-temperature sampling are not equivalent, and Observation 1 about "tokens with few but high-likelihood future paths" gives an intuitive explanation for why the power distribution is a more desirable target for reasoning tasks. This is a genuine pedagogical insight that clarifies a common misconception.

2. **Compelling pass@k diversity results.** Figure 5 shows that power sampling's pass@k curve continues rising with k and matches the base model at high k (~98% at k=16), while GRPO plateaus around 90%. This is a well-documented finding that directly addresses a recognized limitation of RL post-training, and the effect is large enough to be practically meaningful.

3. **Methodologically clean and principled algorithm design.** The progressive block-by-block approach (Algorithm 1) that defines intermediate distributions \(\pi_k\) and sequentially builds up the sequence length is a sensible way to mitigate the exponential mixing-time problem that would plague a direct full-sequence MCMC approach. The algorithm avoids external reward models entirely, relying only on base model likelihoods.

## Weaknesses

### Major

1. **Critical hyperparameter \(N_{\text{MCMC}}\) is never reported.** The paper specifies all other experimental hyperparameters (\(T=3072\), \(B=192\), \(\alpha=4.0\)) but never states the value of \(N_{\text{MCMC}}\), which is listed as a required input to Algorithm 1 and directly determines both the computational cost and the quality of the approximation to \(p^\alpha\). Without this number, the results cannot be reproduced, the compute cost cannot be quantified (even approximately), and the reader cannot assess whether the MCMC chain has had enough steps to mix. This is a basic reproducibility failure.

2. **The comparison to GRPO is presented without quantifying the vast compute gap.** The paper acknowledges "additional compute during sampling" (line 203) and provides a token-cost formula \(\mathbb{E}[\text{tokens}] \approx N_{\text{MCMC}} T^2/(4B)\), but never plugs in actual numbers, never reports the total compute used per response, and never compares against GRPO at matched budgets. Even by the paper's own formula, with \(T=3072\) and \(B=192\), each response costs \(N_{\text{MCMC}} \times 12,\!288\) generated tokens. Whether \(N_{\text{MCMC}}=4\) or \(N_{\text{MCMC}}=64\) changes the compute by orders of magnitude, and neither number is given. The headline claims of "nearly matching and even outperforming RL" are misleading when the comparison is between methods that may differ by 100× or more in inference-time compute. A proper evaluation should report how performance scales with compute and compare against baselines (e.g., best-of-N sampling, majority voting) at the same token budget.

3. **The GRPO baseline on Phi-3.5-mini-instruct is evidently not a functioning reasoning model.** From Table 1: GRPO on Phi-3.5 achieves 40.6% on MATH500 (vs. base 40.0%), 13.4% on HumanEval (vs. base 21.3% — a *degradation* of ~8 points), and 35.9% on GPQA (vs. base 27.3%). On HumanEval, GRPO is worse than the base model, strongly suggesting training failure or poor hyperparameter selection. The paper claims to use "hyperparameters selected from Abdin et al. (2024) that avoids training instabilities and converges to improvement," but the results contradict this. The "up to +59.8%" outperformance claim on HumanEval (line 275) is driven almost entirely by this broken baseline: it reflects the absolute percentage-point gap between power sampling (73.2%) and a degraded GRPO (13.4%). This inflates multiple comparative claims for Phi-3.5.

### Minor

4. **Main results lack error bars or confidence intervals.** All results in Table 1 are point estimates. Given the stochasticity of both the MCMC procedure and the underlying model's sampling, single-run point estimates are insufficient to assess whether the observed gaps (e.g., power sampling 74.8% vs. GRPO 78.5% on MATH500 with Qwen2.5-Math-7B) are statistically reliable.

5. **No MCMC diagnostics are reported.** For a method whose correctness depends on the chain converging to \(p^\alpha\), the paper provides no diagnostics: no acceptance rates, no discussion of mixing time or autocorrelation, and no analysis of whether \(N_{\text{MCMC}}\) iterations are sufficient for convergence. This makes it impossible to assess whether the algorithm is actually sampling from the intended target distribution.

6. **The "outperform on out-of-domain tasks" framing overstates the advantage.** The pattern is not clean: on GPQA (an out-of-domain task), GRPO wins for both Qwen2.5-Math-7B (39.9% vs. 38.9%) and Qwen2.5-7B (35.4% vs. 31.8%). The HumanEval advantage is modest (3–6 points on the Qwen models) and could be within noise given the absence of error bars. The strongest "outperform" claims (59.8%) rely on the broken Phi-3.5 baseline. The paper would benefit from a more measured characterization.

7. **Low-temperature baseline temperature is not specified.** The "Low-temperature" row in Table 1 provides an important ablation, but its temperature is never stated in the experimental setup (lines 237–271), making the baseline uninterpretable and unreproducible.

8. **Algorithm 1 acceptance ratio notation is ambiguous.** The pseudocode (line 227) writes the acceptance ratio as \(\min\{1, \pi_k(\mathbf{x}')/\pi_k(\mathbf{x}) \cdot \ldots\}\) where \(\mathbf{x}\) and \(\mathbf{x}'\) are both of length \((k+1)B\), but \(\pi_k\) is formally defined only over sequences of length \(kB\) (line 199). The intent is likely to evaluate the prefix up to \(kB\) (since the target is \(\pi_{k+1}\)), but as written this is confusing.

9. **Sensitivity to \(\alpha\) is not explored.** The paper uses \(\alpha=4.0\) throughout (with a note that a different proposal temperature helps AlpacaEval) but provides no ablation. The method's sensitivity to this core parameter is unknown.

10. **Improvement percentages mix absolute and relative framing.** The paper reports "+51.9%", "+25.2%", and "+59.8%" (line 274) which are absolute percentage-point differences, not relative improvements. While common in the field, this is ambiguous presentation, and the 59.8% figure is further compounded by the broken Phi-3.5 baseline.

## Nice-to-Haves

- Report power sampling performance as a function of compute budget (varying \(N_{\text{MCMC}}\)) to characterize the inference-time scaling behavior — this would be a valuable contribution in its own right.
- Compare against simpler high-compute baselines at matched budgets: e.g., best-of-\(N\) selection by base model likelihood, or many independent samples with majority voting.
- Provide MCMC acceptance rates and a brief mixing analysis.
- Ablate \(\alpha\) (e.g., \(\alpha=2.0, 4.0, 8.0\)) to understand sensitivity.

## Removed Points

- **Figure 4 "circular" criticism** — Removed. The reviewer claimed this is "trivially true" and circular, but the figure compares power sampling against GRPO and base distributions; it serves to validate the paper's premise that GRPO and power sampling both concentrate on high-likelihood regions, which is informative, not circular.
- **Table 2 single qualitative example** — Removed. This is a standard illustrative example; the paper notes further examples in the appendix and does not present it as statistical evidence.
- **Hyperparameter "irony" criticism** — Removed. The paper claims to "avoid some of the inherent weaknesses of RL methods including extensive hyperparameter sweeps to avoid training instabilities," not that its method has zero hyperparameters. The criticism misreads the claim.
- **Speculative compute estimates** — Removed the specific 100K–400K token numbers from the compute asymmetry point, since without \(N_{\text{MCMC}}\) these are guesswork. The core concern about the unquantified gap is retained.
- **Missing related works / appendix content** — Per policy, these are parser artifacts or out of scope; removed.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Report \(N_{\text{MCMC}}\) explicitly, along with the average token cost per response and acceptance rates.
- Reframe the empirical comparison to include compute-controlled baselines (e.g., best-of-\(N\) sampling at matched budgets), and separate the conceptual contribution (Section 4.1) from the claim of "matching RL."
- Fix or replace the Phi-3.5 GRPO baseline, or explicitly discuss the training issue and exclude that model's comparative claims.
- Add confidence intervals or standard deviations to Table 1.
- Specify the temperature used for the low-temperature baseline.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>
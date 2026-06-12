## Summary

This paper proposes an inference-time MCMC sampling algorithm ("power sampling") that targets a sharpened version \(p^\alpha\) of a base LLM's distribution, aiming to match or exceed the reasoning performance of RL posttraining (GRPO) without any training. The method uses Metropolis-Hastings with a progressive blocking scheme and random resampling proposals. Empirically, on Qwen2.5-Math-7B, Qwen2.5-7B, and Phi-3.5-mini-instruct, the algorithm achieves results comparable to GRPO on in-domain MATH500, often exceeds GRPO on out-of-domain tasks (HumanEval, AlpacaEval 2.0), and maintains better diversity in multi-sample (pass@k) settings.

## Strengths

1. **Clean theoretical motivation, well-executed in the conceptual distinction.** Proposition 1 and Example 1 (Section 4.1) formalize the difference between power distributions ("sum of exponents") and low-temperature sampling ("exponent of sums"). Observation 1 — that power distributions upweight tokens with few but high-likelihood future paths while low-temperature sampling upweights tokens with several but low-likelihood completions — is a genuinely insightful connection to the "critical token"/"pivotal token" literature. This theoretical analysis stands independently of the empirical results.

2. **Empirical results are striking on their face.** Table 1 shows power sampling consistently matching GRPO on MATH500 (e.g., 74.8% vs. 78.5% on Qwen2.5-Math-7B) and outperforming on HumanEval (57.3% vs. 53.7%) and AlpacaEval 2.0 (2.88 vs. 2.38). Figure 5's pass@k results are particularly notable — GRPO's saturating at ~0.90 while power sampling continues rising to ~0.98 — a genuine and important empirical observation about diversity preservation.

3. **Training-free property is meaningful.** If the method works as claimed, it avoids extensive hyperparameter tuning, dataset curation, and training instabilities of RL, and is applicable to any base model without additional training.

## Weaknesses

### Fatal
None.

### Major

1. **No evidence that the MCMC chain converges to the claimed \(p^\alpha\) distribution.** The paper's core theoretical framing is that the algorithm samples from \(p^\alpha\), but: (i) No convergence diagnostics are reported — no trace plots, effective sample size, R-hat, or comparison against ground-truth \(p^\alpha\) samples. (ii) Critically, **\(N_{\text{MCMC}}\) is never reported anywhere** — not in the experimental setup (Section 5.1), not in any table. This single missing hyperparameter makes it impossible to assess mixing quality. (iii) The paper shows outputs have high likelihood under the base model (Figure 4), but this does not distinguish sampling from \(p^\alpha\) from any method that biases toward high-likelihood sequences (e.g., low-temperature sampling, best-of-N). The progressive blocking scheme (Equation 10) may compound errors rather than solve the exponential mixing problem the paper acknowledges (Section 4.3). Without verifying that the method actually targets \(p^\alpha\), the theoretical motivation is disconnected from the empirical results.

2. **The GRPO baseline for Phi-3.5-mini is at best undertuned and may be broken.** From Table 1: GRPO on Phi-3.5 achieves **40.6%** on MATH500 vs. base 40.0% — essentially no improvement. On HumanEval, GRPO achieves **13.4%** vs. base 21.3% — substantially *worse*. Low-temperature sampling (a simple decoding strategy) achieves 47.8% on MATH500 and 58.5% on HumanEval, far exceeding GRPO. This strongly suggests the GRPO training for Phi-3.5 was not properly configured. The paper states it uses "hyperparameters selected from Abdin et al. (2024) that avoids training instabilities," but the results indicate the training either failed or degraded performance. An undertuned baseline inflates power sampling's apparent advantage on this model and weakens cross-model generalizability claims.

3. **No ablation studies.** The algorithm introduces several hyperparameters: block size \(B=192\), power \(\alpha=4.0\), \(N_{\text{MCMC}}\) (unreported), and proposal temperature. None are ablated. Without this, the source of improvement is unclear — the gains could come from the MH accept/reject mechanism, or simply from repeated resampling from the proposal distribution. The paper does not report MH acceptance rates, so it is unknown whether the accept/reject step is doing useful work.

4. **Missing critical baseline: best-of-N sampling.** The most direct training-free competitor that trades inference compute for quality is best-of-N: sample \(N\) outputs from the base model, pick the one with highest base likelihood. At a comparable token budget (~12,000 tokens per output from Equation 12), best-of-N with \(N\approx20\) is the natural baseline. Without it, the paper cannot support the claim that the MCMC structure specifically adds value over simple resampling. Other missing baselines include self-consistency/majority voting and beam search, but best-of-N is the most glaring omission.

### Minor

5. **Compute-asymmetric comparison.** Equation (12) estimates ~\(N_{\text{MCMC}} \cdot T^2 / (4B)\) tokens per output — ~12,288 tokens for \(N_{\text{MCMC}}=1\), versus the base model's ~600 tokens. The paper acknowledges this as "inference-time scaling" (line 203) but does not report wall-clock time, total token budget, or explicitly contextualize the different compute regimes in the headline framing.

6. **\(N_{\text{MCMC}}\) not reported.** This hyperparameter is listed in Algorithm 1 but never given a numeric value. Essential for reproducibility and assessing compute costs. (May reside in the stripped appendix.)

### Trivial
None.

## Nice-to-Haves

- Report MH acceptance rates to verify that the accept/reject mechanism is active.
- Provide confidence intervals or statistical significance for the main results (the GPQA difference between power sampling 38.9% and GRPO 39.9% on Qwen2.5-Math-7B is well within noise).
- Ablate \(\alpha\) to validate that \(\alpha=4.0\) is near-optimal.
- Report wall-clock time comparisons with GRPO single-forward-pass time.

## Removed Points

These points were identified in the input review but are excluded from the main weaknesses above:

- **"Algorithm 1 has a subtle bug or ambiguity in the progressive blocking scheme."** — The algorithm is described correctly as designed. The complex dependency structure (early tokens modifiable during later-block MCMC) is a deliberate design choice, not a bug. Removed.
- **"The claim of being 'verifier-free' is misleading."** — This conflates an external reward function (the standard RL meaning) with using the base model's own likelihood as an MH acceptance criterion. The paper is correct that no external verifier is needed. Removed.
- **"Figure 4 analysis is incomplete."** — The paper explicitly discusses the distribution differences, noting GRPO is "heavily concentrated" while power sampling "maintains noticeable spread." Removed.
- **"Statistical significance not reported."** — Single-point estimates are standard for these benchmarks. Moved to Nice-to-Haves.
- **Formatting nitpicks, grammar/style criticisms, parser artifacts.** — Removed per filtering rules.

## Novel Insights

The input review's most valuable observation is the identification that the unverified MCMC convergence creates a fundamental gap between the paper's theoretical framing ("we sample from \(p^\alpha\)") and the empirical results. The algorithm could reduce to an unprincipled iterative resampling scheme whose success might stem entirely from repeated sampling at low temperature, with the MH mechanism playing no role. A second key insight is the identification of the broken GRPO baseline for Phi-3.5-mini — since this is one of only three models tested, it substantially weakens any claim of consistent cross-model superiority.

## Suggestions

1. **Fix the Phi-3.5-mini GRPO baseline or remove these results.** Either properly tune GRPO for this model or acknowledge that the baseline is non-functional and exclude Phi-3.5 from cross-model comparison claims.
2. **Report \(N_{\text{MCMC}}\).** Show a sweep over \(N_{\text{MCMC}}\) values to demonstrate whether performance improves with more steps or saturates quickly.
3. **Verify MCMC convergence in a tractable setting.** Construct a small controlled setting where \(p^\alpha\) can be enumerated exactly, run the algorithm, and compare empirical vs. ground-truth distributions.
4. **Add a best-of-N baseline at comparable token budget.** This is the single most important missing experiment.
5. **Add ablation studies.** At minimum, ablate \(\alpha\) (e.g., {1.0, 2.0, 4.0, 8.0}) and report MH acceptance rates.

## Score and Decision

**Calibration Anchors:**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| Large Language Monkeys (0xUEBQV54B.md) | 5.00 | R1 | Simpler idea (repeated sampling), better execution. Our paper is more ambitious but has more execution gaps. |
| Learning Extrapolative Sequence Transformations from Markov Chains (DQfHkEcUqV.md) | 4.75 | R1 | Similar MCMC-for-LLMs methodology, similar issues (weak baselines, missing ablations). Comparable quality. |
| Inference Scaling Laws (VNckp7JEHn.md) | 5.75 | R1 | Well-executed empirical study. Our paper has less rigorous execution. |
| Smaller, Weaker, Yet Better (3OyaXFQuDl.md) | 7.00 | R1 | Thorough experiments and ablations. Our paper's execution is significantly weaker. |
| Self-Improvement: The Sharpening Mechanism (WJaUkwci9o.md) | 8.00 | R1 | Similar concept (sharpening) with rigorous theory and clean execution. Our paper lacks similar rigor. |
| Syntactic/Semantic Control via SMC (xoXn62FzD0.md) | 8.00 | R1 | Similar MCMC-for-LLMs with extensive ablations and baselines. Our paper has fewer controls. |

**Round 1 Bracket:** 3.5–5.5. Narrowed to final score by comparing against Large Language Monkeys (5.00) and Learning Extrapolative Sequence Transformations (4.75) — our paper has a more novel theoretical contribution but worse execution (missing convergence verification, broken baseline, no ablations), placing it slightly below those papers.

**Final Score: 4.5** — The paper has a genuinely interesting core idea (the power distribution / low-temperature distinction is a real contribution) and striking preliminary results (Figure 5 is compelling). However, execution has multiple significant gaps: the central claim of sampling from \(p^\alpha\) is unverified with no convergence diagnostics and unreported \(N_{\text{MCMC}}\); the GRPO baseline for Phi-3.5-mini is clearly undertuned; there are no ablation studies; and a critical baseline (best-of-N) is missing. These issues prevent the paper from making its case convincingly in its current form. The paper sits between "reject" and "borderline reject" — too flawed for acceptance but with enough intellectual contribution to distinguish it from a straightforward reject.

**Decision:** Reject

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>
Now I have all the information I need. Let me write the final consolidated review.

## Summary

This paper proposes sampling from the *power distribution* $p^\alpha$ of a base LLM (an exponentiated/ sharpened version of the model's own distribution) as a training-free alternative to RL post-training for reasoning tasks. The authors provide a theoretical analysis distinguishing power sampling from low-temperature sampling (Proposition 1), develop an MCMC algorithm (Metropolis-Hastings with progressive blocking) to approximately sample from $p^\alpha$, and present results on MATH500, HumanEval, GPQA, and AlpacaEval across three model families.

## Strengths

1. **Clean theoretical distinction (Section 4.1, Proposition 1, Example 1).** The paper rigorously shows that low-temperature sampling does *not* sample from $p^\alpha$, and that the "sum of exponents" vs. "exponent of sums" difference (Equations 7–8) gives power distributions a principled bias toward tokens with few but high-likelihood future paths. This is a genuine conceptual contribution connected to the critical-window / pivotal-token literature.

2. **Principled MCMC adaptation to autoregressive structure.** The progressive-blocking scheme (Equation 10, Algorithm 1) — gradually extending the sequence length through intermediate distributions $\pi_k$ — is a well-motivated approach to mitigating the exponential mixing-time problem of naive MH in high-dimensional token spaces. The random-resampling proposal with explicit irreducibility/aperiodicity guarantees is sound.

3. **Training-free, dataset-free, verifier-free property.** The method requires none of the infrastructure that makes RL post-training brittle — curated datasets, reward model training, stability hyperparameter sweeps, or a verifier. If the method is effective, this is a genuine practical advantage for domains where verifiable rewards are unavailable.

4. **Strong pass@k diversity results (Figure 5).** On MATH500, the power sampling pass@k curve is strictly above GRPO's for all $k>1$, converging to the base model's ~98% ceiling at $k=16$, while GRPO plateaus around 90%. This cleanly demonstrates a diversity advantage over RL that the paper's theoretical framing predicts.

## Weaknesses

### Fatal
None.

### Major

1. **Missing compute-matched baselines.** The paper compares against the base model, low-temperature sampling (each one forward pass), and GRPO (one forward pass of a fine-tuned model). But the MCMC procedure generates many candidate tokens per final output — Equation 12 estimates $\frac{N_{\text{MCMC}} T^2}{4B}$ tokens, which with $T=3072, B=192$ is $N_{\text{MCMC}} \times 12,\!288$ proposal tokens. Missing are baselines that control for total compute: best-of-*k* sampling from the base model, self-consistency / majority voting, or rejection sampling at the same compute budget. Without these, it is unclear whether the gains come from the specific MCMC procedure or simply from spending more inference compute. This is the paper's most significant evidential gap.

2. **No MCMC convergence diagnostics.** Section 4.3 explicitly warns about exponential mixing times in high-dimensional spaces, yet the paper provides no trace plots, acceptance rates, effective sample sizes, or multi-seed variance analysis. The paper states the algorithm "converges to sampling from $p^\alpha$" (line 201), but offers no evidence that the chain mixes in practice for the chosen hyperparameters. For a paper whose central algorithm is MCMC, this is a significant methodological gap.

3. **GRPO baseline for Phi-3.5-mini-instruct appears under-trained.** In Table 1, GRPO on Phi-3.5 achieves only 40.6% on MATH500 (barely above base at 40.0%) and *drops* to 13.4% on HumanEval (base: 21.3%). The claim of outperforming GRPO by +59.8 percentage points on HumanEval is technically correct but largely reflects an ineffective baseline, not the method's strength. The method *does* still outperform low-temperature sampling (58.5% → 73.2%) and the base model on this model, so the overall results are not invalidated — but the headline "outperforms RL" claim is partly driven by this weak baseline.

4. **Value of $N_{\text{MCMC}}$ not stated.** Algorithm 1 and the experimental setup (Section 5.1) specify $T=3072$, $B=192$, and $\alpha=4.0$, but never state the number of MCMC steps $N_{\text{MCMC}}$. The paper says "relatively small values" (line 231), but without an explicit number the compute cost is unverifiable and the experiment is not fully reproducible. (This may be in the stripped appendix, but it should appear in the main experimental setup.)

### Minor

5. **No variance or statistical significance reporting.** All results in Table 1 are single point estimates with no confidence intervals. For GPQA (198 questions), binomial confidence intervals are nontrivial — differences of ~2–3 percentage points (e.g., 39.9 vs. 38.9 for Qwen2.5-Math) are within expected sampling noise of a single run. The strong comparative claims would be better supported by multi-run statistics.

6. **Sensitivity to task characteristics underexplored.** The paper uses $\alpha=4.0$ uniformly for reasoning tasks but needs a different proposal temperature ($\tau=0.5$) for AlpacaEval, suggesting task-dependent sensitivity that is not analyzed. No ablation on $\alpha$ (e.g., varying 1 to 8) or $B$ (e.g., 64 to 512) is provided, making it unclear how robust the method is to hyperparameter choice.

### Trivial
None.

## Nice-to-Haves

- **Ablation on $\alpha$, $B$, and $N_{\text{MCMC}}$.** Showing sensitivity of results to these key hyperparameters would strengthen the paper.
- **Wall-clock time comparison.** Reporting time per query across methods would help readers weigh the training-free advantage against the inference-time cost.
- **Comparison against directly sampling from $p^\alpha$ with simpler compute-matched strategies** (e.g., best-of-*k* base samples weighted by $p^{\alpha-1}$) would help isolate the contribution of the MCMC procedure.
- **Exploration of different proposal distributions** beyond the base model with temperature $1/\alpha$.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **"Fundamentally unfair comparison" framing** — removed because the paper explicitly acknowledges the compute tradeoff ("We can interpret this as a new axis for inference-time scaling," line 203) and clarifies what "single-shot" means (simulating a single sequence from $p^\alpha$, not a single forward pass). The comparison class (training-free vs. RL) is a valid framing; the missing compute-matched baselines are a separate issue retained above.
- **"Three orders of magnitude more compute"** — removed because the exact compute multiplier depends on the unstated $N_{\text{MCMC}}$; this quantitative claim is unsupported in the review.
- **"The paper should not be accepted"** — the reviewer's overall recommendation, not a weakness.
- **Various section-by-section observations** (e.g., "Equation 12 is presented as neutral rather than as a limitation," "the proposal temperature change suggests sensitivity") — these are reading notes, not actionable weaknesses; the relevant sensitivity point is retained as a Minor weakness.
- **Strengthening-the-Paper-on-Its-Own-Terms items** that duplicate the compute-matched baseline suggestion — merged into the retained weakness and nice-to-haves.
- **"Missing Parts" items** about ablating the proposal distribution or comparing against multiple low-temperature values — moved to nice-to-haves as they are not standard requirements for a first empirical demonstration.

## Novel Insights

None beyond the paper's own contributions. The harsh critic's main novel observations (the compute disparity and the weak Phi-3.5 baseline) are valid but do not constitute independent insights beyond what the paper's own data reveals when scrutinized.

## Suggestions

1. **Add compute-matched baselines** — best-of-*k* sampling from the base model and self-consistency at comparable total token budgets. This is the single highest-leverage improvement and would isolate whether the MCMC procedure specifically or additional compute drives the gains.
2. **Report MCMC diagnostics** — acceptance rates, effective sample size, and a plot showing how log-likelihood evolves over MCMC steps at each progressive block.
3. **State $N_{\text{MCMC}}$, or if it was determined dynamically, describe the criterion.** Without this, the experimental setup is incomplete.
4. **Fix or replace the Phi-3.5 GRPO baseline** with properly tuned GRPO, or note transparently that training was unsuccessful and remove the "outperforms GRPO" claim for this model.
5. **Report confidence intervals or multi-run statistics** for the main benchmarks.

## Score and Decision

The paper's theoretical contribution (the power-distribution analysis) and the pass@k diversity results are genuine and worth preserving. The algorithmic design (progressive-blocking MCMC) is sensible. However, the experimental evaluation has significant gaps: no compute-matched baselines, no MCMC diagnostics, an unstated $N_{\text{MCMC}}$, and a questionable GRPO baseline on one model. These are addressable but prevent the headline claims from being fully supported as written. The paper falls in the borderline range.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>
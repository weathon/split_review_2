## Summary

This paper proposes "power sampling," a training-free MCMC-based algorithm that targets the power distribution p^α of a base LLM to elicit reasoning capabilities comparable to RL-posttraining (GRPO). The core theoretical contribution is Proposition 1, which cleanly distinguishes sampling from p^α (a "sum of exponents") from low-temperature sampling (an "exponent of sums"), with the former favoring tokens that have fewer but higher-likelihood future paths — a property argued to be valuable for reasoning. Empirically, the method shows strong results on MATH500, HumanEval, GPQA, and AlpacaEval 2.0 across Qwen2.5-Math-7B, Qwen2.5-7B, and Phi-3.5-mini-instruct, with pass@k analysis demonstrating sustained diversity unlike GRPO.

## Strengths

- **The theoretical distinction between p^α and low-temperature sampling (Section 4.1, Proposition 1, Example 1) is genuinely novel and well-articulated.** The "sum of exponents" vs. "exponent of sums" contrast is clear, and the toy example concretely shows the two can disagree on which token to prefer. The intuition that p^α favors tokens with fewer but higher-likelihood futures is compelling for reasoning tasks where "critical window" tokens cause failures. This contribution stands independently of the experimental results.

- **The "training-free, dataset-free, verifier-free" framing is well-motivated (Abstract, Section 1).** If the method works as claimed, it avoids reward hacking, reward model training, dataset curation, and training instability — a genuinely different point in the design space from RL fine-tuning.

- **The pass@k results (Figure 5) demonstrating sustained diversity are compelling.** Power sampling continues improving up to k=16 (98%) while GRPO plateaus at ~90%, supporting the claim of achieving "the best of both worlds."

- **The absolute improvements over low-temperature sampling are meaningful** (e.g., Qwen2.5-Math-7B: 74.8 vs 69.0 on MATH500, 57.3 vs 51.2 on HumanEval; Phi-3.5-mini: 73.2 vs 58.5 on HumanEval), showing the method adds value beyond simple temperature adjustment.

## Weaknesses

### Fatal

None.

### Major

- **N_MCMC, the number of MCMC steps, is never reported (Section 5.1 / Algorithm 1).** Equation (12) gives E[tokens] = N_MCMC·T²/(4B) = N_MCMC·12,288 tokens per sample with T=3072, B=192. The paper states "relatively small values of N_MCMC" (line 231) but never specifies the actual value used. Without this, the computational cost is unquantified: the reader cannot tell whether the method is practical (N_MCMC ~10, ~123K tokens per sample) or prohibitively expensive (N_MCMC ~200+, ~2.5M tokens per sample). This also makes the comparison to GRPO (one forward pass per sample) impossible to contextualize, hollowing the "inference-time" framing. This is the single most critical omission.

- **The Phi-3.5-mini GRPO baseline is broken on HumanEval (Table 1).** For Phi-3.5-mini: Base gets 21.3%, low-temperature gets 58.5%, but GRPO gets only 13.4% — substantially *worse* than the base model. This contradicts the paper's claim (line 268) that the hyperparameters "avoid training instabilities and converge to improvement over the base model." Since the headline "outperforms GRPO by up to +59.8%" on HumanEval relies on this cell (73.2% vs 13.4%), the claim is inflated by a degraded baseline. The Qwen2.5 results (power sampling 57.3 vs GRPO 53.7 on HumanEval) stand independently and are meaningful, but the paper should either fix this baseline or temper claims built on it.

- **No MCMC convergence diagnostics are provided (Section 4.3 / Section 5).** The paper acknowledges the risk of exponential mixing time and proposes block-wise annealing, but presents no evidence the chain actually targets p^α: no trace plots, no effective sample size estimates, no Gelman-Rubin statistics, no comparison of empirical vs. known target distributions. The narrative attributes success to targeting p^α, but without diagnostics the mechanism behind the improvements is unclear — they could arise from some other property of the iterative resampling procedure.

### Minor

- **No variance or confidence intervals for results.** Given MCMC stochasticity and moderate benchmark sizes (e.g., HumanEval: 164 problems), the 3–5 percentage point gaps between methods could be within noise. Bootstrapped CIs would substantially strengthen the empirical claims.

- **The acceptance ratio in Algorithm 1 (line 227) uses π_k instead of π_{k+1}.** The stated goal is to "sample from π_{k+1}" but the ratio evaluates only the first kB tokens via π_k(x')/π_k(x). Since the proposal can resample positions m < kB, overlapping with previously-accepted tokens, it is not obvious that the stationary distribution is π_{k+1}. The paper does not discuss whether this choice introduces bias. This needs clarification.

- **No ablation of N_MCMC or proposal distribution.** The sensitivity of results to MCMC steps (the compute-accuracy trade-off curve) and to the choice of proposal LLM/temperature is not explored, making it hard to judge robustness.

### Trivial

- The reasoning trace length analysis (~679 tokens for power sampling vs ~671 for GRPO vs ~600 for base) reports no variance or significance tests, making the claimed similarity observation weak.

## Nice-to-Haves

- Reporting wall-clock time or FLOPs for power sampling vs. GRPO inference would help contextualize practical cost.
- An ablation of N_MCMC across a range of values (e.g., 5, 10, 20, 50, 100) would be the single most impactful addition.
- Reporting the low-temperature baseline's temperature explicitly would improve reproducibility.

## Removed Points

These points from the harsh critic were filtered per the meta-reviewer rules:

1. **"Single-shot framing is deceptive"** — REMOVED. The paper explicitly states (line 203): "Note that Algorithm 1 is single-shot: *even though multiple inference calls are made*..." The paper is transparent; calling this deceptive misreads the text.

2. **"Comparison to GRPO is unequal, systematically favoring the proposed method"** — REMOVED. The paper's core claim is that inference-time sampling from the base model can match trained RL. Comparing against GRPO is the natural and relevant comparison. The paper also reports base and low-temperature baselines (Table 1) which provide the controlled comparison. The reviewer even acknowledged "This is not a flaw in itself."

3. **"Low-temperature baseline uses different temperature (τ=0.5) than power sampling proposal (τ=0.25)"** — REMOVED. The paper does not state the low-temperature baseline's temperature; the reviewer's τ=0.5 assumption is unsupported.

## Novel Insights

The main novel insight from synthesizing the reviews is that the paper's strongest asset is its theoretical contribution (Proposition 1) — this is clean, verifiable, and stands independently. However, the empirical evaluation has a critical reporting gap (N_MCMC) that makes the practical claims unverifiable without author input. The broken Phi-3.5 baseline further inflates headline claims. These are fixable issues, but they prevent the paper from being evaluated on its own terms as submitted. The paper would benefit from treating the p^α theory and the MCMC algorithm as the primary contribution, with the empirical results as supporting but incomplete evidence.

## Suggestions

1. **Report N_MCMC values** for all experiments and provide an ablation over N_MCMC (e.g., 5, 10, 20, 50, 100) to show the compute-accuracy trade-off curve. This is the single most impactful fix.

2. **Fix or acknowledge the Phi-3.5 GRPO baseline** — either retrain with properly tuned hyperparameters and report corrected numbers, or transparently report the HumanEval degradation and temper the "outperforms by +59.8%" claim.

3. **Add MCMC mixing diagnostics** — at minimum, trace plots of log-likelihood over MCMC iterations for a few representative examples, and an estimate of effective sample size.

4. **Report bootstrapped confidence intervals** for all main results.

## Score and Decision

### Calibration Anchors

| Anchor | Avg Score | Round | Itemized | Comparison |
|--------|-----------|-------|----------|------------|
| Ze4aPP0tIn (TSMC Math Reasoning) | 6.60 | 1 | Yes | Similar MCMC-based inference-time reasoning method; current paper has stronger theory but weaker empirical reporting (missing N_MCMC) |
| DzKdjWe59v (Hint Marginalization) | 5.75 | 1 | Yes | Similar iterative sampling for reasoning; current paper has larger improvements and broader evaluation |
| tQqLV2N0uz (Reprompting via Gibbs) | 5.40 | 2 | Yes | Similar MCMC-style iterative LLM sampling; current paper has broader evaluation and cleaner theory |
| VNckp7JEHn (Inference Scaling Laws) | 5.75 | 1 | Yes | Different contribution type (empirical study); current paper has stronger theoretical novelty |
| 4Po8d9GAfQ (LaTRO Latent Reasoning) | 3.80 | 1 | Yes | Current paper is substantially stronger — broader evaluation, larger gains, cleaner theory |
| F0GNv13ojF (RL Reward Design) | 5.17 | 1 | No | Different focus (RL reward); current paper has stronger theoretical differentiation |
| gdzpnRBP4F (RLSF Self-feedback) | 4.50 | 1 | No | Current paper is significantly stronger empirically and theoretically |

### Bracket and Score

**Round 1 bracket:** 5.0 – 6.5. The paper is clearly above the 3.80 LaTRO anchor (broader evaluation, larger improvements, cleaner theory) and above the 5.40 Reprompting anchor (broader evaluation, stronger theory). It is below the 6.60 TSMC anchor because that paper provided more complete empirical reporting while the current paper omits N_MCMC and has a broken baseline.

**Final score: 5.5.** This places the paper between borderline reject and borderline accept. The genuine theoretical contribution (Proposition 1) and strong Qwen2.5 results support the higher end of this range, but the missing N_MCMC — a basic implementation detail — makes the method's practical claims unverifiable, and the broken Phi-3.5 GRPO baseline inflates headline outperformance claims. These are fixable gaps, but they prevent the paper from being evaluated as a complete contribution as submitted. The decision is **Reject** at the current state, but with revisions addressing the three major weaknesses the paper could become a solid borderline accept (6.0+).

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>
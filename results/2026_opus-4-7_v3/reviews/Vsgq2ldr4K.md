Now let me check the experimental setup section more carefully to see if N_MCMC is stated anywhere:Now let me verify a few more specific claims by the reviewer — particularly about the Phi-3.5 GRPO results and whether the paper acknowledges compute costs anywhere.Now I have sufficient information to draft the review. Let me submit the draft first.Now let me run the calibration search. The paper is about MCMC sampling from power distributions for LLM reasoning — an inference-time scaling method.Let me read a few key anchor papers for calibration:Now let me read one more anchor paper to refine my calibration — the most directly relevant one:I now have sufficient calibration data. Let me form my bracket and write the final review.

**Round 1 Bracket: 5.5–7.0**

Reasoning:
- The paper is clearly above the 3.5–5.5 range (DQfHkEcUqV at 4.75 has weaker theory and worse experiments).
- It sits below the 7.5–8.5 range (xoXn62FzD0 at 8.0 has comparable Monte Carlo methodology but much stronger experimental validation with ablations and divergence analysis).
- It's in the borderline accept zone: stronger theoretical novelty than VNckp7JEHn (5.75), but weaker experimental rigor than 3OyaXFQuDl (7.0).

The theoretical contribution is genuinely novel, results span 3 models × 4 tasks, and the pass@k analysis is compelling. But the missing N_MCMC, absent best-of-N baseline, and no cost analysis prevent it from reaching 7+.

Now let me write the final consolidated review:

---

## Summary
This paper proposes "power sampling," a training-free inference-time algorithm that uses MCMC (Metropolis-Hastings) to approximately sample from the power distribution p^α of a base LLM. The core theoretical contribution is Proposition 1, which shows that sampling from p^α is fundamentally different from low-temperature sampling: the power distribution uses a "sum of exponents" weighting that implicitly plans ahead by upweighting tokens with fewer but higher-likelihood future paths, while low-temperature sampling uses a myopic "exponent of sums." The paper introduces a progressive MCMC scheme that exploits autoregressive structure to address mixing-time challenges, and demonstrates across three 7B-scale models and four benchmarks (MATH500, HumanEval, GPQA, AlpacaEval 2.0) that this approach nearly matches GRPO on in-domain tasks and can outperform on out-of-domain tasks while preserving sample diversity.

## Strengths

- **Novel theoretical distinction between power distribution and low-temperature sampling (Section 4.1, Equations 7–8, Proposition 1).** The "sum of exponents" vs. "exponent of sums" decomposition is mathematically clean and provides genuine insight into how sampling strategies relate to planning in autoregressive models. Example 1 concretely demonstrates the phenomenon with a minimal vocabulary. This is the paper's strongest intellectual contribution.

- **Well-designed progressive MCMC algorithm (Algorithm 1, Section 4.3).** The idea of defining intermediate distributions π_k over progressively longer prefixes and warm-starting each MH stage from the previous one directly addresses the exponential mixing-time problem inherent in high-dimensional discrete spaces. The expected token count formula (Eq. 12) transparently characterizes scaling behavior.

- **Compelling pass@k analysis (Figure 5).** Power sampling achieves single-shot performance competitive with GRPO while the pass@k curve is strictly above both the base model and GRPO for all k > 1, eventually matching the base model's coverage at k = 16. This "best of both worlds" result — GRPO-level single-shot accuracy without diversity collapse — is well-supported by the data and meaningfully contributes to the ongoing discussion about diversity degradation in RL-posttraining.

- **Consistent improvements across model families (Table 1).** The method works across Qwen2.5-Math-7B, Qwen2.5-7B, and Phi-3.5-mini-instruct, with substantial gains over the base model on all tasks (e.g., +25.2% on MATH500, +51.9% on HumanEval for Phi-3.5), demonstrating robustness beyond a single model.

- **Likelihood and confidence analysis (Figure 4)** provides empirical grounding for the theoretical motivation, showing power sampling shifts the distribution toward higher-likelihood regions while maintaining more spread than GRPO, which is heavily concentrated at a single peak.

## Weaknesses

### Fatal
None

### Major

- **N_MCMC is never reported and no computational cost analysis is provided.** N_MCMC is the most critical hyperparameter of Algorithm 1, controlling both sample quality and computational cost. Section 5.1 specifies T_max = 3072, B = 192, and α = 4.0, but omits N_MCMC entirely. While the paper acknowledges using "additional compute at sampling-time" (Section 4.3) and provides the expected token formula N_MCMC · T²/(4B) (Eq. 12), without instantiating N_MCMC the reader cannot assess the cost-performance tradeoff. Critically, no wall-clock time or FLOPs comparison against GRPO inference (a single forward pass per query) is provided. The paper's central framing as a "training-free alternative to RL" requires this comparison to be convincing — RL incurs a one-time training cost amortized over queries, while power sampling incurs its full cost on every query.

- **The most natural baseline — best-of-N with majority voting — is absent.** If one is willing to spend the inference compute implied by Algorithm 1, the obvious question is whether drawing N independent samples from the base model (or a low-temperature variant) and selecting via majority voting achieves comparable results. Best-of-N with majority voting is also verifier-free and training-free, and is the standard inference-time scaling baseline (as studied in the anchor paper VNckp7JEHn). Without this comparison, it is impossible to determine whether the gains come specifically from targeting p^α via MCMC, or simply from spending more inference compute. However, the pass@k diversity result (Figure 5) does suggest power sampling provides something best-of-N cannot: diverse, high-quality *individual* samples, not just a good selected output.

### Minor

- **Out-of-domain GRPO comparison framing is somewhat misleading.** GRPO is trained exclusively on the MATH training split (Section 5.1), yet the abstract states the method can "even outperform" RL without qualification. While the paper does distinguish in-domain vs. out-of-domain in the Table 1 caption ("comparable to GRPO on in-domain reasoning (MATH500), and can outperform GRPO on out-of-domain tasks"), the abstract and introduction conflate the two. On the in-domain benchmark MATH500, power sampling underperforms GRPO for both Qwen models (74.8 vs 78.5; 70.6 vs 74.0). The Phi-3.5 result where power sampling wins (50.8 vs 40.6) appears partly driven by a weak GRPO baseline — GRPO barely improves over the base model on MATH500 (40.6 vs 40.0) and dramatically degrades on HumanEval (13.4 vs 21.3), suggesting GRPO training may not have succeeded for this model.

- **No MCMC convergence diagnostics.** The MH algorithm converges to p^α only asymptotically. The paper provides no acceptance rate statistics, no accuracy-vs-N_MCMC curves, and no effective sample size estimates. The progressive scheme (Algorithm 1) is designed to help mixing, but without evidence that it actually does in the finite regime used, the claim that the algorithm "samples from p^α" remains empirically unverified.

- **No error bars or significance tests.** Some performance differences in Table 1 are small — e.g., GPQA for Qwen2.5-Math-7B (38.9 vs 39.9, a 1 percentage point gap on 198 questions). Without confidence intervals, it is hard to distinguish signal from noise in these comparisons.

### Trivial
None

## Nice-to-Haves

- An accuracy-vs-N_MCMC plot would simultaneously address the missing hyperparameter, demonstrate convergence behavior, and reveal the compute-quality tradeoff — this single experiment would resolve three weaknesses at once.
- Sensitivity analysis for α (set to 4.0 without justification beyond "empirically most performant").
- Experiments at different model scales (all current results are at ~7B) to assess whether effectiveness generalizes.
- The power distribution upweights high-*likelihood* future paths, not necessarily high-*correctness* ones (as noted at the end of Section 4.1). An analysis of when these diverge would sharpen the theoretical claims.
- Discussion of the naturally emerging longer response lengths (679 vs 600 tokens) and whether this correlates with correctness or is an MCMC artifact.

## Removed Points

*These points are flagged to be removed; treat them with caution.*

- **[REMOVED — appendix may address]** The reviewer demands sensitivity analysis for α and N_MCMC reporting. The appendix (stripped by parser) may contain these details. Section 4.3 explicitly says "we empirically find a value for B that makes Algorithm 1 performant for relatively small values of N_MCMC," suggesting this was explored.
- **[REMOVED — paper acknowledges compute cost]** The reviewer criticizes the paper for implying a "free lunch." However, the paper explicitly describes power sampling as "a new axis for inference-time scaling" (Section 4.3) and provides the expected token count formula (Eq. 12), acknowledging the inference overhead. The issue is quantification, not acknowledgment.
- **[REMOVED — entanglement claim is weak]** The reviewer notes that the proposal distribution uses temperature 1/α = 0.25, making it "entangled" with the low-temperature baseline. But the MCMC acceptance/rejection step is the key differentiator — the proposal merely generates candidates. The consistent improvement of power sampling over low-temperature (e.g., 0.690→0.748 on MATH500) directly measures the value added by targeting p^α.
- **[REMOVED — the asymmetry argument is nuanced]** The reviewer frames the out-of-domain comparison as "structurally unfair" and demands GRPO trained on task-relevant data for each benchmark. While the framing could be more careful, the paper's point is precisely that a training-free method generalizes where a domain-specific trained one does not — this is a legitimate comparison axis. The issue is in the abstract's overclaiming, not in the comparison itself, which is retained as a minor weakness.

## Novel Insights

The paper's central insight — that the power distribution p^α and low-temperature sampling, despite both being "sharpening" strategies, differ fundamentally in their treatment of future token paths — is genuinely novel and has implications beyond this specific method. The "sum of exponents" formulation (Eq. 7) reveals that p^α implicitly performs a form of look-ahead planning, preferring tokens that lead to concentrated high-likelihood futures over tokens with many diffuse future paths. This connects naturally to the critical windows / pivotal tokens phenomenon (Li et al., 2025), where a few tokens determine reasoning trajectory correctness. The empirical finding that this planning-ahead property, combined with diversity preservation (Figure 5), can achieve "best of both worlds" — GRPO-level single-shot performance without diversity collapse — is a meaningful contribution to the ongoing discussion about the nature of RL-posttraining and whether it creates genuinely new capabilities or merely sharpens existing ones.

## Suggestions

1. **Report N_MCMC and provide an accuracy-vs-N_MCMC curve.** This single experiment would resolve three weaknesses: the missing hyperparameter, the absent cost analysis, and the lack of convergence diagnostics.
2. **Include a best-of-N baseline with majority voting at matched inference compute.** If power sampling wins at equal compute, the practical contribution is very strong. If not, the theoretical contribution about p^α still stands, but the framing should be adjusted.
3. **Qualify the abstract's "outperform" claim** to explicitly note this applies to out-of-domain tasks where GRPO was not trained, and acknowledge that power sampling underperforms GRPO on the in-domain MATH500 benchmark for both Qwen models.
4. **Discuss the Phi-3.5 GRPO baseline quality.** The near-zero improvement on MATH500 (40.6 vs 40.0) and dramatic HumanEval degradation (13.4 vs 21.3) suggest the GRPO training may have failed for this model. Power sampling's apparent dominance on Phi-3.5 should be interpreted with this caveat.
5. **Report acceptance rates at each progressive stage** to help readers assess mixing quality without requiring full convergence analysis.

## Score and Decision

### Calibration Anchors

| Paper | Path | Avg Score | Round | Comparison to paper under review |
|-------|------|-----------|-------|--------------------------------|
| Systematic Review of LLMs | 8QTpYC4smR | 1.00 | R1 | Survey with no contribution; paper under review is far superior |
| NEMESIS Jailbreaking | 5kMwiMnUip | 1.40 | R1 | Trivial attack catalog; paper under review has genuine theory |
| KL Divergence GFlowNets | Uj0h13lVrR | 1.00 | R1 | Incomplete work; paper under review is a complete submission |
| All Pairs Minimax Path | bEgDEyy2Yk | 1.00 | R1 | Code implementation paper; not comparable |
| Efficiently Deploying LLMs | BjZP3fTlVg | 3.00 | R1 | Inference-time method with limited novelty; paper under review has stronger theoretical contribution |
| FlashSampling | V4Xs283LHH | 2.50 | R1 | Sampling efficiency paper; limited contribution; paper under review far stronger |
| GPT/LLM Limitations | JNZ3Om6NPS | 2.00 | R1 | Theoretical limitations paper with questionable rigor; paper under review is more rigorous |
| Min-p Sampling | FBkpCyujtS | 8.50 (mismatch with score range) | R1 | Related sampling method for LLMs; accepted with strong scores — paper under review has comparable novelty but weaker experiments |
| Extrapolative Sequence from Markov Chains | DQfHkEcUqV | 4.75 | R1 | MCMC + sequences but weaker theory and experiments; paper under review is stronger |
| Fast Value Tracking RL | LZIOBA2oDU | 5.33 | R1 | MCMC for RL but different domain; paper under review has cleaner contribution |
| Fast RBM Training | 3fGtV4Zfgq | 4.25 | R1 | MCMC for RBMs; limited scope; paper under review is broader and more impactful |
| MCMC for Inverse Problems | D7PQ54l5Q1 | 4.75 | R1 | Annealed MCMC (similar technique) but for diffusion models; paper under review has stronger practical motivation |
| Emergent Abilities Evaluation | lDbjooxLkD | 6.00 | R1 | Scaling properties paper; different focus; comparable quality level |
| **Inference Scaling Laws** | **VNckp7JEHn** | **5.75** | **R1** | **Most directly relevant: studies inference compute tradeoffs with best-of-N baselines. Paper under review has stronger novelty but lacks the cost analysis this paper provides.** |
| **Compute-Optimal Sampling** | **3OyaXFQuDl** | **7.00** | **R1** | **Comprehensive compute-matched experimental design with ablations. Paper under review has cleaner theory but weaker experimental rigor.** |
| COrAL Order-Agnostic LM | 0JjsZC0w8x | 5.75 | R1 | Iterative refinement for LMs; mixed reviews; comparable quality |
| **SMC for Controlled LLM Generation** | **xoXn62FzD0** | **8.00** | **R1** | **Most methodologically similar (Monte Carlo for LLM generation). Has ablation studies, divergence analysis. Paper under review has comparably novel theory but weaker experimental validation.** |
| Interpolating AR and Diffusion LMs | tyEyYT267x | 8.00 | R1 | Strong sampling method paper with comprehensive experiments; paper under review doesn't reach this level |
| LLM-SR Scientific Equations | m2nmp8P5in | 8.00 | R1 | Different domain; not directly comparable |
| LLAMBO Bayesian Optimization | OOxotBmGol | 8.00 | R1 | Different application; not directly comparable |

**Round 1 bracket: 5.5–7.0**

The paper's theoretical contribution (Proposition 1) is genuinely novel and its experimental scope is reasonable (3 models, 4 tasks). This places it above the 4.75-range papers (DQfHkEcUqV, D7PQ54l5Q1). However, the absence of N_MCMC, computational cost analysis, and the best-of-N baseline — exactly the kind of analysis that VNckp7JEHn (5.75) and 3OyaXFQuDl (7.0) provide — prevents it from reaching 7+. The SMC paper (xoXn62FzD0, 8.0) shows that Monte Carlo methods for LLMs can score highly when coupled with proper ablations and analysis; this paper doesn't reach that bar.

**Final calibration:** Within the 5.5–7.0 bracket, I place this paper at **6.0**. The theoretical insight is strong enough to make this a borderline accept — it introduces a genuinely new concept (power distribution vs. low-temperature sampling) with clean mathematics and consistent empirical support across models. The pass@k diversity result is particularly compelling and practically significant. However, the major experimental gaps (unreported N_MCMC, missing best-of-N baseline, no cost analysis) prevent the paper's practical claims from being fully supported and keep it from a confident accept. The contribution is real but incompletely validated.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>
## Summary

ASPEC proposes a framework for automated agent design that reconciles the tension between static task-level optimization and expensive query-level adaptation. It introduces (1) an evolutionary discovery process that finds specialist agent archetypes, (2) a cultivation phase where specialists accumulate experience-driven memory, and (3) a lightweight "retain-then-escalate" meta-controller that decides when to reuse the existing architecture vs. trigger architectural resampling. The claimed contributions are stateful knowledge accumulation and cost-efficient adaptation.

## Strengths

- **Well-motivated problem framing.** The paper clearly articulates the tension between static task-level optimization (non-adaptive) and query-level adaptation (expensive, stateless) in Section 1, and positions ASPEC as a reconciliation. This is a genuine gap the community should care about.

- **The retain-then-escalate meta-controller is a practical and novel contribution.** The ablation (Table 6) shows it achieves comparable accuracy to always-resampling (62.7% → 62.8%) at 56% of the cost ($2.00 → $0.88), and outperforms random and heuristic baselines. This is the clearest positive result in the paper.

- **Very strong cost efficiency.** Table 2 reports total training cost of $1.38 for GPQA and inference cost of $0.88, substantially below comparable frameworks (AFlow: $20.14 training + $1.58 inference; MaAS: $3.43 + $2.07). This is a practically meaningful advantage for researchers with limited API budgets.

- **The convergence analysis in Section 5.3 is thoughtful.** Figure 7 shows that on a narrow domain (GPQA), independent discovery runs converge to similar specialist archetypes (physics, chemistry, biology), while on MMLU they diverge, providing evidence that the discovery process responds to the structure of the domain.

## Weaknesses

### Major

- **Cross-domain transfer results contradict strong domain-specific expertise claims.** The paper shows (Figure 5, right) that specialists cultivated on MATH match or exceed the full system on HumanEval (code generation). The post-hoc explanation ("T-shaped reasoning strategies") is plausible but unsupported by direct evidence. If mismatched specialists work equally well, the paper should clarify what cultivation actually contributes — domain-specific knowledge or general problem-solving strategies — and provide experiments that directly test in-domain vs. cross-domain specialist performance. This is the paper's most significant evidential gap.

- **The meta-controller's training procedure is critically underspecified.** Equation 4 uses R_t(s_t, a_t) as a reward function, but R_t is never defined in the main text. The training algorithm (e.g., REINFORCE, PPO) is not specified. Training data, train/test split, and number of environment interactions are not provided. Architecture details (MiniLM variant, MLP dimensions) are absent. While Algorithm 2 may be in the appendix (stripped by the PDF parser), the reward function definition and training algorithm belong in the main text — without them, a core claimed contribution cannot be evaluated or reproduced.

- **No statistical significance or variance reporting for main results.** Table 1 reports all results as single numbers despite using T=0.3 (stochastic LLM outputs). The margins over strong baselines are small: +1.3% over EvoAgent (GPQA), +1.5% over AFlow (GPQA), +0.8% over AFlow (MATH), and ASPEC even trails AFlow on MMLU (90.0 vs 90.5). Without variance estimates, the reader cannot determine whether these differences are meaningful or within noise.

### Minor

- **The ablation analysis reveals the main system benefit is cost reduction, not accuracy.** Removing the meta-controller drops accuracy by only 0.1% (62.8→62.7%) while tripling cost. The Architect adds only 1.8% over a static ensemble. The primary accuracy driver is the specialists themselves (5.4% drop when removed). The paper's framing emphasizes "performance gains" and "expert-level capabilities," but the evidence shows the full system's main advantage over simpler variants is cost efficiency. The claims should be recalibrated.

- **The Architect LLM is not identified.** It is described as "an in-context learning LLM" but whether it is Gemini 2.0 Flash (same as the execution model) or a different model is never stated. This affects both the cost analysis and reproducibility.

- **The meta-controller's reward signal is not justified.** If it uses accuracy as the reward, training it on the same data used for cultivation raises data leakage concerns. If it uses cost, the comparison with the LLM-as-gate baseline is unfair because the two policies optimize different objectives.

### Trivial

None.

## Nice-to-Haves

- Run the main experiment (Table 1) with 3–5 seeds and report means/standard deviations.
- Add an explicit in-domain vs. cross-domain specialist comparison experiment to resolve what cultivation actually learns.
- Identify whether the Architect uses the same LLM backbone as the execution model.

## Removed Points

These points are flagged to be removed; treat them with caution.

- *Rediscovery cost asserted not measured* — removed: this demands measurement outside the paper's stated qualitative scope.
- *V_π_θ notation confusion in Equation 2* — removed: a minor notation issue that does not threaten any core claim.
- *Missing discovery iteration / evaluation details* — removed: these are standard implementation details likely in the (stripped) appendix.
- *Cross-model transferability underexplored* — removed: this is a future-work suggestion, not a weakness.
- *LLM-as-gate fairness (same model)* — removed: cheaper heuristics (random, cosine) are also tested as controls.
- *Confusion matrix / oracle proxy validity* — removed: the paper openly acknowledges this limitation in Section 6.
- *"Strengthening the Paper" experiments* — removed: these are constructive suggestions, not weaknesses of the current submission.

## Novel Insights

The ONLYSPEC finding (MATH-trained specialists working on HumanEval) suggests that the cultivation phase may teach generalizable problem-solving meta-skills (structured decomposition, careful verification) rather than domain-specific factual knowledge. This reframes ASPEC's contribution as "cultivation of robust, domain-agnostic reasoning habits" rather than "deep domain expertise" — a potentially more interesting and general result, but one the paper does not fully develop. The convergence divergence pattern in Figure 7 (domain-labeled roles on GPQA vs. skill-labeled roles on MMLU) further hints that the discovery process finds cognitive strategies on broad domains, but this insight is not explored.

## Suggestions

1. Define R_t(s_t, a_t) explicitly in the main text and specify the meta-controller's training algorithm.
2. Report Table 1 with multiple runs (3–5) and standard deviations.
3. Add an in-domain vs. cross-domain specialist comparison experiment — the single highest-leverage experiment for clarifying the paper's contribution.
4. Identify the Architect LLM model explicitly.
5. Recalibrate the paper's framing to reflect that the primary measured advantage of the full system is cost efficiency at matching accuracy, not a large accuracy gain over the best baselines.

## Score and Decision

The paper addresses a well-motivated problem and has genuine practical strengths — particularly the cost efficiency of the retain-then-escalate meta-controller and the discovery pipeline. However, three significant issues prevent a stronger rating: (a) the ONLYSPEC finding undermines the strong domain-specificity narrative without adequate resolution, (b) the meta-controller's training procedure is underspecified (reward function undefined in the main text), and (c) main results lack variance estimates despite small margins. These are addressable in revision but materially weaken the current submission.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>
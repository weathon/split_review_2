## Summary
# Final Review Report

## Summary

This paper proposes AdaBoN, a prompt-adaptive allocation strategy for Best-of-N alignment. The core idea is to replace the uniform per-prompt sampling budget in standard Best-of-N with a two-stage procedure: (1) explore each prompt with a small budget to estimate its reward distribution via Gaussian kernel density estimation, and (2) allocate the remaining budget adaptively across prompts using a greedy marginal-gain maximization algorithm. The method requires no auxiliary model training and works with any LM-RM combination.

The paper is well-motivated and addresses a practical limitation of Best-of-N sampling—its lack of adaptivity across prompts of varying difficulty. The experimental evaluation is broad, covering 12 LM-RM pairs across 3 datasets with 50 prompt batches. The proposed Batch Win Rate (BWR) and Expected Survival Time (EST) metrics are sensible for evaluating adaptive allocation strategies.

However, the paper has several significant weaknesses: (1) a mathematical error in the Scott's rule bandwidth formula (exponent sign is inverted, which would severely impact KDE quality), (2) no statistical significance testing for the primary BWR metric, (3) the exploration budget consumes 75% of total compute, making the practical efficiency gains modest, (4) the EST metric interpretation potentially overstates savings, and (5) the optimality gap between theoretical guarantees and practical estimation is not addressed. Additionally, novelty claims cannot be fully verified due to the retrieval-disabled mode in this run.

**Score: 6/10** — The paper presents a clean, practical idea with broad evaluation, but the methodological rigor in statistical analysis and mathematical correctness needs substantial improvement.

## Strengths
1. **Well-motivated problem**: The paper identifies a genuine practical limitation of Best-of-N sampling—the uniform allocation of sampling budgets across prompts of varying difficulty. This problem is relevant for on-device and personalized inference scenarios where compute budgets are constrained and prompts differ substantially in alignment difficulty.

2. **Clean and practical method**: AdaBoN's two-stage approach is conceptually simple and does not require auxiliary model training. The use of Gaussian KDE with Scott's rule for reward distribution estimation is lightweight, and the greedy allocation algorithm (Algorithm 1) is computationally efficient since it operates on estimated values without additional LM queries.

3. **Broad empirical evaluation**: The paper evaluates 12 LM-RM pairs across 3 datasets (AlpacaEval, HH-RLHF, PKU-SafeRLHF) with 50 prompt batches each. This is substantially more comprehensive than prior work (Damani et al., 2024, which used a single LM-RM pair and single batch). The evaluation covers 4 different LMs and 3 different reward models, all at 7-8B parameter scale.

4. **Sensible evaluation metrics**: BWR and EST are well-designed for the task. BWR correctly handles the ordinal nature of reward model scores by comparing against the natural baseline (uniform allocation), and EST provides an interpretable measure of computational savings by quantifying the equivalent uniform budget.

5. **Latency-aware design**: By restricting to a two-stage policy, AdaBoN minimizes parallelization overhead—only two sequential calls to the base LM are needed. This is a practical advantage over more adaptive (but less parallelizable) alternatives.

6. **Transparent limitations**: The Discussion section openly acknowledges several limitations, including the Gaussian KDE assumption, the lack of dynamic refinement, and the batch requirement. This improves the paper's scientific credibility.

## Weaknesses
### Major Weaknesses

**W1. Mathematical error in Scott's rule bandwidth formula (Page 5 - Section 3.1)**
The paper states the bandwidth as `h = σ̂ d^{1/5}`, but Scott's rule for 1D Gaussian KDE is `h = σ̂ d^{-1/5}` (exponent -1/5, not +1/5). With d=90, the paper's formula produces h ≈ 2.46σ̂ instead of h ≈ 0.41σ̂ — approximately 6× oversmoothed. If the implementation follows the paper's formula, the KDE would be severely oversmoothed, potentially degrading allocation quality. If the implementation is correct and only the paper has a typo, this is a writing error that must be corrected. In either case, the authors must clarify which formula was actually used and correct the exponent.

*Impact*: Directly affects the validity of the KDE estimates and thus the allocation decisions. Any conclusions about the effectiveness of Gaussian KDE for this problem may be compromised if the bandwidth was misspecified.

*Required action*: (a) Correct the formula to h = σ̂ d^{-1/5}. (b) State explicitly whether the implementation used the correct or incorrect formula. (c) If the wrong formula was used, re-run experiments and report whether results change.

**W2. No statistical significance testing (Page 7 - Section 4.3)**
The paper reports median BWR values ranging from 0.54 to 0.62 across 12 LM-RM pairs, but provides no formal hypothesis test for whether these values are statistically significantly above 0.50. Given that the improvements are modest (most BWRs are between 0.55 and 0.62), some of these could be within the noise of the 100-run estimation procedure. With 12 LM-RM pairs × 3 datasets and no multiple comparison correction, the risk of false positives is non-trivial.

*Impact*: The claim that "AdaBoN consistently outperforms the uniform allocation" is not rigorously supported. Without p-values or confidence intervals, a skeptical reviewer could argue that the observed win rates could arise from random variation.

*Required action*: Add statistical significance tests (e.g., one-sided sign test across batches for each LM-RM pair) with multiple-testing correction (Holm-Bonferroni or FDR). Report which pairs achieve significance. Also report standard errors for each batch's BWR estimate.

**W3. Large exploration budget relative to efficiency gains (Page 7 - Section 4.3)**
AdaBoN uses d = 0.75B for exploration, meaning 75% of the per-prompt budget is consumed *before* any adaptive allocation occurs. For B=120, only 30 samples per prompt (25% of budget) are available for adaptive allocation. The median BWR values (0.55-0.62) indicate that AdaBoN wins against uniform allocation only 55-62% of the time — a relatively modest margin considering that 75% of the budget is already spent uniformly.

*Impact*: The practical efficiency claim is weaker than suggested. A practitioner spending 75% of their budget uniformly and seeing a 55-62% win rate may question whether the additional complexity of AdaBoN is worthwhile.

*Required action*: (a) Add ablation experiments with smaller d values (e.g., d ∈ {0.1B, 0.25B, 0.5B}) to show the exploration-adaptation trade-off. (b) Discuss the cost-benefit ratio in the main text, not only in the hyperparameter tuning paragraph. (c) If KDE with d=0.75B is necessary for good performance, this is a significant practical limitation that should be acknowledged upfront.

**W4. Gap between theoretical optimality and practical estimation (Page 4 - Section 3)**
Proposition 3.1 proves concavity of the expected maximum function for a known distribution D, and Algorithm 1 is optimal for known V_{i,j} values under this concavity property. However, in practice, V_{i,j} is estimated via Monte Carlo from a KDE that itself is estimated from only d samples. The paper acknowledges this gap in one sentence ("While the greedy procedure may not be optimal when run on the estimated vectors") but does not analyze how estimation error propagates to allocation quality. No bound, sensitivity analysis, or diagnostic is provided.

*Impact*: The theoretical framing creates an impression of near-optimality that is not justified. A reader cannot tell whether the observed BWR improvements are due to the adaptive allocation or simply noise from the estimation procedure.

*Required action*: (a) Add a sensitivity analysis in the appendix showing how allocation quality varies with Monte Carlo sample size m and exploration budget d. (b) Provide an empirical diagnostic: compare the greedy allocation computed from estimated V̂_{i,j} against the allocation from a larger-sample "ground truth" estimate for a subset of batches.

**W5. EST metric interpretation potentially overstates savings (Page 6 - Section 4.2)**
The EST is defined as an infinite sum but truncated at N=2B in practice. The paper claims "AdaBoN is competitive against uniform allocations with 20% larger inference budgets" (abstract and contribution list) based on EST values of 148-153 for B=120 (~23-28% savings). However, the stronger claim of "33% larger" (EST≥160) appears only in the main results paragraph and is based on upper-quartile or outlier batches, not median values. The presentation is inconsistent: the abstract suggests 20% savings broadly, while the best-case batches give 33%.

*Impact*: Misleading presentation of results. The practical savings are in the 20-28% range (median), not the 33% (best case).

*Required action*: (a) Consistently report median savings with quartiles. (b) Replace "up to 33%" with "median 23-28%" or similar in the main text. (c) Discuss truncation bias of the EST estimate.

**W6. Contribution (1) is not a true contribution (Page 1 - Introduction)**
The first listed contribution is "We find that the per-prompt reward distributions for the LM-RM pairs we consider are smooth and easy to learn." This is an empirical observation about specific model configurations, not a general scientific contribution or a methodological innovation. It motivates the KDE choice but should not be listed as a standalone contribution alongside the algorithmic proposal and evaluation metrics.

*Impact*: Weakens the contribution framing. A reviewer could argue that this observation is dataset- and model-dependent and does not constitute a novel finding.

*Required action*: Remove (1) from the contribution list and incorporate it into Section 3.1 as motivation for the KDE choice.

### Minor Weaknesses

**W7. Related work comparison with Damani et al. lacks evidence (Page 2 - Related Work)**
The claim that Damani et al.'s method "does not observe significant improvements for large inference budgets" is stated without a supporting citation or quantitative detail. The paper also does not compare against alternative adaptive allocation strategies (e.g., bandit-based approaches, Bayesian optimization for prompt selection) that could serve as baselines.

*Required action*: (a) Add a specific citation to the relevant section/experiment in Damani et al. (b) Discuss at least one additional adaptive baseline conceptually (e.g., Thompson sampling) even if computationally infeasible to implement.

**W8. Notation inconsistency in running example (Page 3 - Section 2.3)**
The Bernoulli example uses notation `R_{1,d}^1` and `R_{1,d}^2` which is confusing and inconsistent with the previously defined `R_{i,1:d}` notation. The superscript index is ambiguous.

*Required action*: Rewrite with consistent notation: M₁ = max{R₁₁, ..., R₁d} and M₂ = max{R₂₁, ..., R₂d}.

**W9. Limited discussion of failure modes (Page 8 - Section 5)**
The limitations section acknowledges the KDE assumption issue for discrete RMs but does not discuss: (a) what happens when reward distributions are multimodal with widely separated modes, (b) the computational cost of the Monte Carlo estimation phase (O(K²B)), or (c) sensitivity to the batch construction method.

*Required action*: Expand the Discussion section to include these additional limitations and failure modes.

**W10. No comparison with any adaptive baseline (Page 6 - Section 4.2)**
The paper justifies not comparing with Damani et al. (2024) due to computational constraints, but this leaves the empirical evaluation without any adaptive baseline. All comparisons are against uniform allocation. While uniform is the natural baseline, the lack of any alternative adaptive method makes it difficult to contextualize AdaBoN's performance within the broader literature.

*Impact*: A reader cannot assess whether AdaBoN outperforms simpler adaptive heuristics, such as allocating extra budget to prompts with the highest variance observed during exploration, or using upper confidence bound (UCB) style allocation.

*Required action*: Implement at least one simple adaptive baseline (e.g., allocate remaining budget proportional to the variance or the maximum reward observed during exploration) to demonstrate that AdaBoN's specific allocation mechanism is beneficial beyond naive adaptivity.

### Deferred Novelty Verification

Due to the retrieval-disabled mode in this run (external paper search unavailable), the following novelty-related judgments could not be fully verified:
- The claim that AdaBoN is the first training-free adaptive allocation method for Best-of-N.
- The positioning relative to Damani et al. (2024) and other concurrent work.
- The claim that reward distributions are "smooth and easy to learn" as a general property.

These judgments are marked as **deferred manual verification** and should be checked by the authors or reviewers against the latest literature.

## Score
**Final Score: 6/10**

*Rationale*: The paper addresses a well-motivated problem with a clean, practical method and a broad evaluation spanning 12 LM-RM pairs across 3 datasets. These are genuine strengths. However, the score is limited by the following factors:

- **Novelty** (deferred verification): Without external literature retrieval, the novelty claims cannot be fully verified. The core idea (two-stage adaptive allocation for BoN) is a natural extension of existing work, and the main differentiator from Damani et al. (2024) is clearly articulated. However, the contribution list includes an empirical observation as a standalone contribution.

- **Validity risk** (major concern): The mathematical error in Scott's rule bandwidth formula (incorrect exponent sign) raises questions about whether the implementation matches the paper's description. If the formula was used as written, the KDE would be severely oversmoothed, potentially compromising results.

- **Statistical rigor** (major concern): The primary claim of "consistent outperformance" is not supported by formal hypothesis testing. BWR values are modest (0.54-0.62), and with 12 LM-RM pairs, multiple comparison corrections are needed.

- **Practical significance** (moderate concern): With 75% of budget consumed in exploration, the effective efficiency gains are modest (median savings of 23-28%). The presentation of EST results could give an inflated impression of savings.

- **Reproducibility** (adequate): The experimental setup is clearly described, and the use of standard HuggingFace generation functions aids reproducibility.

The paper has solid foundations and addresses a worthwhile problem, but the mathematical error, lack of statistical rigor, and modest practical gains prevent a higher score. With corrections to the bandwidth formula, addition of significance tests, and more careful presentation of results, the paper could be strengthened to the 7-8 range.
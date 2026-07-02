## Summary
# Final Review Report

## Summary

This paper proposes Critique-RL, a two-stage reinforcement learning approach for training critiquing language models (critics) that can assess and provide feedback on LLM outputs without requiring stronger supervisors or oracle verifiers. The key insight is that optimizing critics solely through indirect reward signals (based on the actor's refinement outcome) improves helpfulness but degrades discriminability (the ability to judge response correctness), leading to overly conservative or aggressive feedback. Critique-RL addresses this by: (Stage I) optimizing discriminability via direct rule-based rewards that reward correct judgment of the original response, and (Stage II) optimizing helpfulness via refinement-based rewards while preserving discriminability through KL regularization toward the Stage I policy.

Experiments on mathematical reasoning benchmarks (MATH, GSM8K, AQuA) with Qwen2.5-3B/7B, Llama3.2, and DeepSeek models show that Critique-RL consistently outperforms SFT, STaR, Retroformer, and CTRL baselines on both refinement accuracy (Acc@Refine) and discriminability (Acc@Dis). For example, on Qwen2.5-7B it achieves 58.40% Acc on MATH (+12.66 Δ over no-critic baseline) compared to 53.86% for CTRL, and 85.20% Acc@Dis vs 71.42% for CTRL. The method also shows promising cross-task generalization and iterative improvement capability.

**Strengths**: (1) The core research question — building effective critics without stronger supervision — is important and timely for scalable oversight. (2) The diagnostic analysis of why indirect rewards fail on discriminability is well-executed and provides actionable insight. (3) The two-stage solution is conceptually clean and the ablations convincingly demonstrate the necessity of both stages. (4) The paper includes extensive comparisons across multiple models, tasks, and baselines.

**Weaknesses**: (1) No statistical significance reporting or variance estimation across runs (single point estimates in all tables). (2) The "Stage II w/o discrimination" ablation conflates two distinct mechanisms (r_dis removal and KL regularization removal). (3) The beta_2 hyperparameter (KL regularization strength in Stage II) is not reported. (4) The "OOD" claim is overstated — SVAMP and TheoremQA are still math tasks within the same domain. (5) The abstract and conclusion lack specific limitations and precise experimental scope boundaries. (6) Missing discussion on why the same-base-model design was chosen and its implications for capacity.

**Novelty**: Novelty assessment is deferred as external literature verification is unavailable in this run. Based on the manuscript's own comparisons, the two-stage RL design with explicit discriminability optimization appears to be a novel contribution beyond Retroformer and CTRL, which optimize only helpfulness.

## Strengths
**S1. Important and well-motivated problem.** Training LLMs to critique other models without stronger supervision is a core challenge in scalable oversight. The paper clearly identifies the practical limitation: existing methods require expensive stronger-supervisor annotation or oracle verifiers. The motivation for a self-contained RL approach that needs neither is strong and timely.

**S2. Insightful diagnostic analysis (Section 4.1).** The paper's key empirical finding — that optimizing critics via indirect reward signals (r_refine, r_Δ, r_correction) improves helpfulness but degrades discriminability — is a significant contribution beyond the method itself. The training dynamics in Figure 3 convincingly show the "conservative vs aggressive" failure modes and their root cause. This finding has implications beyond the specific method and could influence how future critique models are designed.

**S3. Clean, well-motivated two-stage design.** The decomposition into discriminability-first (Stage I) and helpfulness-with-regularization (Stage II) is conceptually simple and the ablation study confirms both stages contribute. The use of KL regularization toward the Stage I policy (rather than the SFT policy) to preserve discriminability during helpfulness optimization is sensible. The Algorithm 1 pseudocode is complete and reproducible.

**S4. Comprehensive empirical evaluation.** The paper compares against SFT, STaR, Retroformer (PPO-based), and CTRL (GRPO-based) across three in-domain and two OOD datasets, two model scales (3B, 7B), and multiple model families (Qwen2.5, Llama3.2, DeepSeek-R1-Distill). The consistent gains across all settings demonstrate robustness. The inclusion of Acc@Dis as a separate metric is valuable for understanding why the method works.

**S5. Inference-time scaling analysis.** The demonstration that Critique-RL improves the performance ceiling under majority-vote scaling (Figure 1) and is more compute-efficient than parallel sampling (3K vs K×refinement) adds practical value for deployment.

**S6. Iterative improvement validation.** The paper shows both inference-time iterative refinement gains (Figure 4) and iterative training gains (Table 2), indicating the method can potentially bootstrap its own improvement over multiple rounds.

## Weaknesses
**W1. Missing statistical rigor (Critical).** All experimental results (Tables 1-4) are reported as single point estimates with no standard deviations, confidence intervals, or significance tests. It is impossible to determine whether the reported improvements (e.g., 65.75 vs 64.96 on AQuA 7B — a 0.79 point difference) are statistically meaningful or within the noise range of training variability. This is a major reproducibility and reliability concern. The paper should report means ± std over at least 3 independent runs and, where feasible, include paired significance tests against the strongest baseline. [Annotations 11, 12]

**W2. Missing hyperparameter reporting (Major).** The KL regularization coefficient beta_2 in Eq. (9) is not reported anywhere in the main text or implementation details (only beta_1 = 0.2 is given). Since beta_2 controls the strength of regularization toward the Stage I policy — a critical component for maintaining discriminability during Stage II — this omission prevents full reproducibility. The trade-off between beta_1 and beta_2 determines the balance between helpfulness optimization and discriminability preservation. A sensitivity analysis over beta_2 (and ideally beta_1) should be included. [Annotation 10]

**W3. Conflated ablation condition (Major).** The "Stage II w/o discrimination" ablation in Table 3 simultaneously removes both the r_dis reward signal and the KL(pi_Stage-I || pi_Stage-II) regularization. This confound makes it impossible to determine whether the performance drop is caused by losing the direct discriminability signal, losing the KL anchor, or both. A finer-grained ablation with separate conditions (w/o r_dis only, w/o KL only, w/o both) would clarify the mechanism. This is particularly important because Stage I's benefit may come from both better initialization and the KL anchor. [Annotation 14]

**W4. Overclaimed "OOD" generalization (Major).** The paper refers to SVAMP and TheoremQA as "out-of-domain" tasks, but both are mathematical reasoning datasets — the same domain as the training tasks (MATH, GSM8K, AQuA). The generalization is across problem formats and difficulty levels, not across domains. While the summarization experiments in Appendix G partially address this, the main text's claim of "generalize to unseen tasks" and "OOD" is misleading for readers who interpret OOD as cross-domain (e.g., math→summarization). The SVAMP/TheoremQA results should be labeled as "cross-task generalization within math reasoning." [Annotation 15]

**W5. Abstract/conclusion lack specificity (Minor).** The abstract uses "substantial performance improvements" and "highlighting its potential" without specifying the experimental scope (mathematical reasoning tasks). The conclusion is a generic restatement of contributions with no verified quantitative summary, no concrete limitations, and no actionable future directions. Both should be tightened to include specific scope boundaries and verified findings. [Annotations 1, 16]

**W6. Shared-base-model design not justified (Minor).** The paper uses the same base architecture for actor and critic (Page 6, Implementation Details) but does not discuss the implications. Using the same capacity for both roles may limit the critic's ability to outperform the actor's own self-judgment. The paper should explain why separate models of different sizes were not considered and discuss potential capacity bottlenecks. [Annotation 8]

**W7. Arbitrary reward value in Eq. (6) (Minor).** The r_correction reward assigns 0.2 for (correct→correct) transitions. This value is not justified or ablated. Since this reward contributes to the "aggressive" bias pattern, the choice should be explained or replaced with a principled value. [Annotation 9]

**W8. Limited analysis of when/why the method works (Minor).** The main results section reports "Critique-RL outperforms" but does not analyze which error types are corrected (arithmetic vs logic vs estimation errors), whether gains come primarily from improved discriminability or improved helpfulness, or in which cases refinement hurts (Δ^{c→i} remains significant at ~5-10% in Figure 3). A breakdown analysis would strengthen scientific contribution. [Annotation 12]

**W9. Notation inconsistency in Eq. (8)/(9) (Minor).** The expectation subscripts use an unconventional pipe-in-parenthesis notation (|x, y|) instead of the standard conditional bar (c|x, y). While unlikely to cause implementation errors, it may confuse readers and should be corrected for clarity. [Annotation 10]

## Score
**Final Score: 6/10**

**Rationale:** The paper tackles an important problem with a well-motivated and conceptually clean method. The diagnostic analysis of discriminability degradation under indirect rewards is insightful and has value beyond the specific approach. The empirical evaluation is broad (multiple models, datasets, baselines). However, the lack of statistical rigor (single-run point estimates, no variance/significance reporting) and missing hyperparameter (beta_2) undermine reproducibility and prevent full confidence in the reported gains. The OOD claim is overstated, and the key ablation conflates two mechanisms. These weaknesses are fixable but currently reduce the paper's evidentiary strength.

**Score Dimensions:**
- Research value / importance: 8/10 — Important problem for scalable oversight
- Novelty: 6/10 — Two-stage RL with discriminability-first is a clear advance over Retroformer/CTRL, but external verification is deferred (Retrieval-Disabled Mode)
- Experimental soundness: 5/10 — Missing variance, significance, hyperparameter reporting
- Clarity / presentation: 7/10 — Generally well-written with a few overclaim issues

**Post-Revision Target:** [7, 8]/10 — Achievable by adding variance reporting, significance tests, beta_2 sensitivity analysis, finer-grained ablation, and correcting OOD wording.
## Summary

This paper proposes Guided Hybrid Policy Optimization (GHPO), a framework that addresses reward sparsity in RLVR training for LLMs by dynamically detecting when problems are too hard for the current model (via all-zero group rewards) and adaptively injecting partial ground-truth solution hints to provide learning signals. The approach switches between standard on-policy RL for manageable tasks and guided imitation learning for challenging ones, demonstrating ~5% average improvement over GRPO across six mathematical reasoning benchmarks.

## Strengths

- **Clear and well-motivated problem identification.** The paper quantifies the capacity-difficulty mismatch convincingly—showing that even Qwen2.5-7B-Instruct fails on 52% of NuminaMath-1.5 problems—making the reward sparsity problem concrete and actionable.

- **Elegant, computation-efficient difficulty detection.** Leveraging the existing group reward signals from GRPO to detect difficulty (all-zero = hard) requires zero additional model calls or infrastructure, making it practical and lightweight compared to approaches requiring auxiliary models.

- **Comprehensive training dynamics analysis.** Figure 4 provides compelling evidence across four metrics (format reward, accuracy reward, mean response length, gradient norm) showing GHPO's smoother optimization trajectory—particularly the smaller, more stable gradient norms, which directly support the stability claims.

- **Consistent improvements across settings.** GHPO shows gains on both Qwen2.5-Base-7B and Qwen2.5-Math-7B, across easy (Math3to5) and hard (NuminaMath-S) training sets, and over both GRPO and curriculum learning baselines, suggesting genuine robustness rather than brittle gains.

- **Practical relevance for smaller models.** The paper correctly highlights that this problem is most acute for capacity-constrained models, making the work relevant to the growing on-device LLM deployment community.

## Weaknesses

### Fatal
None.

### Major

- **Missing comparison with key competing methods.** The related work section discusses DAPO, LUFFY, Dr. GRPO, and VAPO as relevant zero-RL advances, yet none appear in the experimental comparisons. DAPO's dynamic sampling addresses the same reward sparsity problem from a different angle, and LUFFY's mixing of on-policy/off-policy rollouts is conceptually related. Without these comparisons, it's difficult to assess GHPO's true standing among current methods.

- **Coarse binary difficulty detection.** The mechanism classifies problems as either "hard" (all G rewards zero) or "easy" (any reward nonzero). This misses intermediate cases where, say, only 1 out of G responses is correct—a problem the model can barely solve—which might benefit from partial guidance. The paper does not explore graded difficulty thresholds or analyze sensitivity to this design choice.

- **Evaluation limited to mathematical reasoning.** All experiments use math benchmarks. Since the paper claims general applicability of GHPO, evaluation on at least one other verifiable-reward domain (e.g., code generation with unit tests) would significantly strengthen the generality claims.

### Minor

- **Key design details deferred to appendix.** The adaptive hint ratio ω schedule (Section 3.4) and prompt templates (Appendix B) are central to the method but are not sufficiently described in the main text. A brief description of the multi-stage hint ratio strategy in the main paper would improve self-containedness.

- **No ablation on hint ratio or group size.** The paper does not analyze how the hint ratio ω or the number of sampled responses G affects performance. Given that these are core hyperparameters, understanding their sensitivity would strengthen the empirical contribution.

- **Assumption 1 is presented as theoretical motivation but lacks formal justification.** The assumption that using ground-truth traces for failing problems improves OOD generalization is plausible but stated without proof or formal argument, and the "demonstration" referenced in Section 4 is empirical rather than theoretical. Framing it more clearly as an empirical hypothesis rather than an assumption would be more precise.

### Trivial
None.

## Nice-to-Haves

- A comparison showing how GHPO scales with model size (e.g., 1.5B, 3B, 7B, 14B models) would illuminate whether the capacity-difficulty mismatch grows predictably with model scale.
- Analysis of whether GHPO-generated hints introduce any distribution shift in the learned reasoning style (e.g., do models trained with GHPO tend to produce reasoning traces more similar to the ground-truth format?).

## Novel Insights

The paper's most compelling observation is the empirical quantification of reward sparsity throughout training—Figure 3 shows that ~60% of problems remain "difficult" even in later training stages, contradicting the implicit assumption in many curriculum learning approaches that the model quickly outgrows hard problems. This persistent sparsity provides strong motivation for the adaptive guidance approach. Additionally, the observation that GHPO produces smaller gradient norms while achieving higher accuracy reward suggests that providing hints for intractable problems not only supplies missing learning signals but also stabilizes optimization by reducing the variance of gradient updates across the batch.

## Suggestions

- Add DAPO and at least one other recent baseline (e.g., LUFFY or Dr. GRPO) to Table 2 to contextualize GHPO's improvements against the current state of the art.
- Include an ablation study varying the hint ratio ω schedule and the number of groups G to provide practical guidance for practitioners.
- Add a brief paragraph in Section 3.4 summarizing the multi-stage hint ratio strategy rather than deferring entirely to the appendix.
- Consider evaluating on at least one code generation benchmark (e.g., HumanEval, MBPP) with unit-test-based verifiable rewards to demonstrate cross-domain applicability.

## Score and Decision

The paper presents a practical and well-motivated method that addresses a real problem in LLM RL training. The core idea—using group reward signals for difficulty detection and adaptively providing hints—is simple yet effective, and the experimental results are consistent. However, the absence of comparisons with key competing methods (DAPO, LUFFY, Dr. GRPO) that are discussed in the paper itself, combined with the limited domain evaluation and coarse difficulty detection mechanism, prevent me from recommending strong acceptance. The paper is above average but would benefit from a more thorough experimental evaluation.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: Accept
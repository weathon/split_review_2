## Summary
This paper proposes Critique-RL, a two-stage RL approach for training language models to critique outputs. Stage I optimizes the critic's **discriminability** (judging whether a response is correct) via a direct rule-based reward signal. Stage II optimizes **helpfulness** (constructive feedback) via the actor's refinement correctness while preserving discriminability through continued discrimination reward and KL regularization. Experiments on math reasoning tasks (MATH, GSM8K, AQuA in-domain; SVAMP, TheoremQA OOD) using Qwen2.5-3B/7B show consistent improvements over SFT, STaR, Retroformer, and CTRL baselines.

## Strengths
1. **Clear, empirically-grounded problem diagnosis (Section 4.1, Figure 3).** The paper identifies a genuine failure mode: RL with only indirect actor-refinement rewards produces critics that are either "conservative" (unwilling to suggest changes) or "aggressive" (overly willing to change correct answers), because discriminability is never directly optimized. The training dynamics in Figure 3 make this diagnosis concrete. This analysis is the paper's strongest contribution.

2. **Principled two-stage design that follows directly from the diagnosis.** Stage I optimizes discriminability via a direct correctness-judgment reward ($r_{\text{dis}}$); Stage II optimizes helpfulness via actor refinement correctness ($r_{\text{refine}}$) while preserving discriminability through continued $r_{\text{dis}}$ signal and KL regularization toward the Stage I policy. The design is clean, well-motivated, and the ablations (Table 3) confirm each component's contribution.

3. **Substantial empirical gains on key benchmarks.** On Qwen2.5-7B, Critique-RL outperforms the best baseline (CTRL) by 4.54 points on MATH (58.40 vs 53.86) and 6.37 points on GSM8K (87.72 vs 81.35). Discriminability gains are even larger (85.20 vs 71.42 on MATH). These are practically meaningful improvements that hold across two model sizes.

4. **Clean ablation study (Table 3).** Removing each component (Stage I, Stage II, discrimination reward in Stage II) and replacing $r_{\text{refine}}$ with alternatives all produce consistent degradation. This provides solid evidence that the specific two-stage design, not just RL, drives the improvement.

5. **OOD generalization (Table 4).** The method transfers to SVAMP and TheoremQA (tasks unseen during training) with gains over baselines, demonstrating a generalizable critiquing skill beyond task-specific patterns.

## Weaknesses

### Fatal
None.

### Major
1. **No variance or statistical significance reporting.** Every result in Tables 1–4 is a single point estimate with no confidence intervals, error bars, or standard deviations. For large gains (MATH +4.54, GSM8K +6.37) this is less concerning, but for smaller differences — AQuA 7B: 65.75 vs 64.96 (0.79 point gap), TheoremQA 7B: 21.4 vs 21.1 (0.3 point gap) — it is impossible to assess whether these are meaningful or noise. Given the pipeline involves stochastic sampling of both critiques and refinements, variance reporting across seeds is necessary to substantiate the claims, particularly for the smaller-margin results.

### Minor
1. **Oracle verifier requirement during training is under-discussed as a boundary condition.** The paper explicitly states it does not assume an oracle "during testing" (line 96) and is transparent about using $r_{\text{oracle}}$ for training rewards (Section 3.1, Algorithm 1). However, the framing around "scalable oversight" and "without stronger labeling" (abstract, line 9) could imply broader applicability than the experiments support. The method is demonstrated only on tasks with verifiable answers (math reasoning), and the only non-math experiment (summarization, Appendix G) is mentioned but not shown in the main paper. A limitations paragraph stating the oracle training requirement, the fixed-actor assumption, and the demonstrated scope would strengthen the paper.

2. **RL algorithm confound in the main baseline comparison (Table 1).** Critique-RL uses RLOO, while Retroformer uses PPO and CTRL uses GRPO. The ablation in Table 3 partially addresses this by comparing reward variants within the same RLOO framework, which supports the core architectural claim. Nevertheless, the comparison against Retroformer and CTRL in Table 1 does not control for the RL algorithm, so some portion of the reported gains may derive from the choice of RLOO. An apples-to-apples control (running the same reward with different base algorithms, or vice versa) would sharpen the conclusion.

3. **No dedicated limitations section.** The paper lacks an explicit discussion of key boundary conditions: the oracle verifier needed during training, the fixed-actor assumption, computational cost of two-stage RL, and whether the method extends beyond verifiable-answer tasks.

4. **KL regularization asymmetry is not justified.** Stage I uses $\text{KL}(\pi_{\phi}^{\text{SFT}} || \pi_{\phi}^{\text{Stage-I}})$, while Stage II uses $\text{KL}(\pi_{\phi}^{\text{Stage-I}} || \pi_{\phi}^{\text{Stage-II}})$. The rationale for this progression and the choice of forward KL in Stage II (vs. KL to the SFT model) is not explained.

5. **Hyperparameter $\beta_2$ not reported.** $\beta=0.01$ (line 253) and $\beta_1=0.2$ (line 274) are given, but $\beta_2$ (the KL scaling factor in Stage II, Eq. 9) is not. No sensitivity analysis is provided for the KL coefficients.

### Trivial
None.

## Nice-to-Haves
- Report computational cost (GPU hours, wall-clock time) for the two-stage pipeline vs. single-stage baselines.
- Include at least one non-math result summary (e.g., from the summarization experiment in Appendix G) in the main paper.
- The iterative training experiment (Table 2) shows only two iterations; extending to more iterations would strengthen the convergence analysis.

## Removed Points
These points are flagged to be removed; treat them with caution.
1. **"SFT baseline uses Qwen2.5-3B-Instruct data, making it artificially weak."** — All methods (SFT, STaR, Retroformer, CTRL, Critique-RL) start from the same SFT initialization trained on the same data. The comparison is fair; this criticism misunderstands the setup.
2. **"The claim that discriminability implicitly contributes to helpfulness is speculative."** — The paper phrases this as a tentative observation ("suggesting that the two abilities are not entirely independent," line 331), not a strong causal claim. The criticism overstates what the paper asserts.
3. **"Only two iterations of iterative training shown."** — Moved to Nice-to-Have. Two iterations with clear improvement are informative; requesting more is a suggestion, not a weakness.
4. **"Missing code release."** — Removed per policy as a reproducibility nitpick about artifacts impractical to include in a submission.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. Add standard deviations or confidence intervals across 3–5 seeds for all main results, or at minimum for the smaller-margin comparisons (AQuA, TheoremQA).
2. Add a limitations paragraph explicitly stating the oracle verifier requirement during training, the fixed-actor assumption, and the demonstrated scope (verifiable-answer tasks).
3. Run at least one control experiment using the same base RL algorithm across reward formulations, or explicitly note that Table 3 provides this control internally.
4. Report $\beta_2$ and provide a brief sensitivity analysis or justification for the KL coefficient choices.
5. Briefly justify the asymmetric KL regularization (KL to SFT in Stage I vs. KL to Stage I in Stage II).

## Score and Decision
The paper makes a genuine contribution. The failure-mode analysis in Section 4.1 is insightful, the two-stage design is well-motivated, the empirical gains on MATH and GSM8K are substantial and consistent, and the ablation study cleanly supports the architectural claims. The main weaknesses — no variance reporting, under-discussed boundary conditions, and a partially confounded baseline comparison — are addressable and do not invalidate the core contribution. The evidence supports the paper's central claims about the effectiveness of explicit two-stage optimization for training critique models.

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>
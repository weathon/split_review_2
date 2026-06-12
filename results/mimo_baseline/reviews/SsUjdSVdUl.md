## Summary
This paper proposes Critique-RL, a two-stage reinforcement learning approach for training critique models that can both correctly judge response quality (discriminability) and provide constructive feedback (helpfulness). The key insight is that using only indirect reward signals from actor refinement correctness leads to unsatisfactory critics—either overly conservative or overly aggressive—and that explicit optimization of discriminability with direct rewards in a first stage, followed by helpfulness optimization with discriminability regularization in a second stage, resolves this issue.

## Strengths
- **Insightful failure mode analysis.** The paper's preliminary analysis (§4.1, Figure 3) clearly diagnoses why indirect-reward-only RL fails: the critic develops either conservative or aggressive behavioral patterns because discriminability is insufficiently optimized for one class of responses. This diagnostic contribution is valuable independent of the proposed solution and provides actionable understanding for the community.
- **Consistent and substantial empirical gains.** Critique-RL achieves large improvements over all baselines across three in-domain datasets and two model scales (3B, 7B). For Qwen2.5-7B on MATH, it achieves 58.40% Acc@Refine vs. 53.86% for CTRL, with discriminability jumping from 71.42% to 85.20%. OOD results on SVAMP and TheoremQA similarly demonstrate meaningful gains (e.g., +4.6% on SVAMP for 7B over CTRL), supporting the generalization claim.
- **Thorough evaluation methodology.** The paper includes ablation studies isolating each stage's contribution, analysis with and without oracle verifiers to separately evaluate helpfulness, iterative training and refinement results, inference compute scaling experiments, and OOD generalization—all of which provide a comprehensive picture of the method's properties.
- **Clear practical relevance.** Training critique models without requiring stronger-model annotations for critique quality is an important scalable oversight problem. The approach uses only rule-based correctness verification (available for math tasks) rather than human or stronger-model labels for critiques, making it more practical to scale.

## Weaknesses
### Fatal
None.

### Major
- **Narrow task scope limits the generalizability claims.** All main experiments are on mathematical reasoning (MATH, GSM8K, AQuA, SVAMP, TheoremQA). The paper's abstract and framing position this as a general approach for "complex reasoning tasks" and "scalable oversight," yet the reliance on a rule-based oracle verifier `r_oracle` for both discriminability rewards and evaluation is specific to domains with verifiable answers. The CNN/DailyMail experiment is relegated to the appendix and the main paper provides no results for coding, logical reasoning, or other non-mathematical domains. This makes the broader claims about scalable oversight undersupported.
- **Oracle reward dependency deserves more honest framing.** The paper frames its contribution as training critique models "without stronger labeling," which is technically accurate (no stronger model annotates critiques). However, Stage I and Stage II both critically depend on `r_oracle`—a correctness verifier—during training. For math, this is a ground-truth answer check, which is a form of strong supervision. The paper should more clearly delineate what supervision is assumed and discuss how the method would extend to domains without such verifiers.

### Minor
- **Fixed actor limits analysis.** The actor is frozen throughout training. The paper does not discuss how Critique-RL interacts with an actor that is also being updated (e.g., in a fully online RL loop), which would be the natural next step for iterative self-improvement.
- **Hyperparameter sensitivity not reported.** Key choices—500 steps per stage, β₁=0.2, β₂=0.01 for KL, temperature 0.7 for sampling—are presented without sensitivity analysis. Given that the method involves a two-stage training procedure with multiple coefficients, understanding robustness to these choices would strengthen confidence.
- **AQuA results are relatively weak.** For Qwen2.5-7B on AQuA, Critique-RL's Δ is only +2.36, and several baselines show negative Δ (SFT: -3.94, STaR: -5.51). While the paper acknowledges this, the modest gains on this multiple-choice dataset suggest the method may be less effective when the task format differs from free-form math.

### Trivial
Some table entries inconsistently mark both best and second-best with bold+underline vs. just underline formatting.

## Nice-to-Haves
- Results on at least one non-mathematical reasoning domain (e.g., coding or scientific QA) in the main paper.
- A discussion of how the method extends to settings without a rule-based verifier, e.g., using learned reward models.
- Ablation on the number of training steps per stage and sensitivity to β₁, β₂.

## Novel Insights
The paper's most novel observation is that indirect outcome-based RL rewards (refinement correctness, correction rewards, or their difference) jointly fail to optimize discriminability: they can improve judgment for one response class (correct or incorrect) while degrading it for the other, leading to behavioral collapse into overly conservative or overly aggressive modes. This is a genuine diagnostic insight that explains the underperformance of prior RL-for-critique methods and motivates the decoupled two-stage optimization. The finding that discriminability and helpfulness, while partially coupled, benefit from staged optimization with explicit regularization is a useful contribution to the understanding of multi-objective RL for LLM critique training.

## Suggestions
- Add at least one non-math domain (e.g., code generation with unit test verification, or factual QA with retrieval-based verification) in the main paper to substantiate the scalable oversight claims.
- Include a brief discussion of limitations regarding the dependency on `r_oracle` and the fixed actor assumption, along with potential directions for addressing these.
- Report sensitivity to key hyperparameters (β₁, number of training steps per stage) to aid reproducibility.

## Score and Decision
This paper presents a well-motivated and well-executed contribution: the analysis of why indirect rewards fail for critique model RL is insightful, the two-stage solution is clean and effective, and the experiments are comprehensive within the mathematical reasoning domain. However, the narrow task scope and the unaddressed dependency on oracle verifiers during training limit the breadth of the contribution. The paper is a solid methodological advance for math reasoning critique models but falls short of fully substantiating its broader framing around scalable oversight. This warrants a borderline accept.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>
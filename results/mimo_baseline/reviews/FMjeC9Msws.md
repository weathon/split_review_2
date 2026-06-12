## Summary

This paper presents the first large-scale systematic study (400,000+ GPU-hours) of scaling reinforcement learning compute for LLMs. The authors propose a sigmoidal compute-performance framework to predict RL training trajectories, conduct comprehensive ablations of design choices (loss type, precision, aggregation, normalization, off-policy setup, curriculum), and consolidate the best options into a practical recipe called SCALERL. They validate predictable scaling by extrapolating from smaller runs to a 100,000 GPU-hour training run, demonstrating that performance closely matches predictions.

## Strengths

- **Genuine and important research gap addressed.** While pre-training has well-established scaling methodologies, RL for LLMs lacks any principled framework for predicting how performance scales with compute. This paper fills that gap with a concrete, validated framework. The practical value is enormous—enabling researchers to evaluate RL methods cheaply at small scale and predict large-scale behavior.

- **Massive, rigorous empirical study.** The 400,000+ GPU-hour ablation budget, with individual runs up to 16,000 GPU-hours and a final validation run at 100,000 GPU-hours, is exceptionally thorough. The leave-one-out ablation design (Figure 5) is well-structured to validate that each component contributes positively even in combination. The extrapolation from 50k to 100k GPU-hours (Figure 1) closely matching actual training is a compelling validation of the predictive framework.

- **Clear and actionable scientific framework.** The decomposition of RL performance into asymptotic reward (A) and compute efficiency (B) via the sigmoidal fit (Equation 1) provides a clean, interpretable lens for comparing methods. Figure 2's cross-recipe comparison, showing that methods appearing superior at small compute can be overtaken at larger budgets, is a powerful illustration of why scaling analysis matters.

- **Practical recipe with state-of-the-art results.** SCALERL outperforms all compared methods (DeepSeek GRPO, Qwen DAPO, Magistral, MiniMax) in both asymptotic performance and compute efficiency. The recipe is validated across multiple axes—model size (8B dense to 17B×16 MoE), sequence length (14k to 32k tokens), batch size, and multi-task RL—demonstrating robustness.

## Weaknesses

### Fatal
None.

### Major

- **Limited analysis of when and why the sigmoidal framework breaks down.** The paper demonstrates that the sigmoidal fit works well for stable recipes, but provides limited insight into the failure modes. For instance, the DeepSeek GRPO recipe in Figure 2 shows a notably poor fit (B=1.17), and the paper mentions that some experimental choices "destabilize beyond 3.5k-4k GPU-hours" (Appendix A.16 reference), but the conditions under which predictability fails are not systematically characterized. Understanding the boundary conditions of the framework would significantly strengthen the scientific contribution.

- **Domain generality is not established.** The primary experiments are on verifiable math tasks. While the authors briefly show multi-task RL with math and code (Figure 16 reference), the predictive framework's applicability to domains with different reward structures (e.g., open-ended generation, RLHF with learned reward models, agentic tasks) remains unknown. The sigmoidal fit's validity likely depends on properties of the reward signal that are not analyzed.

### Minor

- **The choice of sigmoidal over power-law is empirically motivated but lacks theoretical grounding.** The authors state the sigmoidal fit is "more robust and stable" than power law (Appendix A.4 reference), but a brief analysis of *why* RL performance should saturate (unlike pre-training loss) would strengthen the framework. The connection to bounded metrics (accuracy ∈ [0,1]) is mentioned but not deeply explored.

- **Cross-recipe comparison fairness.** In Figure 2, the compared methods (DeepSeek GRPO, Qwen DAPO, Magistral, MiniMax) were likely tuned for their own settings. The comparison assumes a fixed model and data distribution, which is methodologically clean but may not reflect each method's intended operating regime.

- **The 2× extrapolation range, while validated, is modest.** Extrapolating from 50k to 100k GPU-hours is a 2× factor. For the framework to be truly transformative for planning, demonstrating reliable extrapolation at 5-10× would be more compelling, though understandably expensive.

### Trivial
None.

## Nice-to-Haves

- A theoretical or mechanistic explanation for why certain design choices affect asymptotic performance (A) while others primarily affect efficiency (B). The empirical observation is clear, but understanding the underlying dynamics would elevate the scientific contribution.
- Analysis of how the sigmoidal parameters (A, B, C_mid) vary with model size, potentially enabling cross-model-scale predictions analogous to Chinchilla scaling laws.
- Sensitivity analysis of the sigmoidal fit to the number and placement of evaluation points used for fitting.

## Novel Insights

The paper's most novel insight is the decomposition of RL design choices into those that shift the asymptotic ceiling (A) versus those that modulate compute efficiency (B). The finding that FP32 precision at the LM head is one of the single largest contributors to asymptotic performance (A: 0.52 → 0.61) is surprising and practically important—it suggests that numerical precision mismatches between generator and trainer are a fundamental bottleneck that has been underappreciated. Similarly, the observation that common interventions like loss aggregation, advantage normalization, and curriculum primarily affect efficiency rather than ceiling performance provides a principled way to prioritize design decisions: first secure a high ceiling, then optimize efficiency. The cross-recipe comparison showing that methods appearing superior at small compute can be inferior at large compute (the "bitter lesson" for RL) is a cautionary finding with broad implications for how the community evaluates RL methods.

## Suggestions

- Add a brief theoretical discussion of why RL performance saturates (bounded reward) versus pre-training (unbounded loss reduction), to motivate the sigmoidal choice beyond empirical fit quality.
- Include a "scaling law table" summarizing fitted (A, B, C_mid) for all major ablation conditions in one place, as a reference for practitioners.
- Discuss the minimum number of evaluation points and compute range needed for reliable curve fitting, as this is critical for the practical utility of the framework.

## Score and Decision

This paper makes a significant and timely contribution by establishing the first predictive scaling framework for RL training of LLMs. The empirical study is exceptionally thorough (400k+ GPU-hours), the methodology is sound and well-validated, and the practical recipe (SCALERL) achieves state-of-the-art results. The key intellectual contribution—decomposing RL performance into asymptotic ceiling and compute efficiency, and showing these can be predicted from small-scale runs—addresses a genuine gap in the field. The major weaknesses (limited failure mode analysis, domain generality) are reasonable limitations for a first study of this scope and do not invalidate the core claims.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: Accept
## Summary

This paper presents a large-scale empirical study (400,000+ GPU-hours) investigating how reinforcement learning compute scales for LLM post-training. The authors propose a sigmoidal compute-performance curve that enables predictive extrapolation of RL performance from smaller-scale runs to much larger compute budgets. They systematically ablate numerous design choices (loss functions, precision, advantage normalization, curriculum, etc.), characterizing each in terms of asymptotic performance (A) and compute efficiency (B). From these insights, they construct SCALERL, a recipe that scales predictably to 100,000 GPU-hours and outperforms established baselines like GRPO and DAPO. The work provides both a scientific framework for analyzing RL scaling and a practical recipe demonstrating that predictable RL scaling is achievable.

## Strengths

- **Massive scale and systematic methodology**: The study is conducted at an unprecedented scale (400,000+ GPU-hours for ablations, 100,000 GPU-hours for the flagship run), enabling robust conclusions about scaling behavior that smaller studies cannot reach. This scale is a genuine contribution to the community.
- **Principled predictive framework**: The sigmoidal scaling law (Equation 1) with interpretable parameters (asymptotic reward A, compute efficiency B, midpoint C_mid) provides a rigorous, falsifiable methodology for predicting RL scaling. The authors validate its predictive power by fitting on early training and successfully extrapolating to much longer runs (Figures 1, 5), which is a strong demonstration.
- **Comprehensive ablation study with clear structure**: The paper systematically evaluates loss types, off-policy setups, precision fixes, loss aggregation, advantage normalization, and curriculum strategies, each characterized by its effect on A and B. This categorization (asymptotic vs. efficiency) is a valuable conceptual contribution that clarifies which design choices actually move the ceiling versus merely accelerating convergence.
- **Leave-one-out validation**: The LOO experiments (Figure 5) are a rigorous way to verify that each component contributes positively even when combined, avoiding common pitfalls of additive design. The transformation to a power-law plot to highlight efficiency differences is clever and insightful.
- **Generalization across scaling axes**: The paper demonstrates that SCALERL's predictiveness holds when scaling model size (8B to 17Bx16 MoE), generation length (14k to 32k tokens), batch size, and tasks (math + code). This multi-axis validation substantially strengthens the claim of general predictable scaling.

## Weaknesses

### Major

1. **In-distribution validation as the primary metric**: The scaling curves are fit exclusively on held-out in-distribution (IID) validation data from the same distribution as training prompts. While this follows pre-training scaling law methodology, RL's value proposition is generalization to out-of-distribution reasoning tasks. The paper acknowledges this limitation but does not provide a systematic study of how IID predictive scaling relates to downstream generalization. Figure 1(b) shows AIME-24 scaling for SCALERL, but this is only for the final recipe, not for the ablations used to derive design choices. Without this mapping, the framework's utility for guiding real-world RL development is uncertain—a method that scales predictably on IID but poorly on held-out tasks would be of limited practical value.

2. **Limited downstream evaluation for ablations**: The core ablations (Section 3) are evaluated almost entirely on IID validation pass rate. Critical design choices like FP32 precision, loss type (CISPO vs. DAPO), and curriculum are selected based on IID asymptotics. However, downstream evaluation (AIME-24, MATH-500, etc.) is only reported for the final SCALERL recipe and a few scaling experiments. It is plausible that choices favoring IID asymptotics could hurt generalization, or that the rank ordering of methods on IID might differ from the rank ordering on downstream tasks. The paper would be substantially stronger if it showed that the key design choices (at minimum, loss type, precision fix, and curriculum) maintain their relative ordering on held-out benchmarks.

3. **Absence of compute budget accounting for generation vs. training**: The scaling curves use GPU-hours as the sole compute metric, but the ratio of generation compute to training compute can vary dramatically across methods (e.g., PipelineRL vs. PPO-off-policy). The paper notes that PipelineRL improves efficiency by reducing idle time (Figure 4a), but the raw GPU-hours metric conflates actual computation with idle time. For a recipe comparison, this is acceptable, but for predicting how a method will scale when generation/training ratios change (e.g., with longer sequences or larger models), a more detailed compute breakdown would be valuable. The comparison in Figure 2 could be affected by different generation-to-training compute ratios across methods.

4. **Reproducibility and hyperparameter transparency**: The paper states that hyperparameters are in Appendix A.3 (removed), so I cannot assess reproducibility. The described recipe involves multiple interacting components (interruption phrase, specific clipping thresholds, batch-level normalization, zero-variance filtering, No-Positive-Resampling threshold of 0.9), and the sensitivity to these specific choices is not explored beyond the LOO experiments. The "sigmoid fit excludes very early low-compute regime" procedure (starting at ~1.5k GPU hours) introduces subjectivity; the paper should specify whether this threshold was fixed in advance or tuned per-run to improve fit quality.

### Minor

- The paper claims SCALERL achieves "state-of-the-art" but this is based on comparison with re-implementations of baselines (DeepSeek GRPO, Qwen DAPO, etc.) from the literature. It is unclear whether these baselines were tuned optimally for the 8B setting. The paper would benefit from stating whether the baselines' hyperparameters were taken from their original papers or tuned on this setup.
- The "bitter lesson" claim (methods superior at small compute can be worse at large compute) is supported by Figure 2, but the paper does not identify which specific methods exhibit this cross-over or quantify the reversal. The statement would be more impactful with concrete examples from the ablation study.
- The multi-task RL experiment (math + code) is mentioned only briefly (Figure 16, Appendix), but this is a practically important direction. A more detailed analysis would strengthen the paper's generality claims.

### Trivial

- Figure captions are overly long (e.g., Figure 1 caption repeats information from the body verbatim). This is a stylistic preference, not a substantive flaw.

## Nice-to-Haves

- A systematic study of how IID validation scaling curves correlate with downstream task performance across different methods, not just for the final recipe.
- A compute breakdown (generation vs. training vs. idle GPU-hours) for the different asynchronous RL setups to help practitioners reason about cost allocation.
- Sensitivity analysis for the sigmoid fit exclusion threshold (the ~1.5k GPU-hour cutoff) to show the method's robustness to this choice.
- Ablation of the specific interruption phrase and comparison with alternative interruption strategies.

## Novel Insights

The paper's central novel insight is that RL compute for LLMs follows a predictable sigmoidal scaling law when evaluated on in-distribution validation, characterized by an asymptotic ceiling (A) and a compute efficiency exponent (B). This framing allows researchers to decouple two fundamentally distinct properties of an RL recipe: how good it could ultimately be (A) versus how fast it gets there (B). The empirical finding that many common interventions (loss aggregation, advantage normalization, curriculum) primarily modulate B rather than A is nontrivial and practically useful—it suggests that ceiling-raising innovations are rarer and harder to find than efficiency improvements. The demonstration that off-policy algorithm choice (PipelineRL vs. PPO-off-policy) and model precision affect the ceiling (A) more than efficiency is similarly insightful. This framework positions RL scaling research on a more scientific footing, analogous to how scaling laws transformed pre-training research from art to engineering.

## Suggestions

1. Add downstream evaluation (at minimum AIME-24 and MATH-500) for the key ablations in Section 3 (loss type, FP32 precision, curriculum) to validate that the asymptotic ceiling A on IID data corresponds to genuine performance gains on held-out tasks. Without this, practitioners cannot trust that optimizing for IID asymptotics is the right objective.

2. Provide a detailed compute breakdown (GPU-hours for generation, training, and idle) for the different asynchronous RL setups (PPO-off-policy-k vs. PipelineRL-k) to clarify how much of the "efficiency" gain is from reduced idle time versus fundamentally better sample efficiency.

3. Specify the exact fitting procedure more precisely: (a) whether the exclusion threshold for early training points is fixed or tuned per-run, (b) the optimization algorithm used for fitting (e.g., least squares on which loss), (c) confidence intervals or standard errors on the fitted A and B parameters, and (d) the number of fitting points used. This would enable others to reproduce the fitting methodology exactly.

4. Include a plot showing the extrapolation quality (predicted vs. actual pass rate) across all LOO experiments as a correlation scatter plot, to quantify the predictive performance of the framework rather than showing only the best-case curves.

## Score and Decision

This paper makes a substantial contribution to the emerging field of RL scaling for LLMs. The scale of the empirical study, the clarity of the proposed framework, and the demonstration of predictable scaling to 100,000 GPU-hours are impressive. The weaknesses—primarily the reliance on in-distribution validation without systematic validation of downstream generalization relevance—are significant but not fatal; they point toward natural future work rather than invalidating the core contribution. The paper is likely to influence how the community evaluates and develops RL recipes, which is the hallmark of an ICLR-worthy contribution.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>
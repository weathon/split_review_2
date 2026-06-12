## Summary
The paper proposes Steady Thought (ST), a thought-level preference optimization framework that mitigates the "under-thinking" problem in Large Reasoning Models, where models excessively switch between reasoning thoughts without deeply exploring promising ones. ST segments model responses into thoughts via entropy-based detection, generates completions of promising thoughts, and trains the model using a novel STPO objective to prefer completing viable thoughts over wasteful switching. Experiments across three model scales (1.5B, 8B, 14B) and four benchmarks show accuracy improvements up to 5.3% with 19–39% token reductions.

## Strengths
- **Well-identified and formalized problem**: The paper convincingly motivates under-thinking with Figures 1a/1b, showing models often discover correct thoughts early yet continue switching. The formalization as a preference optimization problem (Section 2.1, commit vs. switch trajectories) provides a clean conceptual framework.
- **Principled approach over crude suppression**: Unlike prior work that globally suppresses switching tokens or representations, ST's thought-level preference optimization teaches the model *when* to commit and when to switch. This is a meaningful conceptual advance. The empirical finding that smaller models on harder problems can *increase* thought switches while improving accuracy (Section 4.4.1) validates this nuance.
- **Comprehensive and convincing experimental evaluation**: Three model families, four benchmarks (including OOD LiveCode trained exclusively on math data), and three competitive baselines (NoThink, NOWAIT, SEAL). OOD generalization on LiveCode (e.g., Qwen3-8B: +5.3% accuracy, −19% tokens) strongly suggests the method teaches general reasoning patterns rather than memorization.
- **Thorough ablation studies**: Analyses of entropy thresholds (Table 3), training method comparison (Table 4: SFT vs. DPO vs. STPO), thought-switching behavior (Table 2), and in-depth exploration metrics (Figure 2) collectively build a persuasive case.

## Weaknesses
### Fatal
None.

### Major
- **Model-specific entropy threshold tuning**: The entropy threshold is critical to segmentation quality yet determined per-model via hyperparameter search (Section 4.4.3). Table 3 only shows results for the 1.5B model in the main text. This raises scalability and reproducibility concerns: how sensitive is the method to threshold choice, and how much tuning effort is needed for new models?
- **NOWAIT baseline anomaly on Qwen3-8B**: NOWAIT increases tokens by 84.6% and drops accuracy by 21.2% on Qwen3-8B (Table 1), which is highly unusual for a method designed to reduce switching. If this baseline is underperforming due to implementation issues, the comparison fairness for other methods on this model is questionable. This warrants explanation or verification.
- **Incomplete baseline coverage**: The paper does not compare against recent RL-based approaches for controlling reasoning depth (e.g., approaches that train with verifiable rewards to adjust compute), nor against methods like DeepConf. Given the rapidly evolving landscape, the baseline selection could be more comprehensive.

### Minor
- **Missing training data construction details**: The paper uses omni-math but does not specify the number of problems sampled, difficulty distribution, total preference pairs generated, or any filtering criteria. This limits reproducibility.
- **Computational overhead not quantified**: The thought completion stage requires running inference for each segmented thought, potentially multiplying training-time compute. The paper defers this to Appendix E, but a brief summary in the main text would help practitioners assess practicality.
- **Diminishing gains at scale**: Accuracy improvements trend downward with model size (1.5B: +1.9%, 8B: +3.12%, 14B: +2.52%), while the 8B model gains more than the 14B. Whether this reflects saturation or noise is unclear, and experiments on a 70B+ model would strengthen the scalability argument.

### Trivial
None.

## Nice-to-Haves
- Error analysis on problems where ST reduces accuracy: does the model sometimes over-commit to a wrong thought?
- Analysis of how many thought completions are generated per problem during training and the associated compute cost.
- Comparison with methods that dynamically allocate thinking budget based on question difficulty.

## Novel Insights
The paper's key insight is reframing under-thinking mitigation from "suppress switching globally" to "teach the model when to commit." By constructing thought-level preference pairs where completing a promising thought is preferred over switching, the method avoids the over-correction of blanket suppression. The empirical observation that ST can *increase* the number of thought switches for small models on hard problems while simultaneously improving accuracy and reducing length is genuinely interesting—it demonstrates the method teaches *better* switching strategy, not merely *less* switching.

## Suggestions
- Report the number of training problems, preference pairs, and training compute in the main text for reproducibility.
- Investigate and explain the NOWAIT baseline's anomalous behavior on Qwen3-8B.
- Include at least one larger-scale model (e.g., 32B or 70B) to demonstrate scalability.
- Add a brief ablation on whether the thought completion generation (logit suppression of trigger words) is essential vs. simply generating completions without suppression.

## Score and Decision
The paper addresses a timely and practically important problem with a well-motivated, coherent framework. The experimental evaluation is comprehensive across models and datasets, with strong OOD results. However, the reliance on per-model threshold tuning, some baseline concerns, and missing training details temper enthusiasm. The contribution is genuine and useful but would benefit from additional rigor and scale.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: Accept
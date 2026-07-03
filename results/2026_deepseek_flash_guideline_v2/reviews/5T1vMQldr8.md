Now let me produce the final review.

## Summary

SPOT proposes a framework for offline preference-based RL that addresses reward model extrapolation errors by extracting "subgoals" — critical states within preferred trajectories identified via attention weights from a Preference Transformer. A CVAE learns to generate contextually appropriate subgoals for unlabeled data, and rewards are shaped via cosine similarity between predicted subgoals and next states, constraining the policy toward training-distribution regions. The paper achieves the best average performance (78.82) across 10 tasks from D4RL, Robosuite, and Meta-World, outperforming the next-best baseline (PT at 74.76).

## Strengths

1. **Novel and well-motivated idea.** Using attention weights from the Preference Transformer to identify subgoals in preferred trajectories, then employing those subgoals for reward shaping to reduce extrapolation error, is conceptually clean and addresses a real problem in offline PbRL. The pipeline (attention-based identification → dual-criteria filtering → CVAE generation → cosine-similarity shaping) is logically coherent.

2. **Top-K% ablation validates the subgoal selection mechanism.** Table 2 shows a monotonic hierarchy (Top 10% > Top 10–20% > Bottom 10–20% > Bottom 10%) across two tasks, with performance dropping from 99.37 to 55.24 on hopper-medium-expert. This provides direct evidence that attention-weighted subgoal selection, not a confound, drives the performance gains.

3. **Direct extrapolation error evidence.** Figure 2b compares SPOT vs PT in OOD settings across the same similarity measure. SPOT's extrapolation error is substantially lower across all similarity ranges (~0.98 vs ~1.22 at low similarity, ~0.45 vs ~0.85 at high similarity), providing quantitative evidence that the subgoal-shaped reward reduces the target error.

4. **Best average performance.** Across 10 diverse tasks, SPOT achieves the highest mean score (78.82 vs next-best PT at 74.76) with reduced average standard deviation (7.76 vs PT's 13.80), suggesting aggregate benefits from the subgoal guidance.

## Weaknesses

### Fatal
None.

### Major

1. **Empirical claims are substantially oversold relative to the data.** The paper states (Section 5.1) that Table 1 "confirms the consistent superiority of our approach across multiple benchmarks" and that SPOT "achieves state-of-the-art performance on both hopper medium-replay and medium-expert datasets." These claims are contradicted by the paper's own table. SPOT wins outright on 3 of 10 tasks (walker2d-medium-replay, can-mh, plate-slide). On hopper-medium-replay, DTR (94.18) far exceeds SPOT (85.08). On hopper-medium-expert, DTR (102.12) beats SPOT (98.73). On lift-mh, MR (95.62) more than doubles SPOT (65.17). The paper would be more credible if it accurately described its results — "competitive average performance with best average" — rather than claiming dominance on individual tasks where the method is clearly not state-of-the-art. No statistical significance is provided for the average advantage, which matters given the high variances in many baselines.

2. **The "query efficiency" experiment (Section 5.5) is undefined.** The paper varies "query number" across values {30, 50, 100, 500} and calls this "query length," "query number," and "query efficiency" interchangeably, but never defines what a "query" refers to. In PbRL, "query" typically means a human preference query; but the values 30–500 and the environment-dependent variations are not explained. Without a definition, the experiment is uninterpretable and non-reproducible. Additionally, SPOT's variance at 100 queries on hopper (99.37±8.35) is dramatically higher than PT's (76.21±1.74), undermining the text's claim of "stability."

3. **The CVAE — central to the method — receives no quantitative evaluation.** The CVAE is the mechanism that generates subgoals for unlabeled data. Yet the paper provides no reconstruction error (ELBO or MSE on held-out subgoals), no latent-space analysis, and no ablation that replaces the CVAE with ground-truth subgoal retrieval. The only validation is a qualitative case study (Figure 3). Without this, it is unclear whether the CVAE is learning meaningful structure or simply memorizing training data.

### Minor

1. **Partial circularity in extrapolation error analysis (Figure 2).** The x-axis measures cosine similarity between the predicted subgoal and the current state — which is *exactly* the metric SPOT uses for its shaping reward (Equation 11). Showing that SPOT has lower extrapolation error on states similar to its own predicted subgoals is partially testing the method's own objective. A more convincing analysis would use an independent distributional proximity measure (e.g., density estimation or L2 distance to nearest training state). This does not invalidate the result but weakens its force.

2. **Large variance in several ablation results.** Table 3 shows many cosine similarity results with ±30–52 standard deviation (e.g., cosine similarity at λ=0.5 on hopper: 63.89±51.95). The Top-K% ablation (Table 2) uses only 3 seeds with variances as high as ±39.12. These high variances make it difficult to draw robust conclusions from individual comparisons.

3. **Selection bias concern with hyperparameter choices.** The Top-10% setting (selected via ablation on hopper-medium-expert and can-mh) is used in the main results on those same environments. Similarly, λ=1.0 is used in the main experiments but the ablation shows it is only clearly superior for cosine similarity at that exact value. The choices are reasonable but should be discussed as tuned, not canonical.

### Trivial
- Missing implementation details: CVAE architecture (layers, hidden dimensions, latent size), training hyperparameters (learning rate, optimizer, batch size), IQL hyperparameters (expectile τ, temperature).
- No runtime or computational cost comparison.

## Nice-to-Haves
- Ablation replacing the CVAE with nearest-neighbor retrieval of ground-truth subgoals to test whether the generative model is necessary.
- Supplement Figure 2 with an analysis using a distributional proximity measure independent of SPOT's shaping objective.
- Statistical significance test (e.g., paired bootstrap) for the average-score comparison.

## Removed Points

- **"Suspicious results in reward shaping ablation"** (negative distance at λ=0.5/1.0 on walker2d producing near-zero scores). Removed because negative distances can produce unbounded negative values that dominate the reward — the paper's stated explanation ("sensitivity to weight selection with instability") is sufficient; this is a known property of negative-distance shaping, not a bug.

- **"Dual-criteria filtering uses non-independent criteria."** Removed because attention weights and reward values coming from the same model is standard — they serve as corroborating signals, not independent sources. This is not a flaw.

- **"Framing of 'overlooking' information is unfair to reward-free methods."** Removed — this is a rhetorical preference, not a technical weakness.

- **"Strength: query efficiency advantage."** Demoted from strength to neutral because the undefined terminology (what is a "query"?) makes the evidence unreliable. The underlying data in Table 4 is reported; readers can draw their own conclusions once the variable is clarified.

- **"Strength: qualitative case study shows forward-looking subgoals."** Kept in modified form — the case study is included as supporting qualitative evidence, but the missing quantitative CVAE evaluation is noted as a weakness.

## Novel Insights

None beyond the paper's own contributions. The two reviewer inputs did not surface any fundamentally new perspective on the paper that its authors had not already articulated.

## Suggestions

1. **Recalibrate all empirical claims to match the evidence.** Do not claim "consistent superiority" on benchmarks where SPOT is clearly not the best. Frame the contribution honestly: SPOT achieves the best average performance with particular strength on walker2d-medium-replay, can-mh, and plate-slide, while being competitive on several other tasks.

2. **Define the query efficiency experiment.** State precisely what "query" means, how the values were chosen, and why they differ per environment. If the variable is trajectory segment length, rename the experiment accordingly.

3. **Add quantitative CVAE evaluation.** Report held-out reconstruction error (ELBO, MSE). Ideally include an ablation that replaces the CVAE with nearest-neighbor ground-truth subgoal retrieval.

4. **Supplement the extrapolation error analysis** with a distributional proximity measure independent of SPOT's cosine-similarity objective (e.g., distance to nearest training trajectory state).

5. **Add implementation details** (CVAE architecture, training hyperparameters) to improve reproducibility.

## Score and Decision

**Calibration note:** The calibration search tool was unavailable due to a file system error. I therefore calibrated against my knowledge of the ICLR 2026 reviewing conventions. A paper with a genuinely novel and well-motivated idea, best average performance across 10 tasks, and a clean ablation study, but with oversold claims, an undefined experiment, and missing evaluation of a core component — this fits the profile of a borderline accept (6) that requires significant revision. The issues are fixable and do not invalidate the core contribution.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>
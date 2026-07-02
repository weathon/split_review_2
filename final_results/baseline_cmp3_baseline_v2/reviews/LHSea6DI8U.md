## Summary
This paper proposes STBP, a framework for continual spatio-temporal forecasting that combines a general spatio-temporal backbone with a scalable contextual pattern bank. The backbone uses frequency-domain processing to extract stable representations and linear graph attention for efficient dynamic spatial modeling, while the pattern bank is incrementally expanded to capture evolving node-level patterns and mitigate catastrophic forgetting. Experiments on three real-world streaming datasets show STBP outperforms existing continual and non-continual forecasting methods in accuracy, scalability, and few-shot settings.

## Strengths
- **Strong empirical results**: STBP achieves substantial improvements over state-of-the-art baselines, with MAE reductions of 21.44% and 21.93% on PEMS-Stream and CA-Stream respectively, and consistent gains across all three datasets and multiple metrics.
- **Well-motivated problem framing**: The paper clearly identifies four key challenges for continual spatio-temporal forecasting (distributional drift, dynamic spatio-temporal correlations, catastrophic forgetting, and efficient incremental strategy) and designs components that directly address each.
- **Novel technical integration**: The combination of frequency-domain processing for stable representations, linear graph attention for efficiency, and a prompt-based contextual pattern bank for continual adaptation is a coherent and well-engineered solution.
- **Comprehensive evaluation**: Experiments cover main results, few-shot settings, ablation studies, parameter sensitivity, case studies, and efficiency analysis across three real-world datasets, providing strong evidence for the claims.

## Weaknesses

### Fatal
None.

### Major
- **Missing standard deviations for STBP in Table 1**: The main results table reports standard deviations for all baselines but does not report standard deviations for STBP. This makes it impossible to assess the statistical significance of the reported improvements. Given that some gains (e.g., 2.35% on AIR-Stream) are modest, the lack of variance information is a significant omission.
- **Incomplete reporting of baseline results in Table 1**: The table shows empty cells for STBP's results across all metrics and horizons, with only the "Avg." row filled. This is a critical reporting error that prevents the reader from verifying the per-horizon performance and undermines the credibility of the results.
- **Missing details on the continual learning protocol**: The paper does not specify how many incremental periods exist in each dataset, how nodes are added across periods, or the exact training procedure (e.g., number of epochs per period, learning rate schedule, early stopping criteria). Without this information, the experimental setup is not reproducible.

### Minor
- **Limited novelty of individual components**: While the overall framework is well-engineered, the individual components (frequency-domain processing, linear attention, prompt-based pattern banks) are each adapted from existing work. The novelty lies primarily in their integration for the CSTF setting rather than in any single component.
- **The "general" claim is somewhat overstated**: The backbone is designed for spatio-temporal forecasting and relies on specific architectural choices (FreNet, DLGA) that are not truly architecture-agnostic. The term "general" primarily means node-count independent and adjacency-matrix-free, which is a reasonable but narrower claim.
- **AIR-Stream improvements are modest**: On the AIR-Stream dataset, STBP's average MAE improvement over the best baseline is only 2.35%, and for some horizons (e.g., horizon 12 RMSE), STBP is not the best. This weakens the claim of universal superiority.

### Trivial
- The paper uses "STD" in Figure 8 legend but the model is called "STID" in the text; this appears to be a typo.

## Nice-to-Haves
- A discussion of how the number of incremental periods and the size of node additions per period affect performance would strengthen the analysis.
- An analysis of the computational cost of the pattern bank expansion (e.g., how the number of parameters grows with nodes) would be useful for practitioners.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
- Report standard deviations for STBP in Table 1 to allow statistical comparison with baselines.
- Fill in the missing per-horizon results for STBP in Table 1.
- Provide a clear description of the continual learning protocol: number of incremental periods, how nodes are added per period, training epochs per period, learning rate schedule, and early stopping criteria.
- Clarify whether the "Retrain" and "Online" baselines use the same backbone architecture as STBP or a different one, and justify the choice.

## Score and Decision
The paper presents a well-engineered solution to an important problem (continual spatio-temporal forecasting) with strong empirical results. The main weaknesses are reporting issues (missing standard deviations and incomplete results in Table 1) and insufficient experimental protocol details, which are fixable but currently undermine reproducibility and confidence. The technical contribution is solid but incremental—combining known components (frequency-domain processing, linear attention, prompt-based pattern banks) in a novel way for the CSTF setting. The improvements on two of three datasets are substantial, though the AIR-Stream gains are modest. Overall, the paper is above the acceptance threshold but has clear reporting issues that need resolution.

**Score**: 6

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>
## Summary

This paper introduces VisualPRM400K, the first large-scale multimodal process supervision dataset (~400K samples) for training Process Reward Models (PRMs) in multimodal reasoning. Building on this dataset, the authors develop VisualPRM, an 8B-parameter multimodal PRM that serves as a critic for Best-of-N (BoN) test-time scaling, consistently improving reasoning performance across multiple MLLM families (MiniCPM, QwenVL, InternVL) and scales (7B–78B) on seven multimodal reasoning benchmarks (up to +8.4 points). They also construct VisualProcessBench, a 2,866-sample benchmark with 26,950 human-annotated step-level correctness labels, to evaluate step-wise error detection capabilities of PRMs and MLLMs.

## Strengths

- **Timely and important problem:** The paper targets test-time scaling for multimodal LLMs, a largely unexplored area, and addresses the critical gap of lacking multimodal process supervision data and evaluation benchmarks.
- **Substantial resource contributions:** VisualPRM400K and VisualProcessBench are valuable assets for the community. The dataset scale (~400K samples, 2M steps) and the thoughtful benchmark construction (multi-source, human-annotated, all-errors detection) are significant.
- **Strong empirical results:** VisualPRM consistently improves performance across diverse policy models (7B to 78B) and seven reasoning benchmarks, with gains that are often substantial (e.g., +8.4 on InternVL2.5-8B, +6.3 on InternVL2.5-38B). The BoN experiments show PRMs outperforming Outcome Reward Models and Self-Consistency, with the gap widening at larger N.
- **Comprehensive ablations:** The paper systematically studies PRM modeling (value vs. advantage), score aggregation methods, early stopping, and compares against MLLM-as-judge baselines, providing useful design insights.

## Weaknesses

### Major

- **No human validation of training data labels:** The VisualPRM400K annotations are generated automatically via Monte Carlo sampling, and no human evaluation or agreement study is reported for the training set. Given that only ~10% of steps are labeled incorrect (a known issue from automatic pipelines), label noise may affect PRM quality. The paper mentions trying a threshold to reduce false positives (Appendix B) but does not quantify noise or validate against human judgments. A small-scale human evaluation of training labels would strengthen confidence.
- **Limited analysis of text-only improvement:** The model shows notable gains on text-only benchmarks (e.g., +6.1 on MATH-500 for Qwen2.5-7B), but the paper does not explain why a multimodal PRM (trained on multimodal data) transfers to text-only settings. This is interesting but warrants discussion about possible data contamination or general reasoning signals learned.

### Minor

- **VisualProcessBench size and coverage:** 2,866 samples is moderate. The benchmark covers five reasoning sources but does not include diverse domains like chart/table reasoning or scientific diagrams. While useful, it may not fully represent the breadth of multimodal reasoning.
- **BoN critic baselines limited:** In the BoN comparison, the only MLLM-as-critic baseline is InternVL2.5 (Table 4). Other strong critics like Qwen2.5-VL-72B or GPT-4o are not tested in the BoN setting, making the claim that "open-source MLLMs struggle as critic models" less strongly supported (though VisualProcessBench does show their weakness).
- **ORM comparison parity:** The ORM is trained on the same data but aggregated across steps, which may not be the most competitive ORM baseline (e.g., a larger reward model). The paper acknowledges this but does not explore alternative ORM designs.

### Trivial

- Figure 1 bar chart has duplicated entries and unclear x-axis labels in the caption (e.g., "InternVL2.5-8B" appears twice); the actual data table is informative but the figure could be cleaner.

## Nice-to-Haves

- A human-evaluation study on a subset of VisualPRM400K training labels (e.g., 200 samples) to quantify agreement with Monte Carlo annotations.
- Experiments with VisualPRM applied to online RL (e.g., PPO) to demonstrate utility beyond BoN evaluation.
- Release of the data construction pipeline code to facilitate reproducibility and dataset extension by the community.

## Novel Insights

None beyond the paper's own contributions: the paper's core value lies in the dataset, benchmark, and empirical demonstration that a multimodal PRM trained on automatically generated process supervision can effectively improve MLLM reasoning via test-time scaling. The observation that value-based PRMs outperform advantage-based PRMs under automatic labels, and that averaging step scores works better than max/min, are practical insights but not theoretically surprising.

## Suggestions

- Add a small-scale human validation study of training labels (e.g., 200–500 steps) to quantify the noise level in VisualPRM400K and justify the chosen binary threshold (mc_i > 0).
- Include a brief discussion of why the PRM transfers well to text-only tasks, and whether any text overlap between training and test sets could affect the results.
- Expand the BoN critic baselines to include at least one strong open-source MLLM (e.g., Qwen2.5-VL-72B) as a critic, to strengthen the claim that only a dedicated PRM works.
- Clarify how neutral steps are handled in VisualProcessBench evaluation (currently excluded) and whether the macro F1 definition is correctly reported as macro-averaged over classes rather than sources.

## Score and Decision

**Score:** 8  
**Decision:** Accept  

The paper makes a clear and significant contribution by introducing the first multimodal process supervision dataset, a strong PRM baseline, and a dedicated benchmark. The experiments are thorough, the results are convincing, and the resources will benefit future research. The weaknesses (lack of training label validation, limited BoN critic baselines) are manageable and do not undermine the core claims.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>
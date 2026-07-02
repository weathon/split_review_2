## Summary
Blueprint-Bench introduces a benchmark that evaluates spatial reasoning in AI systems by requiring them to convert apartment photographs into standardized 2D floor plans. The benchmark tests a diverse set of models including large language models, image generation models, and agent-based systems on a dataset of 50 apartments. Results show that current AI models perform at or below a random baseline and substantially below human performance, revealing a persistent blind spot in spatial intelligence even when the input modality (photographs) is well within the training distribution.

## Strengths
- **Novel cross-architecture evaluation framework**: Blueprint-Bench is the first benchmark to directly compare the spatial intelligence of LLMs, image generation models, and agent systems on the same task, enabling meaningful comparisons that were previously missing.
- **Well-motivated task design**: The task of converting photographs to floor plans genuinely requires spatial inference (room layout, connectivity, consistent scale) while using in-distribution inputs, making it a clean test of emergent spatial abilities.
- **Open-source and extensible**: The authors release the evaluation code and a sample of the dataset, maintain a public leaderboard, and accept community submissions—this encourages replication and further research.
- **Human baseline and random baseline**: Including both a human comparison and a random baseline provides essential context for interpreting model scores and highlights the size of the gap.

## Weaknesses
### Fatal
None.

### Major
1. **Small dataset (50 apartments) limits statistical power and generalizability**. The variability across floor plan layouts is large, and with only 50 examples, the conclusions about model capabilities may be sensitive to the specific selection of apartments. The standard deviations reported are substantial, yet no formal significance testing (e.g., bootstrap intervals or pairwise comparisons) is provided.

2. **The scoring algorithm conflates instruction-following with spatial intelligence**. The strict formatting rules (line width, exact colors, no furniture, etc.) mean that models producing spatially reasonable floor plans that slightly violate the rules are severely penalized or rendered unscoreable. The paper acknowledges this trade-off but does not quantify how much of the poor performance is due to spatial reasoning failures versus formatting failures. This undermines the claim that the benchmark isolates spatial intelligence.

3. **The human baseline is limited and potentially unfair to humans**. Human drawings were evaluated on only 12 apartments, and the scoring algorithm—which heavily weights size ranking and graph connectivity—may systematically disadvantage human-produced plans that are not perfectly standardized (e.g., slight variations in line placement). The paper notes that humans always got connectivity correct but were penalized for size ranking errors, suggesting the metric may not capture human spatial understanding faithfully.

4. **Random baseline calculation is not adequately explained**. It is stated as 0.279, but how exactly was it computed? Random floor plan generation (random graphs? random room counts? random placements?) needs to be specified to interpret whether models are truly “barely above random.” The lack of methodological detail here weakens one of the paper’s core claims.

5. **No comparison to specialized floor plan generation methods**. Blueprint-Bench is designed to test general spatial intelligence in models not specifically trained for floor plan creation. However, including a model trained end-to-end on floor plan reconstruction from photographs (e.g., using computer vision + graph prediction) would serve as a valuable sanity check on whether the task itself is feasible with current techniques and what an upper bound might look like.

### Minor
- Agent scaffolds are tested with only two systems (Codex CLI and Claude Code). The finding that iterative refinement does not help is interesting, but it may be specific to these scaffolds or the particular environment setup, not a general conclusion about the value of iterative reasoning.
- The selection of evaluated models is a bit dated for a 2026 paper (GPT-5, Claude Opus 4.1, etc.), but since the benchmark is designed to evolve, this is acceptable. However, the text mixes model names (e.g., “GPT-5” and “GPT-5 mini” appear, yet the figure legend occasionally mentions “GPT-6” for Codex—likely a typo).
- The paper would benefit from a more detailed ablation of the scoring metric weights (50% edge overlap, 20% degree correlation, etc.). The choice of weights appears somewhat arbitrary and should be justified or demonstrated to be robust.

### Trivial
None.

## Nice-to-Haves
- Include more diverse floor plan layouts (e.g., non-rectangular rooms, multiple stories) to test deeper spatial understanding.
- Consider an alternative evaluation that uses LLM-based extraction with careful prompting to incorporate room labels and shapes, as the authors mention they attempted but abandoned; a more systematic comparison could be informative.
- Provide confidence intervals or Bayesian hierarchical models to quantify uncertainty in model rankings given the small dataset.

## Novel Insights
Beyond the paper’s own contributions, the finding that iterative refinement agents (Claude Code) did not outperform single-pass LLMs is noteworthy. This suggests that the bottleneck is not in the ability to revise outputs but in the underlying spatial understanding derived from the input images—agents can look again, but they still cannot infer the correct layout. This points to a fundamental limitation in how current multimodal models represent and reason about 3D geometry from 2D photographs.

## Suggestions
- Clarify the random baseline definition and provide a justification for why the specific random graph generation procedure is appropriate.
- Conduct a human evaluation that allows humans to produce floor plans in the same standardized format (e.g., using a constrained drawing tool) to enable a fairer direct comparison with AI models.
- Report results with and without penalizing formatting violations, or provide a separate “format compliance score” to disentangle spatial reasoning from instruction following.
- Increase the dataset size in future iterations to at least a few hundred apartments to improve statistical reliability.

## Score and Decision
This paper proposes a creative and timely benchmark that targets a genuine gap in AI evaluation. The task is well-motivated and the cross-model comparison is novel. However, the small dataset size, the confound between instruction-following and spatial reasoning in the scoring metric, and the inadequate explanation of baselines prevent strong claims. The work is nonetheless of value to the community as a starting point for more rigorous spatial intelligence evaluation.

MY FINAL SCORE: <score>5.0</score>  
MY FINAL DECISION: <decision>Accept</decision>
## Summary
The paper introduces Blueprint-Bench, a benchmark that evaluates spatial reasoning in AI models by requiring them to convert apartment photographs into standardized 2D floor plans. The evaluation scores models on room connectivity graphs and size rankings, and the results show that nearly all tested LLMs, image generation models, and agent systems perform at or near a random baseline, while humans perform substantially better. The benchmark is designed to be model-agnostic and provides a numerical framework for comparing spatial intelligence across different model architectures.

## Strengths
- **Novel and practical task design**: Converting real apartment photos to floor plans is a concrete, visually grounded spatial reasoning task that is clearly within the training distribution of modern multimodal models yet requires genuine spatial inference. This makes the demonstrated blind spot more surprising and impactful than purely abstract benchmarks.
- **Cross-architecture comparison**: The benchmark is one of the first to compare LLMs, image generation models, and AI agents on the same spatial reasoning task, enabling insights into how different approaches (single-pass generation, iterative refinement) affect performance.
- **Well-defined automated scoring**: The two-stage extraction and scoring pipeline (connectivity graph + size ranking) is transparent, rule-based, and allows reproducible evaluation without human annotations once the floor plan follows the specified format.
- **Open-source framework and leaderboard**: I release the evaluation code and a data sample, and accept community submissions, which should facilitate future work and tracking of progress.

## Weaknesses
### Fatal
None.

### Major
1. **Small dataset size and incomplete human baseline**: The benchmark contains only 50 apartments, with a human baseline computed on just 12 of them. This limits the statistical reliability of the results and makes the human advantage less conclusive. A dataset of this size also risks high variance and reduces the benchmark’s ability to reliably rank models.
2. **Limited evaluation scope**: The scoring metric ignores room shapes, precise geometry, and room types (e.g., kitchen vs. bedroom). The paper acknowledges this but argues it is a necessary trade-off for robust automated scoring. However, this means the benchmark measures only a narrow slice of spatial intelligence—connectivity and relative size ordering—while missing critical aspects like layout accuracy and functional understanding. A model could produce a completely wrong floor plan shape and still score decently if the connectivity and size ranks are correct.
3. **Reproducibility concerns**: The majority of the dataset is kept private to prevent overfitting. While this is a common practice, it undermines the ability of other researchers to verify, extend, or build upon the benchmark without access to the full data. The paper does not provide a mechanism for controlled access or synthetic alternatives, limiting the benchmark’s immediate utility to the community.
4. **Confounding of instruction following with spatial reasoning**: The paper notes that some models (e.g., GPT-4o, NanoBanana) failed primarily due to poor instruction following rather than spatial reasoning per se. The strict formatting rules are necessary for scoring, but they make it difficult to disentangle whether low scores reflect a lack of spatial understanding or an inability to follow precise output specifications. This confound weakens the claim that the benchmark specifically measures spatial intelligence.

### Minor
1. **Unclear random baseline derivation**: The random baseline score (0.279) is mentioned but not fully explained. It is not obvious how random floor plans were generated or whether the baseline accounts for the distribution of possible connectivity graphs. More detail is needed to interpret whether models are truly above or below chance.
2. **Limited agent evaluation**: Only two agent scaffolds (Codex CLI and Claude Code) are tested, and the paper notes that Codex CLI did not iterate meaningfully. The conclusion that "iterative refinement through agents [shows] no advantages" is based on very limited evidence and may not generalize to other agent frameworks or prompting strategies.
3. **Human evaluation methodology sparse**: The paper states that a human drew floor plans from images in a folder, but does not describe the number of human subjects, their expertise, the time allowed, or whether multiple trials were conducted. This makes the human baseline less rigorous than it could be.
4. **Potential overclaim on generality**: The abstract and introduction claim the benchmark can compare spatial intelligence across “different model architectures,” but the evaluation is limited to connectivity and size rankings. Without metrics for shape, proportion, or room semantics, the benchmark does not fully capture spatial intelligence as commonly understood.

### Trivial
- Figure 7 labels error bars as “2.5 standard deviation”; standard deviation is typically reported as 1σ. If this is standard error or a different interval, it should be clarified.

## Nice-to-Haves
- Including additional metrics (e.g., IoU of room polygons, room-type accuracy via image segmentation) would make the benchmark a richer test of spatial intelligence.
- Providing a synthetic dataset (e.g., procedurally generated apartments) alongside the real data would improve reproducibility while still allowing privacy protection.
- Testing more agent frameworks or allowing multiple rounds of human-agent interaction could better assess whether iterative refinement can help.

## Novel Insights
None beyond the paper’s own contributions—the results confirm that current generalist AI models (including the latest LLMs and image generators) struggle substantially with converting visual scenes into accurate spatial representations, and that providing an agent loop does not automatically close the gap. This is a useful empirical finding, but not surprising given the well-known limitations of these models in grounded spatial reasoning.

## Suggestions
1. Increase the dataset to at least 200 apartments and collect human baselines on the full set to improve statistical power and credibility.
2. Release the full dataset under a controlled access agreement (e.g., academic use only) to enable full reproducibility while preventing overfitting.
3. Add a geometric similarity metric (e.g., Chamfer distance between room boundaries) as a complementary score, even if it is used only for analysis and not for the primary ranking.
4. Provide a more detailed random baseline generation procedure, and consider reporting chance-level performance on each individual apartment to make scores more interpretable.

## Score and Decision

MY FINAL SCORE: 4.5</score>
MY FINAL DECISION: Reject</decision>
## Summary
The paper introduces Blueprint-Bench, a benchmark that evaluates spatial reasoning by tasking AI models (LLMs, image generation models, and agents) with converting apartment photographs into standardized 2D floor plans. Using a scoring algorithm based on room connectivity graphs and size rankings across 50 apartments, the authors find that most models perform at or below a random baseline and substantially below human performance, suggesting a significant blind spot in current AI spatial intelligence.

## Strengths
- **Novel and well-motivated benchmark concept**: The task of converting real apartment photographs into 2D floor plans is an intuitive yet genuinely challenging spatial reasoning task. The paper compellingly argues that while photographs are well within model training distributions, spatial reconstruction requires capabilities (inference of room layouts, connectivity, and consistent scale) that go beyond pattern matching. The analogy to ARC is well drawn.
- **Cross-architecture evaluation framework**: To my knowledge, this is the first benchmark that evaluates LLMs, image generation models, and agent systems on the same spatial task, enabling meaningful cross-paradigm comparisons. The finding that image generation models' emerging "intelligence" lacks numerical benchmarking is a real gap in the literature that this paper addresses.
- **Standardized format for robust automated scoring**: The 9 formatting rules for floor plan output (black walls, green doors, red room dots, etc.) are well-designed to enable deterministic computer vision-based extraction, removing subjectivity from the scoring pipeline. This is a pragmatic engineering choice that makes the benchmark reproducible.
- **Open-source with leaderboard**: The authors release code and a sample dataset while keeping most data private to prevent overfitting—a sound approach for a benchmark meant to track progress over time.
- **Insightful qualitative analysis**: The agent trace analysis (Figure 8) showing Claude Code's iterative refinement behavior and Codex's single-pass approach provides valuable insight into why agents don't outperform single-pass models, despite having more degrees of freedom.

## Weaknesses
### Fatal
None.

### Major
- **Scoring weights are unjustified**: The composite score uses weights (50% edge overlap, 20% degree correlation, 10% density, 10% room count, 5% door count, 5% door orientation) with no justification or sensitivity analysis. These weights directly determine model rankings. If the weights were changed—e.g., to weight room count more heavily—rankings could shift. A sensitivity analysis showing robustness of relative model ordering to weight choices would significantly strengthen the paper.
- **Insufficient statistical analysis**: The paper claims some models "statistically perform better than the random baseline" but provides no p-values, confidence intervals (beyond visual error bars), or formal hypothesis tests. Given that score differences between mid-performing models are small (e.g., GPT-5 at 0.42 vs. Claude Opus 4.1 at 0.32), statistical significance is critical for supporting the paper's comparative claims.
- **Confounding instruction following with spatial intelligence**: The authors acknowledge this in Section 2.4 but it significantly undermines some conclusions. NanoBanana and GPT-4o's poor scores are largely attributed to rule violations rather than spatial reasoning failures. The paper should report a "conditional" score for models that do follow instructions properly, or at minimum clearly separate the two failure modes in the analysis.

### Minor
- **Human baseline limited to 12 apartments**: Figure 7 explicitly notes "subset of Blueprint-Bench (12 instead of 50)," yet the human baseline is one of the paper's most important comparisons. This limits the statistical power of the human-vs-AI comparison substantially. The paper should acknowledge this limitation more prominently and ideally expand the human evaluation.
- **"Epochs" undefined**: The paper mentions averaging "across epochs and apartments" but never defines what constitutes an epoch. Is it re-running the same model on the same apartment with different random seeds? Different prompts? This needs explicit definition and the number of epochs should be reported.
- **Model categorization errors in Figure 5/table**: "Claude Code (Opus 4.1)" and "Codex (GPT-6)" appear to have their categories (agent vs. image model) inconsistently labeled between the figure and the table description. This is likely a parsing artifact, but if present in the original, it's a notable error.

### Trivial
- The random baseline construction could be more explicitly described (how many floor plans were generated, from which models, with what prompts).

## Nice-to-Haves
- A breakdown of failure modes per model (rule violations vs. spatial errors vs. connectivity errors) would make the results more informative.
- Reporting results separately for "easy" vs. "hard" apartments (e.g., by number of rooms) could reveal whether models handle simpler spatial layouts better.
- A brief analysis of whether models that score well on connectivity also tend to score well on size rankings, or whether these are independent failure modes.

## Novel Insights
The paper's most compelling novel observation is that image generation models—traditionally not evaluated for intelligence—show measurable but limited spatial reasoning capability, and that benchmarking this capability is both feasible and necessary as these models become more general. The finding that iterative agent refinement provides no meaningful improvement over single-pass generation is also noteworthy, suggesting that the bottleneck is not in the refinement loop but in the fundamental spatial representation. The comparison between how a human incrementally builds a mental model versus how agents either don't use iteration (Codex) or use it ineffectively (Claude Code) is a genuinely useful insight for the agent design community.

## Suggestions
- Add sensitivity analysis for the scoring weights—vary the weights and report whether relative model rankings are stable.
- Report formal statistical tests (e.g., bootstrap confidence intervals, Wilcoxon signed-rank tests) for pairwise model comparisons.
- Separately report a "format compliance rate" for each model and present main results both overall and conditional on format compliance.
- Expand the human baseline to all 50 apartments if feasible, or explicitly justify why 12 is sufficient.
- Clearly define "epoch" in Section 2.3 and report the number of epochs per model.

## Score and Decision
The paper presents a genuinely novel and well-motivated benchmark with an interesting cross-architecture evaluation design. The core idea—testing spatial intelligence through floor plan reconstruction from photographs—is creative and fills a real gap in AI evaluation. However, the methodological execution has meaningful gaps: unjustified scoring weights, insufficient statistical analysis, and confounding of instruction following with spatial reasoning. These issues don't invalidate the contribution but reduce confidence in the specific comparative claims. With stronger statistical rigor and scoring justification, this would be a solid accept.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>
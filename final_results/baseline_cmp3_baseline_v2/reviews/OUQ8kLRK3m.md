## Summary

This paper introduces DRE-Bench, a dynamic reasoning evaluation benchmark designed to assess the fluid intelligence of large language models through abstract reasoning tasks. The benchmark is structured around a four-level cognitive hierarchy (Attribute, Spatial, Sequential, Conceptual) from psychology, uses a code-based generator-solver pipeline for scalable and verifiable data generation, and supports dynamic task variants with varying complexity. Experiments on 11 LLMs show that while reasoning models outperform general LLMs, all models struggle with high-level cognition and exhibit limited generalization, indicating that current LLMs fall short of genuine fluid intelligence.

## Strengths

- **Cognitively grounded benchmark design:** The four-level hierarchy (Attribute, Spatial, Sequential, Conceptual) is explicitly motivated by established psychological frameworks (Primi, 2001), providing interpretability and a principled basis for evaluating different facets of abstract reasoning. This is a clear improvement over prior benchmarks that lack such cognitive alignment.
- **Dynamic and verifiable data generation:** The code-based generator-solver pipeline with human-in-the-loop verification ensures 100% correctness of generated samples and enables scalable production of diverse task variants with controllable complexity. This addresses the critical issues of data contamination and static complexity that plague existing benchmarks.
- **Comprehensive evaluation and insightful findings:** The paper evaluates a wide range of state-of-the-art LLMs (both general and reasoning-specialized) across multiple dimensions, including accuracy, variance, complexity scaling, in-context learning, visual information, and inference time. The findings—such as the systematic divergence in spatial orientation processing (better vertical than horizontal) and the failure of inference-time scaling for high-level tasks—are novel and valuable.

## Weaknesses

### Fatal
None.

### Major
- **Limited scope of Level-4 tasks and near-floor performance:** Level-4 (Conceptual) contains only three tasks (Gravity, Reflection, Expansion) and all models achieve near-zero accuracy. While this demonstrates that current LLMs fail at conceptual reasoning, the extremely low performance makes it difficult to draw fine-grained distinctions or track progress. The benchmark would benefit from a broader set of Level-4 tasks with more granular difficulty to avoid a ceiling/floor effect.
- **Human evaluation methodology is underspecified:** The human study (40 annotators, ~400 samples) is mentioned but lacks crucial details: how were annotators screened for cognitive ability? Were they given the same prompt format as LLMs? What was the inter-annotator agreement? The claim that "human accuracy also generally decreases as the level increases" is expected but the quantitative comparison is weakened without reporting variance or confidence intervals for human performance.
- **Lack of analysis on prompt sensitivity:** The paper uses a single standardized prompting template from ARCPrize. Given that LLMs are known to be highly sensitive to prompt phrasing, especially on abstract reasoning tasks, the absence of any prompt variation or robustness analysis is a significant gap. The results may not generalize beyond this specific prompt format.

### Minor
- **The "variance" metric is not clearly defined:** The paper uses "variance" in Figure 5 and the leaderboard (Figure 1c) but never formally defines what variance is computed over (e.g., across task variants? across random seeds? across trials?). This makes the stability analysis difficult to interpret or reproduce.
- **Table 1 has formatting issues:** The table appears to have duplicate rows (e.g., "o3-mini" appears twice with different numbers) and some values seem inconsistent (e.g., o3-mini's Avg-2 is 91.78, which is far higher than any individual task score in Level-2). This suggests a possible data entry or parsing error.
- **The ablation on visual information is limited to two models:** Only GPT-4o and Claude 3.7 support the multi-image format, so the conclusion that "current models struggle to derive meaningful improvements from auxiliary visualized image inputs" may not generalize to other vision-language models.

### Trivial
- The paper uses "Agentness" in Figure 7's left graph title, which is not a term defined or used elsewhere in the paper.

## Nice-to-Haves

- Include a formal definition of the "variance" metric and how it is computed.
- Add a prompt robustness analysis (e.g., test 2-3 different prompt templates) to assess whether results are sensitive to prompt phrasing.
- Expand Level-4 with more conceptual tasks (e.g., thermodynamics, electromagnetism) to provide finer granularity and avoid floor effects.
- Report human performance with confidence intervals or standard deviations to enable proper statistical comparison with LLMs.

## Novel Insights

Beyond the paper's own contributions, a genuinely novel observation is the systematic spatial orientation bias in LLMs: models perform significantly better on vertical (up/down) movements and horizontal symmetry than on horizontal (left/right) movements and vertical symmetry. This asymmetry is not present in human cognition, suggesting that current LLMs may have learned spatial representations that are fundamentally different from human spatial reasoning. This finding opens a new direction for investigating the inductive biases learned by LLMs from text-only training data, where directional language may be unevenly distributed (e.g., "up" and "down" may appear more frequently or in more predictable contexts than "left" and "right").

## Suggestions

- Clarify the definition of "variance" in the main text and ensure the scatter plots are reproducible by specifying what the variance is computed over.
- Fix the apparent data errors in Table 1 (duplicate o3-mini rows, inconsistent Avg-2 value) before publication.
- Add a brief discussion of the limitations of the single-prompt evaluation and acknowledge that results may be prompt-dependent.
- Provide the full human study details (screening, instructions, inter-annotator agreement) in the appendix to strengthen the validity of the human comparison.

## Score and Decision

The paper presents a well-motivated, cognitively grounded benchmark with a novel dynamic generation pipeline that addresses important limitations of existing static benchmarks. The evaluation is comprehensive and yields several non-trivial findings. The major weaknesses (limited Level-4 scope, underspecified human evaluation, lack of prompt sensitivity analysis) are addressable and do not invalidate the core contribution. The benchmark is likely to be a useful resource for the community.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>
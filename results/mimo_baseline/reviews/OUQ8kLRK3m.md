## Summary

The paper proposes DRE-Bench, a dynamic benchmark for evaluating fluid intelligence in LLMs through abstract reasoning tasks organized in a four-level cognitive hierarchy (Attribute, Spatial, Sequential, Conceptual) grounded in Primi (2001)'s psychology framework. A code-based generator-solver pipeline dynamically produces task variants with controlled complexity, enabling contamination-resistant evaluation. Experiments on 11 LLMs reveal that performance degrades with increasing cognitive level and complexity, with reasoning models outperforming general LLMs but all models falling well short of human performance on higher-level tasks.

## Strengths

- **Well-grounded cognitive framework**: The four-level hierarchy is directly motivated by an established psychology framework (Primi, 2001), and the authors validate it with a human study (40 annotators, ~400 samples) showing that human accuracy also decreases with cognitive level, supporting the framework's construct validity. This provides interpretability that prior abstract reasoning benchmarks like ARC-AGI lack.

- **Code-verifiable dynamic generation pipeline**: The generator-solver approach is a genuine methodological contribution. By parameterizing task variables and using code-based verification, the benchmark achieves 100% correctness of generated samples while enabling unlimited variants with controlled complexity. This directly addresses data contamination concerns plaguing static benchmarks.

- **Comprehensive and nuanced evaluation**: The paper evaluates 11 models (both general and reasoning LLMs) with multiple ablation studies—examining in-context learning sample counts, visual information modalities, and inference time scaling. The accuracy-vs-variance analysis across complexity levels provides a more informative picture than accuracy alone.

- **Interesting empirical findings**: The directional bias discovery (models perform better on vertical than horizontal movement, and better on horizontal than vertical symmetry) reveals systematic divergences from human spatial cognition that are genuinely novel and worth further investigation.

## Weaknesses

### Fatal
None.

### Major

- **Limited task diversity within each cognitive level**: Each level contains only 3 rules, and each rule has roughly 3 task variants. While the dynamic generation produces many samples per rule, the underlying reasoning patterns tested are relatively narrow. The claim of "36 abstract reasoning tasks" somewhat overstates diversity when many are parameter variations of the same rule. This limits the benchmark's ability to comprehensively characterize a model's cognitive capabilities at each level.

- **Human study lacks key methodological details**: The human evaluation (40 annotators, 400 samples) does not report inter-annotator agreement, which is essential for establishing the reliability of the human baseline. Without this, it is difficult to assess whether the human accuracy numbers are robust or whether certain tasks have ambiguous ground truth.

### Minor

- **The ablation on visual information only tests two models** (GPT-4o and Claude 3.7), limiting the generalizability of the finding that visual inputs don't help. Given that many models now have vision capabilities, a broader evaluation would strengthen this claim.

- **The variance metric lacks clear thresholds**: The paper uses variance as a "stability" measure but doesn't establish what constitutes a meaningful difference or provide statistical tests for comparing stability across models.

- **The claim of being "first" to introduce dynamic evaluation for abstract reasoning** is stated somewhat strongly, given that dynamic evaluation concepts have been explored in adjacent areas.

### Trivial
None.

## Nice-to-Haves

- A more detailed analysis of the code generation pipeline's reliability (e.g., how many refinement iterations were typically needed, failure rate of initial code agent outputs).
- An analysis of whether models that perform well on one cognitive level also tend to perform well on others, to understand whether the levels truly test distinct capabilities.
- Discussion of how the benchmark could be extended to new cognitive levels or rules over time.

## Novel Insights

The directional bias finding—that LLMs systematically process spatial orientations differently from humans (better at vertical movement but horizontal symmetry, while humans treat these as roughly equivalent)—is a genuinely novel observation. This suggests that LLMs' spatial representations may be shaped by training data distributions (e.g., text descriptions of vertical movement being more common or differently phrased) rather than developing human-like spatial cognition. This finding has implications beyond the benchmark itself for understanding how LLMs encode spatial information.

## Suggestions

- Expand the number of distinct rules per cognitive level (ideally 5+) to improve the breadth of cognitive assessment and reduce the risk that performance on 3 rules generalizes poorly to the broader cognitive category.
- Report inter-annotator agreement (e.g., Cohen's kappa or Fleiss' kappa) for the human study to strengthen the validity of the human baseline.
- Consider adding a "rule transfer" evaluation where models must apply a learned rule to a structurally different task variant, which would more directly test the fluid intelligence claim.

## Score and Decision

The paper makes a solid contribution through its cognition-aligned framework, dynamic generation pipeline, and comprehensive evaluation. The cognitive hierarchy provides genuine interpretability advantages over existing abstract reasoning benchmarks, and the code-based generation approach is a practical and verifiable solution to data contamination. The main limitations are the relatively narrow task diversity within each cognitive level and the incomplete human study methodology. These are addressable weaknesses that don't invalidate the core contribution.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: Accept
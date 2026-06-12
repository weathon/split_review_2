## Summary

This paper introduces GeoGramBench, a benchmark of 500 geometry problems that require LLMs to interpret procedural drawing code (Asymptote/Matplotlib) and perform geometric reasoning. The authors formalize the "Program-to-Geometry" task, propose a three-level taxonomy (Primitive Recognition, Local Relation Composition, Global Abstract Integration) based on geometric complexity, and evaluate 19 frontier LLMs. Their key finding is that even the strongest models achieve less than 50% accuracy on the highest abstraction level, revealing significant limitations in program-driven spatial reasoning.

## Strengths

- **Novel and well-motivated task formulation**: The Program-to-Geometry task is a genuinely underexplored capability that bridges symbolic code understanding and spatial reasoning. The authors provide compelling preliminary evidence (Figure 1) showing accuracy drops of 10-23% when models transition from text-only to text+code problems in existing benchmarks, justifying the need for a dedicated benchmark.

- **Rigorous benchmark construction with attention to data contamination**: The authors identify and address the critical issue of "answer leakage" in procedural code (Section 4.1), implementing systematic decontamination strategies including coordinate rescaling and code parameter modification. The two-stage human refinement process with 4 domain experts adds credibility to the dataset quality.

- **Comprehensive evaluation across 19 models**: The benchmark covers a wide range of models from 1.5B to frontier systems, with consistent evaluation protocols. The taxonomy-based analysis reveals meaningful patterns about where models fail (e.g., all models below 50% on Abstract level, angle and volume as most challenging subtypes).

## Weaknesses

### Major

- **Limited novelty beyond the benchmark itself**: The paper's core contribution is the dataset and evaluation. The behavioral analysis (Section 6) is largely descriptive and confirms expected patterns (models struggle with complex spatial reasoning, CoT doesn't help much). The "common failure patterns" are based on manual review of representative examples rather than systematic annotation, limiting their reliability. The paper would benefit from deeper mechanistic insights or proposed solutions.

- **The taxonomy validation is weak**: Figure 2 attempts to validate the taxonomy by showing that accuracy on P_TC problems correlates with geometric complexity rather than reasoning complexity. However, the analysis is based on only 42 P_TC problems from MATH-500, and the results are noisy (e.g., Abstract level shows 86.2% accuracy while Compositional shows 56.9%, which contradicts the claim that Abstract is hardest). The validation would be stronger if done on the full GeoGramBench dataset itself.

- **Missing analysis of code language effects**: The authors mention that "experiments indicate minimal impact from the choice of drawing language" (Section 4.4) but provide no supporting evidence. Given that the benchmark mixes Asymptote and Matplotlib code, this is a potentially confounding factor that deserves explicit analysis.

### Minor

- **The research questions (RQs) are addressed at a surface level**: RQ1 is answered by noting that models achieve >60% on Primitive level, but this doesn't distinguish between models that truly understand the code versus those that solve problems through textual cues or algebraic shortcuts. The qualitative examples in Figure 6 are illustrative but not systematic.

- **The Token Budget Forcing experiment is relegated to the appendix**: Given that RQ3 about CoT reasoning is a central question, the quantitative analysis of CoT limitations should be in the main text rather than Appendix E.

### Trivial

- The paper uses inconsistent model naming (e.g., "GP-4" in Table 1 likely refers to GPT-4, "GP-3.5-turbo" appears multiple times with different names).

## Nice-to-Haves

- An ablation study comparing model performance when given code vs. rendered images vs. both would help isolate whether the bottleneck is code parsing or spatial reasoning.
- Analysis of whether models that perform well on Primitive but poorly on Abstract fail due to error accumulation or fundamentally different capability requirements.
- A breakdown of whether the 500 problems are balanced across geometric shapes (triangles, circles, 3D solids, etc.) to identify shape-specific weaknesses.

## Novel Insights

None beyond the paper's own contributions. The key insight—that LLMs struggle with program-driven geometric reasoning, particularly at higher abstraction levels—is well-documented but not surprising given existing work on spatial reasoning limitations. The paper's value lies primarily in providing a standardized benchmark for measuring this capability rather than revealing unexpected phenomena.

## Suggestions

- Provide explicit validation that the taxonomy categories are separable and meaningful by showing inter-annotator agreement or confusion matrix analysis.
- Include a controlled experiment where the same geometric problem is presented with vs. without code to quantify the added difficulty of code interpretation.
- Release the benchmark with clear guidelines for how to handle the two code languages (Asymptote vs. Matplotlib) to ensure fair comparison across future work.

## Score and Decision

The paper makes a solid contribution by introducing a well-constructed benchmark for an underexplored task. The dataset construction is rigorous, the evaluation is comprehensive, and the findings are clearly presented. However, the paper's contributions are primarily empirical/benchmarking rather than methodological or theoretical, and the behavioral analysis lacks depth. The work is valuable to the community but does not represent a breakthrough.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>
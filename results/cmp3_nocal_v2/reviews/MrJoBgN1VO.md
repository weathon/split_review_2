## Summary

GeoGramBench introduces the "Program-to-Geometry" task, evaluating whether LLMs can parse procedural drawing code (Asymptote, matplotlib) into an internal geometric representation and reason over it. The benchmark contains 500 carefully curated problems organized by a three-level taxonomy (Primitive Recognition, Local Relation Composition, Global Abstract Integration) based on geometric rather than reasoning complexity. Evaluating 19 models reveals that no model exceeds 50% accuracy at the highest abstraction level, and the paper provides behavioral analyses identifying common failure patterns.

## Strengths

1. **Well-motivated and genuinely underexplored task.** The Program-to-Geometry problem—requiring models to parse procedural drawing code and reason over the implied geometry—fills a clear gap between visual-geometry benchmarks (Euclid, GeoSense) and SVG-code benchmarks (SGP-Bench). The Figure 1 data showing consistent accuracy drops when Asymptote code is introduced (e.g., GPT-o1 dropping from 65.8% to 45.9% on AIME24) concretely motivates the benchmark.

2. **Answer leakage mitigation is a genuine methodological contribution (Section 4.1).** The paper identifies a non-obvious confound in procedural-code benchmarks: answers can be read directly from coordinate values or computed from code parameters. The two-pronged mitigation (rescaling coordinates for direct leakage, modifying parameters for indirect leakage) addresses a real threat to validity and will benefit future benchmark builders in this space.

3. **Broad model coverage with informative core finding.** Evaluating 19 models spanning closed-source (GPT-5, GPT-4o, GPT-o1, Gemini-Pro-1.5) and open-source (DeepSeek-R1, Qwen3, QwQ-32B, distilled variants) systems provides a useful capability landscape. The robust finding that no model exceeds 50% on the Abstract level, despite strong performance on Primitive (e.g., GPT-5 at 90.44%), is a genuine and informative result.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **Taxonomy validation figure (Figure 2) is confusingly presented.** The paper claims that geometric complexity (not reasoning complexity) drives accuracy decline on P_TC problems. The P_gg series (accuracy on P_TC by geometric complexity: 86.1 → 81.7 → 75.0) does support this claim. However, the figure description is ambiguous: a table embedded in the caption maps reasoning complexity levels to geometric complexity categories with a third column labeled "Reasoning Steps" containing values (79.4, 56.9, 86.2) that a reader could conflate with geometric-complexity accuracy. The figure's core evidence is present and valid, but the garbled presentation undermines the paper's claimed empirical grounding for its taxonomy. A clean, unambiguous figure is needed.

2. **All four models report exactly 68.9% on the MATH-500 P_TC subset in Figure 1(c).** On 42 problems sampled 8 times each (336 outcomes per model), four distinct models (GPT-o1, R1, QwQ-32B, R1-Distill-32B) are all reported at exactly 68.9%. The paper should clarify whether this reflects a genuine coincidence, a rounding artifact, or a specific property of the P_TC subset (e.g., most problems are easy enough that all models solve the same majority). The AIME24 data (5 problems, coarser granularity) does not raise the same concern.

3. **Minor circularity between motivation data and benchmark content (Section 4.4).** The paper motivates GeoGramBench by showing models struggle on MATH-500 and AIME24 problems with code (Figure 1), but then includes 42 MATH-500 problems and 5 AIME24 problems (9.4% of the benchmark) in GeoGramBench itself. While small in proportion, the motivation would be stronger if it used entirely disjoint data. The authors should either run the preliminary study on held-out portions or explicitly acknowledge and justify the overlap.

4. **RQ3 (CoT analysis) lacks quantitative evidence in the main text.** The central claim about CoT's limited benefit in this task is supported in the main paper only by qualitative observations of models "cycling through algebraic steps." The Token Budget Forcing experiment (Appendix E) provides the actual quantitative evidence. At minimum, the main paper should summarize the budget-forcing results; without this, RQ3 reads as an informal impression rather than a research finding.

5. **GPT-4o's dramatically low performance is not discussed.** GPT-4o achieves only 40.02% on the Primitive level and 23.40% overall, far below GPT-3.5 variants (~70–85%) that the text describes as earlier models. If this is a genuine result, it is itself a significant finding about GPT-4o's inability to handle Asymptote code and deserves analysis. If it reflects an evaluation issue (e.g., API behavior under the specific prompt template), that needs clarification.

6. **Per-subtype-per-level problem counts are not reported in the main paper.** The paper reports accuracy across 18 cells (3 levels × 6 subtypes: angle, length, area, volume, ratio, count) but never states how many problems fall into each cell. With only ~500 problems, many cells likely contain very few examples (especially Volume at the Abstract level, which appears only there). Without these counts, the per-subtype comparisons emphasized in Section 5.3 are difficult to interpret reliably. (The paper notes these are in Appendix C.8, but the main text should at minimum summarize the counts.)

### Trivial

- **Mathverse transcription verification underspecified (Section 4.4).** The 61 Mathverse problems were manually transcribed into matplotlib code, but the paper does not describe how these transcriptions were verified or whether the same four experts checked them.

## Nice-to-Haves
- Reporting variance across the 8 samples per problem would help readers assess which model differences are reliable.
- Including a summary of the Token Budget Forcing experiment (Appendix E) in the main paper would strengthen the CoT analysis.

## Removed Points
The following points from the input review are removed per policy:

- **Model name inconsistency between Table 1 and Section 5.2.** The garbled model names in Table 1 (e.g., "GP-4" for GPT-5, "DeepSeek-K1" for DeepSeek-R1, "v1.1-32B" for s1.1-32B) are parser corruption artifacts, not author errors. The text clearly states which models were evaluated. Policy: remove formatting/parser artifacts.
- **Figure 1(a) garbled caption.** Parser corruption of an image caption. Remove per policy.
- **Request for missing related works.** Policy: not possible to verify without external sources.
- **Criticism about missing appendix content.** Policy: the appendix is stripped by the parser; it exists in the original submission.
- **General reproducibility nitpicks about undisclosed hyperparameters.** Not a genuine flaw for a benchmark paper.

## Novel Insights
None beyond the paper's own contributions. The review did not surface contradictory evidence or alternative explanations that challenge the paper's framing.

## Suggestions
1. Revise Figure 2 to make the three series (P_r, P_g, P_gg) and their correspondence to reasoning vs. geometric complexity unambiguous. Remove or clarify the embedded table that conflates reasoning levels with geometric categories.
2. Explain the uniform 68.9% in Figure 1(c)—whether it is a rounding coincidence, a real uniformity, or an artifact of the 8-sample evaluation methodology.
3. Either separate the Figure 1 motivation data from the benchmark (use held-out problems) or explicitly justify the 9.4% overlap in the text.
4. Include summary quantitative results from the Token Budget Forcing experiment in the main paper to support RQ3's claim about CoT limitations.
5. Add per-cell problem counts (or a supplementary table) for the 3 levels × 6 subtypes, to contextualize the subtype accuracy comparisons.
6. Discuss the GPT-4o result: why does a capable multimodal model score far below GPT-3.5 variants on Primitive-level code parsing?

MY FINAL SCORE: <score>7.5</score>
MY FINAL DECISION: <decision>Accept</decision>
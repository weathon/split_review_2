## Summary

GeoGramBench introduces the **Program-to-Geometry** task, which evaluates LLMs on their ability to reason over geometry problems presented through procedural drawing code (Asymptote/Matplotlib). The paper presents a 500-problem benchmark organized by a three-level taxonomy (Primitive → Compositional → Abstract) grounded in geometric complexity, evaluates 19 frontier models, and finds that even the best models score below 50% on the hardest level. The answer leakage analysis (Section 4.1) is a valuable methodological contribution that goes beyond typical benchmark construction.

## Strengths

- **The Program-to-Geometry task is genuinely novel and well-motivated.** The paper identifies a real gap: existing geometry benchmarks focus on visual perception (diagrams) or pure text, but not on reasoning from procedural drawing code. The preliminary experiments (Figure 1) provide compelling evidence — consistent accuracy drops of 10–23% across multiple models (GPT-o1, DeepSeek-R1, QwQ-32B, R1-Distill-32B) when procedural code is present — establishing that this measures a distinct capability.

- **The answer leakage analysis (Section 4.1, Figure 3) is a substantive methodological contribution.** The identification of direct leakage (answer explicit in coordinates) and indirect leakage (answer derivable from code parameters), along with practical mitigation strategies (coordinate rescaling, parameter masking), demonstrates awareness of a subtle confound that would otherwise invalidate the benchmark. This is the kind of insight that makes a benchmark paper valuable beyond just releasing data.

- **The three-level taxonomy (Primitive → Compositional → Abstract) is well-reasoned** and appropriate for the task. Basing difficulty on geometric complexity rather than reasoning steps (Section 3.2) is well-motivated, since the core challenge in Program-to-Geometry is spatial construction, not multi-step algebra. The distribution (20.8% / 23.8% / 55.3%) appropriately weights the benchmark toward the challenging region.

- **The finding that all 19 models score below 50% on the Abstract level** is an informative result that establishes a clear difficulty ceiling and gives the community a concrete target for improvement.

- **The benchmark construction pipeline is thorough.** From 905K candidates to 392 refined problems (68% attrition through multi-stage human verification, decontamination, and answer leakage prevention), the process suggests careful quality control.

## Weaknesses

### Major

- **No uncertainty quantification reported anywhere.** The paper samples 8 responses per problem per model and reports mean accuracy, but provides no confidence intervals, standard deviations, or significance tests. For a benchmark paper whose main deliverable is comparative model rankings, this omission makes it impossible to assess whether reported differences between models (e.g., 75.01% vs. 74.00% for the top two models) are meaningful or reflect sampling noise. The paper reports accuracy to two decimal places, which implies a precision that cannot be verified.

- **Taxonomy validation is conducted on a single model.** The empirical analysis supporting the taxonomy (Figure 2) uses only QwQ-32B on the MATH-500 dataset. The paper's central argument — that geometric complexity rather than reasoning complexity drives task difficulty — would be substantially stronger if validated across multiple models. As it stands, the pattern could be model-specific.

- **Partial overlap between preliminary analysis and main benchmark is not discussed.** The augmentation step (Section 4.4) adds exactly the same number of problems from AIME24 and MATH-500 (5 and 42 respectively) that Figure 1 uses as its P_TC subsets. This means the P_TC accuracy drops shown in the preliminary analysis are based on problems that are *also included in the main benchmark*. A reader cannot tell whether the main benchmark results are independent of the preliminary analysis or whether the same problems appear in both. The paper should clarify this.

- **The qualitative behavior analysis would benefit from systematic quantification.** The "Common Failure Patterns" in Section 6 (algebraic bias, no auxiliary lines, orientation struggles, symbol mapping confusion) are plausible and interesting, but presented as informal impressions without prevalence estimates or structured error categorization. The paper acknowledges this ("based on representative examples rather than exhaustive annotation"), which is honest, but the diagnostic value of the benchmark would be higher with quantitative failure-type distributions across a random sample of model errors.

### Minor

- **No inter-annotator agreement reported.** The human refinement process (Section 4.3) involved four expert reviewers through a two-stage process, but no agreement metrics are provided, making it difficult to assess the reliability of the curation decisions.

- **Results are not disaggregated by problem source.** The 392 base problems and 108 augmented problems (from AIME24, MATH-500, Mathverse) are pooled in the results. Reporting results separately would enable analysis of whether different sources behave differently and whether the manually transcribed Mathverse problems (61/500) introduce any systematic bias.

- **The evaluation uses temperature 0.6 for all models without justification.** For reasoning-oriented models (GPT-o1, DeepSeek-R1, QwQ-32B) that are commonly evaluated with lower temperatures or greedy decoding in their original benchmarks, this choice could affect relative rankings. Sampling 8 responses partially mitigates stochasticity, but the paper does not discuss whether this choice could systematically affect different model families.

- **No discussion of answer correctness for ambiguous problems.** Some geometry problems admit multiple valid interpretations (e.g., which region is shaded, orientation of a figure). The paper does not describe how answer correctness was adjudicated for such cases.

### Trivial

None.

## Nice-to-Haves

- Disaggregating results by programming language (Asymptote vs. matplotlib) would directly support the claim of minimal language impact.
- Adding bootstrap confidence intervals over the 8 samples per problem would substantially increase confidence in the comparative results.
- A control experiment testing whether models can solve problems by merely extracting coordinate values (the simplest cheating strategy) would directly validate the leakage mitigation.

## Removed Points

The following points from the input review were removed after verification:

- **Table model name garbling** (GP-4 → GPT-5, DeepSeek-K1 → DeepSeek-R1, etc.): These are PDF parser artifacts that do not reflect the original submission. Removed per formatting-artifact guidelines.
- **Figure 1(a) shoelace formula error** (0.5×|0−0|=0, answer=54): The computation as printed is clearly a PDF extraction artifact where coordinate values were mangled. Removed per guidelines.
- **Figure 2 data "contradicts" independence claim**: The critic asserted that P_g values (79.4 → 56.9 → 86.2) contradict the paper's claim of independence from reasoning complexity. A non-monotonic pattern across reasoning-complexity levels *supports* independence rather than contradicting it. This criticism was factually incorrect.
- **Figure 2 embedded table column confusion**: Column header garbling in the figure caption is a parser artifact. Removed per guidelines.
- **Mathverse transcription confound**: The critic's concern references Appendix A ("minimal impact from the choice of drawing language"), which was stripped by the parser. Removed per guidelines (missing appendix).
- **Qwen3 scale discrepancy (235B vs 23B)**: This is consistent with a parser artifact dropping a digit. Removed per formatting-artifact guidelines.
- **Bespoke-Stratos → DeepSeek-Stratos discrepancy**: Consistent with known parsing of special characters. Removed per guidelines.
- **Missing related works, missing appendix content, and reproducibility nitpicks about hyperparameters**: Removed per guidelines.

## Novel Insights

None beyond the paper's own contributions. The reviews identify useful refinement directions (uncertainty quantification, broader taxonomy validation, disaggregated analyses) but do not surface any observation about the paper's core contribution that the paper itself does not already articulate.

## Suggestions

1. Add confidence intervals or standard deviations to all reported accuracies (either bootstrap over the 8 samples per problem or per-problem variance).
2. Validate the taxonomy analysis on at least 3–4 additional models to demonstrate the pattern generalizes.
3. Clarify the relationship between the Figure 1 preliminary data and the main benchmark — specifically whether the 5 AIME24 and 42 MATH-500 P_TC problems also appear in GeoGramBench.
4. Disaggregate results by problem source (base vs. augmented) and ideally by programming language.
5. Add inter-annotator agreement metrics for the human curation process.

## Score and Decision

The paper identifies a genuinely novel evaluation dimension (Program-to-Geometry), constructs a well-scoped benchmark with careful attention to data quality and answer leakage, and provides informative baselines across 19 models. The weaknesses are real but addressable — none threatens the paper's core contribution. The most significant gap (no uncertainty quantification) is common in benchmark papers but should be addressed to strengthen the comparative claims. I assess this as a solid contribution to the evaluation landscape that, with minor revisions, readily merits acceptance.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>
## Summary

Blueprint-Bench introduces a benchmark for evaluating spatial reasoning by having AI models convert apartment photographs into 2D floor plans. It provides a dataset of 50 apartments (~20 interior images each), a scoring pipeline based on room connectivity graphs and size rankings, and evaluations of several LLMs, image generation models, and agent systems. The core motivation — testing spatial intelligence using in-distribution inputs but out-of-distribution outputs — is well-founded.

## Strengths

- **Well-motivated spatial reasoning task.** The argument (Section 1) that converting natural photographs into a coherent 2D floor plan requires genuine spatial inference — layout reconstruction, connectivity reasoning, scale consistency — is clear and defensible. This is a stronger test than artificial pattern-matching tasks like ARC grids, and the "in-distribution input, out-of-distribution output" framing is a meaningful contribution.

- **Transparent, interpretable scoring algorithm.** The multi-component weighted score (Section 2.3: 50% edge overlap, 20% degree correlation, 10% density, 10% room count, 5% door count, 5% door orientation) is clearly specified, avoids pixel-level matching, and captures the essential spatial structure through connectivity graphs and size rankings.

- **First unified cross-architecture comparison framework.** The paper provides the first numerical framework for comparing spatial intelligence across LLMs, image generation models, and agent systems on the same task (Section 1, final paragraph). This cross-architecture comparison is novel and could gain value as more models are evaluated.

## Weaknesses

### Fatal
None.

### Major

1. **The central narrative claim contradicts the paper's own data.** The abstract states "most models perform at or below a random baseline," and Section 3 says "most do not outperform the random baseline." However, Figure 5 shows the random baseline at 0.279, and 10 out of 12 models scored above it (only GPT-4o at 0.15 and Nano Banana at 0.18 are below). Even models with "on par" scores like GPT Image (0.32) are numerically above 0.279. This is not a subjective disagreement — it is a factual mismatch between the paper's stated conclusions and the reported numbers. The paper's central finding is the one readers will remember, and it is not supported by the evidence presented.

2. **Human baseline on only 12 of 50 apartments with no justification.** Figure 7 reports human performance on a 12-apartment subset, with no explanation of why only 12 were used, how they were selected, whether they are representative, or whether the same participants drew all 12 floor plans. For a benchmark paper, the human baseline is the primary calibration point for the entire task, and its incomplete coverage is a significant methodological gap.

3. **Metric calibration is insufficiently validated.** Humans with "all connectivity correct" score only 0.547 (Figure 7). The gap between the best model (GPT-5/Gemini 2.5 Pro, 0.42) and humans is 0.13. The paper itself speculates that "one similarity scoring model would make the human's lead over the AI models much larger" (Section 3), effectively acknowledging that the metric may not properly capture the ability differences it is supposed to measure. The limitations section (2.4) discusses this but does not provide the calibration analysis, sensitivity analysis, or alternative metric comparisons needed to establish validity.

### Minor

4. **Unsupported statistical claims.** The paper uses "statistically perform better" (Section 3, twice) without reporting any formal statistical tests, p-values, confidence intervals, or multiple-comparison corrections. Only standard deviation error bars are provided. This language implies a rigor that the analysis does not deliver.

5. **The "random baseline" conflates two distinct concepts.** The baseline is defined as generating floor plans *without any image input* (Section 2.2) — a no-information/prior-only baseline — but is labeled and discussed as a "random baseline" throughout. These are not the same thing. Additionally, the baseline value shifts between Figure 5 (0.279 on 50 apartments) and Figure 7 (0.322 on the 12-apartment subset) with only the figure caption explaining the difference. This needs prose clarification.

6. **Output pipeline confound is acknowledged but not addressed in interpretation.** LLMs generate SVG code (then rendered), image models generate images directly, and agents use Docker environments with tools. Failures could stem from spatial reasoning deficits or from code-generation errors, instruction-following failures, or tool-use difficulties. The paper mentions this briefly (Limitations 2.4) but draws broad conclusions about "spatial reasoning" without disentangling these confounds.

7. **Model categorization inconsistency.** The table embedded in Figure 5's caption lists Claude Code (Opus 4.1) as "Image model" despite Section 2.2 identifying it as an agent scaffold. The bar chart uses "Agents (dotted bars)" vs. "Image models (striped bars)," so either the table or the visual encoding is wrong.

8. **Missing experimental reproducibility details.** No information is provided about number of trials/runs per model, hyperparameters (temperature, top-p, etc.), or how results vary across runs. The term "epochs" (used in Section 3 and figure captions) is never defined.

9. **Scoring weights are stated without justification or sensitivity analysis.** The weights (50/20/10/10/5/5) are given but never justified. It is unclear whether the relative model rankings would hold under different weightings, and no sensitivity analysis is provided.

10. **Ground-truth creation process is not documented.** Section 2.1 states ground-truth floor plans were "adapted from the apartment listing's official floor plan image" but does not describe who adapted them, the quality control process, or any validation steps.

### Trivial

11. **Ambiguous phrasing.** "We suspect that one similarity scoring model would make the human's lead over the AI models much larger" (Section 3) — the word "one" is unclear; it likely should be "a different" or "our."

## Nice-to-Haves

- Run the human evaluation on the full 50-apartment set or provide statistical evidence that the 12-apartment subset is representative.
- Add a sensitivity analysis for the scoring weights to establish that model rankings are robust.
- Control for the output-pipeline confound by having all models produce SVG code.
- Include per-apartment difficulty analysis (how models handle varying layout complexity).

## Removed Points

*These points are flagged to be removed; treat them with caution.*
- The critic's observation about missing related work: removed per instructions (cannot verify existence of unmentioned works from this position).
- The critic's broader "the metric may not be measuring the right thing" speculation beyond what the paper's own data concretely supports: removed as speculative without a specific paper anchor beyond what is already captured in Major weakness #3.
- The critic's point about "the paper would benefit from a larger dataset": removed as a generic request that does not identify a specific problem with the current size.
- The critic's suggestion that Section 2.4's limitations "implicitly undermine the metric": already captured in Major weakness #3 above.
- Formatting/style nitpicks (typos, caption formatting): removed per instructions (parser artifacts).

## Novel Insights

None beyond the paper's own contributions. The reviews do not surface a perspective on the paper's approach or results that the authors did not already express or anticipate.

## Suggestions

1. **Correct the central narrative.** Replace "most models perform at or below a random baseline" with an accurate description of the data (e.g., "all models remain substantially below human performance, with most scoring modestly above a no-image baseline but far from human-level spatial reasoning").
2. **Complete the human baseline** on the full 50-apartment set, or rigorously justify and characterize the 12-apartment subset.
3. **Add statistical tests** (bootstrap confidence intervals or permutation tests) for all key comparisons, and remove or qualify the phrase "statistically perform better" until these tests are reported.
4. **Validate the metric** with a calibration analysis: show how scores vary with known difficulty levels, compare against alternative weighting schemes, and quantify how the size-ranking propagation affects scores.
5. **Disambiguate the model categorization** — fix the Claude Code labeling error in Figure 5's table.
6. **Report trial details** (number of runs, temperature settings, definition of "epochs").

## Calibration Anchors

| Path | Avg Score | Round | Itemized? | Comparison |
|------|-----------|-------|-----------|------------|
| /home/.../WK6K1FMEQ1.md | 6.75 (Accept) | 1 | Yes | SPACE spatial cognition benchmark — broader scope, better-validated metric, full human baselines, accepted. Current paper is weaker across all dimensions. |
| /home/.../9Y6QWwQhF3.md | 4.25 (Reject) | 1 | Yes | FoREST spatial reasoning benchmark — similar weaknesses around limited scope and insufficient validation, rejected. Comparable quality level. |
| /home/.../oecFal31WP.md | 5.75 (Reject) | 1 | Yes | STBench spatio-temporal benchmark — larger dataset (60k+ QA pairs), more models, but rejected for insufficient rigor. Current paper has less data but some similar rigor issues. |
| /home/.../a7eIuzEh2R.md | 6.25 (Reject) | 2 | Yes | MANGO navigation/mapping benchmark — well-curated 53-maze dataset, careful experimental design, but rejected. Current paper is less rigorous. |
| /home/.../uBhqll8pw1.md | 4.00 (Reject) | 2 | Yes | On Inherent 3D Reasoning — spatial reasoning evaluation with overclaiming issues, rejected. Similar severity of overclaim to current paper. |

**Score placement:** My draft's most negative-favorability weakness (-2.42 for unsupported statistical claims) is comparable to the rejected anchors' most negative items (FoREST: -2.99; STBench: -2.02; On Inherent 3D: -3.55). The SPACE benchmark (accepted, 6.75) had a similar-magnitude negative item (-2.36 for missing citations) but was carried by many more high-favorability strengths (12+) and stronger validation. My paper's strengths (favorability 11–12) are solid but not exceptional. The distinguishing factor is the verified narrative overclaim — no accepted anchor had a verified factual contradiction between its central claim and its own data. This pushes the score decisively below the acceptance threshold, placing it alongside the rejected spatial reasoning benchmarks.

## Score and Decision

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>
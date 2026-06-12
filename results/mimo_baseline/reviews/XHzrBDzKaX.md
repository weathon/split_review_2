## Summary
This paper introduces VISFACTOR, a benchmark that digitizes 20 vision-centric subtests from the Factor-Referenced Cognitive Test (FRCT) battery to evaluate MLLMs across four domains of human visual cognition: visualization/spatial processing, perceptual/closure, memory, and reasoning. The benchmark includes creative chance-level reduction techniques and parametric generation for controllable difficulty. Evaluation of 23 frontier MLLMs reveals the best model achieves only 30.17% (vs. 78.8% for humans), with systematic failures on mental rotation, spatial reasoning, and figure-ground discrimination tasks.

## Strengths
- **Well-grounded in cognitive science**: The paper systematically adapts an established psychometric instrument (FRCT) covering 10 distinct cognitive factors, providing more diagnostic depth than existing omnibus benchmarks. The factor-referenced design enables pinpointing specific visual cognitive deficiencies rather than relying on aggregate scores.
- **Creative and rigorous chance-level reduction**: The four methods (decomposed multiple-choice, grouped-consistency, symmetry variants, specialized rewrites) reduce average guessing accuracy from 22.47% to 2.89%, making the benchmark substantially more discriminative than typical multiple-choice evaluations.
- **Scalable parametric generation**: Implementing difficulty-controllable generators for 12 of 20 subtests future-proofs the benchmark against saturation and data contamination. The difficulty scaling results (Table 3) convincingly demonstrate controllability—e.g., GPT-4.1 drops from 92.86% to 33.33% on MA1 as pairs increase from 10 to 80.
- **Comprehensive and fair evaluation**: 23 models spanning major families (GPT, Gemini, Claude, Qwen, LLaMA, Seed) with a proper human baseline (31 participants, same protocol), controlled hyperparameters, and robustness checks across temperatures.

## Weaknesses
### Fatal
None.

### Major
- **Task reformulation may confound results**: The decomposed multiple-choice approach (one yes/no query per option) fundamentally changes the cognitive demand from discrimination/recognition to sequential verification. This could disproportionately affect models in ways unrelated to the underlying visual cognition being tested. The human evaluation uses the same protocol, so the relative comparison remains valid, but the absolute scores may not directly correspond to the original FRCT factors being measured.

### Minor
- **Human evaluation sample composition**: The 31 university students may not represent the broader population, and the paper does not report demographic details or cognitive ability distributions. The original FRCT was normed on broader populations, so the 78.8% human baseline may not be fully comparable.
- **Some failure analysis claims rest on small-scale experiments**: The "bias toward diagonal orientations" finding is based on a controlled test with only 20 non-45-degree vectors, which is somewhat thin evidence for a broad claim about model representations.
- **Partial parametric coverage**: Only 12 of 20 subtests have generators. The remaining 8 subtests (including several where models perform poorly, like S1, SS2, VZ3) lack controllable-difficulty augmentation, limiting the benchmark's full scalability promise.

### Trivial
None.

## Nice-to-Haves
- A stratified human evaluation across different education levels or cognitive ability tiers would strengthen the human baseline interpretation.
- Analysis of whether few-shot or in-context learning improves performance on specific cognitive factors, beyond the zero-shot and CoT settings tested.
- Correlation analysis between VISFACTOR subtest scores and existing benchmark scores (e.g., MMBench) would quantify the degree to which current benchmarks miss these capabilities.

## Novel Insights
The paper's most compelling contribution beyond benchmark creation is the demonstration that MLLMs' apparent memory and recognition strengths are largely driven by concept-level verbalization rather than genuine visual processing. The MA1 ablation (Table 5) elegantly shows that models maintain high accuracy with semantically rich images but collapse with abstract line patterns at the same task, and extreme but semantically parseable images (e.g., "horse on moon") preserve performance. Combined with the CF3 textual-vs-visual comparison (100% vs. 6.2% accuracy), this provides strong evidence that current MLLMs operate through a language-mediated bottleneck rather than possessing gestalt-like perceptual processing. The "Middle Score Anomaly" observation—models achieving 30-50% on tasks where humans either succeed near-perfectly or fail completely—further suggests fundamentally different processing mechanisms rather than merely degraded versions of human cognition.

## Suggestions
- Add a discussion of how the task reformulation methods interact with model capabilities—for instance, whether models that perform poorly on decomposed multiple-choice might perform differently on standard multiple-choice, and what this tells us about their visual cognition.
- Include a brief analysis of error patterns (e.g., are errors random or systematic?) for the key failing subtests to deepen the failure analysis.
- Consider adding a "factor profile" visualization that maps each model's performance across the 10 cognitive factors, making the diagnostic value of the benchmark more immediately apparent.

## Score and Decision
This is a well-executed benchmark paper with a clear and important research question, sound methodology grounded in cognitive psychology, comprehensive evaluation, and genuinely novel insights about MLLM visual cognition limitations. The chance-level reduction techniques and parametric generation add methodological rigor. The main concern about task reformulation confounding results is notable but mitigated by the consistent human-model comparison protocol. The contribution is valuable to the community and charts clear research directions.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>
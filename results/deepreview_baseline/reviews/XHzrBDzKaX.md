## Summary

This paper introduces VisFACTOR, a benchmark that digitizes 20 vision-centric subtests from the Factor-Referenced Cognitive Test (FRCT) battery—an established cognitive psychology assessment—spanning four domains of human visual cognition. The authors evaluate 23 frontier MLLMs (both proprietary and open-source) and find that the best-performing model achieves only 30.17%, with systematic failures on core visual tasks such as mental rotation, spatial relation inference, and figure-ground discrimination. Additionally, they implement a parametric generator to produce unlimited difficulty-controlled test cases for 12 subtests, future-proofing the benchmark against overfitting.

## Strengths

- **Novel grounding in cognitive science**: Adapting a well-established psychometric battery (FRCT) to MLLM evaluation is a principled and underexplored approach. The benchmark covers 10 distinct cognitive factors across 20 subtests, providing a fine-grained diagnostic profile rather than a single aggregate score.

- **Rigorous reduction of chance-level accuracy**: The paper carefully designs answer formats (decomposed multiple-choice, grouped-consistency items, symmetry variants) to lower the average random guessing accuracy to 2.89%, making observed performance far more meaningful than typical multiple-choice benchmarks.

- **Comprehensive evaluation and insightful failure analysis**: Testing 23 models from major families (GPT, Gemini, Claude, LLaMA, Qwen, Seed) with standardized protocols reveals consistent and striking failures. The analysis of *why* models fail—reliance on concept recognition over low-level perception, insensitivity to length/angle/scale, and a diagonal bias—is insightful and actionable.

- **Human baseline and parametric generation**: The human evaluation (78.8% accuracy across 31 participants) confirms a large gap between current models and human visual cognition. The parametric generator for 12 subtests allows dynamic difficulty control and unlimited data, which helps prevent future benchmark saturation.

## Weaknesses

### Fatal
None.

### Major

- **Selection of 20 out of 65 eligible subtests is not fully justified**: The authors explain that 45 of 65 FRCT subtests accept text answers, but they select only 20. The criteria for which 20 subtests were chosen (beyond mentioning Figure 5/Table 6 in the appendix) is unclear. This raises a question about whether the benchmark systematically covers all important visual factors or omits some that might be easier for models.

- **Human evaluation has limited sample size and reliability**: With only 31 university students and three independent participants per question, the human baseline may have higher variance than desirable, especially on subtests that are already challenging for humans (e.g., CS1 at 35%). While the overall gap is large, per-subtest comparisons against human performance should be interpreted cautiously.

- **Parametric generation covers only 12 of 20 subtests**: The claim of "unlimited test cases" applies only to a subset of the benchmark. The remaining 8 subtests (including important ones like I3, MV1–MV3, RL2, SS2, VZ3) rely on the original finite item sets, which limits the future-proofing argument for those tasks.

### Minor

- **The "Middle Score Anomaly" discussion is somewhat speculative**: The paper interprets intermediate scores (e.g., 30–50% on P3) as evidence against genuine reasoning, but given the very low chance baseline (3.13%), intermediate scores could also reflect partial perceptual ability. The argument would benefit from a more controlled ablation (e.g., degrading image quality to see if models become random or near-perfect).

- **Temperature sensitivity analysis is narrow**: Only three GPT models were tested at different temperatures. Results might differ for other model families (e.g., Qwen, LLaMA) where decoding behavior is less stable.

### Trivial
- Table 1 column headers appear garbled (e.g., "CoT" repeated) due to PDF parsing; this does not affect the substance.
- The paper references an appendix section (e.g., §C) that is not included; we do not penalize this.

## Nice-to-Haves
- Include a per-factor analysis that aggregates scores across subtests within each of the four cognitive domains (Visualization/Spatial, Perceptual/Closure, Memory, Reasoning) to give a higher-level diagnostic signal.
- Discuss potential mitigation strategies beyond curriculum pre-training, such as architectural changes (e.g., dedicated spatial encoding modules) or training on synthetic psychometric tasks with step-by-step spatial supervision.
- Provide confidence intervals or statistical significance tests for the main results (Table 1) to quantify the reliability of observed differences between models.

## Novel Insights

The paper's failure analysis yields several genuinely novel observations beyond the benchmark itself. The finding that MLLMs succeed on the MA1 memory test primarily through concept-level recognition (translating images into verbal labels) rather than raw visual pattern memorization is revealing—when abstract line figures replace semantically rich images, performance drops dramatically (e.g., GPT-4.1 from ~90% to ~33% at 80 pairs). The discovery of a systematic diagonal bias (models defaulting to 45-degree approximations for any orientation) and the demonstration that start-point identification degrades with marker size (92%→68%) indicate fundamental limitations in continuous spatial perception. The connection to cognitive psychology—where verbalization can *hurt* human visual reasoning—provides a compelling interpretation of why CoT sometimes degrades performance on visuospatial tasks, suggesting that MLLMs' text-mediated reasoning creates a structural mismatch with the spatial cognition these tasks demand.

## Suggestions

- Clarify the selection process for the 20 subtests: state the exact criteria (e.g., diversity of factors, feasibility of digitization, coverage of core visual abilities) and whether any subtests were excluded despite being feasible.
- Report human evaluation with confidence intervals or inter-rater agreement metrics to strengthen the reliability of the human baseline.
- Extend parametric generation to at least a few more subtests from the non-generated set (e.g., I3 or MV1), even with a simpler generation scheme, to strengthen the future-proofing claim.

## Score and Decision

**Score**: 8.5

**Decision**: Accept

MY FINAL SCORE: <score>8.5</score>
MY FINAL DECISION: <decision>Accept</decision>
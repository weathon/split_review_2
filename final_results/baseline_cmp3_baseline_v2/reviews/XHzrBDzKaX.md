## Summary

This paper introduces **VisFACTOR**, a benchmark that digitizes 20 vision-centric subtests from the Factor-Referenced Cognitive Test (FRCT) battery, a well-established cognitive psychology assessment, to evaluate Multimodal Large Language Models (MLLMs) on foundational human visual cognition abilities. The benchmark spans four cognitive domains (Visualization/Spatial Processing, Perceptual/Closure, Memory, and Reasoning) and employs careful design to reduce chance-level accuracy to ~2.9%. Evaluating 23 frontier MLLMs, the best model (GPT-5.1) achieves only 30.17% accuracy, with systematic failures on tasks like mental rotation, spatial relation inference, and figure-ground discrimination, revealing a significant gap between MLLM performance on holistic benchmarks and genuine human-like visual cognition.

## Strengths

- **Strong psychometric grounding**: The benchmark is built upon the established FRCT battery from cognitive psychology, providing a principled, factor-analytic decomposition of visual cognition rather than ad-hoc task design. This gives the evaluation construct validity that many existing benchmarks lack.

- **Rigorous chance-level reduction**: The paper carefully designs multiple-choice variants, grouped-consistency items, and symmetry variants to reduce random guessing accuracy from 22.47% to 2.89%, making the benchmark genuinely diagnostic rather than susceptible to lucky guesses.

- **Comprehensive evaluation**: The paper evaluates 23 frontier models across major families (GPT, Gemini, Claude, LLaMA, Qwen, SEED) with controlled hyperparameters, providing a thorough and reproducible assessment of the current state of MLLM visual cognition.

- **Parametric generation for future-proofing**: The implementation of controllable-difficulty generators for 12 subtests allows the benchmark to scale with model improvements and prevents overfitting, addressing a common limitation of static benchmarks.

- **Insightful failure analysis**: Section 4 provides detailed analysis of why models fail, including the finding that models rely on concept-level recognition rather than low-level visual processing, and specific deficiencies in length/angle/scale perception.

## Weaknesses

### Fatal
None.

### Major

- **Limited novelty of the core finding**: The paper's main result—that MLLMs perform poorly on basic visual reasoning tasks despite strong performance on holistic benchmarks—has been demonstrated in prior work (e.g., Ramakrishnan et al. 2025 on mental rotation, Fu et al. 2024 on Blink). While VisFACTOR is more comprehensive and psychometrically grounded, the fundamental insight is not new. The paper would benefit from more clearly articulating what novel scientific understanding VisFACTOR provides beyond existing benchmarks.

- **Human evaluation limitations**: The human evaluation uses only 31 university students with 20 items per subtest. University students are not representative of the general population, and the sample size is relatively small for establishing a reliable human baseline. The paper reports human performance as 78.8% overall, but this may not reflect the true difficulty of these tasks for humans, especially given that some subtests (e.g., CS1 at 35%) show surprisingly low human performance, suggesting either task difficulty or evaluation issues.

- **Insufficient analysis of the "Middle Score Anomaly"**: The paper observes that models achieve 30-50% on P3 (Identical Pictures) where chance is 3.13%, calling this a "Middle Score Anomaly." However, this pattern could simply reflect that models have partial but imperfect visual capabilities—a perfectly natural outcome for a learned system. The claim that this "suggests that current models lack genuine reasoning capabilities" is not well-supported by the evidence presented.

### Minor

- **The parametric generation evaluation is limited**: Only GPT-4.1 is evaluated on the generated subsets (Table 3), and the "Easy"/"Hard" manipulation shows relatively modest performance differences (28.9% vs 22.0%). The paper would benefit from evaluating multiple models on these generated subsets to demonstrate that the difficulty manipulation is effective across different architectures.

- **The connection to downstream applications is asserted but not demonstrated**: The paper claims that weak foundational vision has "practical ramifications" for embodied AI, safety-critical applications, etc., but provides no empirical evidence linking VisFACTOR performance to downstream task performance.

### Trivial
- The paper uses "VISFACTOR" and "ViSFACtor" inconsistently in the text.

## Nice-to-Haves

- A correlation analysis between VisFACTOR performance and performance on popular holistic benchmarks (MMBench, etc.) would strengthen the claim that these benchmarks measure different capabilities.
- The paper could benefit from testing whether fine-tuning on VisFACTOR data improves performance on downstream tasks, which would validate the benchmark's practical relevance.
- Including more diverse human participants (varying age, education, etc.) would strengthen the human baseline.

## Novel Insights

The paper's most novel insight is the finding that MLLMs' apparent visual capabilities are largely driven by concept-level recognition rather than genuine low-level visual processing. The MA1 experiment (Section 4.1) elegantly demonstrates this: models perform well on memory tasks with semantically meaningful images but fail dramatically when the same task uses abstract line patterns (CF2 figures). This suggests that current MLLMs lack the gestalt-like perceptual capabilities that humans possess, instead relying on verbalizable concept mappings. The paper also provides a systematic catalog of specific visual deficiencies—bias toward diagonal orientations, insensitivity to length/angle/scale, and failure to attend to critical local features—that provides a concrete roadmap for improving MLLM visual capabilities.

## Suggestions

- Strengthen the novelty claim by more explicitly comparing VisFACTOR's diagnostic value to existing benchmarks (e.g., what specific cognitive factors does VisFACTOR measure that Blink or MMT-Bench do not?).
- Expand the human evaluation with a larger and more diverse sample, and report inter-rater reliability.
- Evaluate multiple models on the generated subsets to validate the difficulty manipulation.
- Add a correlation analysis between VisFACTOR and popular holistic benchmarks to empirically demonstrate the gap.

## Score and Decision

The paper presents a well-designed, psychometrically grounded benchmark that systematically evaluates MLLMs on foundational visual cognition tasks. The benchmark design is rigorous, the evaluation is comprehensive, and the failure analysis provides valuable insights. However, the core finding that MLLMs struggle with basic visual reasoning is not entirely novel, and the human evaluation has limitations. The paper makes a solid contribution to the evaluation methodology for MLLMs, but the incremental nature of the core finding and the limited validation of the generated subsets prevent it from being a top-tier contribution.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>
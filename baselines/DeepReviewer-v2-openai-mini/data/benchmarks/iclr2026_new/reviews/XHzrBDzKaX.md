## Summary
# Final Review Report

## Summary

This paper introduces VisFACTOR, a benchmark that digitizes 20 vision-centric subtests from the Factor-Referenced Cognitive Test (FRCT) battery—a well-established cognitive psychology assessment—into an automated multimodal evaluation for MLLMs. The benchmark spans four cognitive domains (visualization/spatial processing, perceptual/closure, memory, reasoning) and covers 10 FRCT factors. A key methodological contribution is the reduction of chance-level accuracy from 22.47% to 2.89% through rule-based variant generation, decomposed multiple-choice scoring, and grouped-consistency items. The paper also implements parametric generation for 12 subtests to enable difficulty-controlled synthetic augmentation.

The authors evaluate 23 frontier MLLMs (GPT, Gemini, Claude, Qwen, LLaMA, SEED, and others) and find that the best model (GPT-5.1) achieves only 30.17% overall accuracy, compared to a human baseline of 78.8%. Consistent failures appear on mental rotation, spatial relation inference, and figure-ground discrimination regardless of model size or prompting strategy. The failure analysis reveals that MLLMs rely heavily on concept-level recognition rather than low-level visual processing, and exhibit specific weaknesses such as coarse categorical representations of spatial orientation (a 45-degree bias) and degraded performance with reduced visual saliency.

**Research value assessment:** The paper makes a meaningful contribution by bringing psychometric rigor to MLLM evaluation. The systematic digitization of established cognitive tests provides a diagnostic tool that existing holistic benchmarks lack. However, novelty verification is deferred (external literature search unavailable in this run), and several methodological concerns (unfair hyperparameter comparisons, incomplete selection transparency, unsupported causal claims about downstream impact) affect the overall assessment.

## Strengths
**1. Psychometric grounding of MLLM evaluation.** The paper's central contribution—digitizing the well-validated FRCT battery for MLLM assessment—is a principled approach. Unlike existing holistic benchmarks that measure aggregate performance on downstream tasks, VisFACTOR provides factor-level diagnostic scores (10 FRCT factors across 20 subtests). This enables researchers to identify specific cognitive deficiencies (e.g., closure flexibility vs. spatial orientation) rather than a single performance number, which is more actionable for guiding model improvement.

**2. Rigorous chance-level control.** The reduction of random-guessing accuracy from 22.47% to 2.89% through decomposed multiple choice, grouped-consistency items, and symmetry variants is carefully designed and well-motivated. The all-or-nothing scoring per item cluster, while strict, ensures that above-chance performance genuinely reflects visual reasoning ability rather than lucky guessing. The 2.89% floor is convincingly low and the per-test cap of 6.25% is clearly documented.

**3. Comprehensive model coverage.** Evaluating 23 frontier MLLMs across proprietary (GPT, Gemini, Claude) and open-source (LLaMA, Qwen) families provides a thorough landscape. The inclusion of reasoning-specialized models (o1, o3, o4-mini, GPT-5.1 with different reasoning efforts) enables meaningful analysis of how model architecture and inference budget affect visual reasoning performance.

**4. Insightful failure analysis.** Section 4's investigation into why models succeed on MA1 (concept recognition rather than low-level perception) and the systematic documentation of specific failure modes (45° angular bias, marker-size sensitivity, text-vs-vision gap on CF3) provides valuable diagnostic information that goes beyond a simple leaderboard. The diagonal orientation bias finding is particularly noteworthy as a concrete, testable hypothesis about MLLM visual processing limitations.

**5. Human baseline.** The inclusion of a human evaluation with 31 participants under the identical digital protocol provides an essential reference point. The 78.8% human accuracy confirms that the benchmark is solvable and that the 30.17% best model score represents a genuine gap rather than task ambiguity. The finding that MLLMs outperform humans on RL2 (Diagramming Relationships) offers a useful boundary condition for interpreting results.

**6. Future-proofing via parametric generation.** The implementation of controllable-difficulty synthetic augmentation for 12 subtests addresses the overfitting risk inherent in finite benchmark sets. The ability to modulate parameters (rotation angle, occlusion, grid size, number of folds) creates a scalable evaluation framework that can adapt as models improve.

## Weaknesses
**1. Unfair model comparison due to inconsistent hyperparameters (Major).** 
*Evidence:* Page 4 - Experiment Settings. Temperature, Top-P, and thinking budget vary across model families (Qwen: T=0.01, Top-P=0.001; LLaMA-3.2: T=0.6, Top-P=0.9; most others: T=0). Thinking budget is "high" for some models but not others. 
*Impact:* The 30.17% best score could be partially attributed to more favorable hyperparameter settings rather than superior visual ability. The CoT token analysis is confounded because models with higher thinking budgets produce longer chains as an artifact of the budget setting, not necessarily greater reasoning depth. 
*Repair:* Standardize hyperparameters (temperature=0, greedy decoding) across all models where API permits. Report sensitivity analysis with matched settings. Document which models required non-standard parameters as exceptions.

**2. Incomplete subtest selection transparency (Major).**
*Evidence:* Page 1 - Section 2.1. The text states "In the remaining 65 subtests, 45 of them can be completed with pure text input. Those demanding visual reasoning but accept text answers form our benchmark." This implies all 45 were selected, yet only 20 appear.
*Impact:* The missing filtering step (45→20) raises concerns about selection bias. If the 20 chosen subtests are those where MLLMs perform worst, the overall score of 30.17% may underestimate capabilities. Conversely, if the 25 excluded tests were excluded for valid reasons (e.g., redundancy, digitization challenges), this should be explicitly documented. Transparency about this selection is essential for scientific reproducibility.
*Repair:* Provide a complete selection flowchart showing counts at each stage and explicit inclusion/exclusion criteria for each of the 20 selected subtests.

**3. Unsupported causal claims about downstream impact (Major).**
*Evidence:* Page 6 - Conclusion. "Hallucinated perception in safety-critical applications, brittle spatial reasoning in robotics, and misaligned multimodal feedback loops all trace back to weak foundational vision." Also Page 0 - Abstract: "rendering high-level downstream applications (e.g., embodied AI) infeasible."
*Impact:* The paper does not provide any evidence that VisFACTOR scores correlate with downstream task performance. The causal chain (poor psychometric test performance → downstream application failure) is asserted but not demonstrated. This weakens the paper's objectivity and may trigger reviewer skepticism.
*Repair:* Either remove these unsupported claims or replace them with testable hypotheses. If correlation data with downstream tasks exist, present them. Otherwise, bound claims to what the benchmark directly measures: "These results suggest that current models lack robust foundational visual skills, which may be relevant for downstream applications that depend on such skills—a hypothesis for future work."

**4. Contribution 2 contains a grammatical error and appears incomplete (Major).**
*Evidence:* Page 1 - Contribution list, Item 2: "Implemented with VLMEvalKit, we digitize FRCT vision items, [devise variants, and synthesize controllable-difficulty items for harder tests and model reinforcement learning](#)."
*Impact:* The bracketed text with the hyperlink symbol suggests an unfinished edit or placeholder. The sentence is grammatically incomplete (missing a main verb for the subject "we"). Contribution statements are the most scrutinized part of a paper; such presentation errors reduce confidence in manuscript carefulness.
*Repair:* Rewrite as a complete sentence: "We implement a VLMEvalKit-based pipeline that digitizes FRCT vision items, generates rule-based variants, and synthesizes difficulty-controlled instances for harder tests and potential model training."

**5. Critical failure analysis lacks methodological rigor (Major).**
*Evidence:* Page 8 - Diagonal bias claim. "In a controlled test with 20 non-45-degree vectors (e.g., vector (2, 1)), models achieve zero correct angular identification." Also Page 7 - CF3 text-vs-vision gap: "when models are provided with textual descriptions... GPT-4.1 achieves perfect accuracy (100%)."
*Impact (Diagonal bias):* The sample of 20 vectors is small, the protocols are incompletely described (which models? visual or text input? single run?), and the claim that models have "only coarse categorical representations" is a strong conclusion from limited data. The confound of training data statistics (natural images over-represent cardinal/diagonal orientations) is not discussed.
*Impact (CF3 gap):* The text condition is only tested on GPT-4.1, while the visual condition covers all 23 models. Without testing multiple models in the text condition, the modality gap claim is under-supported. Additionally, the text format may provide more precise information (exact coordinates) than visual estimation, making the comparison less controlled.
*Repair:* (a) For diagonal bias: test on 3+ models, report per-vector accuracy, discuss training data confound. (b) For CF3: test 2-3 additional models in text condition, describe the exact text prompt format, and discuss information equivalence between modalities.

**6. "First" claim unverifiable in current manuscript (Minor-Moderate).**
*Evidence:* Page 1 - Introduction: "which for the first time, adapts 20 vision-centric FRCT subtests into an automated, multimodal benchmark." Related Work (Page 9) mentions CoreCognition (Li et al., 2025b) and other cognitive-style benchmarks.
*Impact:* Without external literature verification (deferred in this run), the "first" claim cannot be confirmed. CoreCognition and similar works may overlap in using cognitive science frameworks. The "first" qualifier should be scoped precisely.
*Repair:* Replace "for the first time" with a scoped claim: "to our knowledge, the first benchmark to systematically digitize the FRCT battery for MLLM evaluation."

**7. Middle Score Anomaly interpretation overreaches (Minor).**
*Evidence:* Page 5 - "It would be highly unusual for a human to achieve, say, 70% accuracy on this task—suggesting partial understanding but inexplicable failures."
*Impact:* The claim that humans perform either perfectly or at chance on P3 is an intuition, not an empirical observation from the paper. Human perceptual performance can vary continuously due to individual differences and stimulus difficulty. The binary framing is not supported by evidence in the manuscript.
*Repair:* Replace the binary human-performance assumption with a more measured interpretation: "The intermediate performance (30-50% accuracy, well above chance of 3.13%) suggests that models have partial pattern-matching capabilities—sufficient to exceed random guessing but not to achieve consistent accuracy—consistent with noisy perceptual processing rather than robust visual reasoning."

**8. Related work reads as citation lists without structured positioning (Minor).**
*Evidence:* Page 9 - Related Work. Each subsection lists numerous references without articulating clear comparison axes between VisFACTOR and prior work.
*Impact:* Without explicit differentiation along identifiable dimensions (e.g., cognitive factor coverage, chance-level control, synthetic controllability), the novelty claim remains vague. Reviewers may perceive shallow citation coverage.
*Repair:* Add a structured comparison (table or paragraph) mapping each related benchmark to specific axes: number of cognitive factors, synthetic generation capability, chance accuracy level, psychometric validation, and visual stimuli type.

## Score
**Final Score: 6/10**

**Rationale:** The paper addresses an important problem—systematic evaluation of MLLMs' foundational visual abilities—and brings valuable psychometric rigor to multimodal benchmarking. The benchmark design (chance-level reduction, factor coverage, synthetic augmentation) and the extensive evaluation (23 models, human baseline, failure analysis) represent meaningful contributions. However, the score is constrained by several major weaknesses that affect research validity: (1) unfair model comparison due to inconsistent hyperparameter settings across model families, which confounds the headline 30.17% result; (2) incomplete transparency in subtest selection (72→65→45→20, with the critical 45→20 step unexplained); (3) unsupported causal claims about downstream application failures that weaken the paper's objectivity; (4) incomplete methodological detail in key failure-analysis experiments (diagonal bias, CF3 text-vs-vision comparison). These issues are individually fixable but collectively reduce confidence in the reported findings. Novelty verification is deferred (external literature search unavailable in this run), which introduces additional uncertainty about the "first benchmark" claim. With thorough revision addressing the hyperparameter standardization, selection transparency, claim bounding, and methodological rigor, the paper's contribution could warrant a higher score.
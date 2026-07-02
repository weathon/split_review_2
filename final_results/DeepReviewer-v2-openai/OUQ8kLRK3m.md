## Summary
# Final Review Report

## Summary

This paper presents DRE-Bench, a benchmark for evaluating the fluid intelligence of LLMs through abstract reasoning tasks organized across a four-level cognitive hierarchy (Attribute, Spatial, Sequential, Conceptual). The benchmark uses a code-based generator-solver pipeline to dynamically produce grid-based reasoning tasks with controllable complexity, aiming to reduce data contamination risk and provide interpretable, fine-grained assessment. The authors evaluate 11 LLMs (including both general and reasoning-specialized models) and report that: (1) performance declines consistently across cognitive levels, (2) reasoning models outperform general models, especially at higher levels, (3) most models fail at Level-4 conceptual tasks, and (4) in-context learning and inference-time scaling provide limited benefit for high-level reasoning. A human study with 40 annotators validates the expected difficulty progression.

The paper addresses an important problem — measuring genuine reasoning ability beyond memorized knowledge — and proposes a creative benchmark design with a cognitive hierarchy grounding. However, the manuscript has several significant weaknesses: a critical data error in Table 1 (duplicate o3-mini rows with impossible average), insufficient statistical rigor (no confidence intervals on main results), unsupported claims about "100% reliability" and "first" dynamic evaluation, and conflation of fluid vs crystallized intelligence in Level-4 tasks. The cognitive hierarchy's applicability to LLMs is asserted without validation. Novelty assessment is deferred due to unavailable literature retrieval in this review run.

## Strengths
**1. Well-motivated problem and thoughtful benchmark design.** The paper identifies a genuine gap in LLM evaluation — the need to measure fluid intelligence (abstract rule generalization) rather than crystallized intelligence (knowledge recall) — and designs DRE-Bench around a cognitive psychology hierarchy (Primi, 2001). The four-level framework provides a structured approach to diagnose which aspects of reasoning LLMs have mastered, which is more informative than single-score benchmarks.

**2. Dynamic generation pipeline addresses data contamination concerns.** The code-based generator-solver approach is a practical solution to the static-benchmark contamination problem that plagues many LLM evaluations. By varying task parameters (e.g., moving distance, number of steps), DRE-Bench can create numerous variants of each latent rule, making memorization less effective. The human-in-the-loop verification process adds a quality control layer.

**3. Comprehensive model evaluation with interesting findings.** The authors evaluate a wide range of 11 LLMs spanning both general-purpose and reasoning-specialized models. The finding that reasoning models (o1, DeepSeek-R1) significantly outperform general models on higher cognitive levels is informative. The spatial orientation bias discovered (vertical > horizontal accuracy) and the near-zero performance on Level-4 conceptual tasks are genuine contributions to understanding LLM reasoning limitations.

**4. Human validation of the difficulty progression.** The human study (40 annotators) provides evidence that the four-level hierarchy reflects genuine difficulty differences, as human accuracy declines across levels in a pattern consistent with the framework. This strengthens the claim that DRE-Bench measures meaningful cognitive dimensions.

**5. Thoughtful ablation studies.** The paper investigates in-context learning, visual information, and inference-time scaling effects, providing a nuanced picture of what helps (and does not help) LLMs on abstract reasoning tasks. The finding that visual information does not improve — and sometimes harms — performance is particularly non-obvious and valuable.

## Weaknesses
**Critical Issues:**

**W1. Table 1 contains a critical data error (P5 - Main Results).** The model "o3-mini" appears twice (lines 201-202) with entirely different performance figures — e.g., Shape score jumps from 18.33 to 71.67, and Avg-2 for the first entry is listed as 91.78 despite the three constituent values (63.04, 32.10, 0.00) averaging to ~31.71. This is an arithmetic inconsistency that renders the table unreliable as presented. The authors must clarify whether these are two distinct model variants (e.g., o3-mini vs o3-mini-high), correct the Avg-2 calculation, and verify all other averages in Table 1. This error undermines confidence in the quantitative findings and must be corrected before publication.

**W2. Unsupported truth claims about pipeline reliability (P1 - Related Work, P2 - Introduction).** Section 2.2 claims "our data generation process is code-verifiable, ensuring 100% reliability of the generated samples" and Section 3.2 states the pipeline "achieves high correctness." No quantitative verification statistics are provided — no pass rate, no human inspection sample size, no automated consistency check results. Claiming "100% reliability" is scientifically indefensible without exhaustive testing. The authors should report the actual verification rate and acknowledge that code-verifiability enables correctness checking but does not guarantee it.

**W3. Level-4 tasks may conflate fluid and crystallized intelligence (P3-Method/3.1).** Level-4 Conceptual tasks (gravity, reflection, expansion) require models to apply physical concepts. The paper does not clarify whether LLMs are expected to infer these rules from in-context examples (fluid intelligence) or retrieve pre-existing physics knowledge from parametric memory (crystallized intelligence). If models rely on memorized physics knowledge, then poor Level-4 performance may reflect knowledge gaps rather than fluid reasoning deficits. This confound directly threatens the paper's central claim about measuring genuine fluid intelligence. The authors must either (a) redesign Level-4 tasks to use entirely novel physical rules that cannot be known a priori, or (b) explicitly control for prior knowledge and clarify which cognitive faculty is being tested.

**W4. Insufficient statistical rigor in main results (P5 - Experiments/4.1).** Accuracy is defined as exact grid match (binary), which provides no partial credit. While auxiliary metrics exist in the appendix, the main results (Table 1) report only point estimates averaged over 3 trials without standard deviations or confidence intervals. Given small sample sizes (12 samples per variable value), performance gaps of a few percentage points between models may not be statistically significant. The authors should add variance information (standard deviations or confidence intervals) to Table 1 and consider reporting a partial-credit metric in the main text alongside exact-match accuracy.

**Major Issues:**

**W5. "First" claim is overbounded (P3 - Section 2.2).** The paper claims "we are the first to introduce a dynamic evaluation paradigm for abstract reasoning tasks." Prior work on dynamic evaluation (DyVal, NPHardEval) already proposed dynamic generation for reasoning domains. While DRE-Bench may be the first for grid-based abstract reasoning specifically, the current wording invites contradiction. The claim should be scoped precisely: "the first dynamic evaluation paradigm specifically designed for grid-based abstract reasoning tasks."

**W6. Cognitive hierarchy applicability to LLMs is assumed, not validated (P1 - Intro, P3 - Method/3.1).** The paper adopts Primi's (2001) hierarchy from human cognitive psychology but does not justify why this hierarchy should map onto transformer-based LLM reasoning. The human study validates that humans find higher levels harder, but this does not validate that the hierarchy captures distinct LLM reasoning faculties. LLMs may succeed at Level-2 Spatial tasks for reasons unrelated to "spatial reasoning" as defined in psychology (e.g., pattern matching on serialized grid representations). The authors should add analysis showing that model error patterns differ qualitatively across levels, or acknowledge this as a limitation.

**W7. Inference-time scaling analysis is too limited (P8 - Section 4.4).** The analysis uses only o1, only two tasks (Count vs Planning), and does not control for output sequence length when measuring inference time. Longer latencies on Planning may simply reflect longer output sequences rather than "deeper reasoning." The strong claim that "inference time scaling is insufficient for high-level reasoning" requires testing on additional models (e.g., DeepSeek-R1) and tasks with proper length normalization.

**W8. Spatial bias finding lacks mechanistic depth (P8 - Section 4.5).** The observation that LLMs perform better on vertical than horizontal spatial tasks is interesting, but the paper attributes this to "systematic divergences from human cognitive patterns" without proposing any mechanistic explanation. Possible causes (tokenization biases, training data distribution, positional encoding asymmetries, grid serialization effects) are unexplored. Additionally, the claim that humans perceive directions as "equivalent" oversimplifies known human spatial anisotropies.

**Minor Issues:**

**W9. ICL results are overstated relative to actual gains (P7 - Section 4.4).** The text states "increasing training samples leads to noticeable performance improvements" for higher levels, but the actual gains are 2-4% absolute (Level-2: 60→62%, Level-3: 38→42%). These are marginal, not "noticeable." The null result on Level-1 and Level-4 is worth reporting as a finding about ICL's limits.

**W10. Abstract lacks quantitative anchoring (P0 - Abstract).** The abstract describes findings qualitatively ("competent and robust," "struggle with high-level cognition") without any numerical evidence. Adding 1-2 key numbers (e.g., accuracy drop from Level-1 to Level-4) would significantly improve informativeness.

**W11. Conclusion grammar error and overclaim (P9 - Conclusion).** "The results indicates" should be "The results indicate." The conclusion also claims DRE-Bench offers "interpretability, scalability and robustness beyond prior benchmarks" without quantitative evidence for these properties in the paper.

**W12. Incomplete "Work" citation (P7 - Section 4.4).** The citation "(Brown et al., 2020; OpenAI, 2023; Work)" contains "Work" which appears to be a placeholder or incomplete reference.

**Novelty Note:** Due to retrieval-disabled mode (external paper search unavailable), novelty and comparative positioning claims could not be independently verified against the literature. The authors' claims about DRE-Bench being the first dynamic evaluation for abstract reasoning and the novelty of the cognitive hierarchy approach should be manually verified by reviewers against the full related-work landscape.

## Score
**Final Score: 5/10**

**Rationale:** The paper tackles a worthwhile problem (measuring fluid intelligence in LLMs) with a creatively designed benchmark that incorporates a cognitive hierarchy and dynamic task generation. The empirical findings about LLM performance across cognitive levels are informative.

However, the score is constrained by several significant weaknesses. The critical data error in Table 1 (duplicate o3-mini entries with impossible average calculations) undermines trust in the reported numbers and requires immediate correction. The unsupported "100% reliability" and "first" claims, insufficient statistical rigor (missing confidence intervals, binary-only metric), and the potential confound between fluid and crystallized intelligence in Level-4 tasks are substantial methodological concerns. The inference-time scaling analysis is too narrow to support its conclusions. Additionally, novelty and comparative positioning could not be independently verified due to literature retrieval unavailability in this review run.

The paper has a solid conceptual foundation and the benchmark design is thoughtful, but the current presentation has too many unaddressed validity risks and reporting errors to score higher. With corrections to the table error, addition of variance reporting, softening of overclaims, and clearer delineation of fluid vs crystallized intelligence in the task design, the paper could reach a score of 6-7/10.

Post-Revision Target: [6, 7]/10
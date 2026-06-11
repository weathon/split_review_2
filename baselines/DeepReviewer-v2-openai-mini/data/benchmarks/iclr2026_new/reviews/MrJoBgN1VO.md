## Summary
# Final Review Report

## Summary

This paper presents GeoGramBench, a benchmark of 500 geometry problems designed to evaluate LLMs on the "Program-to-Geometry" task—translating procedural drawing code (Asymptote/Matplotlib) into geometric representations and reasoning over them. The benchmark is organized by a three-level taxonomy (Primitive Recognition, Local Relation Composition, Global Abstract Integration) based on geometric complexity. The authors evaluate 19 frontier LLMs, finding that even the strongest models fall below 50% accuracy on the most complex (Abstract) level. Behavioral analyses (RQ1-RQ3) reveal that LLMs can parse basic geometric elements but struggle with compositional integration, and that chain-of-thought reasoning provides limited benefit for spatial abstraction.

The paper addresses a genuinely underexplored capability—program-driven spatial reasoning—and the benchmark construction pipeline is methodologically thoughtful, particularly regarding answer leakage mitigation. However, the paper has several notable weaknesses: (1) a factual inconsistency between the Introduction's reported accuracy drops and Figure 1 data; (2) insufficient statistical rigor in evaluation reporting (no variance or significance testing); (3) taxonomy validation relies on a single model; (4) behavioral analysis is qualitative rather than systematically quantified; and (5) the conclusion lacks a limitations discussion. Despite these issues, GeoGramBench represents a useful contribution to the benchmarking landscape for geometric reasoning.

## Strengths
**S1 — Well-motivated and timely task formalization.** The Program-to-Geometry task fills a genuine gap in the LLM evaluation landscape. While visual geometry benchmarks (e.g., MathVista, GeoSense) test diagram interpretation, they do not assess the ability to construct spatial representations from symbolic code—a capability that is relevant for code-generating models and procedural graphics applications. The formalization is clear and decomposes the challenge into two testable sub-capabilities (construction and reasoning).

**S2 — Rigorous data curation pipeline with novel attention to answer leakage.** The benchmark construction pipeline (Section 4) is methodologically strong. The authors identify a unique vulnerability in Program-to-Geometry benchmarks—answer leakage through code coordinates—and implement targeted mitigation strategies (coordinate rescaling, parameter masking). The human verification process (two rounds, four experts) is thorough, and the three-level taxonomy grounded in geometric complexity rather than reasoning steps is a principled organizational choice.

**S3 — Comprehensive model evaluation.** Evaluating 19 models across proprietary and open-source families at multiple scales provides a broad picture of current capabilities. The multi-sample evaluation (8 responses per problem) appropriately addresses model stochasticity. The taxonomy-aligned analysis (per-level and per-subtype accuracy) enables fine-grained diagnosis of where models succeed and fail.

**S4 — Insightful behavioral analysis and failure pattern identification.** The qualitative analysis (RQ1-RQ3) and the four identified failure patterns (algebraic bias, lack of auxiliary constructions, orientation confusion, symbol grounding issues) provide actionable insights for model developers. The observation that chain-of-thought reasoning provides limited benefit for spatial abstraction is a non-trivial finding that challenges common assumptions about CoT generalization.

**S5 — Clear presentation of main empirical finding.** The headline result—that all models fall below 50% accuracy on the Abstract level—is striking and well-supported by the data. The subtype analysis further reveals that angle and volume problems are particularly challenging, providing specific targets for improvement.

## Weaknesses
### W1 — Factual Inconsistency in Introduction (Page 1 - Introduction, Paragraph 3)

**Severity: Major | Type: Issue**

The Introduction states that DeepSeek-R1 "suffers substantial drops in accuracy: 23.5% in AIME24 and 10.9% in MATH-500" when transitioning from text-only to text+code problems. However, Figure 1(b) and 1(c) report different values: R1 drops 15.1% in AIME24 (63.9% to 48.8%) and 15.3% in MATH-500 (84.2% to 68.9%). Neither 23.5% nor 10.9% matches R1's data. These numbers appear to correspond to other models (QwQ-32B drops 23.0% in AIME24; GPT-o1 drops 15.9% in MATH-500), but the attribution to DeepSeek-R1 is incorrect. This factual error undermines the credibility of the empirical motivation and must be corrected before publication.

**Required action**: Correct the numbers to match Figure 1 data, or rephrase to cite the appropriate model for each drop value.

### W2 — Taxonomy Validation Relies on a Single Model (Page 1 - Section 3.2, Taxonomy)

**Severity: Major | Type: Issue**

The taxonomy validation in Section 3.2 uses only QwQ-32B performance on MATH-500 to argue that geometric complexity (not reasoning steps) is the primary challenge. A single-model validation on a small subset (42 $\\mathbb{P}_{TC}$ problems from MATH-500) is insufficient to support a claim that is central to the paper's organization. Furthermore, the accuracy pattern is non-monotonic: QwQ-32B achieves 86.2% on Abstract vs. 56.9% on Compositional problems, which contradicts the expected difficulty ordering and is not explained. The authors should (a) validate the taxonomy on at least 3 models, (b) compute statistical significance, and (c) explain the non-monotonicity.

**Required action**: Expand taxonomy validation to multiple models and provide significance tests. Explain why Abstract sometimes shows higher accuracy than Compositional.

### W3 — Evaluation Protocol Lacks Statistical Rigor (Page 6 - Section 5.1)

**Severity: Major | Type: Suggestion**

The evaluation protocol reports only mean accuracy over 8 samples (temperature 0.6) without any variance or confidence intervals. In a benchmark paper that aims to establish a standardized evaluation framework, the absence of statistical reliability measures is a significant gap. Readers cannot determine whether the reported accuracy differences between models (e.g., GPT-5 at 75.01% vs. Qwen3-235B at 74.00%) are statistically significant. The choice of temperature 0.6 is also not justified. Additionally, the prompt template "Let's think step by step" is known to interact differently with different model families, but this is not discussed as a potential confound.

**Required action**: Report standard deviation or 95% CI alongside mean accuracy. Add bootstrap-based significance tests for key model comparisons. Discuss how prompt template and temperature choices may affect results.

### W4 — Behavioral Analysis Is Qualitative and Not Systematically Quantified (Page 7-8 - Section 6)

**Severity: Major | Type: Suggestion**

The behavioral analysis (RQ1-RQ3) and the Common Failure Patterns section rely heavily on illustrative model response quotes and anecdotal observations. While the authors honestly note the lack of "accurate automated assessment methods," this does not excuse the absence of a systematic error annotation study. Key claims such as "LLMs rarely introduce auxiliary lines" and "models exhibit a pronounced preference for algebraic methods" are not backed by frequency statistics. Without quantification, these insights—while plausible—remain at the level of reviewer impressions rather than rigorous empirical findings.

**Required action**: Conduct a small-scale error annotation study (e.g., 100-200 failure cases, stratified by model and difficulty level) with inter-annotator reliability, and report the distribution of error types.

### W5 — Conclusion Lacks Limitations Discussion (Page 9 - Section 7)

**Severity: Minor | Type: Suggestion**

The conclusion does not include a limitations section. For a benchmark paper, readers expect a brief discussion of scope boundaries (e.g., coverage limited to Asymptote/Matplotlib code, potential contamination from source datasets, restriction to numeric-answer problems, lack of open-ended reasoning evaluation). The absence of limitations weakens the scientific framing and may lead readers to over-interpret the benchmark's coverage.

**Required action**: Add a short limitations paragraph to the conclusion.

### W6 — Related Work Lacks Explicit Comparison Axes (Page 1 - Section 2, Symbolic Graphics)

**Severity: Minor | Type: Suggestion**

The SVG benchmark paragraph (Section 2, third paragraph) states that existing SVG benchmarks differ from GeoGramBench but does not articulate the specific comparison axes. The reader is left wondering: is the difference in the type of reasoning (perceptual vs. deductive), the format (SVG vs. Asymptote), or the depth (parsing vs. construction+reasoning)? Explicit differentiation would strengthen the novelty positioning.

**Required action**: Add one sentence that explicitly contrasts evaluation dimensions (e.g., "SVG benchmarks primarily test perceptual parsing, whereas GeoGramBench requires spatial construction + deductive reasoning").

### W7 — Missing Details in Data Augmentation Process (Page 5 - Section 4.4)

**Severity: Minor | Type: Suggestion**

The transcription of Mathverse diagrams into matplotlib code is described in a single sentence without detail on quality assurance, inter-rater reliability, or whether any problems were discarded due to transcription difficulty. The claim of "minimal impact from drawing language" is referenced to Appendix A without a main-text summary.

**Required action**: Briefly summarize the control experiment results in the main text and describe the transcription verification process.

### W8 — Difficulty Categorization Contains Minor Inconsistency (Page 5-6 - Section 4.5)

**Severity: Minor | Type: Suggestion**

The text states that Volume problems are introduced only at the Abstract level, but Figure 5 shows Volume listed under all three levels. Additionally, the claim "largest and most diverse benchmark for the Program-to-Geometry task to date" is vacuously true since the task is newly formalized.

**Required action**: Resolve the Volume subtype inconsistency and replace the "largest and most diverse" claim with a more measured statement.

### W9 — Task Definition Lacks Language Scope (Page 2 - Section 3.1)

**Severity: Minor | Type: Suggestion**

The Program-to-Geometry task is defined in a language-agnostic way, but the benchmark uses only Asymptote and matplotlib. A brief scope statement would clarify whether the task formulation is intended to be general or specifically tied to these languages.

**Required action**: Add a sentence specifying that the task is language-agnostic but the current benchmark operationalizes it with Asymptote and matplotlib.

## Score
**Final Score: 6/10**

### Scoring Rationale

**Research Value (8/10):** The Program-to-Geometry task is a well-motivated and genuinely underexplored capability. GeoGramBench addresses a gap that exists between visual geometry benchmarks and symbolic graphics benchmarks, and the answer leakage mitigation strategy is a methodological contribution that will benefit future benchmark builders. The comprehensive evaluation across 19 models provides a useful snapshot of current limitations. The paper has clear potential to influence how the community evaluates spatial reasoning in LLMs.

**Novelty (Deferred — Retrieval-Disabled Mode):** External literature verification is unavailable in this run due to API token limitations. Based on internal evidence, the formalization of Program-to-Geometry as a distinct task and the geometric-complexity-based taxonomy appear original. However, a proper novelty assessment against prior program-driven reasoning benchmarks (e.g., Muennighoff et al., 2025; SVG-related work cited in the paper) requires manual literature verification, which is deferred.

**Validity & Soundness (5/10):** The paper has several notable validity concerns that lower confidence in the current version:
- A factual inconsistency between the Introduction's reported accuracy drops and Figure 1 data (W1) directly affects the credibility of the empirical motivation.
- The taxonomy, a core contribution, is validated on only a single model with unexplained non-monotonic accuracy patterns (W2).
- The evaluation protocol lacks variance reporting and significance testing (W3), making it impossible to assess whether model ranking differences are reliable.
- The behavioral analysis relies on qualitative examples rather than systematic error annotation (W4).

These issues are fixable, but they currently limit how much confidence a reader can place in the paper's central claims.

**Reproducibility & Reusability (7/10):** The benchmark construction pipeline is described in sufficient detail to be reproducible. The evaluation framework uses publicly available models and APIs. The main gaps are the missing statistical detail (W3) and the lack of clarity on matplotlib transcription verification (W7), which slightly reduce reusability.

**Overall:** GeoGramBench is a valuable addition to the LLM evaluation ecosystem with a well-designed benchmark and a strong headline finding. However, the factual error in the Introduction, the insufficient taxonomy validation, and the lack of statistical rigor in the evaluation protocol are non-trivial weaknesses that should be addressed before the paper can be considered publication-ready. The score reflects a solid contribution that is currently weakened by fixable methodological gaps.
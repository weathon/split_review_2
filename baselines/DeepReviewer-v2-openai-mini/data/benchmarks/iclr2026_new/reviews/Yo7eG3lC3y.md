## Summary
This paper introduces LEGO-EVAL, a tool-augmented evaluation framework for assessing the alignment between fine-grained textual instructions and generated 3D scenes. The framework augments vision-language models (VLMs) with 21 domain-specific tools across three categories (Environment Interaction, Textual Reasoning, Multimodal Reasoning) to perform multi-hop grounding: identifying scene components, verifying their attributes, and checking spatial relationships. The authors also release LEGO-BENCH, a benchmark of 130 natural-language instructions with 1,250 constraints covering floor layouts, materials, object selection, and placement.

The main empirical results show that LEGO-EVAL (with GPT-4.1) achieves 0.81 F1 and 0.63 Cohen's kappa in agreement with human judgments, substantially outperforming VLM-as-a-judge baselines (0.40 F1, 0.05 kappa). When used to benchmark existing LLM-based 3D scene generation methods on LEGO-BENCH, all evaluated approaches satisfy at most 10% of fine-grained instructions holistically, revealing significant limitations in current generation capabilities. The paper also demonstrates LEGO-EVAL's utility as a feedback signal for iterative scene refinement, improving Holodeck's holistic success rate from 8.5% to 18.5% over three refinement rounds.

The core idea—decomposing complex instructions into atomic constraints and evaluating them via specialized tools—is well-motivated and the empirical gains are substantial. However, the paper has several notable weaknesses: a critical logical inconsistency in the case study (Figure 8), missing statistical rigor (no confidence intervals or significance tests), underspecified experimental protocols (particularly for the refinement loop), an overclaim of "robustness" without supporting evidence, and modest benchmark scale. Novelty assessment is deferred as external literature verification was unavailable in this run.

## Strengths
1. **Well-motivated and timely problem.** The paper identifies a genuine bottleneck in 3D embodied AI research: while automatic scene generation has advanced, reliable evaluation of generated scenes against fine-grained constraints remains unresolved. The multi-hop grounding concept (identify components → verify attributes → check spatial relations) provides a clear framing for why existing methods (CLIPScore, vanilla VLM scoring) fall short.

2. **Impressive empirical gains.** LEGO-EVAL's F1 score of 0.81 and Cohen's kappa of 0.63 represent a substantial improvement over VLM-as-a-judge baselines (0.40 F1, 0.05 kappa). The gap is large enough that the qualitative advantage is convincing even without formal significance testing. The tool-augmented approach clearly addresses the multi-hop grounding limitation identified in the problem analysis.

3. **Principled four-stage evaluation pipeline.** The decomposition into (1) constraint identification, (2) tool execution planning, (3) argument selection and execution, and (4) constraint validation is logically sound and well-aligned with the multi-hop grounding requirement. The graph-structured execution plan with parallel tool support adds practical efficiency.

4. **Comprehensive tool set.** The 21 tools across three categories (Environment Interaction, Textual Reasoning, Multimodal Reasoning) are thoughtfully designed to cover the diverse aspects of 3D scene understanding. The ablation study confirms that all three categories contribute to overall performance, with Environment Interaction being the most critical.

5. **Useful diagnostic tool for the community.** The finding that all four evaluated generation methods satisfy at most 10% of fine-grained instructions holistically is an important empirical result that clearly demonstrates the gap between current generation capabilities and real-world requirements. LEGO-EVAL could serve as a valuable diagnostic and benchmarking tool for future research in 3D scene synthesis.

6. **Refinement demonstration.** The iterative refinement experiment (improving Holodeck from 8.5% to 18.5% holistic success rate) shows a practical application of the framework beyond pure evaluation, hinting at its potential as a training signal for generation models.

## Weaknesses
### W1 — Critical Logical Inconsistency in Figure 8 Case Study (Major)
**Location:** Page 8 — Case Study in Section 5

The case study in Figure 8 presents a fundamental logical error in LEGO-EVAL's output. For a scene where neither the flashlight nor the laptop is present, LEGO-EVAL outputs **"Valid ✓"** while simultaneously stating "Since neither object is present, there is no way to assess whether the flashlight and the laptop are facing the same way. This means the constraint cannot be satisfied." The binary judgment (Valid ✓) directly contradicts the reasoning (constraint cannot be satisfied). A correct evaluation should output **"Invalid ✗"** because the scene fails to meet the specified constraint. This inconsistency suggests a possible bug in how LEGO-EVAL derives binary judgments from its constraint evaluation reasoning. If this error is systematic, the reported F1 scores may be unreliable — scenes could receive valid judgments when they contain missing objects simply because the framework treats "cannot assess" as "no violation." The authors must investigate and correct this decision logic, then re-run experiments to verify whether F1 scores change.

### W2 — Missing Statistical Rigor (Major)
**Location:** Page 5 — Table 1 and Section 4.1

All reported metrics (F1, precision, recall, Cohen's kappa) in Table 1 are point estimates without any uncertainty quantification. No confidence intervals, standard deviations, or statistical significance tests are provided. This is a significant omission for several reasons. First, with only 260 instruction-scene pairs, the estimates may have substantial sampling variability. Second, Cohen's kappa of 0.63 for LEGO-EVAL versus 0.05 for VLM baselines is a large gap, but without confidence bounds, readers cannot assess the precision of these estimates. Third, the comparison of different LEGO-EVAL backbones (GPT-4.1 vs. GPT-4.1-mini vs. Qwen2.5VL-32B) lacks any indication of whether the performance differences are meaningful. At minimum, the authors should report bootstrapped 95% confidence intervals for all metrics and include a paired significance test between LEGO-EVAL and the strongest VLM baseline.

### W3 — Asymmetric Comparison in Evaluation Methods (Major)
**Location:** Page 5 — Section 4.1.1

The comparison between LEGO-EVAL and baselines is structurally asymmetric. LEGO-EVAL uses tool-augmented reasoning, access to structured scene metadata (object lists, coordinates, room layouts), and multiple tool execution steps, while the VLM-as-a-judge baseline only receives scene images from four perspectives. The comparison conflates two factors: (1) the tool-augmented reasoning approach, and (2) access to privileged scene information. A fairer comparison would give VLM baselines access to the same structured information (e.g., as text descriptions of object lists and positions) or restrict LEGO-EVAL to only using rendered images. The authors should include an additional baseline where a VLM receives both images and structured scene metadata as text input, to isolate the benefit of the tool orchestration framework from the benefit of additional input information.

### W4 — Underspecified Refinement Experiment Protocol (Major)
**Location:** Page 8 — "LEGO-EVAL as a feedback signal for refinement"

The refinement experiment is presented as evidence of LEGO-EVAL's practical utility, but the experimental protocol is critically underspecified. The paper states "use LEGO-EVAL to evaluate scenes generated by Holodeck, then provide feedback to refine invalid scenes" without explaining: (a) how the feedback is formatted and conveyed to the generation system, (b) what specific changes are made between iterations, (c) whether the refinement uses the same LLM or a separate refinement module, and (d) how the VLM feedback baseline is matched for structure and information content. Without this detail, the experiment is not reproducible and the results cannot be properly interpreted. The authors should provide the complete prompt used for refinement, the feedback format, and the exact experimental procedure in the appendix.

### W5 — Overclaim of "Robustness" Without Supporting Evidence (Moderate)
**Location:** Page 1 — Abstract, Page 9 — Conclusion

The abstract and conclusion claim "significant improvements in robustness," but the experiments exclusively measure agreement with human judgments, not robustness to domain shifts, input perturbations, noise, or varying conditions. The term "robustness" in evaluation contexts typically refers to stability under challenging conditions (e.g., different render qualities, scene styles, camera angles, lighting conditions). None of these are tested. The authors should replace "robustness" with "accuracy" or "reliability" to accurately reflect what was measured.

### W6 — Limited Benchmark Scale and Missing Annotation Protocol (Moderate)
**Location:** Page 4 — Section 3.3

LEGO-BENCH contains 130 instructions with 1,250 constraints. While this is a useful starting point, 130 instructions is modest for benchmarking scene generation methods, particularly when evaluating holistic success rates (where only 10% of instructions pass). With approximately 13 successes out of 130, the confidence intervals around success rates are wide. Additionally, the benchmark construction lacks transparency: the paper does not report how many annotators were used, inter-annotator agreement on constraint annotation, or how scenes were selected to avoid bias. The authors should report these reliability metrics and discuss plans for scaling the benchmark.

### W7 — Figure 8 LEGO-EVAL Output Has Additional Error (Moderate)
**Location:** Page 8 — Figure 8, LEGO-EVAL panel

Beyond the Valid/Invalid inconsistency (W1), the LEGO-EVAL output in Figure 8 contains an additional logical error. It states "Since neither object is present" but the scene image description (line 303) clearly shows a laptop on the desk: "A 3D rendered room scene. It contains a desk with a lamp, a chair, a plant in a pot with a red ribbon, and a laptop on the desk." So the laptop IS present; only the flashlight is missing. LEGO-EVAL incorrectly claims neither object is present. This raises concerns about the reliability of LEGO-EVAL's object detection tools. The authors should verify whether this is a tool failure (object detection missed the laptop) or a reasoning failure (LLM ignored tool output), and report the frequency of such failures.

### W8 — Confounded Ablation Conditions (Minor)
**Location:** Page 6 — Section 4.1.3, Table 2

The ablation study disables tool categories but retains "tools returning list of scene components" in all conditions by necessity. This means the "w/o T" condition (without Textual Reasoning) still uses some textual tools, creating a confound. The authors should clarify exactly which tools remain enabled in each ablation condition and consider a complementary ablation where list-returning tools are controlled separately. Additionally, only F1 changes are reported; reporting kappa, precision, and recall changes would give a more complete picture of each tool category's contribution.

### W9 — Acronym Mismatch and Narrative Positioning (Minor)
**Location:** Page 1 — Abstract, Introduction

The acronym LEGO-EVAL is expanded as "Language-guided Environment Generation for embodied agents," but the paper's contribution is an *evaluation* framework, not a generation method. This creates confusion about the paper's focus. Additionally, the introduction spends considerable space discussing the challenges of scene *generation* (manual creation is costly, LLM generation is coarse) before revealing that the contribution is an *evaluation* framework. Consider renaming to clarify the evaluation focus and restructuring the introduction to foreground the evaluation gap earlier.

### W10 — Novelty Assessment Deferred (Deferred)
Due to external literature search being unavailable in this run (Retrieval-Disabled Mode), novelty and positioning conclusions cannot be verified against the literature. The authors' positioning against SceneEval, CLIPScore, and VLM-as-a-judge appears reasonable from the manuscript content, but a thorough assessment of overlap with tool-augmented VLM frameworks (VisProg, ViperGPT, AVIS, Chameleon) and other 3D evaluation methods requires dedicated literature verification. The authors should ensure their novelty claims are precise and bounded in the final manuscript, particularly regarding the distinction between general tool-augmented reasoning and domain-specific 3D scene evaluation.

## Score
**Final Score: 6/10**

**Rationale:** The paper addresses a well-motivated and timely problem — reliable evaluation of fine-grained 3D scene synthesis — and presents a tool-augmented framework that achieves substantially higher agreement with human judgments than existing methods. The empirical gains (0.81 vs 0.40 F1) are compelling and the four-stage evaluation pipeline is principled.

However, the score is limited by several significant weaknesses. The critical logical inconsistency in Figure 8 (LEGO-EVAL outputs "Valid ✓" while stating the constraint cannot be satisfied, and also misidentifies the laptop as absent) raises questions about the reliability of the binary judgments that underpin all reported metrics. The complete absence of confidence intervals, significance tests, or variance estimates for any experimental result limits the scientific rigor. The asymmetric comparison against VLM baselines (which lack access to structured scene information) and the underspecified refinement protocol reduce confidence in the experimental conclusions. Additionally, the "robustness" claim in the abstract and conclusion is unsupported by the evidence presented.

These issues are fixable: correcting the judgment logic, adding proper statistical reporting, controlling for information access in baselines, and tempering unsupported claims would substantially strengthen the paper. External novelty verification was deferred in this run due to literature search unavailability.

**Post-Revision Target: [7, 8]/10** — achievable if the Figure 8 inconsistency is resolved, statistical rigor is added, and experimental protocols are fully specified.
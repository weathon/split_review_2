## Summary
# Final Review Report

## Summary

This paper presents TARS (Tactile Affordance in Robot Synesthesia), a framework for dexterous robotic manipulation that integrates visual and tactile modalities through a unified point cloud representation. The key idea is to combine visual-tactile synesthetic encoding (mapping both modalities into a shared 3D space) with visual-tactile affordance learning (predicting contact-relevant features from visual input even before contact). The framework is trained via teacher-student reinforcement learning in Isaac Gym and evaluated on four simulated manipulation tasks.

The manuscript tackles a relevant and underexplored problem: seamless handling of both contact and non-contact states in visuo-tactile manipulation. However, the manuscript in its current form has severe structural and completeness issues that prevent scientific evaluation. **Critical problems include:** (1) Section 3.2 is titled "Visual-Tactile Affordance" but contains an unrelated finite-element model of a soft-bubble tactile sensor, with no description of the actual affordance learning module; (2) the Conclusion describes a soft-bubble FEM force estimation method that has no connection to the TARS framework; (3) all referenced tables (Tab. I, II, III) and key figures (Fig. 3-5) are missing from the manuscript; (4) the VTP loss function equation is referenced but not shown; (5) references [9]-[42] are cited but not included; and (6) "real-world experiments" are claimed in the introduction but no real-world results appear in the experimental section. These issues suggest the manuscript may have been assembled from multiple source documents with incomplete editing.

Due to Retrieval-Disabled Mode (external paper search unavailable in this run), novelty and literature comparison conclusions are deferred for manual verification. This review is grounded entirely in manuscript evidence.

## Strengths
1. **Relevant and timely problem formulation.** The paper addresses a genuine gap in robotic manipulation: handling the transition between contact and non-contact states when fusing visual and tactile modalities. This is an important practical problem for real-world deployment where reliable tactile feedback is intermittent.

2. **Unified point cloud representation is a sound design choice.** Encoding both visual and tactile data as point clouds processed through a shared PointNet encoder is a principled approach to cross-modal fusion. It avoids the complexity of separate modality-specific architectures and naturally supports the teacher-student distillation framework.

3. **Well-structured training framework.** The use of SAC-trained teacher policies with privileged information, distilled via DAgger into student policies that only use available sensory input, follows established sim-to-real best practices. The Gaussian Mixture Density output is appropriate for handling multimodal action distributions in manipulation tasks.

4. **Four diverse manipulation tasks.** The task suite (Lift, Pick and Place, Pull Drawer, Open Door) covers both single-stage and multi-stage scenarios with varying contact requirements, providing a reasonable testbed for evaluating the framework's capabilities.

5. **Ablation design covers meaningful comparisons.** The three baselines (RS, VA, PN+MLP) are designed to isolate the contributions of: (a) classification encoding, (b) affordance prediction, and (c) raw point cloud features. This is a methodologically sound ablation strategy when the tables are present.

## Weaknesses
The following weaknesses are ordered by severity (critical first), consistent with the ranked defect board.

### Critical Issues

**W1. Section 3.2 content mismatches its title and claimed contribution.**
Section 3.2, titled "Visual-Tactile Affordance," contains a detailed finite-element model of a soft-bubble tactile sensor (membrane tension, Young's modulus, Reissner-Minlin plate theory, Equations 1–13). This content has no connection to affordance learning. The actual Visual-Tactile Affordance (VTA) module—the core claimed contribution—is never described. Readers cannot determine how affordance labels are generated, what network architecture is used, or how affordance predictions are integrated into the policy. This is a fatal completeness error that makes the paper's central technical contribution unverifiable. *(See pdf_annotate: Section 3.2 misalignment.)*

**W2. Conclusion describes a different paper.**
Section 5 (Conclusion) reads: "We presented a finite element force estimation method for soft-bubble grippers with only three parameters that can be calibrated with small amounts of data." This describes a soft-bubble force estimation method, not the TARS framework. The conclusion does not summarize the TARS results, ablation findings, or manipulation task outcomes. This suggests the manuscript was compiled from multiple sources without proper editing. *(See pdf_annotate: Conclusion mismatch.)*

**W3. All experimental tables and key figures are missing.**
Tab. I (baseline comparisons), Tab. II (generalization tests), and Tab. III (training dynamics) are repeatedly referenced in the text but absent from the manuscript. Likewise, Fig. 3 (tactile decoupling), Fig. 4 (VTP framework), and Fig. 5 (task visualizations) are missing. A paper cannot be evaluated without its core empirical evidence. Claims such as "our method achieves the best overall performance" and "significant improvement" are unsupported. *(See pdf_annotate: Missing tables.)*

**W4. VTP loss function equation is missing.**
The manuscript states "The loss function for the VTP module is shown as follows:" but no equation follows. The subsequent text describes the kernel function and mixing coefficients without providing the actual loss expression. This prevents understanding of the student policy's training objective and makes the method non-reproducible. *(See pdf_annotate: Missing loss function.)*

**W5. Incomplete reference list.**
The related work section cites references [9]–[13], [14]–[17], [18]–[19], [20]–[27], [28]–[32], [33]–[42], but the provided reference list only includes entries up to the 7th reference. The remaining ~35 references are missing. Without these, claims about prior work and the positioning of TARS relative to existing methods cannot be verified. *(See pdf_annotate: Missing references.)*

### Major Issues

**W6. Real-world experiment claim is unsubstantiated.**
The introduction states "we successfully conducted real-world experiments to demonstrate the applicability of our approach," yet Section 4 (Experiments) describes only simulation experiments in Isaac Gym. No real-world setup, results, trials, or success rates are reported. This is a clear claim-evidence mismatch. *(See pdf_annotate: Real-world claim.)*

**W7. Weak introduction narrative and novelty positioning.**
The first introduction paragraph reads as a general sensor survey rather than establishing a motivated research gap. The claim "we are the first to apply these concepts to a robotic system using optical tactile sensors and external cameras" is too strong without verified literature support (Retrieval-Disabled Mode prevents external verification in this run). The differentiation from prior synesthesia work [18, 19] and affordance work [24, 26] is not clearly articulated. *(See pdf_annotate: Intro paragraph 1, "first to apply" claim.)*

**W8. Abstract lacks quantitative anchoring.**
The abstract describes the approach and mentions "extensive experiments" but provides no specific performance numbers. A reader cannot determine whether the method is effective or by how much it improves over baselines. *(See pdf_annotate: Abstract revision.)*

**W9. Equation formatting errors hinder reproducibility.**
Equations (3), (6), (9), and (11) contain non-standard notation (semicolons, colons, missing brackets, undefined indices). While the underlying FEM physics is standard, the notational errors suggest insufficient proofreading and can lead to implementation ambiguity. *(See pdf_annotate: Equation formatting.)*

**W10. Sim-to-real gap and tactile simulation fidelity are not analyzed.**
The tactile simulation uses "linearly adjusted" force predictions from a CNN trained on real tactile images, but no analysis is provided on how accurate this linear adjustment is, how much domain gap exists, or how sensitive the policy is to tactile simulation inaccuracies. Given that the paper emphasizes real-world applicability, this analysis is essential. *(See pdf_annotate: Real-world claim.)*

### Minor Issues

**W11. Mixing coefficient description is ambiguous.**
The text states "mixing coefficient = 0.1, ..., 0.9" without clarifying whether these are fixed constants or learned parameters of the Gaussian mixture output. If fixed, the normalization constraint (sum to 1) and the learning mechanism need clarification. *(See pdf_annotate: Missing loss function.)*

**W12. Related work is organized as a list rather than a comparison-driven narrative.**
While the three subsections cover relevant categories, each reads as a literature sweep with generic positioning ("represents a significant advancement"). The section would benefit from explicit comparison axes and clear differentiation statements for each prior work cluster. *(See pdf_annotate: Related work.)*

### Novelty and Comparison Note (Deferred)

Due to Retrieval-Disabled Mode (external paper search unavailable in this run), all novelty and literature comparison conclusions are deferred for manual verification. This review does not make external-evidence-dependent judgments about SOTA status, novelty ranking, or strongest-baseline positioning. The authors are advised to conduct a thorough literature review and clearly position TARS against the most relevant prior works, especially [18, 19] (synesthesia) and [24, 26] (affordance).

### ASCII Diagram — Paper Structure & Evidence Map

```text
[Problem: Visuo-tactile integration for contact/non-contact transitions]
    |
    ├── [Claim C1: Unified point cloud representation for both modalities]
    |       └── Evidence: Missing (VTA module not described; Section 3.2 is wrong content)
    |
    ├── [Claim C2: Visual-tactile affordance learning without CAD models]
    |       └── Evidence: Missing (no affordance network architecture or training described)
    |
    ├── [Claim C3: Teacher-student distillation for sim-to-real transfer]
    |       └── Evidence: Partial (VTP framework outlined but loss function missing)
    |
    └── [Experimental validation on 4 tasks]
            └── Evidence: Missing (Tab. I-III absent; real-world results absent)
```

### ASCII Diagram — Revision Strategy Roadmap

```text
[Current State: Manuscript with severe structural issues]
    |
    ├── P0 Fix (before submission):
    |   ├── Replace Section 3.2 with actual VTA description
    |   ├── Replace Conclusion with TARS summary
    |   ├── Insert all missing tables (I, II, III) and figures (3, 4, 5)
    |   ├── Insert VTP loss function equation
    |   └── Include complete reference list [1]-[42]
    |
    ├── P1 Fix (high priority):
    |   ├── Add real-world experiment results or remove claim
    |   ├── Revise "first to apply" claim with scoped, defensible language
    |   ├── Add concrete prior-work citations to substantiate gap
    |   └── Fix equation formatting errors
    |
    └── P2 Fix (quality improvement):
        ├── Add quantitative results to abstract
        ├── Restructure related work as comparison-driven narrative
        ├── Add sim-to-real gap analysis
        └── Clarify mixing coefficient learning mechanism
```

## Score
**Final Score: 3/10**

**Rationale:** The score reflects that the paper tackles a relevant problem and has a reasonable conceptual framework, but the manuscript in its current form is not scientifically evaluable due to three fatal completeness issues: (1) the core technical contribution (VTA module) is entirely missing from Section 3.2, replaced by unrelated content; (2) all experimental evidence (Tab. I, II, III) is absent; and (3) the conclusion describes a different paper. These issues prevent assessment of validity, reproducibility, and contribution magnitude. The score weights research value (the idea is worthwhile) lower than completeness and validity (the execution is critically incomplete). Novelty cannot be assessed without the missing reference list and without external literature retrieval (deferred due to Retrieval-Disabled Mode).

**Revision outlook:** The underlying framework idea has potential. If the authors address the P0 fixes (restore Section 3.2 content, insert tables, replace conclusion, add loss function, complete references), the paper could be re-evaluated at a substantially higher score in the 5-7 range depending on the strength of empirical results and novelty positioning.
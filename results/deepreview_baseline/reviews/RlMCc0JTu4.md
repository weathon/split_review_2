## Summary

The paper proposes TARS, a framework for dexterous robotic manipulation that integrates visual and tactile modalities through a unified point cloud representation. The claimed contributions include a visual-tactile affordance module (VTA), a visual-tactile policy module (VTP), and a teacher-student training pipeline to handle both contact and non-contact states. The evaluation is performed on four simulated manipulation tasks (Lift, Pick and Place, Pull Drawer, Open Door) with comparisons to three baselines.

## Strengths

- The problem of smoothly integrating visual and tactile feedback across contact and non-contact states is relevant and important for dexterous manipulation.
- The use of a unified point cloud representation for both modalities is a conceptually clean design choice.

## Weaknesses

### Fatal

- **The paper is not a coherent, self-contained research paper.**  The content is a corrupted combination of two distinct papers. Section 3.2, titled “Visual-Tactile Affordance,” instead presents an unrelated finite-element force estimation model for soft-bubble grippers (Equations 1–13), with no connection to affordance learning. The conclusion (Section 5) and the first reference are from a different work on soft-bubble force estimation. This contamination makes it impossible to evaluate the claimed TARS framework because the method description is fundamentally wrong and incomplete.

- **Key experimental results are missing.**  The paper refers to Table I, Table II, and Table III in the text, but no tables are actually present. The results that are discussed qualitatively (e.g., “Tab. I, demonstrate that our method… achieves the best overall performance”) cannot be verified. Without the actual data, the core empirical claims are unsupported.

- **Core method components are not described.** The paper fails to explain how the visual-tactile affordance (VTA) module is trained, what its loss function is, or how it produces affordance predictions from point clouds. The VTP section includes a placeholder equation for the loss function (“where …”), but the actual expression is missing. The Gaussian mixture density model and the teacher-student distillation are mentioned but not sufficiently detailed to allow reproducibility.

### Major

- **The paper is essentially unreviewable in its current form.** The mixture of unrelated content, missing tables, and incomplete method descriptions mean that no informed assessment of the technical contribution or experimental validation is possible.

### Minor

- The paper claims to be “the first to apply these concepts to a robotic system using optical tactile sensors and external cameras,” but this claim is not substantiated with proper citations to earlier visual-tactile synesthesia work.

### Trivial

- None.

## Nice-to-Haves

- The idea of a unified point-cloud representation for visual and tactile data has merit. A clean, self-contained paper with complete method descriptions and full experimental tables would be interesting to evaluate.

## Novel Insights

None beyond the paper’s own contributions—the paper as presented does not contain a coherent exposition from which novel insights could be extracted.

## Suggestions

- The authors should carefully re-assemble the correct version of the paper, ensuring that all sections (especially the method and experiments) are consistent and complete. The irrelevant soft-bubble content must be removed, all tables should be included, and the mathematical formulations for the VTA and VTP modules should be clearly stated.

## Score and Decision

The paper as submitted is not a valid, coherent research contribution. It contains content from two different papers, missing experimental results, and incomplete method descriptions, making it impossible to evaluate its claims. Therefore, the appropriate outcome is an error.

MY FINAL SCORE: -100 <score>-100</score>  
MY FINAL DECISION: Error
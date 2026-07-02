## Summary
This paper investigates whether generative (decoder-based) or non-generative (encoder-based) approaches are necessary for achieving compositional generalization—a key component of data-efficient visual perception. The authors provide theoretical and empirical evidence suggesting that enforcing the inductive biases required for compositional generalization is feasible for decoders but infeasible for encoders in practical settings. Theoretically, they show that the inverse generator class $\mathcal{G}_{\text{int}}$ (which must be captured by encoders) has structure that depends on the unknown geometry of out-of-domain regions of the data manifold, making it difficult to enforce through regularization or architecture design. In contrast, the generator class $\mathcal{F}_{\text{int}}$ (for decoders) can be enforced via global coordinate constraints. Empirically, on the PUG dataset with controlled OOD splits, non-generative methods often fail at compositional generalization unless they leverage large-scale pretraining, while generative methods using gradient-based search and generative replay achieve substantial OOD accuracy gains without additional data.

The paper is well-structured, the formalization is mathematically principled, and the central question is important for the field. However, the experimental comparison between generative and non-generative methods is confounded by asymmetric resource usage (search/replay provide additional computation/data to generative methods), the theoretical assumptions ($\mathcal{F}_{\text{int}}$) are strong and may limit practical relevance, and the "data efficiency" framing overreaches what the experiments actually measure (compositional generalization on synthetic data). The paper would benefit from controlled experiments that isolate the benefit of the generative paradigm from the benefit of extra resources, a broader discussion of assumptions, and a more precise mapping of contribution claims to evidence.

## Strengths
**1. Well-posed and important research question.** The paper tackles a fundamental question in AI: whether generative approaches are necessary for data-efficient perception. This question has deep roots in cognitive science and neuroscience and has practical implications for designing more sample-efficient vision systems.

**2. Clean theoretical framework.** The formalization of perception as an inverse problem (Eq. 2.1), the characterization of compositional generalization through identifiability (Eqs. 2.5-2.6), and the function class $\mathcal{F}_{\text{int}}$ provide a mathematically principled foundation. The contrast between the structure of $\mathcal{F}_{\text{int}}$ (global coordinate constraints) and $\mathcal{G}_{\text{int}}$ (manifold-dependent constraints) is insightful and provides a clear theoretical distinction between generative and non-generative approaches.

**3. Strong theoretical result (Theorem 3.2).** The proof that when $d_x \gg d_z$, the Jacobian and Hessian of inverse generators can be arbitrary matrices (up to measure zero) is a nontrivial contribution. It formally demonstrates why enforcing encoder-side constraints for OOD generalization is fundamentally harder than decoder-side constraints in high-dimensional settings—a claim that was previously only conjectured.

**4. Well-designed OOD benchmark.** The use of the PUG dataset with controlled OOD splits (Background, Texture, Object) is a smart experimental design choice. It allows clean evaluation of compositional generalization while controlling for concept interaction type, which is not possible with web-scale benchmarks.

**5. Transparent limitations.** The paper acknowledges its key limitation (theory restricted to $\mathcal{F}_{\text{int}}$, experiments on simplified data), which supports the credibility and scientific honesty of the presentation.

## Weaknesses
### Major Weaknesses

**W1. Confounded experimental comparison (severity: major).**
The generative methods (Fig. 6) benefit from additional computation (gradient-based search per test image) or additional training data (replay-generated OOD images) that are not provided to non-generative methods (Fig. 5). This asymmetry makes it impossible to attribute the performance difference to the generative paradigm per se rather than to the extra resources. A controlled experiment is needed where: (a) non-generative encoders are trained on the same replayed OOD data used by generative methods; (b) non-generative methods receive an auxiliary decoder for test-time optimization to match the computational budget of search. Without these controls, the paper's central claim—"generation is required"—is not decisively supported by the experiments. (Page 1 - Sec 5.2, Lines 107-111)

**W2. The theoretical "infeasibility" claim is not formally proven (severity: major).**
Theorem 3.2 shows that the derivatives of $g$ can be arbitrary matrices when $d_x \gg d_z$, and the residual structure (Eq. 3.4) is manifold-dependent. However, the paper's conclusion that constraining an encoder is "infeasible" or "ill-posed" is argued informally, not proven. A formal hardness result—showing, for example, that no polynomial-time algorithm can learn $g \in \mathcal{G}_{\text{int}}$ from in-domain data alone—would be needed to support "infeasibility." Currently, the argument is that the constraint depends on unknown OOD manifold geometry, which makes it *challenging* rather than *provably infeasible*. The conclusion should be softened to reflect what the mathematics actually establishes. (Page 1 - Sec 3.1, Lines 58-63)

**W3. Assumption $\mathcal{F}_{\text{int}}$ is strong and unvalidated (severity: major).**
The entire theoretical framework assumes the ground-truth generator $f$ belongs to $\mathcal{F}_{\text{int}}$ (Eq. 2.7), a polynomial-type function class with slot-wise additive structure and bounded interaction degree. While the paper cites this as "the largest function class shown to enable OOD identifiability," there is no evidence that real image generators (involving occlusion, non-linear lighting, perspective, stochastic textures) fall into this class. When $f \notin \mathcal{F}_{\text{int}}$, the identifiability guarantees break down, and the practical implications are unknown. The paper should discuss: (a) what aspects of real image formation violate $\mathcal{F}_{\text{int}}$; (b) whether there are known approximation bounds; (c) how violations would affect the experimental results. (Page 1 - Sec 2, Lines 38-41)

**W4. "Data efficiency" framing overreaches the evidence (severity: major).**
The abstract introduces the paper as addressing whether "generation is required for data-efficient perception," but the experiments only measure compositional generalization on PUG data. Data efficiency is a broader concept encompassing few-shot learning, sample complexity, transfer learning, and robustness. The paper does not measure how many ID examples are needed to reach a given performance level, which would be the direct test of data efficiency. The connection between compositional generalization and data efficiency is asserted but not operationally defined or tested. The title and abstract should be revised to match the actual scope. (Page 1 - Abstract, Lines 5-6; Page 1 - Sec 1, Lines 10-16)

**W5. Missing slot assignment details for evaluation (severity: minor).**
The evaluation protocol trains slot-wise readouts on ID data and tests OOD accuracy, but does not specify how slots are matched to ground-truth factors (animals, background). Since slot ordering is arbitrary, low OOD accuracy could result from permutation misalignment rather than genuinely poor representations. The paper should describe the matching procedure (e.g., Hungarian matching on ID accuracy) and report whether slot-factor alignment is stable across OOD conditions. (Page 1 - Sec 5.1, Line 97)

### Minor Weaknesses

**W6. The "task-based view is a special case" claim is unsupported.**
The paper asserts (Line 23) that the task-based view "can be framed as a special case of Eq. (2.1)." This reduction is non-trivial and requires the task variables to align with generative latent factors—an assumption that does not generally hold. The claim should be qualified or removed. (Page 1 - Sec 2, Line 23)

**W7. Reproducibility details missing for gradient-based search.**
Sec 4.1 describes search as an OOD inference strategy but provides no practical details: learning rate, number of steps, convergence criteria, or whether the decoder is frozen or updated. These are critical for reproducibility. (Page 1 - Sec 4.1, Lines 81-84)

**W8. n=0 analysis conflates theoretical structure with empirical difficulty.**
The paper attributes near-perfect OOD accuracy on PUG-Object to the constrained $\mathcal{G}_{\text{int}}$ structure, but an alternative explanation is that the task is simply easier (no occlusion, objects appear separately). The paper should discuss this alternative. (Page 1 - Sec 3.1, Line 65; Page 1 - Sec 5.2, Line 109)

**W9. Conclusion introduces unsupported claims about scalability.**
The final sentence states "While scaling such generative approaches to more challenging settings remains an open problem, we hope our findings will inspire renewed interest in this direction." The paper provides no evidence about scalability—no compute budget analysis, no failure case study for more complex scenes. This is acceptable as aspirational language but should be paired with a concrete discussion of what scaling challenges arise. (Page 1 - Sec 7, Lines 118-174)

**W10. Related Work contrast needs sharper articulation.**
The paper claims its contribution is "more fundamental" than prior work showing non-generative limitations, but does not explain mechanistically *why* the prior explanations (objective issues) are insufficient or *how* the current theory implies a different conclusion about fixability. (Page 1 - Sec 6, Lines 112-113)

## Score
**Final Score: 6/10**

**Rationale:** The paper makes a meaningful theoretical contribution by formalizing the structural asymmetry between generators ($\mathcal{F}_{\text{int}}$) and their inverses ($\mathcal{G}_{\text{int}}$) for compositional generalization, and Theorem 3.2 provides genuine insight into why encoder-side constraints are challenging. The experimental setup with PUG data is well-designed for controlled OOD evaluation. However, the score is limited by the following factors:

- **Research value (primary dimension):** The central claim—that generation is *required*—is not decisively supported by the current evidence, due to the confounded experimental comparison (W1) and the gap between the theoretical infeasibility claim and what is formally proven (W2).
- **Novelty:** The $\mathcal{F}_{\text{int}}/\mathcal{G}_{\text{int}}$ asymmetry analysis is novel, but the paper builds heavily on Brady et al. (2025) and Lachapelle et al. (2023), making the incremental contribution smaller than the presentation suggests. The search and replay techniques (Sec 4) are not claimed as novel. The empirical finding that pretrained models generalize better OOD is consistent with existing knowledge.
- **Validity:** The theoretical analysis is sound within its assumptions (W3), but the experimental conclusions are weakened by the resource-asymmetry confound (W1) and missing slot-matching details (W5).
- **Reproducibility:** The paper lacks implementation details for the search procedure (W7) and the readout evaluation (W5). The appendix (removed) may contain these details.

The paper presents a compelling research direction and a clean theoretical framework, but the evidence for its strongest claim is incomplete. A revision that addresses the experimental confound, softens the claim language, and broadens the limitation discussion would significantly strengthen the paper.
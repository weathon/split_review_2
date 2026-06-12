## Summary

CP4D proposes a compositional framework for physics-aware 4D scene generation that decomposes the task into three stages: (1) generating 3D representations of static backgrounds and dynamic foregrounds using pre-trained models with style-coherent image editing, (2) simulating physically grounded motion by combining physical simulators (MPM, rigid-body, PBD) with SDS-based refinement using video diffusion priors, and (3) automatically composing foreground and background via monocular depth estimation, a depth-aware heuristic for scale initialization, and optimization-based refinement. The framework aims to produce physically plausible, photorealistic 4D scenes with controllable editing capabilities.

## Strengths

- **Well-motivated compositional formulation**: The decomposition of 4D scenes into static backgrounds and dynamic foregrounds is grounded in the structure of real-world scenes and enables modular editing. The pipeline design is logical, with each stage addressing a clear sub-problem (3D representation, motion synthesis, scene composition).

- **Hybrid motion synthesis strategy**: Combining physical simulators with video diffusion model refinement via SDS is a sensible approach that addresses real limitations of each individual method—VLM-estimated material parameters lack precision, and grid-based physics solvers produce geometrically inaccurate collisions. The SDS-based optimization of both material parameters (Eq. 4) and inter-object displacements (Eq. 5) directly targets these failure modes.

- **Practical composition mechanism**: The depth-aware heuristic for scale initialization (Eq. 8) and the sequential optimization strategy (scale then translation) are pragmatic solutions to the non-trivial problem of aligning independently generated 3D representations. The insight that simultaneous optimization of S and P leads to suboptimal local minima is a useful practical finding.

- **Comprehensive baseline comparison**: The paper compares against three distinct categories of methods (physics-driven, video generation, text-to-4D) across multiple metrics (VBench, WorldScore, GPT-4o evaluation), providing a broad comparison landscape.

## Weaknesses

### Fatal
None.

### Major

- **Extremely small evaluation set**: The entire quantitative evaluation is conducted on only 17 examples. This is far too few to draw statistically meaningful conclusions or to support claims of "significantly outperforming existing methods." The paper provides no justification for this small sample size, no confidence intervals, and no discussion of how these 17 examples were selected. This severely undermines the quantitative results in Tables 1 and 2.

- **Questionable evaluation methodology**: GPT-4o is used to score "physical realism," "photorealism," and "semantic alignment" (Table 2), but no validation of this automated evaluator against human judgments is provided. GPT-4o is a language model, not a physics oracle—its ability to assess physical plausibility from rendered video frames is unverified. The paper should either validate GPT-4o scores against human ratings or use established physics-aware evaluation benchmarks (e.g., VideoPhy, which is cited but not used).

- **Limited novelty in individual components**: The framework is a pipeline of existing pre-trained models (text-to-image, image editing, image-to-3D, video diffusion, physical simulators, depth estimation, segmentation). No new model is trained and no existing model is fine-tuned. While system integration has value, the individual technical contributions (SDS for parameter optimization, depth-based scale estimation) are incremental rather than novel.

### Minor

- **Overstated claims about physical dynamics**: The paper claims to handle "complex physical dynamics" but the demonstrated scenarios are relatively simple (dropping objects, two-sphere collisions, wind on fabric). The three solver types (MPM, rigid-body, PBD) are mentioned but the diversity of demonstrated physical phenomena is limited. The paper does not discuss failure modes or the boundaries of its physical modeling capabilities.

- **Limited ablation study**: The ablation in Section 5.3 and Figure 5 covers only a single example with two variants (w/o material opt., w/o position opt.). A more thorough ablation across diverse scenarios and additional design choices (e.g., the sequential vs. simultaneous optimization strategy, the choice of depth estimator, the effect of different video diffusion models) would strengthen the paper.

- **Depth-aware heuristic assumptions**: The scale initialization assumes the foreground should be fully visible in the reference view, which may not always be desirable (e.g., large objects partially visible, or objects at the edge of the frame). The paper does not discuss these edge cases.

### Trivial
None.

## Nice-to-Haves

- A user study comparing CP4D outputs against baselines for physical plausibility and visual quality would substantially strengthen the evaluation.
- Analysis of failure cases and computational cost breakdown across the three stages would improve transparency.
- Discussion of how the method scales to more complex scenes with many interacting objects.

## Novel Insights

The key insight—that physics simulators and video diffusion models are complementary for motion synthesis, with simulators providing physical grounding and diffusion models providing perceptual refinement—is not entirely new (prior work like DreamPhysics and related methods explore similar ideas). The specific contribution is the systematic integration within a compositional 4D generation pipeline and the targeted use of SDS to address two specific failure modes (parameter inaccuracy and geometric approximation errors). The depth-aware heuristic for scale initialization is a practical contribution, though straightforward.

## Suggestions

- **Expand evaluation significantly**: Increase the evaluation set to at least 50-100 diverse examples covering varied object types, physical interactions, and scene complexities. Report standard deviations and conduct statistical significance tests.
- **Validate automated metrics**: Conduct a human study to validate GPT-4o-based physical realism scores, or adopt established physics-aware benchmarks like VideoPhy (Bansal et al., 2024, which is already cited).
- **Provide failure case analysis**: Discuss scenarios where the method fails (e.g., highly complex multi-body interactions, fluid dynamics, scenes requiring precise material modeling) to set appropriate expectations.
- **Ablate more design choices**: Include ablations on the sequential optimization strategy, the choice of video diffusion model, and the sensitivity to VLM-inferred parameters.

## Score and Decision

The paper presents a reasonable system design for a relevant problem, and the qualitative results are promising. However, the evaluation is critically weak—17 examples is insufficient to support the paper's strong claims, and the GPT-4o-based evaluation is unvalidated. The novelty is primarily in system integration rather than in individual technical contributions. These issues place the paper below the acceptance threshold despite its practical appeal.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: Reject
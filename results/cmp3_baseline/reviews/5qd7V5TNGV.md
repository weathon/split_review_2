## Summary

CP4D presents a compositional framework for text-driven 4D scene generation that explicitly enforces physical plausibility. It decomposes a scene into a static 3D background and physically grounded dynamic foreground objects, then follows a three-stage pipeline: (1) generating coherent 3D representations of background and foreground using pretrained expert models, (2) hybrid motion synthesis that combines a physical simulator with video diffusion model refinement (via SDS) to produce realistic trajectories and interactions, and (3) automated composition via monocular depth cues and optimization to fuse elements into a unified 4D scene. The method is evaluated on a small dataset of 17 prompts and shows improvements over baselines in terms of visual quality, physical realism, and controllability.

## Strengths

- **Novel composition of ideas**: Separating a 4D scene into static background and dynamic foreground and then integrating physical simulation with video diffusion priors in a joint pipeline is a sensible and well-motivated design. The hybrid motion synthesis strategy (physical simulator + SDS refinement) is a creative way to combine the strengths of both approaches.
- **Clear and well-structured methodology**: The three-stage pipeline is explained in sufficient technical detail, with key equations (Eqs. 2–9) and figures that help the reader understand the contributions. The writing is fluent and easy to follow.
- **Competitive results across multiple metrics**: The method outperforms a diverse set of baselines (including closed-source video generators Sora, Runway and physics-driven approaches PhysGen, PhysGen3D, OmniPhysGS) on VBench, WorldScore, and GPT-4o evaluations. The qualitative examples (Fig. 4) show noticeable improvements in temporal consistency and physical plausibility over other methods.
- **Potential for controllable editing**: The compositional design naturally supports editing of individual scene elements (background, foreground objects, motion trajectories), which is demonstrated qualitatively in Fig. 6. This is a useful property for practical applications.

## Weaknesses

### Major

- **Very small evaluation dataset (17 examples)**: The paper only curates 17 prompts for quantitative and qualitative evaluation. This is far below what is needed to draw statistically reliable conclusions, especially when comparing against multiple baselines. The risk of cherry-picking or overfitting to these specific scenes is high, and the reader cannot assess the method’s robustness across diverse real-world contexts.
- **Weak validation of physical plausibility**: The main metric for physical realism is GPT-4o scoring, which is known to be unreliable and not reproducible. No human evaluation, collision detection rates, or other objective physics metrics are provided. The claim that CP4D “faithfully adheres to physical dynamics” is therefore supported only by qualitative examples and a black-box LLM score. A more rigorous evaluation (e.g., Physion-like benchmarks, violation rates) is necessary to establish the core claim.

### Minor

- **Complex pipeline with many pretrained models**: The method chains together Qwen-Image, Qwen-Image-Edit, SAM, Depth Anything, Trellis, Viewcrafter, and an MPM/rigid/PBD solver, each with its own failure modes. Error propagation is a concern, and the paper does not analyze how failures in early stages affect the final result. Robustness across different initial models is not studied.
- **SDS refinement for “physical” correctness**: The refinement of material parameters and object positions uses a video diffusion model’s priors, not a true physics loss. This ensures visual plausibility but does not guarantee that the output follows laws of physics. The paper conflates “visually plausible” with “physically consistent” without demonstrating the latter.
- **Limited comparison with text-to-4D methods**: Only DreamGaussian4D is compared among text-to-4D approaches. More recent or stronger baselines (e.g., 4D-fy, Consistent4D, STAG4D) are omitted. The claim of “significantly outperforming existing methods” would be stronger with a broader set of 4D-specific competitors.

### Trivial

- The abstract states “extensive experiments” yet only 17 examples are used; the term is exaggerated.
- The editing examples (Fig. 6) show only one edit per panel; more variety would strengthen the demonstration.

## Nice-to-Haves

- Release the evaluation dataset and code to enable reproducibility and community adoption.
- Perform a human preference study (e.g., pairwise comparisons) to validate the GPT-4o results.
- Analyze failure cases and limitations more transparently (e.g., when the VLM estimates are far off, or when the depth heuristic fails).

## Novel Insights

Beyond the paper’s own contributions, this work highlights a structural insight: that cleanly separating static background and dynamic foreground—inspired by real-world scene composition—can simplify the challenging problem of physics-aware 4D generation into more manageable subproblems (3D asset creation, motion simulation, and spatial composition). It also demonstrates that video diffusion models can be used as a “perceptual critic” to correct approximations made by physical simulators and VLMs, suggesting a general paradigm for combining classical simulation with data-driven refinement.

## Suggestions

- **Scale up the evaluation**: Provide results on a larger and more diverse set of prompts (e.g., 50–100) with statistical significance reporting (confidence intervals). A dedicated physics-specific evaluation using a benchmark like VideoPhy (Bansal et al., 2024) would greatly strengthen the paper.
- **Add a human evaluation**: Since physical plausibility is the central claim, a small human study (e.g., 10 raters judging paired comparisons of physical realism) would add credibility beyond the GPT-4o scores.
- **Measure novel-view consistency**: To back the claim of “explorable 4D scenes,” report metrics such as NeRF’s PSNR or LPIPS across camera trajectories, or at least show multi-view renderings quantitatively.

## Score and Decision

Score: 6.0

Decision: Accept (borderline)

The paper proposes a novel and well-motivated compositional pipeline for generating physically plausible 4D scenes, with clear technical contributions and promising qualitative and quantitative results. However, the evaluation is too small (17 examples) and the physical plausibility claim is insufficiently validated, which prevents a higher score. The work is nonetheless valuable to the community and merits acceptance if the authors can address these concerns in the camera-ready version or discussion.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>
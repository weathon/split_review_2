## Summary

This paper formalizes the all-day multi-scenes lifelong vision-and-language navigation (AML-VLN) problem, where an agent must continually adapt to diverse scenes and environmental conditions without catastrophic forgetting. The authors propose Tucker Adaptation (TuKA), which represents multi-hierarchical navigation knowledge as a fourth-order tensor decomposed via Tucker decomposition into shared components (core tensor, encoder, decoder) and scenario-specific experts (scene and environment). An agent called AllDayWalker is built on top of TuKA with a decoupled knowledge incremental learning strategy, achieving strong results across 24 sequential navigation scenarios spanning simulation and real-world environments.

## Strengths

- **Well-motivated problem formulation**: The AML-VLN setting is practically important—real robots must navigate across scenes and lighting conditions. The paper clearly argues why existing two-dimensional adapter representations (LoRA, HydraLoRA) are insufficient for multi-hierarchical knowledge, motivating the high-order tensor approach with a concrete conceptual gap.
- **Substantial empirical improvements**: AllDayWalker achieves 65% average SR versus 44% for BranchLoRA and 52% for O-LoRA, and reduces average forgetting rate to 11% versus 18% for SD-LoRA (the next best). The improvements are consistent across nearly all 24 tasks, which is compelling.
- **Comprehensive experimental design**: The paper compares against 12 baselines covering sequential fine-tuning, knowledge distillation (LwF), regularization (EWC), MoE-LoRA variants, orthogonality-based methods, and test-time adaptation. Ablations cover tensor order, shared components, scaling to 30 tasks, and generalization to 6 completely unseen scenarios.
- **Novel benchmark contribution**: Extending Habitat with three physically-grounded imaging degradation models (atmospheric scattering, low-light sensor noise, overexposure saturation) creates a reusable evaluation platform for this emerging problem.

## Weaknesses

### Fatal
None.

### Major
- **No computational/storage cost analysis**: For lifelong learning methods, storage cost is critical. TuKA stores a shared core tensor, encoder, decoder, plus per-scene and per-environment expert vectors. The paper states it keeps "trainable parameters comparable" but never presents actual parameter counts, memory footprints, or FLOPs for AllDayWalker versus baselines. This omission makes it difficult to assess practical deployability.
- **Inference expert retrieval is fragile and under-analyzed**: The two-step CLIP similarity matching for scene and environment expert selection (§3.4) assumes clean separability of scene and environment identity from a single observation. No failure analysis is provided—what happens when the scene is ambiguous, when lighting changes mid-route, or when the environment condition is atypical? The 30% average F-SR on T13 (Table 2) and generally higher forgetting on certain tasks suggest instability that warrants discussion.
- **Unexplained phenomena not discussed**: AllDayWalker shows negative F-SR values on T14 (-3%) and T20 (-4%), meaning performance on these tasks actually improved after learning later tasks (backward transfer). This is an interesting and potentially important finding that the paper completely ignores rather than analyzing.

### Minor
- **Somewhat unfair inclusion of TTA methods**: FSTTA and FeedTTA are designed for temporary single-task test-time adaptation, not lifelong learning. Including them without clearly framing this distinction inflates the comparison space and muddies the evaluation.
- **High variance across tasks with no error bars**: Performance varies dramatically (T2 at 23% vs T7 at 87%), but no variance estimates, confidence intervals, or analysis of what makes certain tasks harder are provided. Table 3's ablation also appears to have minor inconsistencies (e.g., the last row showing 68% OSR vs the row above showing 69% for the same configuration), suggesting possible variability.
- **Theoretical justification for tensor order is limited**: The claim that "two-dimensional matrix form fails to capture multi-hierarchical knowledge" is argued intuitively but lacks formal analysis. The paper could benefit from explaining precisely what the fourth-order structure can represent that lower-order decompositions cannot, beyond empirical validation.

### Trivial
None.

## Nice-to-Haves
- A comparison of storage cost and inference latency across methods would significantly strengthen the practical value argument.
- Analysis of the CLIP-based retrieval accuracy and its correlation with downstream navigation performance.
- Discussion of the negative forgetting rates as evidence of beneficial backward transfer.

## Novel Insights

The key novel insight is that navigation knowledge in lifelong multi-scene, multi-environment settings has a natural hierarchical structure (shared skills, scene-specific, environment-specific) that can be explicitly captured through tensor decomposition rather than implicitly through MoE routing. The Tucker decomposition provides a principled way to factor this knowledge, where the core tensor captures cross-factor interactions and the factor matrices provide clean interfaces for knowledge inheritance and constraint during continual learning. This is a meaningful conceptual advance over prior adapter-based continual learning approaches that conflate all hierarchy levels into a single shared-specific decomposition.

## Suggestions
- Add a table comparing trainable parameters, total stored parameters, and inference cost across all methods.
- Analyze the backward transfer phenomenon (negative forgetting rates) and discuss when and why learning new tasks helps on old ones.
- Evaluate the robustness of the CLIP-based expert retrieval under distribution shift and provide failure case analysis.
- Add error bars or multiple random seed evaluations to establish statistical significance of the improvements.

## Score and Decision

The paper makes a solid contribution by formalizing an important practical problem, proposing a conceptually novel tensor decomposition approach, and demonstrating strong empirical results with comprehensive comparisons. The Tucker decomposition for multi-hierarchical knowledge representation is a genuine technical advance over existing LoRA-based approaches. However, the absence of computational cost analysis (critical for lifelong learning claims), unanalyzed inference fragility, and unexplained empirical phenomena prevent a higher score.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>
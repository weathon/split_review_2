## Summary

This paper proposes a shape-adaptive guidance signal for interactive cortical sulcal labeling. The key idea is to encode user clicks on the spherical domain using a Weighted Geodesic Distance Transform (WGDT) that solves the eikonal equation with a curvature-based speed function, allowing the signal to propagate faster along sulcal valleys and slower over gyri. The WGDT signal is integrated with a spherical CNN (SPHARM-Net) to enable iterative refinement with few user clicks. Experiments on 72 HCP subjects with 17 LPFC sulci show that a single WGDT click outperforms automatic baselines and equidistance-based signals (ADT, Disk), especially on small and variable sulci.

## Strengths

- **Novel and well-motivated guidance signal design**: The use of mean curvature to modulate geodesic propagation speed is a principled way to align user clicks with cortical folding patterns. This directly addresses the limitation of standard Euclidean/geodesic distance transforms that ignore surface anatomy.
- **Convincing experimental validation**: The paper provides thorough ROI-wise comparisons (17 sulci) across multiple guidance signal variants and hyperparameters, with statistical significance testing and FDR correction. The iterative click simulation and 10-run averaging per subject demonstrate careful evaluation.
- **Practical real-time performance**: The runtime analysis (less than 0.5 seconds per click) demonstrates that the framework is suitable for interactive use, including the WGDT encoding, re-tessellation, and model forward pass.
- **Clear presentation**: The problem is well-motivated with neuroanatomical context, the method is described with precise equations and figures, and results are presented with informative visual comparisons.

## Weaknesses

### Fatal
None.

### Major
- **Lack of comparison with alternative interactive segmentation methods on meshes**: The paper only compares against automatic baselines from the same group (Lyu et al., Lee et al. a/b). There is no comparison with any other interactive segmentation approach that could be adapted to meshes, such as graph-cut based methods, or learning-based approaches using SAM projections onto 2D views (which the paper criticizes but does not benchmark). This limits the assessment of relative improvement over the state of the art in interactive 3D segmentation.
- **Limited dataset and region scope**: The evaluation is restricted to 72 subjects and the LPFC region only. While the authors acknowledge generalization to other cortical regions as future work, the current results do not demonstrate robustness across broader neuroanatomical contexts, which is important for clinical utility.

### Minor
- **Per-sulcus training**: Each sulcus requires a separate model (17 models total). This is a significant practical limitation for scaling to whole-brain labeling, and the paper does not discuss strategies to reduce the number of models or share parameters across sulci.
- **Hyperparameter sensitivity**: The WGDT signal has tunable parameters \(k\) and \(\sigma\), and the paper notes that selecting appropriate values requires manual tuning. While ablation over \(k \in [6,8,10]\) is shown, the interaction with \(\sigma\) and the optimal choice across different sulci is not fully explored.

### Trivial
None.

## Nice-to-Haves
- An experiment combining automatic model predictions as a starting point for interactive refinement (joint use), as mentioned in the discussion, would strengthen the practical impact.
- Analysis of failure cases where WGDT performs poorly (e.g., noise, pathological anatomy) would help understand limitations.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Benchmark against at least one alternative interactive paradigm** for 3D meshes, such as a graph-cut with user strokes, or a SAM-based projection approach adapted to the spherical domain. This would contextualize the improvement over the existing interactive segmentation toolbox.
2. **Discuss scalability to whole cortex explicitly**: estimate number of models needed, or propose a multi-class variant that could reduce model count.
3. **Provide guidance on selecting \(k\) and \(\sigma\)**: a simple rule-of-thumb based on sulcus size or curvature statistics would increase practical usability.

## Score and Decision

**Score**: 7  
**Decision**: Accept

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>
## Summary

This paper trains a stable sparse autoencoder on DINOv2-B to extract a 32,000-unit concept dictionary, then uses it to analyze how downstream tasks (classification, segmentation, depth estimation) recruit concepts, characterize concept geometry and statistics, and ultimately propose the "Minkowski Representation Hypothesis" (MRH) — an alternative to the Linear Representation Hypothesis where tokens are sums of convex polytopes around archetypal landmarks, naturally realizable through multi-head attention. The paper finds task-specific specialization (Elsewhere concepts, border detectors, monocular depth cue families) and geometric departures from near-orthogonal sparse coding, motivating the MRH as a working hypothesis with theoretical justification and preliminary empirical support.

## Strengths

- **Largest-scale vision interpretability demo.** The 32,000-unit stable SAE dictionary for DINOv2-B (d=768, R²>88%) is a substantial and practically valuable contribution, constrained to the convex hull of real activations for reproducibility. This backbone enables all downstream analyses and will be useful to the community as a released resource.

- **Well-designed task-specific concept analysis.** The controlled perturbation experiments for depth cues (median blurring, edge-preserving smoothing, high-pass filtering isolating projective/shadow/frequency cues) and the causal masking analysis for Elsewhere concepts are methodologically sound. The observation that segmentation concepts form tight clusters with decaying eigenspectra, and that classification relies on "object negation" concepts, provides genuinely new insights about DINOv2's functional organization.

- **Thorough geometric diagnostics with appropriate baselines.** The analysis of dictionary coherence vs. random/Grassmannian baselines, singular value spectra decay, Hoyer scores, co-activation vs. geometric affinity correlation, and antipodal pairs is comprehensive. The finding that task-aligned concepts break quasi-orthogonality locally (intra-task similarity >> random) while the global dictionary shows structured redundancy is a nuanced and well-supported observation.

- **The MRH proposal is mathematically grounded.** The connection between multi-head attention producing convex combinations per head and the Minkowski sum across heads (Proposition 1) is elegant. The link to Gärdenfors conceptual spaces and the practical implications for steering (bounded trajectories, archetypal vs. directional steering) provide a coherent theoretical framework with testable predictions.

- **The PCA/token geometry analysis (Section 5)** showing that positional encoding collapses to a 2D sheet in later layers while leading PCs capture semantic (non-positional) structure is independently interesting and well-executed.

## Weaknesses

### Fatal
None.

### Major

- **MRH empirical validation is preliminary.** The three empirical tests (geodesic interpolation, archetypal analysis matching SAE, block structure in code Grams) are suggestive but each admits alternative explanations: (1) curved manifolds generally show geodesic vs. Euclidean discrepancies; (2) AA matching SAE with ~10 archetypes shows low-dimensionality but not necessarily Minkowski sum structure; (3) "block structure" in Gram matrices is observed visually without rigorous quantification. The paper acknowledges this ("working hypothesis"), but the core novel contribution would benefit from stronger discriminative tests — e.g., directly measuring whether head-polytope decompositions match the observed token geometry, or testing specific predictions that distinguish MRH from general manifold structure.

- **Single-model evaluation.** All analyses are conducted on DINOv2-B with specific hyperparameters (k=8, c=32,000, 128k centroids). No robustness checks across model sizes (DINOv2-S/L/G), sparsity settings, or alternative vision transformers are provided. This limits the generalizability of claims about "what DINO sees" and whether MRH applies beyond this specific configuration.

### Minor

- **Elsewhere concept interpretation is overstated.** The paper claims these implement "learned negation" (Section 3) while noting the alternative interpretation of "distributed off-object evidence." The causal masking evidence (concepts vanish when the object is removed) is consistent with both interpretations — a negation concept and a contrast/distribution-sensitive feature would both exhibit this behavior.

- **Non-identifiability (Proposition 2) somewhat undermines practical impact.** While mathematically correct and honest, acknowledging that Minkowski decomposition is generally non-unique from final activations alone raises questions about how actionable MRH is for the interpretability tools the paper advocates. The suggestion to use intermediate signals (attention weights, per-head outputs) is noted but not developed.

- **The co-activation/geometry correlation analysis** (Section 4) shows a weak positive correlation, which the footnote explains may be an intrinsic property of linear reconstruction methods. This makes the negative result harder to interpret — the observed weak correlation could be entirely methodological rather than reflecting genuine organizational principles.

## Nice-to-Haves

- Applying the same SAE analysis to a second model (e.g., DINOv2-L or a standard ViT) to demonstrate generalizability
- A quantitative test distinguishing MRH from alternative geometric explanations (e.g., testing whether polytope faces align with head boundaries using attention weights)
- Analysis of whether the 32k dictionary is saturated or whether scaling c substantially changes the findings

## Novel Insights

The paper's most novel insight is that multi-head attention mechanically implements a Minkowski sum of head-level convex polytopes, and that this provides a geometrically grounded alternative to the sparse linear direction view of representations. This reframes concepts as landmarks and regions rather than unbounded directions, explains steering saturation, and suggests that interpretability must leverage architectural structure (per-head signals) rather than treating final activations in isolation. The connection to convex conceptual spaces (Gärdenfors) gives this a broader cognitive science grounding that is underexplored in the mechanistic interpretability literature.

## Suggestions

- Add at least one quantitative discriminative test for MRH — e.g., measure whether head-polytope boundaries predicted by attention patterns align with token cloud faces, or test the specific prediction that token diversity should increase with the number of active heads
- Include robustness checks across DINOv2 model sizes or alternative SAE hyperparameters
- Develop the practical implications more concretely — the "archetypal steering" idea is compelling but would benefit from a proof-of-concept experiment showing improved steering by moving toward landmarks rather than along directions

## Score and Decision

The paper delivers a substantial empirical study with valuable contributions: the largest vision SAE dictionary to date, well-designed task-specific concept analyses with novel findings (Elsewhere concepts, border detectors, monocular cue families), and thorough geometric diagnostics. The MRH proposal is intellectually stimulating and mathematically grounded, but its empirical validation is preliminary and the single-model evaluation limits generalizability. The empirical findings alone (task recruitment patterns, concept geometry departures from LRH, token cloud structure) constitute meaningful contributions to the interpretability literature, while MRH opens a promising research direction even if not yet fully validated.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>
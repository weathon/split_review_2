## Summary

This paper introduces a nonlinear, multimodal encoding model (PCA + single-hidden-layer MLP on concatenated Llama and Whisper features) for predicting fMRI brain responses to naturalistic speech. Evaluated on a large-scale dataset (3 subjects, 20 hours), the approach achieves relative improvements of 17.2% (r²) and 17.9% (CC_norm) over unimodal linear baselines. The authors systematically ablate nonlinearity and multimodality using carefully designed controls (MLLinear, DIMLP), and introduce a RED-based clustering analysis to probe spatiotemporal cortical organization. The main contributions are empirical: demonstrating that even a minimal nonlinear multimodal readout reveals structure missed by linear methods, and using the resulting model to examine patterns of cortical integration.

## Strengths

- **Well-designed ablation hierarchy (Section 2.4, Table 1).** The inclusion of MLLinear (linearized MLP, isolating nonlinearity from dimensionality reduction) and DIMLP (separate nonlinear processing per modality with linear cross-modal fusion, isolating cross-modal interactions) provides the cleanest ablation design in current speech encoding literature. The consistent ordering MLP > DIMLP > MLLinear ≈ Linear tells a clear, internally consistent story.

- **RED-based clustering (Section 3.1.2).** The Relative Error Difference metric preserves temporal dynamics and yields substantially higher modularity (nonlinear RED Q=0.155 vs. FC Q=0.068), revealing spatiotemporal functional organization (e.g., motor regions clustering by body part, speech areas aligned with the dorsal stream) that correlation-based methods miss.

- **Large-scale dataset.** 20 hours, 33k time points, 80k–90k voxels per subject (LeBel et al., 2023) make nonlinear modeling more feasible than on smaller datasets, and the paper leverages this scale for a comprehensive evaluation.

- **Computational efficiency.** The PCA+MLP approach uses 5.64M parameters vs. 1.31B+ for full-voxel linear models while achieving better performance — a practically meaningful result that makes nonlinear encoding tractable for speech fMRI.

- **Honest limitations (Section 4).** The paper candidly acknowledges overfitting with deeper architectures, interpretability challenges, and the complementarity (not replacement) of linear models, lending credibility to its empirical claims.

## Weaknesses

### Fatal
None.

### Major
- **Numerical inconsistency in headline improvement claims over prior SOTA.** The abstract and contributions claim "7.7% and 14.4% improvement over prior state-of-the-art models" (Antonello et al., 2024). From Table 1, the prior SOTA (text+audio Linear, all voxels) achieves 4.10% r² and 31.36% CC_norm, while the proposed method achieves 4.29% r² and 34.32% CC_norm. The relative improvements are 4.6% (r²) and 9.4% (CC_norm) — neither matches 7.7% or 14.4%. The 7.7% in the table is the CC_norm improvement of the *linear* multimodal model over the unimodal baseline, not the proposed method's gain over prior SOTA; 14.4% does not appear in the table at all. This inconsistency undermines a central quantitative claim and must be resolved before acceptance.

- **Claims about general principles of brain organization from N=3 subjects.** The paper asserts it "reveals previously hidden patterns of brain organization" and extends neurolinguistic theories (Motor Theory of Speech Perception, Convergence-Divergence Zone model, embodied semantics). These are claims about general cortical organization, but the evidence comes from only 3 subjects. While N=3 is standard in deep fMRI encoding studies using this dataset, the paper's theoretical framing goes well beyond describing within-subject patterns. The claims should be either explicitly bounded or supported by stronger cross-subject consistency evidence (currently deferred to Appendix M.4).

### Minor
- **Neurological theory claims are correlational, not causal.** The paper interprets prediction improvement patterns as evidence for specific mechanisms (Motor Theory, CDZ, embodied semantics). However, these are based on which model predicts better in which regions — correlational patterns consistent with (but not testing) these theories. The paper notes this limitation once (Section 3.3.1: "our current design cannot distinguish between these explanations"), but the abstract, contributions list, and discussion all strongly assert theoretical alignment. Claims should be more carefully bounded.

- **Statistical significance for the main DIMLP-vs-MLP comparison is deferred.** The 2.6% relative r² gain (0.11 pp absolute) is the paper's central analytical finding, but significance testing is entirely relegated to Appendix C. Given the small absolute difference, readers need main-text evidence that this gap is reliable across voxels and subjects.

### Trivial
- **RED metric motivation is underdeveloped.** The paper states RED "preserves temporal dynamics" but does not explain why this specific formulation (signed absolute error difference) enables better clustering than alternatives (e.g., log ratio of error variances, difference in squared errors).

## Nice-to-Haves
- Report noise-ceiling-normalized performance for r² metrics alongside raw r² values (CC_norm already provides this for correlation).
- Direct comparison against prior nonlinear unimodal approaches (Moussa et al., 2024; Vatikonda et al., 2025) would further strengthen the scope claims.
- Clarify that the MLP predicts 512 PCA components (inverse-projected to voxels), which explains the efficient 5.64M parameter count — this is stated in Section 2.3 but could be more explicit when comparing to full-voxel models.

## Removed Points
1. [Removed — factual error] Claim that paper lacks noise ceiling context: CC_norm is defined as CC_abs/CC_max (Section 2.5), directly expressing performance as fraction of the noise ceiling in correlation space.
2. [Removed — not a weakness] Criticism that the method (PCA+shallow MLP) is too simple: The paper acknowledges this limitation and frames the contribution as an empirical demonstration, not a novel architecture.
3. [Removed — addressed in paper] Parameter count concern: Section 2.3 clearly states the MLP predicts 512 PCA components (inverse-projected), explaining the efficient parameter count.
4. [Removed — addressed in paper] Request for comparison against prior nonlinear unimodal approaches: Table 1 includes unimodal nonlinear baselines (text MLP PCA, audio MLP PCA).
5. [Removed — strawman] RED-clustering advantage mainly from RED vs FC, not nonlinearity: The paper reports both comparisons (nonlinear RED Q=0.155, linear RED Q=0.145, FC Q=0.068) without misrepresenting the contrast.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. Resolve the 7.7%/14.4% numerical inconsistency — either correct the numbers to match Table 1, or clarify the exact reference values from Antonello et al. (2024) and show the computation.
2. Tone down neurolinguistic theory claims to reflect they are *consistent with* rather than *evidence for* specific mechanisms.
3. Report confidence intervals or significance tests for the DIMLP-vs-MLP comparison in the main text.
4. Explicitly caveat claims about general principles of cortical organization as being based on N=3 subjects.

MY FINAL SCORE: <score>5</score>
MY FINAL DECISION: <decision>Reject</decision>
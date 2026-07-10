## Summary

This paper compares three neural network architectures — a plain MLP, a "U-Net-like" residual network, and a "DeepONet-style" model — on the task of predicting the temporal evolution of a hydrogen-oxygen-air thermal explosion system. The key finding is that the residual-skip-connection architecture (called U-Net-like) achieves substantially lower mean squared error (MSE ≈ 0.0014) than the MLP (0.020) and DeepONet-style (0.018) models, demonstrating that architecture choice matters for data-driven combustion kinetics surrogates.

## Strengths

- **Well-motivated and practically important problem.** Accelerating stiff chemical kinetics is a genuine bottleneck in combustion CFD, and the paper clearly grounds this motivation (Section 1). The problem choice is relevant and timely.

- **Broad and realistic parameter range in the dataset.** The training data spans T ∈ [250, 5000] K, p ∈ [10⁴, 2×10⁷] Pa, and Δt ∈ [10⁻¹⁰, 10⁻⁵] s (Section 3), covering diverse combustion regimes from slow reactions through autoignition — a more challenging and realistic range than some prior work.

- **Multi-step recursive loss function.** The 30-step rollout with 1/k weighting (Eq. 4) is a sensible design for temporal prediction tasks, directly penalizing error accumulation in the way that matters for ODE integration.

## Weaknesses

### Fatal
None.

### Major

- **Architecture naming is misleading; paradigm-level claims are unsupported.** The "U-Net-like" network (Section 4.2) has no downsampling, upsampling, convolutions, or encoder-decoder structure — it is a residual MLP with two skip connections. Yet Section 5 calls it an "encoder-decoder design" and claims it "capture[s] both global trends and localized transients," which the described architecture does not support. The "DeepONet-style" network (Section 4.3) does not implement operator learning: the branch takes a pointwise 12-vector (not an input function sampled at sensor points) and the trunk takes only `dt`. This is a two-branch feedforward network. Since the paper's central argument is framed as a comparison of architectural *paradigms* (hierarchical encoder-decoders vs. operator learning), mislabeling both non-trivial architectures fundamentally undermines the conclusions drawn.

- **No computational cost comparison despite the paper's core motivation.** The paper repeatedly frames accelerating stiff chemical kinetics as the motivating problem (Sections 1–2) and asserts "without increasing computational cost relative to the simpler models" (Section 5), yet provides zero evidence: no parameter counts, FLOPs, or wall-clock time. The practical accuracy-vs-cost trade-off cannot be assessed.

- **DeepONet description is mathematically inconsistent and not reproducible.** Section 4.3 describes the trunk output as a 32×10 matrix and the branch output as a 12×10 matrix. A "matrix product" of these shapes is undefined, and the claimed 12-component fused vector cannot be produced as described from the stated dimensions. This section cannot be implemented from the paper alone.

- **Per-trajectory error analysis is insufficient and may overstate practical reliability.** The evaluation selects two trajectories — one from the "lowest 10%" and one from the "upper quartile" (Section 5, Figures 3–4) — with no systematic characterization of failure modes. With std/mean ratios of 15.9× (U-Net), 3.2× (DeepONet), and 3.4× (MLP), many individual predictions are orders of magnitude worse than the mean. The paper does not quantify what fraction of test trajectories are practically unreliable.

### Minor

- **Modest significance of the core finding.** That residual/skip connections improve neural network accuracy is one of the most established findings in deep learning. Demonstrating this on one combustion dataset — with no out-of-distribution testing, no comparison with established combustion-specific surrogate methods (e.g., ISAT, cited as Pope 1997), and no deployment in a CFD loop — limits the contribution.

- **No ablation to isolate which architectural feature drives the improvement.** The "U-Net" improvement could come from the local skip, the global skip, or both. An MLP with a single global residual connection would disentangle these factors but is not tested.

- **Figure captions list species not present in the described chemical system.** Figures 3 and 4 captions reference CO and NO, which cannot arise from the 9-species H₂-O₂-Ar-N₂ system described in Section 2. This may be a parser artifact but, if genuine, indicates a scientific inconsistency.

### Trivial
None.

## Nice-to-Haves

- Report per-trajectory error distributions (deciles, fraction of trajectories exceeding a threshold) rather than only mean±std.
- Add parameter counts and inference timing to support the acceleration claims.
- Run an ablation: compare the "U-Net" against an MLP with a single global residual connection.
- Include at least one out-of-distribution generalization test.

## Removed Points

- "No dataset/code release mentioned" — removed per filtering rules (reproducibility nitpick; the dataset is described in sufficient detail).
- "Compare against ISAT" — removed as scope creep; the paper scopes itself as a comparison of NN architectures, not NN vs. tabulation methods.
- "Standard deviations dwarf the means" — this is subsumed under the per-trajectory analysis weakness above.
- "References contain typographical errors in author names" — removed as a trivial formatting issue.
- "Missing related works" — cannot be verified; removed.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Rename the architectures honestly:** "Residual MLP" (not U-Net-like) and "Two-branch MLP" (not DeepONet-style), or implement actual U-Net and DeepONet architectures. The paper would be strengthened by accurate naming that matches its actual empirical comparison.
2. **Resolve the CO/NO discrepancy** in Figure 3 and 4 captions.
3. **Add parameter counts and wall-clock inference time** to support the computational cost claims.
4. **Report deciles or threshold-exceedance rates** for per-trajectory errors.
5. **Add an ablation** comparing against an MLP with a single global residual connection.

## Score and Decision

The paper addresses a genuine problem and has a well-constructed dataset and a sensible training setup. However, it has four significant structural issues: (1) the two non-trivial architectures are misleadingly named, with paradigm-level conclusions that the described architectures cannot support; (2) no computational cost data is provided despite this being the paper's core motivation; (3) the DeepONet description is mathematically inconsistent and not reproducible; and (4) the per-trajectory analysis is insufficient to support the reliability claims. These weaknesses collectively undermine the paper's central contribution as framed. The paper would need substantial revision — in particular honest re-labeling of architectures and a more thorough evaluation — before it could be considered for acceptance.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>
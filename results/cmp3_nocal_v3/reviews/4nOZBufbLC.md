## Summary

Count Bridges proposes a generative framework for integer-valued data based on a Poisson birth-death bridge process on ℤ^d, delivering closed-form conditionals (Proposition 3.1) that enable efficient training via distributional scoring and an EM-style extension for deconvolving aggregated observations. The method is validated on synthetic integer-distribution matching benchmarks and on two biological applications: nucleotide-resolution single-cell RNA-seq modeling with bulk deconvolution, and reference-free spatial transcriptomic deconvolution.

## Strengths

1. **Genuinely novel and theoretically well-grounded formulation.** The Poisson birth-death bridge (Prop. 3.1, Eqs. 8–9) provides closed-form conditionals with a Bessel slack posterior, binomial draws for N_s, and hypergeometric draws for B_s — a clean, tractable construction that is not available in prior discrete diffusion work. The connection to Schrödinger bridges and entropy-regularized OT (Eqs. 127–135, showing recovery of discrete OT with cost |x₁−x₀| as κ→0, paralleling the Gaussian case) is a genuine theoretical contribution that grounds the method beyond heuristics.

2. **Impressive scaling behavior in high dimensions.** Figure 3 shows CB maintaining near-zero W₁ across dimensions 4–512, while both CFM and DFM degrade sharply. If the baselines are configured fairly, this is a significant practical advantage for high-dimensional biological count data.

3. **Real biological applications with meaningful outcomes.** The bulk RNA-seq deconvolution (Tables 2–3) and spatial transcriptomic deconvolution (Tables 4–5) tackle genuinely hard, unsolved problems. CB outperforms STDeconvolve on proportion metrics (Table 4) and the spot-mean baseline on distributional metrics (Table 5), providing evidence that the method can recover meaningful signal from aggregate observations where reference-free deconvolution is needed.

4. **Clean mathematical framing of the bridge modeling paradigm.** The parallel between the Gaussian case (σ controls entropy regularization, recovering quadratic OT as σ→0) and the birth-death case (κ controls entropy regularization, recovering |x₁−x₀| OT as κ→0) demonstrates genuine understanding and situates the method within a well-understood theoretical landscape.

## Weaknesses

### Fatal
None.

### Major

1. **Baseline comparisons in synthetic benchmarks are structurally disadvantaged for CFM and DFM.** CB is compared against Continuous Flow Matching (designed for ℝ^d) and Discrete Flow Matching (designed for categorical data) on integer-valued tasks. CFM outputs are discretized by rounding (Figure 2 caption), which destroys the gradient structure it relies on. DFM operates on unordered categorical states, not ordinal counts. The abstract's claim of "state-of-the-art performance on integer distribution matching benchmarks" overstates what the evidence supports given that the only count-specific baseline (Blackout Diffusion) is excluded because it "cannot transport between arbitrary distributions" (line 15, line 262). Including a simple Poisson factor model or independently-trained marginal Poisson distributions would establish a lower bound. This does not invalidate CB's contribution but the synthetic results primarily show that a method designed for integer data outperforms methods designed for other data types. *Supported by: Section 6.1, Figure 2 caption, Figure 3, line 262.*

2. **The deconvolution EM framework rests on an E-step approximation whose quality is uncharacterized.** The E-step (Algorithm 3) uses a projection-guided diffusion rather than sampling from the true aggregate-conditional distribution. The paper forthrightly admits this is a "first-order surrogate" that "lacks serious theoretical support" (line 367, Limitations). This is not a minor caveat — the deconvolution claims depend on this step. The identifiability analysis is relegated to the stripped appendix (Apps. B.2, B.3) and summarized only briefly (line 292). Without characterization of the approximation error (e.g., through a controlled synthetic experiment comparing against an oracle sampler for small G), it is difficult to assess whether the deconvolution results reflect genuine recovery of unit-level distributions or artifacts of the projection heuristic. *Supported by: Section 4, Algorithm 3, lines 199–236, 367.*

### Minor

3. **Bulk RNA-seq deconvolution evaluation is indirect.** For the bulk application, the evaluation aggregates nucleotide-level predictions into gene counts and assigns predicted cells to the closest cell type, then computes JSD/RMSE/Spearman on cell-type proportions (lines 333–337, Tables 2–3). This collapses the evaluation back to proportion-level accuracy, making it asymmetric with the spatial deconvolution evaluation (Table 5, which reports MMD, W₂, and Energy directly on count profiles). The paper provides MSE for nucleotide-level predictions (Table 1) and mentions "distributional quality" against the bulk mean, but does not report per-gene distributional metrics for bulk deconvolution. This weakens the claim that CB is recovering accurate single-cell count profiles from bulk data. *Supported by: Section 6.2, lines 333–337.*

4. **Relevant baseline DestVI is absent from main spatial deconvolution results.** DestVI (Lopez et al., 2022) is mentioned in the related work (line 270) as a method that "outputs count profiles" for spatial deconvolution, making it the most natural competitor for CB's spatial application. The paper references "Appendix F for comparisons to reference-based methods" (line 345), but the appendix is not available in the main text. The lack of this comparison in the body is a gap. *Supported by: Section 5 (line 270), Section 6.3 (line 345).*

5. **Model architecture and training details are almost entirely absent.** The paper does not report the number of parameters, training steps, batch size, learning rate, optimizer, or compute budget for any experiment. The synthetic benchmarks, bulk model, and spatial model use different architectures (residual attention blocks vs. UViT), but none are specified at a level that would allow reproduction. *Supported by: Sections 6.2–6.3.*

6. **Number of function evaluations (NFE) is not consistently reported.** Figure 3 lists NFE values 8, 32, 128 but it is unclear which line corresponds to which NFE value in the visualization. Algorithm 2 uses a fixed grid without specifying K. The spatial experiment (Section 6.3) does not mention NFE. Since step count directly affects sampling quality and cost in bridge models, this is a reproducibility gap. *Supported by: Figure 3 caption, Algorithm 2.*

7. **The learned projection module is not ablated.** Section 6.2 describes a learned projection Π_ψ trained on 10% of examples where a₀ is provided. There is no comparison showing whether this learned projection outperforms the simple rescaling from Proposition 4.1, which is important because the learned projection is used only in the bulk RNA-seq experiment while the spatial experiment uses only simple rescaling. *Supported by: Section 6.2, line 329.*

### Trivial
- The Bessel slack posterior distribution (the Bes distribution) is non-standard and its pmf is never stated explicitly in the main text; readers must hunt for it in the appendix.
- The notation in Section 4 is somewhat confusing: X_t ∈ ℤ^G is introduced as a group-level vector, but the method seems to operate on one group at a time with a denoiser producing unit-level predictions.

## Nice-to-Haves
- Evaluate bulk RNA-seq deconvolution at the count level directly (per-gene MMD or W₂), matching the spatial evaluation protocol.
- Run a controlled synthetic deconvolution experiment comparing the projection-guided E-step against an oracle that samples from the true conditional distribution (e.g., via rejection sampling for small G) to characterize the approximation error.
- Present a brief summary of the identifiability bounds (Apps. B.2, B.3) in the main text — e.g., how deconvolution error scales with group size G and heterogeneity α.
- Ablate the learned projection module vs. the simple rescaling (Prop. 4.1) to show whether the additional learned component adds value.

## Removed Points
These points are flagged to be removed; treat them with caution.
- *"Nucleotide resolution claim is underspecified / implausible"* — REMOVED. The paper clearly states each training example corresponds to a nucleotide position in a single cell (line 327). The data dimensionality per example is the count at one position, not the number of genomic positions. The critic misread the dimensionality; this is not a weakness.
- *Section-by-section notes about the projective posterior identity being unclear, the Bessel pmf not in main text, energy score variance, etc.* — REMOVED as presentation-level concerns that are either standard or addressed in the appendix. The Bessel pmf point is kept as a Trivial note above.
- *Circularity concern about EM (E-step generates samples, M-step trains on them)* — REMOVED. The paper discusses identifiability limits (Figure 4, line 292) and acknowledges the theoretical gap in its limitations. The circularity is inherent to EM and not unique to this work; what matters is the quality of the approximation, which is already flagged as Major weakness #2.
- *"Blackout Diffusion should have been included as a baseline"* — REMOVED. The paper provides a clear justification for exclusion: Blackout Diffusion uses pure-death processes that "cannot transport between arbitrary distributions" (line 15, line 262), which is the core task being evaluated. This is a reasoned methodological choice, not an omission.

## Novel Insights

The input reviews surface a key tension: the paper's core theoretical contribution (the Count Bridge process with closed-form conditionals and its connection to Schrödinger bridges) is genuinely novel and well-executed, but its applied claims are partly over-calibrated to the evidence. The synthetic benchmarks compare against methods not designed for integer data, the deconvolution extension rests on an uncharacterized approximation whose limitations the authors themselves flag, and the bulk RNA-seq evaluation collapses to proportion-level metrics. The spatial deconvolution results (Table 5) are the cleanest evidence for the method's practical value. The most insightful observation from the reviews is that the paper would be stronger if it explicitly characterized where the E-step approximation breaks down (e.g., a controlled synthetic study varying group size and heterogeneity) and if it presented the identifiability bounds in the main text rather than deferring to the appendix. None of this undermines the core Count Bridge contribution, but it does mean the paper's significance rests more on its theoretical framing and spatial deconvolution demonstration than on its synthetic benchmarks or bulk deconvolution claims.

## Suggestions
1. Add a controlled synthetic deconvolution experiment where the projection-guided E-step can be compared against an oracle sampler (e.g., rejection sampling for small G) to characterize the approximation error.
2. Include a simple baselines for synthetic benchmarks (e.g., Poisson factor model, independent marginal Poisson distributions) to establish a lower bound.
3. Present a brief summary of the identifiability bounds from Apps. B.2/B.3 in the main text.
4. Add count-level evaluation metrics (per-gene MMD or W₂) for the bulk RNA-seq deconvolution to match the spatial evaluation.
5. Include DestVI in the main spatial deconvolution comparison, even if it requires a reference atlas.
6. Report all key training hyperparameters (architecture sizes, learning rate, batch size, optimizer, compute budget, training steps) for each experiment.

## Score and Decision

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>
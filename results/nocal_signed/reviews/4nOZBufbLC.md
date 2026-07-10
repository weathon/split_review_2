## Summary

This paper introduces Count Bridges, a novel stochastic bridge process on ℤ<sup>d</sup> based on Poisson birth-death dynamics, providing a principled generative framework for integer-valued data. The method yields closed-form conditionals (Bessel, Binomial/Hypergeometric) enabling exact training and sampling, and connects naturally to entropy-regularized optimal transport. The framework is extended to deconvolution from aggregated observations via an EM-style algorithm with projection-guided diffusion. The paper demonstrates the approach on synthetic distribution matching benchmarks and two large-scale biological applications: nucleotide-resolution single-cell expression modeling for bulk RNA-seq deconvolution, and spatial transcriptomic deconvolution into single-cell count profiles.

## Strengths

- **Principled discrete bridge with closed-form conditionals (Proposition 3.1, Algorithms 1–2).** The Poisson birth-death bridge on ℤ<sup>d</sup> is genuinely novel. The slack-variable reparameterization (M<sub>t</sub>, d<sub>t</sub>) yields tractable conditional distributions that are exact to sample from, and the CUDA kernel for fast Bessel sampling addresses practical scalability. This is a clean, theoretically satisfying construction that fills a clear gap in the discrete diffusion literature.

- **Elegant connection to Schrödinger bridges and optimal transport (Sections 3.1–3.2).** The derivation showing that Count Bridges solve an entropy-regularized OT problem is explicit, not superficial: κ → 0 recovers discrete OT with |x₁−x₀| cost and κ → ∞ yields the independent coupling. This echoes the Gaussian bridge case and gives practitioners principled guidance for choosing the jump intensity.

- **Ambitious and well-motivated biological applications.** The paper tackles two genuinely hard problems — nucleotide-resolution single-cell expression profile prediction from DNA sequence, and deconvolution of spatial transcriptomic spots into single-cell count profiles. These go beyond what existing methods (CIBERSORTx, STDeconvolve, cell2location) provide, as those output cell-type proportions rather than full count profiles and often require external reference atlases.

- **Honest limitations section (Section 7).** The paper explicitly acknowledges that the projection step "lacks serious theoretical support," that identifiability degrades with group size, and that Euclidean models may match performance when counts approximate continuous values. This candor is rare and valuable.

## Weaknesses

### Fatal
None.

### Major

- **The deconvolution evaluation tests an in-distribution task that is easier than the most challenging real-world scenario.** For bulk RNA-seq (Section 6.2), the model is trained on 90% of patients from a PBMC scRNA-seq dataset and tested on synthetic aggregates from held-out patients of the same dataset — sharing the same tissue, cell types, and assay. For spatial transcriptomics (Section 6.3), the model is trained on MERFISH data and tested on artificial aggregates from the same dataset. In neither case is generalization to a genuinely unseen tissue (where no matching single-cell reference is available) demonstrated. The paper does not claim cross-tissue generalization, so the evaluation is not invalid, but the limitations section (Section 7) does not specifically address this in-distribution scope. The claims about deconvolution capability should be accompanied by a clearer statement about the evaluation scope.

### Minor

- **The Blackout Diffusion comparison is absent from experiments.** The paper acknowledges Blackout Diffusion as the only count-specific generative method (Section 5, line 262) and correctly notes it uses a pure-death process that "cannot transport between arbitrary distributions." This fundamental limitation makes direct comparison on the bridge tasks infeasible. However, the claim of "state-of-the-art performance on integer distribution matching benchmarks" would be strengthened by either (a) including Blackout Diffusion on tasks where it is applicable, or (b) explicitly discussing why the pure-death constraint prevents direct comparison on the chosen benchmarks.

### Trivial

- Table 1 shows ±0.000 for Count Bridge Bulk MSE and MMD across 3 inference seeds. With a stochastic sampling procedure (Algorithm 2), exactly zero variance is unusual and warrants clarification (e.g., whether this reflects near-zero variance rounded to three decimal places, or a deterministic component in evaluation).

## Nice-to-Haves

- The Enformer comparison (Table 1) could be more precisely framed: CB uses Enformer-encoded features as input (line 327), so the comparison shows that adding the Count Bridges generative framework on top of Enformer features improves over fine-tuning Enformer alone. This is a positive result, but the current framing may lead readers to misinterpret it as an independent comparison rather than an ablation.
- Reporting the number of sampling steps (NFE) used in the real-world applications and key training details currently in the (parser-stripped) appendix would strengthen the main text.

## Removed Points

These points were flagged for removal based on the filtering rules; they should be treated with caution:

- "Table 3 is missing data": The table body is absent from the extracted text — this is a parser artifact. The original submission contains the table.
- "Code availability with placeholder link": Standard for blind review; not a substantive criticism.
- "Missing comparisons against cell2location/RCTD in spatial experiment": The paper benchmarks against STDeconvolve (the SOTA reference-free method) and states reference-based comparisons are in the appendix (stripped by the parser).
- "Deconvolution evaluation is fatal/framework-invalidating": Overstated. Held-out-patient evaluation is standard practice in the field.
- "Missing appendix details / proof sketches deferred to appendix": The appendix is stripped by the parser; these are access limitations, not author errors.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Add a clearer statement about the in-distribution scope of the deconvolution evaluation in the limitations section.
2. Clarify the ±0.000 entries in Table 1 by reporting variances with more significant figures or explaining why the variance is negligible.
3. Explicitly state that CB uses Enformer-encoded features in the Enformer comparison, framing it as an ablation showing the additive value of the generative framework.
4. Discuss why Blackout Diffusion cannot be straightforwardly compared on the bridge benchmarks (as the paper already notes its pure-death limitation) to preempt this question.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>
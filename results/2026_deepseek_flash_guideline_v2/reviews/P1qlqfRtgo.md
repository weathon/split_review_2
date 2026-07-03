Now I'll write the final review.

## Summary

This paper compares three neural network architectures — a plain MLP, a "U-Net-like" residual network (an MLP with two skip connections), and a "DeepONet-style" model — for approximating thermal explosion kinetics in hydrogen-oxygen-air mixtures. The dataset covers wide parameter ranges (T ∈ [250, 5000] K, p ∈ [10⁴, 2×10⁷] Pa, Δt ∈ [10⁻¹⁰, 10⁻⁵] s). The U-Net-like model achieves substantially lower MSE (0.00137) than MLP (0.0203) and DeepONet (0.0181), with non-overlapping 95% confidence intervals, establishing a statistically significant difference under controlled conditions.

## Strengths

1. **Controlled head-to-head comparison under identical conditions.** All three architectures are trained on the same 50k/15k/5k dataset split with the same optimizer (Adam, LR=0.001), batch size (5,000), number of epochs (100), and identical test set (Section 4.4, Table 1). This isolates architecture as the primary variable and makes the comparison clean.

2. **Multi-step recursive loss function.** The loss (Eq. 4) trains models to recursively forecast 30 steps ahead with 1/k weighting, directly penalizing error accumulation over multiple timesteps. This is well-motivated for stiff chemical kinetics, where single-step losses can mask long-horizon drift, and goes beyond simpler benchmarks.

3. **Physically diverse dataset covering extreme combustion regimes.** The training data spans rapid autoignition to slow relaxation phases (Section 3), addressing a gap noted in prior DeepONet combustion studies (e.g., Goswami et al., 2024, which used fixed timesteps and narrow ranges).

4. **Qualitative trajectory analysis validating physical consistency.** The paper examines representative low-MSE (Figure 3) and high-MSE (Figure 4) trajectories, showing that the U-Net-like model preserves phase alignment with reference dynamics (ignition timing, plateau shape, decay synchrony) in cases where other models drift.

## Weaknesses

### Major

1. **The "U-Net" is not a U-Net, and the paper's explanatory narrative about why it succeeds is unsupported.** The architecture described in §4.2 and Figure 2(B) is: input → 13×100 → 100×120 → 120×120 → 120×100 → 100×13, with a local skip (adding expansion output to the middle-block output) and a global skip (adding the original input to the final output). This is a fully-connected residual network — it contains no downsampling, no upsampling, no convolutions, no encoder-decoder symmetry, and no multi-scale feature hierarchy at any level. It is not a U-Net by any standard definition (Ronneberger et al., 2015). Despite the paper's consistent use of qualifiers like "U-Net-like" and "U-Net-style," the post-hoc explanation in Sections 5–6 attributes the architecture's superior performance to mechanisms it does not possess: **"hierarchical feature extraction"** (§6), **"multi-scale representation"** (Section 5, p. 157), and **"encoder-decoder design"** (Section 5, p. 157). Because the architecture actually lacks these properties, the paper's explanation for *why* it outperforms the alternatives is vacuous. The advantage could come from the residual connection alone — a well-known and unsurprising phenomenon in MLPs — or from some other factor. This is not a naming quibble; it is a disconnect between the claimed mechanisms and the actual experiment. **Impact:** This undermines the paper's central explanatory claim and means the paper does not deliver on the architectural comparison its framing promises.

2. **The DeepONet implementation is non-standard, making the comparison uninformative about operator-learning methods.** In the standard DeepONet formulation (Lu et al., 2021), the branch network encodes an input function evaluated at multiple sensor points, and the trunk network encodes the output coordinate. Here, the "branch" takes the 12 state variables as a fixed-dimensional vector (not a function), and the "trunk" takes a single scalar (dt) rather than an output coordinate. The resulting architecture is a two-stream MLP with a matrix-product fusion layer — it is not representative of the operator-learning paradigm that motivates the comparison in §1. The paper's stated open question asks whether "operator-learning architectures such as DeepONet can provide superior accuracy" (§1), but the experiment cannot answer this question with the current implementation. The conclusion "DeepONet and MLP have comparable performance" may be true of this specific implementation but cannot generalize to DeepONet as a class.

3. **The 95% confidence interval method is not specified, and interpretation is questionable given the error distribution.** The standard deviations in Table 1 are 3–16× larger than the corresponding means (e.g., U-Net: SD=0.0218, mean=0.00137). For MSE (a non-negative quantity), this implies a heavily right-skewed distribution — most test samples have very small errors but a few have catastrophically large errors. The paper does not state whether the CIs were computed via bootstrap, normal approximation, or another method, nor whether the method accounts for the skewed distribution. Without this information, the CIs cannot be properly evaluated. Additionally, the fact that SD/mean is ~16 for U-Net vs. ~3–4 for MLP and DeepONet raises the question of whether the U-Net's advantage is concentrated in easy samples while it fails as dramatically on hard cases as the other models — the paper does not analyze this.

### Minor

4. **No hyperparameter tuning and limited training budget.** All models are trained for 100 epochs with batch size 5,000 on 50,000 samples = 1,000 total gradient updates. No learning rate schedule, early stopping, or hyperparameter search (layer widths, learning rate, batch size) is reported (§4.4). When the training budget is this constrained, default optimizer settings may arbitrarily favor some architectures, conflating convergence rate with final capacity. The paper does not report whether models converged or whether 100 epochs was sufficient for all architectures to plateau.

5. **No per-species or per-regime quantitative error breakdown.** The paper reports only total MSE and qualitative trajectory plots. It does not analyze whether the U-Net's advantage varies by species, by combustion regime (e.g., ignition vs. equilibrium), or by trajectory difficulty (e.g., by ignition delay time or temperature gradient). Such analysis would directly support the paper's goal of understanding architecture impact.

6. **No ablation framing.** Since the U-Net differs from the MLP primarily by two residual skip connections, the comparison essentially tests "do residual connections help in MLPs?" — a well-known result. The paper never frames the plain MLP as an ablation of the U-Net (i.e., U-Net minus skip connections), missing an opportunity to present the comparison as a controlled ablation study.

7. **Unclear whether test MSE is one-step or multi-step.** The paper states "MSE on an identical test set" (§5) but does not clarify whether this is single-step prediction or k-step recursive prediction, despite the loss using a multi-step formulation (Eq. 4).

8. **Unclear whether copied components (dt, N₂, Ar) contribute to the loss.** The paper states these are "directly copied from the input" but does not specify whether their contribution to the MSE is zeroed. If included, the reported MSE includes a trivial component all models master, slightly inflating apparent performance.

### Trivial

9. **No runtime or parameter count comparison**, despite claiming the U-Net "does not increase computational cost" (§5). All models have ~40K parameters, so this gap is small but should be substantiated.

10. **The choice of n_steps=30 is not justified.** The paper does not explain why 30 steps was chosen or how Δt variation over 5 orders of magnitude affects the effective time horizon across trajectories.

## Nice-to-Haves

- A proper U-Net implementation (with down/up-sampling, convolutions, true multi-scale connections) or, alternatively, renaming the architecture to "Residual MLP" and reframing the explanation to match.
- A faithful DeepONet implementation where the branch encodes a function (e.g., a past time window) and the trunk encodes the prediction coordinate.
- Per-species error tables and per-regime breakdowns to locate the source of the U-Net's advantage.

## Removed Points

The following points from the inputs were removed as invalid, speculative, or not anchored in the paper:

- **"Abstract contradiction" (Harsh Critic, §1):** The abstract states both that "the problem remains unresolved" and that U-Net outperformed. These are not contradictory — the overall challenge of accurate combustion modeling remains open (an honest assessment), while U-Net was the best among tested architectures. This is a reasonable framing.
- **"Training data modest by modern standards":** 70k trajectories from an ODE solver with randomized conditions is a reasonable dataset size for this task. This criticism has no quantitative anchor.
- **"Limited architectural scope" (no transformers, LSTMs, etc.):** The paper explicitly scopes to three architectures. Demanding more is scope creep.
- **"No discussion of multi-step evaluation" (partially):** This is addressed as Minor weakness 7 above (unclear test MSE formulation), but the Harsh Critic's broader framing of this as a major gap overstates the issue.
- **Strength Finder's generic strengths** (e.g., "this paper addresses an important problem"): Removed as generic/superficial.

## Novel Insights

None beyond the paper's own contributions. The reviews confirm the obvious reading: the paper compares three architectures, one is mislabeled, the explanations are mismatched to the actual design, and the methodological reporting has gaps.

## Suggestions

1. **Rename the architecture.** The "U-Net-like residual network" is simply an MLP with residual skip connections. Call it "Residual MLP" or "MLP with skip connections." Remove all references to "multi-scale representation," "hierarchical feature extraction," and "encoder-decoder design" that the architecture does not possess. The empirical finding (skip connections help) is genuine and worth reporting, but the current framing is misleading.

2. **Implement faithful baselines** — either a proper U-Net (with down/up-sampling, convolutions) and a proper DeepONet (branch encodes a function at sensor points, trunk encodes output coordinates), or disclaim that the tested architectures are "inspired by" these families and do not represent canonical implementations. Currently the paper's framing promises a comparison it does not deliver.

3. **Specify the CI computation method** and consider bootstrap confidence intervals given the skewed error distribution. Report the number of test samples and the CI formula.

4. **Clarify whether test MSE is one-step or multi-step** and whether the loss includes the copied components (dt, N₂, Ar). Report per-species and per-regime errors.

5. **Frame the plain MLP as an ablation** of the U-Net (i.e., U-Net without residual connections) to clarify what the comparison actually shows.

---

### Score and Decision

I was unable to use the calibration search tool due to a file-access issue, so I rely on direct judgment. This paper has a genuine empirical finding (residual connections in MLPs improve surrogate accuracy for combustion kinetics) and a clean experimental setup. However, the paper's central contribution is undermined by a significant gap between its framing and its content: the "U-Net" tested is an MLP with residual connections, not a U-Net, and its performance is attributed to properties (multi-scale representation, hierarchical feature extraction) that the architecture does not instantiate. The DeepONet baseline is also non-standard. These issues mean the paper does not deliver the architectural comparison its title and framing promise. Combined with several methodological gaps (unreported CI method, no hyperparameter tuning, unknown test-MSE formulation), the paper does not meet the bar for a top conference. The work could be strengthened substantially by honest reframing and additional analysis, but in its current form it is not ready for publication.

**Score:** 3.5 (Reject)

**Decision:** Reject

MY FINAL SCORE: <score>3.5</score>
MY FINAL DECISION: <decision>Reject</decision>
## Summary

This paper introduces Proper Velocity (PV) Neural Networks, the first systematic treatment of the PV model of hyperbolic geometry for deep learning. The authors derive the complete Riemannian toolkit (exponential/logarithmic maps, parallel transport, geodesic distance) on PV space by leveraging an isometry to the Poincaré ball, and construct practical neural network layers (MLR, FC, convolution, activation, batch normalization). Experiments across numerical stability, image classification, graph node classification, and genomic sequence learning demonstrate that the unconstrained PV representation avoids boundary singularities that cause numerical issues in the Poincaré ball and hyperboloid models, while matching or exceeding their downstream accuracy.

## Strengths

1. **First systematic treatment of an underexplored hyperbolic model.** Almost all existing HNN work operates on the Poincaré ball or hyperboloid. The paper correctly identifies this gap and provides a complete Riemannian toolkit for PV space (Thms. 4.2–4.3), which is a genuine contribution to the hyperbolic learning literature.

2. **Clean theoretical derivation via isometry.** Rather than re-deriving operators from scratch, the paper proves (Thm. 4.2) that PV space and the Poincaré ball are Riemannian isometric, then obtains closed-form Exp, Log, parallel transport, and geodesic distance by pushing the Poincaré operators through the isometry (Thm. 4.3). The differentials are verified explicitly (Lem. 4.1).

3. **Practical simplification of the MLR layer (Eq. 19).** The translation from the gyro-formulation (Eq. 18) to the inner-product-based simplified form (Eq. 19) is a genuine engineering contribution. The original gyro-form requires a `b × C × n` intermediate tensor or a loop over classes; Eq. 19 reduces this to a matrix multiplication `<x, z_k>`. The paper calls this out explicitly and correctly (lines 161–162).

4. **Convincing numerical stability evidence.** Tables 1–3 are the strongest empirical contribution. The PV model shows zero failure rate up to r=1000 in FP32, while the hyperboloid fails catastrophically (100% failure at r=200). The round-trip error for PV (2.1×10⁻⁷ in FP32) is orders of magnitude better than Poincaré (2.1×10⁻⁴) and hyperboloid (1.0). These results cleanly demonstrate that the unconstrained PV representation translates to a real numerical advantage.

5. **Broad experimental scope with thorough ablations.** The paper evaluates on four distinct tasks and provides multiple ablations per task: tangent vs. Riemannian layers (Tab. 6), Fréchet vs. approximate batch statistics (Tab. 7), with/without Exp₀ lifting (Tab. 8), and activation variants (Tab. 9). This is more thorough than typical for a first paper proposing a new hyperbolic model.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **Accuracy gains on image classification are modest and within noise.** On CIFAR-10, PV MLR achieves 95.30% vs. the best Poincaré baseline at 95.12% — a 0.18% gap with overlapping standard deviations (±0.18 vs. ±0.20). On CIFAR-100, the gap is 78.20% vs. 77.96% (+0.24%). These differences are not statistically meaningful with the reported error bars. The paper's wording ("matches or outperforms") is technically correct, but the abstract's framing of "effectiveness" rests more on the graph and genomics results. This does not threaten the core contribution (the stability experiments are the primary evidence), but it tempers the downstream performance claims.

2. **The large Airport result is not explained.** On Airport (δ=1), PVNN achieves 97.96% vs. the best baseline (KNN Klein ball) at 92.10% — a 5.86% gap that is an order of magnitude larger than gains on other datasets. The paper attributes this to strong hyperbolicity, but Disease (δ=0, more hyperbolic) shows only a +0.58% gain over the strongest baseline. Since all models share the same architecture, this outlier magnitude warrants some analysis — e.g., tracking feature norms during training to show that the Poincaré/hyperboloid baselines hit boundary constraints on Airport while PV avoids them. Without such analysis, the result is striking but unexplained, weakening the claim that PV is *generally* superior for strongly hyperbolic data.

3. **Lack of statistical significance testing.** The paper reports 5-fold means and standard deviations across all experiments but does not perform any formal significance tests (e.g., paired t-tests between PVNN and the best baseline per dataset). Some claimed improvements (CIFAR-10, CIFAR-100, PubMed) have overlapping error bars. Reporting whether differences are statistically significant would strengthen the empirical claims.

4. **No curvature sensitivity analysis.** The paper uses K=-1 for stability tests and "a single curvature shared for all layers" for downstream tasks (line 379). Curvature is a critical hyperparameter in hyperbolic networks. A sensitivity analysis showing how PVNN, Poincaré, and hyperboloid models respond to different curvature values would be informative and could further demonstrate PV's stability advantage.

5. **No end-to-end wall-clock or memory comparison.** While the paper reports Fréchet mean computation time (Tab. 7), there is no end-to-end training time or memory usage comparison for full PVNN vs. baselines. Since PV's advantage is partly computational (e.g., the simplified MLR avoids large intermediate tensors), showing that PVNN is faster or more memory-efficient at scale would be persuasive but is currently missing.

### Trivial
None.

## Nice-to-Haves

- A second genomics dataset would strengthen the task category beyond TEB.
- Analyzing why the Airport dataset specifically benefits so dramatically from PV (e.g., tracking feature norms during training) would turn an unexplained gap into a mechanistic demonstration.
- Reporting whether a numerically stabilized Poincaré baseline (e.g., with gradient clipping) closes any of the downstream accuracy gaps would address a natural counterargument.

## Removed Points

These points from the input review are removed with justification:

- **"PV convolution is essentially a PV FC on concatenated Euclidean inputs."** — The paper is fully transparent about this (Sec. 5.3: "Because PV space is unconstrained, we define PV concatenation to coincide with Euclidean concatenation."). Calling this a "weakness" misunderstands the nature of the contribution: the convolution inherits from the FC layer, and the genomics experiments show it benefits from the PV components. This is not a flaw, it is a design choice that is clearly stated.

- **"The paper does not compare against a stabilized Poincaré baseline"** (as a general concern about all downstream experiments). — Table 1 shows the Poincaré ball already has 0% failure rate and 0% violation rate in FP32 for gyro operations; its numerical stability for standard operations is good. The gradient vanishing in Table 3 is a *geometric* property of the bounded representation, not a numerical implementation artifact that clipping or mixed precision could fix. The concern has more validity for hyperboloid baselines, but even there it is speculative and does not invalidate the paper's core evidence.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Add statistical significance tests (paired t-tests or similar) between PVNN and the best baseline on each dataset to clarify which gains are robust.
2. Add a brief analysis of the Airport outlier: e.g., track feature norms during PVNN vs. Poincaré/hyperboloid training to demonstrate that the constrained models hit boundary issues on that dataset while PV does not.
3. Include a curvature sensitivity sweep (K ∈ {−0.1, −1, −10}) on at least one graph and one vision dataset.
4. Report wall-clock training time per epoch and peak GPU memory for PVNN vs. baselines at matching batch sizes and dimensions.

## Score and Decision

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>
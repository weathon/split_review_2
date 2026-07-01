## Summary

This paper introduces Automatic Complementary Separation Pruning (ACSP), a structured pruning method that constructs a graph space encoding each channel/neuron's class-pair separability (via JM distance), then uses k-Medoids clustering + the Kneedle algorithm to automatically select a diverse, complementary subset of components to retain. The method is evaluated on VGG, ResNet, DenseNet, and MobileNet across CIFAR-10/100 and ImageNet, consistently achieving 1.5–2.5× FLOP reduction with minimal accuracy loss, and is supported by actual latency measurements.

## Strengths

1. **Novel graph-space formulation.** Encoding each component's separability via JM distances across all class pairs and using clustering to enforce complementary selection is a genuinely original departure from ranking-based pruning heuristics. The conceptual shift from "which components are individually important" to "which components collectively cover the separation space" is well-motivated (Section 3.3, Figure 1).

2. **Broad experimental coverage.** The evaluation spans four architecture families (VGG-16/19, ResNet-50/56, DenseNet-40, MobileNet-V2) and three datasets (CIFAR-10/100, ImageNet), with ACSP achieving the highest or near-highest speed-ups in most settings while maintaining or slightly improving accuracy (Table 1).

3. **Actual latency measurements.** The paper reports real inference latency in both batch and single-input modes (Table 2), going beyond the FLOP-only reporting common in pruning papers. The transparency about the gap between FLOP ratios and wall-clock speed-ups is a genuine point of rigor (Section 4.5).

4. **Clear algorithmic exposition.** The pipeline from activations → separation matrix → clustering → knee-finding → weight-based selection is well-structured and reproducible in principle (Algorithm 1, Section 3).

## Weaknesses

### Fatal
None.

### Major

1. **Core claims are unsubstantiated by ablation studies.** The method rests on several non-trivial design choices that are asserted as contributions but never isolated via controlled experiments:
   - *Complementary selection via k-Medoids+MSS* vs. simply selecting top-k components by weight (which would test whether the entire graph-space machinery is necessary).
   - *Kneedle-based automatic pruning extent* vs. a manually-tuned or fixed per-layer ratio.
   - *JM distance* vs. alternative separability metrics (Hellinger, Wasserstein — the paper claims these were tested, line 127, but provides no results).
   - *Weight-based within-cluster selection* vs. medoid-only or random within-cluster selection.

   Without these ablations, the reader cannot determine whether ACSP's empirical success follows from the complementary-selection principle or from simpler factors such as the fine-tuning protocol, the weight-based selection (which is effectively magnitude pruning with a diversity prior), or the layer-by-layer iterative procedure. The paper's claimed novelties are therefore asserted, not demonstrated. This is the most consequential weakness — it does not invalidate the method, but it means the paper's central intellectual contribution is untested.

2. **"Fully automated" claim is overstated relative to remaining design choices.** The paper emphasizes that ACSP eliminates manual tuning of the pruning ratio (abstract: "fully automated method"; line 27: "fully automates neural network pruning"). However, the method still requires user-specified parameters: the polynomial degree for Kneedle (fixed at 2, line 174), the distance metric for k-Medoids (not specified at all), the proportion of data used for fine-tuning (25%), and the fine-tuning schedule (learning rate, epochs). Crucially, the paper studies sensitivity to none of these choices. If the method requires per-dataset or per-architecture tuning of internal parameters to produce good results, the "automatic" framing is weaker than suggested.

### Minor

3. **Numerical inconsistency in ResNet-50/ImageNet results.** Table 1 (line 231) reports ACSP on ResNet-50 as 76.32 → 76.98 with Δ = +0.59. However, 76.98 − 76.32 = 0.66, and the main text (line 265) states "+0.66% accuracy improvement." The table's Δ value is inconsistent with both the numbers in the same row and the text. This needs correction.

4. **Fine-tuning protocol confounds baseline comparisons.** ACSP fine-tunes after each layer (2 epochs on CIFAR, 3 on ImageNet). The paper does not state whether the baselines in Table 1 use a similar fine-tuning regimen. If ACSP benefits from more aggressive or differently scheduled fine-tuning than the baselines, the comparison is not informative about the pruning criterion itself. The paper should either standardize fine-tuning across methods or clearly discuss each baseline's protocol.

5. **Scalability of graph-space construction is insufficiently addressed.** For ImageNet (C=1000), the separability vector per component has dimension p × p × C(C−1)/2 — e.g., for an early ResNet layer with p=28, this is ~392 million dimensions. The paper claims (line 71) that the Kneedle step runs in "below 0.1 s," but this applies only to the knee-finding, not to constructing the graph space itself. The conclusion (line 283) acknowledges this limitation but dismisses it without quantitative analysis. For practitioners, the actual cost of building the graph space per layer at ImageNet scale is a practical concern that the paper does not characterize.

### Trivial

6. **Incorrect citation in Table 1.** In the MobileNet-V2/CIFAR-10 section, the ACSP row reads "ACSP (Gao et al., 2023)" (line 193), attributing the authors' own method to a different paper. This appears to be a template carry-over from the SANP row above and should be corrected.

## Nice-to-Haves

- **Report statistical variability.** Pruning results can be sensitive to random seeds (data subsets, initialization); reporting standard deviations across multiple runs (especially for CIFAR experiments, where this is computationally feasible) would strengthen the empirical claims.
- **Add a random-pruning baseline.** Comparing ACSP against random channel/neuron pruning at the same FLOP reduction rate, with the same fine-tuning protocol, would contextualize the benefit of the proposed selection criterion.
- **Ablate the separability metric choice.** A small table showing post-pruning accuracy with JM, Hellinger, and Wasserstein distances for one architecture would substantiate the claim that "JM distance consistently achieved the best balance" (line 127).
- **Sensitivity analysis for Kneedle parameters.** Exploring stability across polynomial degrees or alternative knee-detection algorithms would strengthen the claim of automated, robust pruning extent selection.

## Removed Points

These points are flagged to be removed; treat them with caution:

- **Section-by-section notes about Introduction/Related Work** (e.g., "does not discuss how DepGraph/SCOP determine pruning ratios"). These are exposition preferences about how sharply the contrast is drawn with prior work, not substantive weaknesses.
- **"FLOP vs. latency in the abstract" framing concern.** The paper is transparent about this in Section 4.5, and the abstract's speed-up claim cites a FLOP ratio, which is standard in the pruning literature.
- **Missing comparisons to prior automated methods.** The paper cites AMC, MetaPruning, and gating-based approaches; requesting a quantitative comparison of their automation mechanisms goes beyond what the paper sets out to do.
- **Statistical variability / confidence intervals.** This is not a standard reporting requirement for large-scale pruning benchmarks; it is a nice-to-have.
- **Request for random-pruning comparison.** While reasonable, this belongs in Nice-to-Haves, not as a core weakness — the paper compares against published methods, many of which are stronger than random.

## Novel Insights

None beyond the paper's own contributions. The harsh critic's review surfaces a genuine structural issue (missing ablation) but does not reveal any insight about the method or problem that the paper itself does not already state or imply.

## Suggestions

1. **Add a focused ablation study** that compares ACSP against at least three variants: (a) top-k selection by weight alone (removing the graph-space/clustering machinery), (b) random within-cluster selection, and (c) medoid-only selection (no weight-based refinement). This single experiment would substantiate or refute the paper's core claim about complementary selection.
2. **Quantify the computational cost** of graph-space construction as a function of C (classes) and spatial size p, ideally with a table showing per-layer construction time on ImageNet for a representative architecture.
3. **Correct the numerical inconsistency** in Table 1's ResNet-50 row (Δ should be +0.66, not +0.59) and remove the spurious "(Gao et al., 2023)" citation from the ACSP row.
4. **Add a brief sensitivity discussion** for the method's fixed parameters (Kneedle polynomial degree, fine-tuning data fraction) to substantiate the claim of automation.

## Score and Decision

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>
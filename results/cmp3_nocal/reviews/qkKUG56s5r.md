## Summary

ACSP introduces a method for automated structured pruning that avoids manual per-layer pruning ratios. It constructs a "graph space" encoding each neuron/channel's class-pair separability (via Jeffries-Matusita distance), then uses k-Medoids clustering guided by a Mean Simplified Silhouette index and Kneedle knee-finding to select a diverse, complementary subset of components to retain. Experiments span CIFAR-10/100 and ImageNet across VGG, ResNet, DenseNet, and MobileNet architectures.

## Strengths

- **Honest latency measurements (Table 2).** The paper reports both FLOP reduction and wall-clock inference latency, explicitly noting (line 277) that hardware speedup is smaller than FLOP ratios would suggest. This transparency is rare and valuable.
- **Broad empirical coverage.** Results span CIFAR-10, CIFAR-100, and ImageNet-1K across four architecture families (VGG-16/19, ResNet-56/50, DenseNet-40, MobileNet-V2), demonstrating competitive or leading speedups on most configurations.

## Weaknesses

### Fatal

- **The method as described is computationally infeasible for ImageNet, yet ImageNet results are reported without explanation.** The paper specifies (lines 59, 67, 101) that each component's separability vector has dimensionality \(p \times p \times \binom{C}{2}\). For ImageNet \(C=1000\), \(\binom{C}{2} \approx 500,\!000\). For a ResNet-50 convolutional layer with spatial size \(p=7\) (the smallest in the network), each component's vector is \(49 \times 500,\!000 \approx 24.5\) million entries. For a layer with 2048 channels, the full graph-space matrix would be roughly 200 GB in float32; for mid-network layers with \(p=28\) or \(p=56\), it grows to 400 GB–1.6 TB. The paper's hardware (4× RTX 6000 with 24 GB each) cannot accommodate this. The paper acknowledges this only as a "limitation" and "future work" (Section 5, line 283), yet reports ImageNet results as though the method ran without issue. No approximation or dimensionality-reduction strategy is stated. This is not a missing ablation or minor gap — the method definition and the reported experiments are in direct contradiction. The ImageNet results cannot be reproduced from the description provided.

### Major

- **Computational cost of the pruning algorithm is understated.** The paper states (line 71) "The Kneedle implementation runs in \(\mathcal{O}(N_i^2)\) time, but with \(N_i \leq 256\) the wall-clock cost is below 0.1 s on an RTX 6000, so ACSP adds negligible overhead." This refers only to the knee-finding step. Algorithm 1 (lines 7–10) runs a full k-Medoids clustering *from scratch* for every \(k \in \{2, \dots, N_i\}\) — up to 255 separate k-Medoids runs per layer. The dominant cost is this loop, not Kneedle. For a network with ~50 prunable layers, this overhead is non-negligible and should be quantified and reported rather than conflated with the trivial Kneedle step.

- **No statistical reliability measures.** All accuracy numbers in Table 1 are single points with no standard deviation, confidence intervals, or indication of multiple runs. The fine-tuning uses a random 25% subset of data (line 172); different random draws would yield different results. Many accuracy changes are within \(\pm 0.6\%\), which is within typical training variance for these architectures. Without multiple trials, the reader cannot distinguish genuine improvement from random variation, and claims of "consistently" maintaining accuracy cannot be evaluated.

- **Critical ablations absent.** Two central design choices are untested: (1) The paper never compares ACSP against a baseline that simply selects the top-\(k'\) components by weight magnitude (no graph-space clustering, no complementarity) — this is the most direct test of whether the graph-space machinery adds value. (2) The paper claims to have evaluated JM, Hellinger, and Wasserstein distances (line 127) but provides no quantitative comparison; the reader is simply told JM "consistently achieved the best balance." Without these ablations, the results cannot be attributed to the claimed innovations (complementary selection, JM-based separability) rather than to the fine-tuning or weight-based refinement.

### Minor

- **Tension between "complementary" framing and final selection mechanism.** Section 3.3.2 motivates clustering in graph space to select medoids as complementary representatives. However, Section 3.4.2 (line 120, Algorithm 1) switches to selecting the *highest-weight* component from each cluster instead. The paper provides a rationale (weights matter for performance), but this means the final selection is weight-driven within clusters. An ablation comparing medoid selection against weight-refined selection is needed to clarify which mechanism drives results.

- **"Automatic" is somewhat overstated.** The Kneedle algorithm has a design parameter (second-degree polynomial, noted in line 174) whose sensitivity is never analyzed. The method is not parameter-free; it eliminates manual per-layer pruning ratios but still has design choices.

- **Base accuracy discrepancies across methods.** In Table 1, base accuracies for the same architecture/dataset differ across compared methods (e.g., ResNet-56 base ranges from 92.80 to 93.71). This is standard in pruning evaluations (different training setups), but it makes \(\Delta\) Accuracy comparisons noisier than they appear, and the paper does not acknowledge this.

### Trivial

None.

## Nice-to-Haves

- **Provide the missing ablations** (weight-only baseline, JM vs. Hellinger/Wasserstein comparison, medoid vs. weight-refined selection) to validate the claimed innovations.
- **Repeat experiments with at least 3 random seeds** and report means and standard deviations for the reported accuracy numbers.
- **Quantify wall-clock pruning time** for each architecture, including the k-Medoids loop, so practitioners can assess the automation cost.
- **Report what approximation was used for ImageNet** (e.g., class-pair sampling, dimensionality reduction, or per-layer batching) if the method was made tractable — this is essential for reproducibility.

## Removed Points

- *"No code or model release is mentioned"* — Removed per hard rules: criticisms about unreleased code being framed as reproducibility doubts about cited entities. Code is not cited in the paper. Moved here as context.
- *"Typo: ACSP (Gao et al., 2023)"* — Removed per hard rules: formatting artifacts from PDF parsing are attributed to parser errors, not author errors.
- *"Addresses a genuine pain point"* (original Strength 1) — Removed per filtering rules: generic strength about the importance of the problem, not specific to the paper's contribution.
- *"The characterization that 'none of the above methods fully automate' is arguable"* — Removed per filtering rules: this is a qualitative judgment about related-work framing, not a concrete weakness in the paper's claims.
- *"Pixel-level granularity may help or hurt"* — Removed per filtering rules: speculative concern about spatial granularity without identifying a concrete problem in the reported results.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Resolve the ImageNet tractability issue as the highest priority.** Either clearly describe the approximation or computational strategy used to make the method work for 1000 classes, or restrict claims to datasets (CIFAR-10/100) where the method is clearly feasible. The current contradiction between the stated dimensionality and the reported experiments undermines the entire empirical contribution.
2. **Report the wall-clock time of the full pruning process** (including the k-Medoids loop), not just the Kneedle step.
3. **Add the three missing ablations** listed above; they are the simplest way to validate that the complexity of the graph-space machinery earns its keep.
4. **Run multiple trials with different random seeds** and report standard deviations, given the small accuracy differences at stake.

## Score and Decision

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>
## Summary

This paper compares three neural network architectures—a plain MLP, a U-Net-style residual network, and a DeepONet-inspired model—for predicting the temporal evolution of chemical species and temperature in a hydrogen-oxygen-air thermal explosion system. The authors generate a dataset using a reduced kinetic mechanism with 11 species across wide ranges of temperature, pressure, and time steps, and evaluate each architecture on its ability to predict 30-step-ahead trajectories. The U-Net-style residual network achieves substantially lower mean squared error (0.00137) and narrower confidence intervals compared to the MLP (0.0203) and DeepONet (0.0181), demonstrating that architectural choices significantly impact predictive performance for stiff chemical kinetics.

## Strengths

- **Practical relevance**: The paper addresses a genuine computational bottleneck in combustion simulations—the high cost of solving stiff ODE systems for chemical kinetics—and evaluates neural network surrogates as a potential acceleration strategy.
- **Fair comparison setup**: All three architectures are trained on the same dataset with identical training procedures (Adam optimizer, learning rate, batch size, epochs, and the same multi-step loss function), ensuring that performance differences are attributable to architecture rather than training conditions.
- **Statistically rigorous reporting**: The paper reports 95% confidence intervals and standard deviations alongside mean MSE, and correctly notes that the U-Net's confidence interval does not overlap with those of the other models, establishing statistical significance of the improvement.
- **Qualitative validation**: Figures 3 and 4 provide visual evidence that the U-Net preserves phase alignment and qualitative dynamics (ignition peaks, decay phases) even on challenging trajectories where MLP and DeepONet drift, which strengthens the claim beyond aggregate metrics.

## Weaknesses

### Fatal
None.

### Major
- **The DeepONet implementation is non-standard and likely suboptimal**: The paper's DeepONet-style model uses a branch network that takes 12 state variables and a trunk network that takes only the scalar `dt`. In standard DeepONet, the trunk network encodes the evaluation coordinate (here, the time point), and the branch network encodes the input function. However, the authors' design feeds the entire state vector into the branch and only `dt` into the trunk, then performs a matrix product. This deviates significantly from the standard DeepONet formulation where the trunk should encode the coordinate at which the operator is evaluated (e.g., the specific time step index or absolute time), and the branch should encode the initial condition or input function. The resulting architecture is more akin to a two-stream network with a bilinear layer than a proper operator-learning model. This likely handicaps DeepONet's performance and makes the comparison unfair.
- **The U-Net architecture is misnamed**: The paper calls its residual network "U-Net-style," but the described architecture (input → 13×100 → 100×120 → 120×120 → 120×100 → 100×13 with a single skip connection) is a standard residual MLP, not a U-Net. U-Nets are characterized by an encoder-decoder structure with downsampling/upsampling and multiple skip connections at different resolutions. The paper's architecture has no downsampling, no upsampling, and only one skip connection. This is a significant misrepresentation that could mislead readers about what architectural features actually drive the performance improvement.
- **Limited architectural exploration**: The paper only tests three architectures, and the "U-Net" is essentially an MLP with one residual connection. The conclusion that "U-Net-based architectures" are promising is overstated given that the tested architecture is not a true U-Net. The paper would benefit from testing a proper U-Net with hierarchical downsampling, a deeper residual network, or a transformer-based model to better understand which architectural features matter.
- **No ablation study on the skip connection**: The U-Net's improvement over the MLP could be entirely due to the single residual skip connection. Without testing an MLP with just that skip connection (i.e., a ResNet-style MLP), the paper cannot attribute the improvement to any "U-Net-like" hierarchical representation. The comparison conflates multiple architectural differences.

### Minor
- **The dataset generation and preprocessing details are insufficient**: The paper states the dataset covers T ∈ [250, 5000] K, p ∈ [10^4, 2×10^7] Pa, and Δt ∈ [10^{-10}, 10^{-5}] s, but does not specify how many trajectories were generated, how initial conditions were sampled (uniformly? log-uniformly?), or how the 70,000 total samples (50k train, 15k val, 5k test) are distributed across these conditions. The claim of "broad and relatively unbiased sampling" is unverifiable.
- **The multi-step loss function (Equation 4) is unusual**: The loss sums MSE over 30 steps with a 1/k weighting, which downweights later steps. The authors do not justify this weighting scheme or show results without it. Standard practice for multi-step prediction is either unweighted sum or exponential weighting; the 1/k weighting is atypical and could affect which architectures perform best.
- **No computational cost comparison**: The paper claims the U-Net improves performance "without increasing computational cost," but provides no runtime, parameter count, or FLOPs comparison. Given the architectures have different structures, this claim is unsupported.
- **The figures are difficult to read**: Figures 3 and 4 use dashed lines of similar styles (red dashed, blue dashed, green dotted) on small subplots with many overlapping curves. The species labels in the figures (CO, NO) do not match the 11 species listed in the paper (which includes OH*, H, O, HO2, H2O2, N2, Ar but not CO or NO), suggesting the figures may be from a different dataset or contain labeling errors.

### Trivial
- The abstract states "the problem remains unresolved," which is an unusual framing for a paper that claims a successful architecture.
- The paper uses "U-Net" and "U-Net-like" interchangeably in the text and tables, but the architecture is not a U-Net.

## Nice-to-Haves

- An ablation study that isolates the effect of the residual skip connection by comparing the MLP with and without it.
- A proper DeepONet implementation where the trunk network encodes the evaluation time coordinate and the branch encodes the initial state, following the standard formulation.
- Parameter count and inference time comparisons for all three architectures.
- An analysis of which chemical species or temporal regimes are most challenging for each architecture.

## Novel Insights

None beyond the paper's own contributions. The finding that residual connections improve prediction accuracy for stiff ODE systems is consistent with established knowledge in the field. The paper's main contribution is a practical comparison on a specific combustion dataset, but it does not introduce new architectural ideas or theoretical insights.

## Suggestions

1. Rename the "U-Net-style residual network" to "residual MLP" or "MLP with skip connection" to accurately reflect the architecture.
2. Re-implement the DeepONet following the standard formulation (branch network encodes the initial condition vector, trunk network encodes the evaluation time) and re-run the comparison.
3. Add an ablation experiment: compare the plain MLP with an MLP that has exactly one residual skip connection (the same as the "U-Net" but without the expansion/compression layers) to isolate the effect of the skip connection from the dimensional changes.
4. Report the number of parameters and inference time for each model to support the claim of no additional computational cost.
5. Clarify the dataset: specify the number of trajectories, the sampling strategy for initial conditions, and verify that the species labels in Figures 3 and 4 match the 11 species described in the paper.

## Score and Decision

The paper addresses a relevant problem and provides a fair comparison framework, but the major issues—particularly the misrepresentation of the U-Net architecture and the non-standard DeepONet implementation—undermine the validity of the core claims. The paper's conclusions about "U-Net-based architectures" and the comparison with DeepONet are not supported by the actual experiments conducted. The contribution is incremental and the experimental design has significant flaws that would need to be addressed before the paper could be accepted.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>
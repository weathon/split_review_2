## Summary
This paper compares three neural network architectures—a standard MLP, a U-Net‑style residual network, and a DeepONet‑inspired model—for predicting the temporal evolution of chemical species and temperature during a thermal explosion in a hydrogen‑oxygen‑air mixture. The authors generate a dataset covering wide ranges of temperature, pressure, and time steps using a reduced kinetic mechanism. They report that the U-Net‑style model achieves substantially lower mean squared error (MSE ≈ 0.0014) and tighter 95% confidence intervals compared to the other two architectures (MSE ≈ 0.02), and conclude that network architecture is a critical factor in building accurate surrogates for stiff chemical kinetics.

## Strengths
- **Practically relevant problem**: Accelerating combustion simulations is of clear importance for engineering applications, and the paper targets a genuine bottleneck—stiff chemical kinetics.
- **Broad parameter range in training data**: The dataset covers wide intervals (250–5000 K, 10⁴–2×10⁷ Pa, 10⁻¹⁰–10⁻⁵ s), which increases the likelihood of capturing diverse combustion regimes.
- **Multi‑step prediction loss**: Training with a recursive multi‑step objective (up to 30 steps) encourages the models to handle error accumulation, a sensible strategy for time‑series forecasting.

## Weaknesses
### Major
1. **Misrepresentation of the “U‑Net” architecture**: The so‑called U‑Net is simply a fully‑connected MLP with one local skip (adding the output of the first expansion layer to the output of the last hidden block) and a global skip from the input to the output. It contains no downsampling/upsampling, no convolutional layers, and no encoder‑decoder structure. Labeling it as “U‑Net‑style” is misleading and inflates the perceived novelty. A more accurate term would be “residual MLP” or “ResNet‑like MLP.”
2. **Unfair and non‑standard DeepONet baseline**: The DeepONet implementation departs significantly from the standard formulation. The trunk network receives only the scalar *dt*, while the branch network processes the 12 state variables. In standard DeepONet, the trunk typically encodes coordinates (e.g., time) and the branch encodes the input function (e.g., initial condition). Here, the separation is artificial, and the model likely does not benefit from the operator‑learning principles that make DeepONet effective. The poor performance of this variant therefore does not inform us about the capabilities of proper DeepONet models for chemical kinetics.
3. **Unclear prediction task and evaluation protocol**: The paper does not clearly describe how the models are used to generate predictions. The loss (Eq. 4) suggests training with recursive multi‑step prediction up to 30 steps, but Figures 3‑4 show predictions over 0‑40 μs with a single trajectory. How many autoregressive steps are taken? What is the time step size? How is the initial state for each rollout chosen? Without this information, the reported MSE values are hard to interpret and reproduce.
4. **Trivial core claim and insufficient novelty**: That “architecture matters” is well‑known and not a novel finding. The paper offers little analysis of *why* the residual connections in the “U‑Net” help specifically for stiff chemical systems. Moreover, the study does not compare against state‑of‑the‑art surrogates for chemical kinetics (e.g., tabulation methods, PCA‑based models, or other operator‑learning approaches such as FNO). Such comparisons are needed to establish the value of the proposed architecture.
5. **Self‑undermining statement**: The abstract and Section 5 state that “the problem remains unresolved” and that certain trajectories remain “challenging to approximate.” While honest, this undercuts the positive conclusion that the U‑Net provides a reliable solution. The paper reads as an interim report rather than a completed study demonstrating a trustworthy surrogate.

### Minor
6. **Inconsistent species in figures**: Figures 3‑4 show subplots for “CO” and “NO,” yet the reduced mechanism described in Section 2 includes only hydrogen‑oxygen compounds plus N₂ and Ar. Either the figures correspond to a different dataset or the text is inaccurate. This discrepancy undermines trust in the results.
7. **Insufficient dataset documentation**: The paper mentions 50,000 training, 15,000 validation, and 5,000 test samples, but it is unclear whether these are individual time‑steps or entire trajectories. If each sample is a single (state, next‑state) pair, then temporal correlations are ignored. The number of trajectories, the length of each trajectory, and how they are split should be specified.
8. **Loss weighting not justified**: The multi‑step loss uses a factor 1/*k* that down‑weights later steps. The rationale is not explained, and it is unclear whether this choice biases the comparison.
9. **Statistical test absent**: The 95% confidence intervals are computed, but the paper does not state how (e.g., bootstrap, standard error). A paired test across trajectories would be more appropriate to compare models.

### Trivial
- Figure 2 mislabels the MLP and U‑Net architectures (both diagrams appear nearly identical except for the skip connections, but the labels in the figure are not perfectly aligned with the text descriptions).

## Nice-to-Haves
- Compare with a standard DeepONet (branch net encodes the entire initial condition, trunk net encodes time and parameters) and with a convolutional U‑Net on a 1D grid if applicable.
- Report inference speed (wall‑clock time) alongside MSE to demonstrate practical acceleration over the ODE solver.
- Provide an ablation study: remove the local skip, the global skip, or both to attribute the improvement to specific architectural components.
- Include scatter plots of predicted vs. true values for key species to visualize systematic biases.

## Novel Insights
None beyond the paper’s own contributions. That a fully‑connected network with skip connections (a residual MLP) outperforms a plain MLP and a poorly‑designed DeepONet variant on this specific task is a narrow empirical observation, not a generalizable insight about operator learning or stiff kinetics.

## Suggestions
1. **Rename the “U‑Net”** to “Residual MLP” or “ResNet‑like MLP” to accurately reflect the architecture and avoid borrowing credibility from the U‑Net name.
2. **Implement a proper DeepONet** that uses the branch network to encode the initial (or current) state vector and the trunk network to encode the time coordinate and possibly additional parameters. This would provide a fair and informative baseline.
3. **Clarify the prediction protocol**: Clearly state whether the models are used to predict one step, recursively roll out multiple steps, or directly predict entire trajectories. If recursive, specify the number of steps and the initial condition for each test trajectory.
4. **Reconcile the species list** in the text with those shown in Figures 3‑4. If the figures include CO and NO, either the mechanism was extended or the figures belong to a different experiment; in either case, correct the discrepancy.
5. **Include a simple baseline** such as linear interpolation or a constant‑state predictor to calibrate the difficulty of the task.
6. **Provide computational cost** (training time, inference time per sample) to justify the practical benefit of the proposed architecture.
7. **Use statistical testing** (e.g., paired bootstrap or Wilcoxon signed‑rank test on per‑trajectory MSE) to confirm that the U‑Net improvement is statistically significant beyond the observed CI separation.
8. **Justify the 1/k weighting** in the loss or remove it to avoid introducing an unexplained bias.

## Score and Decision
**Score**: 3.5 – The paper addresses a practically important problem and includes a reasonable dataset, but the contributions are weakened by mischaracterised architectures, an unfair baseline, unclear evaluation, and a lack of novelty. The claims are not well supported in their current form, and the study does not meet the bar for acceptance at ICLR.

MY FINAL SCORE: 3.5
MY FINAL DECISION: Reject
## Summary

This paper presents a real-time adaptive stimulation framework for manipulating latent neural dynamics. It integrates streaming dimensionality reduction (novel sjPCA, proSVD, mmICA), dynamical modeling (Kalman filter, VJF, Bubblewrap), a nonparametric kernel regression model for stimulus-response mapping, and an optimization procedure that designs high-dimensional stimulation patterns (with sparsity and non-negativity constraints) to drive latent activity along desired directions. The method is demonstrated on a toy model and two real neural datasets (calcium imaging, electrophysiology) where stimulations are simulated.

## Strengths

- **Addresses an important and timely problem**: Closed-loop manipulation of latent neural dynamics with realistic experimental constraints (non-negativity, limited number of targets) is a significant challenge for optogenetic experiments and clinical applications. The paper carefully considers these constraints.
- **Modular and flexible framework**: The combination of streaming latent space construction, online dynamics modeling, kernel regression, and constrained optimization allows the method to operate with different latent representations and models, and to adapt to non-stationary stimulus-response mappings (shown with the toy model's flip and rotation).
- **Computational efficiency**: End-to-end runtime below 100 ms (average <10 ms) is demonstrated, which is critical for future *in vivo* real-time experiments.
- **Clear presentation of the core optimization objective**: Equation (8) cleanly captures the trade-off between aligning the perturbation with a desired latent direction and satisfying sparsity constraints, and the differentiable stimulus-response model enables gradient-based solution.

## Weaknesses

### Fatal
None.

### Major

1. **Lack of validation on real stimulation data.** The "real neural data" experiments use *simulated* stimulations (an autoregressive additive process applied to the recorded traces), not actual optogenetic or electrical stimulations with measured neural responses. The stimulus-response mapping \(S\) is therefore not learned from real evoked activity. This severely limits the support for the paper's core claim of "stimulation-response modeling" and the closed-loop adaptation mechanism. Without real stimulation data, the effectiveness of the kernel regression and the optimization in an actual experimental setting remains unvalidated.

2. **Insufficient baselines.** The only comparison is to random stimulation (single neurons, groups, shuffled) and a "blind" model that ignores stimulation effects. No comparison is made to existing closed-loop stimulation approaches such as Bayesian optimization (Minai et al., 2024), active learning/experimental design (Wagenmaker et al., 2024), or other input-output modeling methods (Yang et al., 2021) that are cited in the paper. Comparing against these would better position the contribution relative to the state-of-the-art.

3. **Overclaimed novelty of sjPCA.** The streaming jPCA (sjPCA) adds an Orthogonal Procrustes stabilization step to the eigenvectors of the skew-symmetric matrix estimated via the Sherman-Morrison formula. This is an incremental engineering improvement rather than a principled new method. The paper’s main contribution is the integrated framework, not the individual components, which are mostly adopted from prior work.

4. **Optimization results rely on simulated or assumed mappings.** The results in Figures 4 and 5 are either from the toy model (where ground-truth \(S\) is known and simple) or from the calcium dataset where \(S\) is assumed (open-loop case \(S(u)=Q^\top u\) or a simulated non-trivial mapping). The "closed-loop" evaluation therefore still uses a hand-crafted \(S\), not one learned from real stimulation experiments. This borrows credibility from the actual pipeline.

5. **Missing ablation/analysis of the multi-space selection.** The paper adaptively selects among latent spaces (proSVD, sjPCA, mmICA) and dynamical models based on predictive error, but no experiment demonstrates whether this selection improves stimulation design or downstream performance. Figure 1c is only illustrative; there is no quantitative evaluation of the benefit of this parallel structure.

### Minor

- The kernel regression hyperparameters (kernel length scales and the time discount factor) are tuned via stochastic coordinate descent, but no details are given about the update rule, convergence, or sensitivity to initialization. The choice of \(\lambda_1\) in the objective is not discussed or ablated.
- The "blind" comparison model simply withholds stimulation timepoints from the dynamics update; a stronger baseline would be a model that treats stimulation as an unknown input and attempts to infer its effect without explicit learning.
- The electrophysiological dataset is mentioned but only the calcium dataset is used for the main stimulation optimization results (Figures 3–5). The paper would be stronger if both modalities were used for all experiments.

### Trivial
None.

## Nice-to-Haves

- Evaluate the framework on an existing dataset containing real optogenetic stimulation responses (e.g., from published holographic photostimulation experiments) to substantiate the stimulus-response model.
- Compare against Bayesian optimization or other active learning baselines for stimulus selection.
- Provide an ablation study showing the impact of adaptive latent space selection on stimulation alignment error.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Run the method on a dataset with real optogenetic stimulations, or at minimum, use a more realistic stimulation response model grounded in published electrophysiological recordings (e.g., a Poisson spiking model with known opsin dynamics). This would significantly strengthen the validation.
- Add baselines such as Bayesian optimization (with a GP model over latent perturbation effects) and random search with rejection sampling, and compare the alignment error and sample efficiency.
- Clarify the kernel regression details: provide the update rule for length scales, describe how the time kernel's length constant is adapted, and discuss the choice of \(\lambda_1\).

## Score and Decision

**Score:** 4

**Decision:** Reject

**Rationale:** The paper addresses an important problem and builds a reasonable integration of existing components, but the experimental validation is not sufficient for a top venue. The core claims about stimulation-response modeling and closed-loop adaptation are supported only by toy simulations and simulated stimulations on real data, not by actual neural responses to stimulation. The lack of strong baselines and the incremental novelty of sub-components further weaken the contribution. While the framework is promising, the evidence does not yet demonstrate that it works reliably in realistic experimental conditions.

MY FINAL SCORE: 4.0
MY FINAL DECISION: Reject
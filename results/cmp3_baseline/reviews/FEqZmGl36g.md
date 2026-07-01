## Summary

The paper introduces ESS-Flow, a training-free method for controlled generation with pretrained flow-based generative models that performs Bayesian inference in the Gaussian source space using Elliptical Slice Sampling (ESS). The method requires no gradients through the generative model or potential function, only forward evaluations, making it applicable to problems with non-differentiable operations like quantization or simulation-based likelihoods. The authors demonstrate ESS-Flow on materials design with target properties and protein structure prediction, showing competitive performance particularly in settings where gradient-based methods struggle.

## Strengths

- **Novel and well-motivated approach**: The insight of leveraging elliptical slice sampling in the source space of flow-based models is creative and addresses a genuine gap in existing methods. The gradient-free nature is a significant advantage for scientific applications where likelihoods involve non-differentiable simulators or quantization.

- **Clear problem identification**: Section 1 and Figure 2 convincingly demonstrate limitations of gradient-based source-space methods (getting trapped in disconnected manifold components), providing strong motivation for the gradient-free alternative.

- **Impressive empirical results**: On materials generation tasks (Table 2), ESS-Flow achieves dramatically lower absolute errors compared to D-Flow, PnP-Flow, and DAPS (e.g., 8.99 vs 205.88 for bulk modulus). The S.U.N.T. rates in Table 3 also show ESS-Flow consistently outperforms baselines on the composite metric.

- **Minimal hyperparameters**: The method has essentially one tuning parameter (number of MCMC iterations), which is a practical advantage over optimization-based methods that require careful learning rate scheduling.

- **Good theoretical grounding**: Proposition 1 provides a convergence guarantee, and the paper acknowledges limitations honestly (e.g., when target distribution is poorly informed by prior).

## Weaknesses

### Major

1. **Computational cost is not adequately addressed**: ESS-Flow requires many forward passes through the full ODE solver (one per ESS proposal evaluation). The authors mention using "moderate numbers of function evaluations" but provide no runtime comparisons or wall-clock times. Given that gradient-based methods like D-Flow require only a single forward pass with backpropagation, the computational overhead of ESS-Flow could be substantial. Table 5 in Appendix would help but is not in the main paper.

2. **Protein structure prediction results are mixed**: While ESS-Flow produces more realistic structures (better ELBO, fewer clashes) than ADP-3D and DAPS, it has much worse data fidelity ($d_y = 37.02$ vs 3.43 for ADP-3D) and higher RMSD to ground truth. The authors frame this as a trade-off, but it's unclear whether the ESS-Flow samples actually solve the inverse problem adequately. The 10.63 Å minimum RMSD is still poor for structure prediction.

3. **Multi-fidelity evaluation reveals serious limitations**: The importance weighting approach for multi-fidelity sampling fails dramatically on two of four tasks (0.1% and 1.0% effective sample sizes for band gap and stability). This suggests the proof-of-concept is not robust, and the paper's claim of "improving computational efficiency" is not well-supported.

### Minor

1. **Comparison to D-Flow on the materials task uses a continuous approximation** to make atomic numbers differentiable, which disadvantages ESS-Flow's gradient-free advantage. A more compelling comparison would be the space-group task (where D-Flow cannot be applied), but ESS-Flow results are only compared to unconditional sampling for that task.

2. **The paper claims ESS-Flow is "asymptotically exact"** but the practical discretization of the ODE solver introduces approximation error that is not quantified. The convergence guarantee in Proposition 1 assumes access to the exact transport map.

### Trivial

- The multi-fidelity discussion in Section 4.2 uses notation $T_\delta^\Delta(z)$ in equation (4) which appears to have a typo (should likely be $T_\theta^\Delta$ vs $T_\theta^\delta$).

## Nice-to-Haves

- A wall-clock time comparison between methods would greatly strengthen the paper.
- An ablation study showing sensitivity to the number of ODE steps would be valuable.
- The multi-fidelity approach could be strengthened by exploring delayed acceptance ESS rather than importance weighting.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Include wall-clock timing comparisons and number of ODE solver evaluations for all methods in the main paper.
2. Consider adding experiments on simpler, well-understood inverse problems (e.g., image inpainting on toy data where ESS-Flow is expected to struggle) to clearly delineate the method's regime of applicability.
3. For the multi-fidelity section, either develop a more robust approach (e.g., delayed acceptance) or be more measured in claims about efficiency gains given the poor effective sample sizes.
4. Report acceptance rates and effective sample sizes for ESS-Flow on the materials tasks to help readers understand sampling efficiency.

## Score and Decision

The paper presents a genuinely novel method that addresses an important gap (gradient-free controlled generation for flow-based models), with strong empirical results on challenging scientific applications. However, the computational cost is under-analyzed and the protein experiments show mixed results. The multi-fidelity contribution is preliminary and has serious limitations. Despite these issues, the core idea is sound and well-executed on the main tasks.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>
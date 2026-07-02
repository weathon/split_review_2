## Summary

The paper proposes three one-step diffusion-based solvers (CMILP, SCMILP, MFILP) for integer linear programming (ILP), extending existing consistency, shortcut, and meanflow models to the combinatorial optimization domain. To handle non-binary integer variables without costly binarization, the authors introduce an iterative integer projection (IIP) layer, and they enhance solution quality with objective-guided sampling augmented by momentum. Experiments on binary and non-binary ILP benchmarks show that the proposed methods achieve faster inference than both traditional solvers and previous diffusion-based ILP solvers, though with often substantially larger optimality gaps.

## Strengths

- **Addresses an important practical problem**: Extending neural ILP solvers to non-binary variables without exponential problem growth is a relevant direction, and the IIP layer provides a differentiable relaxation.
- **Significant speed improvements**: The one-step diffusion variants reduce inference time by orders of magnitude compared to multi-step DDPM/DDIM baselines, making them more practical for time-sensitive applications.
- **Comprehensive empirical evaluation**: The paper evaluates on multiple binary (set cover, facility location, combinatorial auction) and non-binary (inventory management, synthetic) datasets against a wide range of baselines including Gurobi, SCIP, COPT, and prior learning-based methods.

## Weaknesses

### Fatal

- **Incorrect diffusion formulation** (Equation 5): The reverse denoising step is written as \( \mathbf{x}_{t-1} = \frac{1}{\sqrt{\alpha_t}}(\mathbf{x}_t - \frac{1 - \alpha_t}{\sqrt{1 - \alpha_t}}\epsilon_t) + \sqrt{\frac{1 - \bar{\alpha}_{t-1}}{1 - \bar{\alpha}_t}}\beta_t \mathbf{z} \). This does not match the standard DDPM reverse process (the coefficient for \(\epsilon_t\) simplifies incorrectly and the variance term is not standard). Presenting a flawed foundation for the diffusion background, even if the paper primarily uses one-step variants, undermines confidence in the technical rigor.

### Major

- **Misapplication of the consistency model**: The CMILP loss in Equation (6) minimizes distance to the target solution \(\delta(\mathbf{x}-\mathbf{x}^*)\) at each timestep separately, rather than enforcing the self-consistency property \(f_\theta(\mathbf{x}_t,t)=f_\theta(\mathbf{x}_{t'},t')\) that defines consistency models. This reduces to a simple denoising autoencoder objective, not genuine consistency training. The claimed connection to consistency models is therefore misleading, and the “one-step” advantage is obtained by a direct mapping from noise to solution rather than through consistency distillation.
- **Poorly motivated and unclear objective-guided sampling** (Section 3.3): The variational free energy derivation is introduced without clear justification, and the connection between the free energy \(F\), the gradient updates, and the actual sampling procedure is not explained. It is unclear how the point estimate \(\boldsymbol{\eta}\) is updated or how the guidance interacts with the diffusion process. This makes the method hard to reproduce or assess.
- **Weak optimality performance**: On binary benchmarks, the proposed methods often exhibit gaps exceeding 80% (e.g., 90.2% on SC, 79.2% on CF, 80.2% on CA for CMILP). On non-binary problems, the gaps are sometimes worse than the much slower IP Guided DDIM. The paper claims superiority, but the trade-off between speed and solution quality is downplayed, and the practical value of a solver with such large gaps is limited.
- **Overclaimed novelty and insufficient prior comparison**: The authors claim “for the first time … we extend the binary 0-1 ILP neural solver to the non-binary case,” yet they cite Tang et al. (2025) which introduces an integer correction layer for non-binary variables. The contribution is incremental and the positioning is not accurate. Additionally, the claim of “without resorting to traditional algorithms for post-processing” is contradicted by the use of hard rounding to enforce integrality.

### Minor

- **Table typos**: In Tables 2 and 3, the label “SCMILP (Ours)” appears twice, likely substituting for CMILP, causing confusion.
- **Lack of ablations**: The paper does not ablate key components—the IIP layer (versus simple rounding), the guidance mechanism (with/without), or the momentum (except one configuration in Table 5). This makes it difficult to attribute improvements to specific contributions.
- **Reproducibility**: Code is promised after acceptance, but no supplementary material is provided, making it impossible to verify the correctness of the implementation, especially given the questionable diffusion equations.

### Trivial

No additional trivial issues.

## Nice-to-Haves

- Provide a clear algorithmic pseudocode for training and inference.
- Compare the IIP layer to simpler integer projections (e.g., rounding after softplus-based logits).
- Include experiments without objective-guided sampling to measure its isolated effect.

## Novel Insights

None beyond the paper’s own contributions. The application of existing one-step diffusion techniques (consistency, shortcut, meanflow) to ILP is an engineering contribution rather than a conceptual advance. The IIP layer is a straightforward application of a periodic function to approximate rounding, and the momentum modification to gradient-based sampling is minor.

## Suggestions

1. Correct the diffusion formulation to the standard DDPM reverse process or remove the erroneous equation if no multi-step diffusion is actually used.
2. Rethink the CMILP loss to genuinely enforce self-consistency across timesteps, or rename the method to avoid misleading claims.
3. Provide a clear, self-contained description of the objective-guided sampling, including the exact update rule for \(\boldsymbol{\eta}\) and how it integrates with the one-step generative process.
4. Include ablation experiments comparing IIP versus rounding, guidance versus no guidance, and momentum versus plain gradient descent over a range of settings.
5. Discuss the optimality gap issue honestly and characterize the niche where speed at the cost of quality is acceptable.
6. Fix the table labeling errors and ensure all method names are consistent.

## Score and Decision

**Score**: 4.0  
**Decision**: Reject

The paper tackles an important problem and demonstrates impressive speed, but the technical flaws (incorrect diffusion equations, misapplication of consistency models, unclear guidance derivation) and weak solution quality relative to prior diffusion-based methods prevent acceptance at ICLR. The contributions are incremental and the experimental evaluation does not convincingly demonstrate superiority.

MY FINAL SCORE: <score>4.0</score>  
MY FINAL DECISION: <decision>Reject</decision>
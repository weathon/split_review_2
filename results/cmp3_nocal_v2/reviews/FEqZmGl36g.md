## Summary

ESS-Flow proposes a gradient-free method for controlled generation with pretrained flow-based models. The core idea is to perform Bayesian inference in the source (latent) space of the flow — where the prior is Gaussian — using Elliptical Slice Sampling. Because both the prior and posterior are expressed in source space, the Jacobian of the transport map cancels, requiring only forward evaluations of the generator and the potential. The method is demonstrated on materials design (FlowMM with differentiable property predictors and a genuinely non-differentiable space-group symmetry task) and protein backbone prediction from sparse distance measurements (Chroma). It achieves substantially lower absolute errors on materials property targeting and succeeds on the space-group task where no gradient-based competitor can be applied at all.

## Strengths

1. **Elegant and principled formulation (Section 4.1, Equation 3).** The Jacobian cancellation when performing inference in the source space is a clean and correct insight. The reduction to a Gaussian prior with a pullback potential places the problem in the exact setting where elliptical slice sampling excels (Gaussian prior, arbitrary likelihood). The derivation is mathematically sound and the reasoning is clearly presented.

2. **Unique capability demonstrated via the space-group symmetry task (Section 5.1, Table 3).** The space-group task uses a binary indicator computed by an external non-differentiable program (Togo et al., 2024). ESS-Flow achieves 81.9% target rate and 25.5% S.U.N.T. rate vs. 2.3% / 1.3% for unconditional sampling. No gradient-based competitor can participate in this task at all. This is the paper's cleanest demonstration of its unique value proposition and is compelling evidence for the method.

3. **Strong quantitative results on materials property targeting (Tables 2 and 3).** ESS-Flow achieves substantially lower mean absolute errors than all baselines: e.g., 8.99 GPa bulk modulus error vs. 39.14 (next best DAPS), 10.53 GPa shear modulus vs. 75.48 (PnP-Flow), 1.85 eV band gap vs. 3.90 (DAPS). The margins are large enough that implementation artifacts cannot explain them. ESS-Flow achieves the highest S.U.N.T. rates across all four property-targeting tasks.

4. **Convergence guarantee (Proposition 1).** The paper provides a geometric convergence result for the ESS-Flow Markov chain under mild regularity conditions (boundedness away from 0 and ∞ on compact sets, regular tail behavior). This gives meaningful theoretical grounding, adapted from Natarovskii et al. (2021).

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **Multi-fidelity section is presented as a contribution but is a failed proof of concept.**
   The introduction lists the multi-fidelity extension as a main contribution (line 40), but the effective sample sizes for the band gap and stability tasks are 0.1% and 1.0% (Section 5.1.1). An importance-reweighting scheme with ESS below 1% means the coarse samples have essentially no overlap with the high-fidelity target distribution on these tasks. While the paper acknowledges this as a "shortcoming," listing it as a bullet-point contribution overstates what is actually a negative result suggesting a direction for future work. The paper would be more credible if this were demoted to a limitations/future-work discussion.

2. **The protein experiment's framing overclaims what the evidence supports.**
   In Table 4, ESS-Flow does not unambiguously outperform baselines on any single independent metric: on data fit ($d_y$) ESS-Flow (37.02) is worse than ADP-3D (3.43) and DAPS (11.79); on RMSD to ground truth ESS-Flow (13.55) is worse than ADP-3D (11.45) and DAPS (11.41); on clash count ESS-Flow (24.8) is worse than D-Flow (14.8) and unconditional sampling (10.1). The ELBO metric favors ESS-Flow (8.89 vs. -5.68 and -8.07 for ADP-3D/DAPS), but ELBO measures compatibility with the Chroma prior — a method that explicitly enforces that prior will naturally score well on it. The paper's claim of achieving "a better trade-off between data fidelity and sample realism" (line 267) is stated as a qualitative assertion without formal multi-objective comparison (e.g., Pareto frontier analysis). The results honestly portray a tension (prior fidelity vs. data fit), and the paper should frame them that way rather than claiming an unqualified better trade-off.

3. **Dimensionality scaling is discussed only in the appendix.**
   The main text (line 101) references scaling evaluations in Appendix A.1, but MCMC methods — and ESS specifically — are known to degrade with dimension. For the protein problem the state space is 4×147×3 = 1764 dimensions. A brief qualitative discussion in the main text about the practical scaling regime (e.g., acceptance rates or ESS as a function of dimension) would help readers assess applicability. This is an omission from the main text, not from the paper overall (since the appendix contains it).

4. **Equation (4) notation is unclear.**
   The notation $T_\delta^\Delta(z)$ is confusing: line 139 says it denotes a transport map with *coarse* discretization $\Delta$ and *fine* discretization $\delta$, but it is not clear whether the superscript or subscript denotes the level. The derivation in Equation (4) appears tautological as written (multiplying and dividing by the same term $g(T_\delta^\Delta(z))$), and the importance weight formula on line 143 uses $g(T_\delta^\Delta(z_1))$ where the subscript $1$ appears to be a typo for $i$. The intended expression likely involves a ratio $g(T_\theta^\delta(z_i))/g(T_\theta^\Delta(z_i))$ but this is not what is written.

### Trivial

- The toy problem (Figure 2) is purely illustrative; no quantitative results (acceptance rates, objective values) are reported for it. This is acceptable for motivation but noting it explicitly would be helpful.

## Nice-to-Haves

- The space-group task is the paper's most distinctive experiment. Leading with it in the abstract and introduction (it currently appears in one row at the bottom of Table 3) would better highlight ESS-Flow's unique advantage.
- Adding a brief discussion of burn-in, chain count, and convergence diagnostics in the main text (even a single sentence) would strengthen the MCMC reporting, though these details are in the appendix.

## Removed Points

The following points from the input review are removed with justification:

- **Missing comparison to Wang et al. (2025) / Purohit et al. (2025):** These are explicitly described as concurrent works. The paper cannot reasonably be expected to include experimental comparisons to methods published simultaneously. Moreover, the critic acknowledges they require gradients, which is precisely the dimension ESS-Flow avoids. This criticism is factually unreasonable given the submission timeline.

- **ELBO as "circular":** The claim that ELBO is structurally circular conflates "the method scores well on a metric aligned with its objective" with a methodological flaw. ELBO under Chroma measures how protein-like a structure is according to the Chroma model — this is a legitimate measure of structural realism. The observation that the posterior mean ELBO (8.89) slightly exceeds the unconditional mean ELBO (8.70) is not theoretically impossible, since conditioning on observations can concentrate mass on regions the learned model assigns higher density.

- **Soft atomic approximation giving ESS-Flow an unfair advantage:** The paper explicitly acknowledges (line 183) that D-Flow and PnP-Flow use a soft approximation while ESS-Flow uses exact discrete atomic numbers via the Metropolis-Hastings proposal. This is a feature of the comparison, not a hidden confound, and is transparently disclosed.

- **Missing related works / formatting nitpicks / single-protein dataset limitation:** These are either parser artifacts, scope issues, or acknowledged limitations.

- **Strengths about the importance of the problem:** These are generic; only concrete, evidenced strengths are retained.

## Novel Insights

The input review's key insight is that the protein experiment reveals a fundamental tension (prior fidelity vs. data fit) rather than a definitive win for ESS-Flow, and that the multi-fidelity section is more of a negative result than a contribution. These observations sharpen the assessment but do not extend beyond what a careful reading of the paper yields.

## Suggestions

1. Demote the multi-fidelity section from a main contribution to a limitations/future-work discussion. The current framing as a contribution with ESS values of 0.1% and 1.0% on half the test cases weakens the paper's credibility.
2. Re-frame the protein experiment conclusion to honestly characterize the trade-off (ESS-Flow preserves prior fidelity at the cost of data fit) rather than claiming an unqualified "better trade-off." Remove or qualify the ELBO-based structural realism argument.
3. Move a brief dimensionality-scaling discussion (even 2–3 sentences on acceptance rates vs. dimension) from the appendix into the main text, since this is the most practically relevant information for potential users.
4. Clarify the notation in Equation (4) and fix the apparent typo in the importance weight formula.

## Score and Decision

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>
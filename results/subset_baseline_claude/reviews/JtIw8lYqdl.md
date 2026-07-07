## Summary
This paper investigates whether predictive uncertainties in deep learning (Total, Aleatoric, and Epistemic) follow empirical scaling laws analogous to those for test loss, with respect to dataset size N and model size P. Through experiments spanning ResNets, WideResNets, ViTs, and GPT-2 across CIFAR-10, ImageNet32, and an algorithmic dataset, the authors find power-law decay patterns for multiple UQ methods (MC Dropout, Deep Ensembles, MCMC, IVON). They also derive a formal connection between Watanabe's generalization error and Total Uncertainty in Bayesian linear regression, providing a speculative theoretical bridge to the SLT framework.

## Strengths
- **Novelty and timeliness.** To the best of reviewers' knowledge, this is the first systematic empirical investigation of scaling laws for predictive uncertainty. The research question is well-motivated and interesting to the BDL community.
- **Breadth of coverage.** The paper includes multiple UQ methods (MC Dropout, Deep Ensembles, MCMC, Laplace/IVON), several architectures (ResNet, WideResNet, ViT, GPT-2), vision and language modalities, and both in- and out-of-distribution evaluation, lending breadth to the empirical claims.
- **Practically valuable finding.** The argument that epistemic uncertainty remains non-negligible even at large data scales is important for dispelling naïve dismissals of Bayesian methods, and is backed by results across multiple independent setups.
- **Interesting secondary observations.** The SAM+Dropout interaction (Fig. 3) and the sensitivity of ViT uncertainty dynamics to learning rate scheduling (Fig. 4) are novel observations that add value beyond the main claim.

## Weaknesses

### Fatal
None.

### Major
- **Too few data points for credible power-law fitting.** The central claim—that uncertainty follows a power law—rests in most experiments on only 4 data points (25%, 50%, 75%, 100% subsets of training data). Fitting a two-parameter power law to 4 points yields near-zero degrees of freedom and cannot distinguish power-law from other monotone decays (e.g., exponential, logarithmic). For ImageNet32, the main paper has only 3 points (Fig. 6). This is a fundamental methodological issue, as scaling laws typically require spanning 1–3 orders of magnitude with sufficient sampling density to reject alternative functional forms. The paper should include goodness-of-fit tests (e.g., log-linear R², AIC vs. alternatives) across a wider range of N.

- **Exponents vary widely and unpredictably.** The paper reports EU exponents ranging from -0.13 (ResNet-34 + SAM) to -2.95 (GPT-2), with even same-architecture configurations varying substantially (e.g., -0.36 to -0.80 in Fig. 1 for CIFAR-10 with different UQ methods). This undermines claims of "robust" scaling and makes the laws difficult to use practically for extrapolation. The paper acknowledges that exact exponents "vary unpredictably with design choices," but this acknowledgment weakens the practical utility argument central to the contribution.

- **AU decreasing with N is inconsistent with its theoretical role.** Aleatoric uncertainty is by definition irreducible, yet the paper consistently reports AU decay with N (e.g., γ_AU ≈ -0.53 for ResNet-18 MC Dropout). The paper briefly acknowledges this citing Wimmer et al., but does not reconcile this inconsistency. If AU is not actually irreducible in practice, the decomposition EU = TU − AU becomes unreliable, and conclusions about epistemic uncertainty specifically are weakened.

### Minor
- The model-size scaling (Section 4.1.1) covers ResNet-18 to ResNet-152, a range of roughly 11M–60M parameters—less than 1 order of magnitude. The results are accordingly inconclusive: MC Dropout shows flat EU while IVON shows slight increase, but the range is too narrow to establish a meaningful scaling law.
- The Phi-2 fine-tuning experiment (Section 4.2) shows flat uncertainty throughout—precisely the failure mode—without further analysis of why or whether scaling could be recovered under different settings.
- The theoretical analysis in Section 5 establishes a connection between generalization error and TU only in Bayesian linear regression (well-specified, low-dimensional). The extension to over-parameterized deep models is labeled "speculative" by the authors, limiting its explanatory power for the empirical findings.

### Trivial
- Fig. 1 caption describes CIFAR-10 ResNet-18 but the figure title says "three log-log plots" without indicating which UQ method corresponds to which subplot.

## Nice-to-Haves
- Including a goodness-of-fit comparison (power law vs. log-linear vs. exponential) would substantially strengthen the scaling law claim.
- Varying N over a wider range (e.g., 1% to 100%) with finer resolution would improve statistical reliability.
- An analysis of why the scaling exponents vary—potentially linking them to task difficulty, architecture inductive bias, or UQ method—would transform the paper from an observation study into a more explanatory contribution.

## Novel Insights
The observation that epistemic uncertainty remains sizeable at dataset scales typically considered "sufficient" is a genuinely useful empirical finding for practitioners. The SAM-dropout interaction producing anomalous EU behavior (near-zero exponent, indicating persistent diversity) is an unexpected and interesting result suggesting optimizer choice can qualitatively alter uncertainty scaling. If confirmed with better statistical methodology, these would be significant contributions to understanding deep learning uncertainty in the large-data regime.

## Suggestions
- Expand the data-size sweep to span at least 2 orders of magnitude with 8+ data points, and include a formal test for power-law vs. alternatives.
- Report confidence intervals on the fitted exponents (currently absent) to indicate statistical reliability.
- Address the AU-decreasing phenomenon more substantively—it either invalidates the EU/AU decomposition or signals that entropy-based AU is not equivalent to irreducible uncertainty in practice.
- For the model-size experiment, consider using a family with broader parameter range, or report results on a dataset with more data, to make the scaling informative.

## Score and Decision
The paper addresses a timely and interesting question, and the breadth of experiments is commendable. However, the central empirical claim of power-law scaling rests on extremely sparse data (typically 4 points per curve), no goodness-of-fit analysis, and exponents that vary by an order of magnitude across configurations. The AU-decreasing anomaly is unresolved. The theoretical contribution, while interesting, is limited to linear models and does not extend to the deep learning regime studied experimentally. As a borderline paper, the findings are intriguing and worthy of further development, but the current evidence is insufficient to firmly establish the claimed scaling laws.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>
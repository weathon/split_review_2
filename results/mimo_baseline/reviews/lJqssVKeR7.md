## Summary
This paper proposes HiSo, a Hessian-informed zeroth-order federated optimization method that accelerates convergence for LLM fine-tuning while preserving dimension-free (scalar-only) communication. The key insight is that a global diagonal Hessian approximation can be maintained and reconstructed from the same scalar gradient information already being communicated, requiring no additional communication overhead. The authors provide convergence analysis showing the rate can be independent of model dimension $d$ and Lipschitz constant $L$ under a low-effective-rank Hessian assumption, and demonstrate 1–5× communication-round speedups over DeComFL on OPT models up to 2.7B parameters.

## Strengths
- **Effective generalization of scalar-only communication framework**: The paper identifies that the key enabler of dimension-free FL communication is the scalar representation itself, not ZO-SGD specifically. Algorithm 1 cleanly decouples the communication mechanism from the optimizer choice, enabling broader algorithmic exploration—a valuable conceptual contribution.

- **Principled integration of Hessian preconditioning without communication cost**: The diagonal Hessian approximation (Eq. 12) is reconstructed from the already-communicated global $\Delta x$ values, so clients and server can independently maintain the same $H_r$ with zero extra communication. This is an elegant solution to the fundamental tension between curvature-aware optimization and dimension-free communication.

- **Meaningful theoretical contributions**: Corollary 3 resolves an open question from DeComFL by extending convergence guarantees to $\tau > 1$ local updates under the low-effective-rank assumption, showing the rate remains independent of $d$ and $L$. The connection between the whitening rank $\zeta$, effective rank $\kappa$, and dimension $d$ (with $\zeta \ll \kappa \ll d$) provides a principled explanation for why ZO methods often converge much faster than worst-case $\mathcal{O}(d)$ bounds suggest.

- **Comprehensive and realistic experimental evaluation**: Experiments span OPT-125M through OPT-2.7B on three diverse NLP tasks (SST-2, QQP, SQuAD), comparing against both first-order FL methods (FedAvg, FedAdam, FedYogi, FedAdagrad) and ZO baselines (FedZO, DeComFL). The communication cost comparisons clearly show HiSo achieves TB→KB reductions over first-order methods while consistently outperforming DeComFL in both convergence speed and final accuracy.

## Weaknesses
### Fatal
None.

### Major
- **Strength of the well-approximate condition**: Corollary 1's convergence rate of $\mathcal{O}(\sqrt{\zeta/mR})$ depends critically on the well-approximate condition $\text{Tr}(H^{-1/2}\Sigma H^{-1/2}) \leq \zeta$ where $\zeta$ is dimension-independent. The authors acknowledge this is hard to verify for LLMs. While Theorem 1 holds without this condition, the headline result—dimension-independent convergence—relies on it. The paper would benefit from stronger empirical evidence that this condition approximately holds, beyond the MNIST-level long-tail histogram in Figure 5. The additional experiments mentioned in Appendix F.7.2 may address this, but the main text should provide more direct validation.

- **Hessian approximation is really Adam-style second moment estimation**: The update rule in Eq. 12 is essentially RMSProp's running average of squared gradients. While the theoretical framework connects this to Hessian approximation through the whitening rank concept, in practice the method functions as an adaptive preconditioner rather than a true Hessian-informed method. The gap between the theoretical Hessian approximation guarantee and the practical Adam-style update could be more explicitly discussed.

### Minor
- **Limited non-IID analysis**: The FL experiments don't systematically vary the degree of data heterogeneity (e.g., different Dirichlet $\alpha$ values). Since client drift is a major source of difficulty in FL and the theory includes explicit heterogeneity terms ($\sigma_G^2$), understanding sensitivity to non-IIDness would strengthen the practical contribution.

- **Single perturbation direction**: The paper uses $P=5$ perturbation directions per update but doesn't ablate this parameter or discuss the tradeoff between estimation quality and computation cost in the Hessian-informed setting, which may differ from vanilla ZO-SGD.

- **The $\tau > 1$ convergence rate has mixed terms**: Corollary 3's rate $\mathcal{O}(\sqrt{\zeta/\tau mR}) + \mathcal{O}(\sqrt{\tau\kappa/mR})$ shows the local-update benefit ($\tau$ in the denominator) is partially offset by the drift term ($\tau$ in the numerator). A more careful treatment of how $\tau$ should be set in practice would be helpful.

### Trivial
- The table showing the upper-bound comparison (Table 1) uses "2d" for L-smooth with Hessian preconditioning, which assumes a specific choice of $H$. A brief clarification would improve readability.

## Nice-to-Haves
- A comparison with LoRA-based FL methods in the same communication budget regime would contextualize HiSo against the other major approach to communication-efficient federated LLM fine-tuning.
- Wall-clock time comparisons (not just communication rounds) would help practitioners understand the full cost picture, including the overhead of maintaining and applying $H_r^{-1/2}$ at each step.

## Novel Insights
The paper's most genuinely novel observation is that the global diagonal Hessian approximation in FL can be maintained entirely from scalar-only communicated quantities without any additional communication overhead. This resolves the seemingly fundamental tension between curvature-aware optimization and dimension-free communication: the Hessian approximation piggybacks on information that must already be transmitted for the scalar-only framework to function. Combined with the low-effective-rank spectral analysis (demonstrating $\zeta \ll \kappa \ll d$ for LLM Hessians), this provides a compelling theoretical and empirical explanation for why zeroth-order methods converge far faster than their worst-case dimension-dependent bounds in practice.

## Suggestions
- Provide empirical validation of the well-approximate condition by computing $\text{Tr}(H^{-1/2}\Sigma H^{-1/2})$ on a smaller model where the full Hessian is tractable, and compare against $\text{Tr}(\Sigma/L)$ and $d$.
- Include an ablation on the number of perturbation directions $P$ in the Hessian-informed setting to understand the estimation-quality vs. compute tradeoff.
- Add experiments with varying levels of data heterogeneity to demonstrate robustness of the convergence improvement.

## Score and Decision
This paper makes a clear and well-executed contribution to a timely problem: accelerating federated zeroth-order optimization for LLM fine-tuning while preserving its key advantage of dimension-free communication. The generalization of the scalar-only framework, the integration of Hessian preconditioning without communication overhead, and the theoretical analysis extending to multiple local updates are all meaningful contributions. The experiments are comprehensive and convincing. The main limitations—the strength of the well-approximate condition and the gap between the Hessian-informed framing and the practical Adam-style update—do not invalidate the contribution but represent areas for deeper investigation.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: Accept
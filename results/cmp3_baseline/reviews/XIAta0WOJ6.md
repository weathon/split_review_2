## Summary

This paper studies stochastic bilevel optimization when the upper-level problem is nonconvex and the lower-level problem is strongly convex. The authors reinterpret the existing F²SA method as using a first-order forward-difference approximation of the hyper-gradient and propose a generalized family of methods, F²SA-\(p\), which employ \(p\)-th order finite-difference approximations. Under the additional assumption that the functions are \(p\)-th-order smooth in the lower-level variable, they prove that F²SA-\(p\) achieves an \(\tilde{\mathcal{O}}(p\epsilon^{-4-2/p})\) stochastic first-order oracle complexity, improving upon the \(\tilde{\mathcal{O}}(\epsilon^{-6})\) rate of F²SA. They also provide an \(\Omega(\epsilon^{-4})\) lower bound via a reduction to single-level optimization, showing near-optimality for sufficiently large \(p\). Experiments on a logistic regression hyper-parameter tuning problem validate the theoretical improvements.

## Strengths

- **Novel algorithmic insight:** The connection between the penalty reformulation of bilevel optimization and finite-difference approximations is a clean and original observation. This leads to a natural family of algorithms that systematically improve the hyper-gradient approximation error by exploiting higher-order smoothness.
- **Significant complexity improvement:** The upper bound improves from \(\tilde{\mathcal{O}}(\epsilon^{-6})\) for first-order smooth problems to \(\tilde{\mathcal{O}}(p\epsilon^{-4-2/p})\) for \(p\)-th-order smooth problems, narrowing the gap to the \(\Omega(\epsilon^{-4})\) lower bound. The analysis is rigorous and the parameter choices are clearly specified.
- **Near-optimality for highly smooth problems:** The paper shows that when \(p = \Omega(\log(\epsilon^{-1})/\log\log(\epsilon^{-1}))\), the method is optimal up to logarithmic factors, matching the best-known complexity of HVP-based methods without requiring stochastic Hessian oracles.
- **Clear presentation:** The paper is well structured, explains the key ideas (forward difference, central difference, general finite difference) intuitively, and provides sufficient context with respect to existing work. The notation is consistent, and the main results are summarized in a helpful table.

## Weaknesses

### Major

- **Assumption 2.5 (smoothness only in \(y\)) may be insufficient for Lemma 3.2:** The lemma claims that \(\frac{\partial^{p+1}}{\partial\nu^p\partial x}\ell_\nu(x)\) is Lipschitz in \(\nu\) with a specific constant, relying only on smoothness in the lower-level variable \(y\). Since \(\ell_\nu(x)=\min_y(\nu f(x,y)+g(x,y))\), derivatives with respect to \(\nu\) involve derivatives of the optimal solution \(y_\nu^*(x)\) with respect to \(\nu\), which in turn depend on mixed partials of \(f\) and \(g\) in both variables. The paper does not provide a proof or a sketch of why the \(y\)-only smoothness is sufficient; a more detailed justification is needed to convince the reader that the main technical lemma holds under the stated assumptions.

### Minor

- **Experiments are limited:** The experiments are run on a single problem (logistic regression with learn-to-regularize) and no error bars or multiple seeds are reported. It is unclear whether the observed performance differences are statistically significant. Additional experiments on other highly smooth problems would strengthen the empirical claims.
- **Use of normalized gradient step:** The outer-loop update uses a normalized gradient step \(x_{t+1}=x_t-\eta_x\Phi_t/\|\Phi_t\|\). The authors state this is for ease of analysis and believe standard gradient steps also work, but they do not test both variants nor discuss the practical impact of normalization (e.g., it may affect the effective step size). The experiments do not specify whether they used normalized steps; if they did, comparisons with methods using standard gradient steps might not be fair.
- **Hyper-parameter dependency on \(R\):** The parameter settings (Eq. 10) involve \(R=\|y_0-y^*(x_0)\|\), which may not be known in practice. The paper could note that this can be bounded by a known constant or estimated.

### Trivial

- The lower bound is a direct reduction to the single-level construction of Arjevani et al. (2023); while valid, it does not provide new insight into bilevel-specific hardness. The authors acknowledge this and cite concurrent work for stronger lower bounds when \(p=1\).

## Nice-to-Haves

- A proof sketch or intuitive explanation of Lemma 3.2, clarifying why smoothness only in \(y\) suffices.
- Experiments with multiple random seeds and reporting mean/variance.
- Empirical comparison between normalized and unnormalized gradient steps.
- Discussion on practical strategies for choosing \(p\) when the smoothness order is unknown.

## Novel Insights

The paper’s central insight—that the penalty reformulation for bilevel optimization can be viewed as a first-order finite-difference approximation of the hyper-gradient, and that higher-order finite-difference schemes directly lead to better convergence rates—is both elegant and productive. It opens a systematic pathway to accelerate fully first-order bilevel methods under higher-order smoothness conditions. The observation that for even \(p\) the number of lower-level subproblems per iteration does not increase compared to \(p=1\) (both require two subproblems) is practically important.

## Suggestions

- Provide a proof or a detailed sketch of Lemma 3.2 in the main paper or appendix to reassure readers that the \(y\)-only smoothness assumption is sufficient.
- Run experiments with multiple random seeds (at least 5) and display mean + standard deviation or confidence bands.
- Clarify in the experimental section whether normalized gradient steps were used; if so, discuss the effect on convergence and compare with standard gradient steps.
- Add a brief remark on how to estimate \(R\) or choose the initial \(y\) to satisfy the condition in practice.

## Score and Decision

Score: 7.5

Decision: Accept

MY FINAL SCORE: <score>7.5</score>
MY FINAL DECISION: <decision>Accept</decision>
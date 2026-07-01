## Summary

This paper establishes a theoretical framework connecting certified machine unlearning with continual learning. It adapts two classes of certified unlearning methods (gradient-based and Hessian-based) to operate within a continual learning setting, providing theoretical guarantees by decomposing post-unlearning excess risk into continual learning excess risk and unlearning loss. The Hessian-based algorithm is shown theoretically to achieve lower unlearning loss at the cost of storage, while a forgetting-enhanced variant reduces storage. Experiments on MNIST are presented.

## Strengths

- **Clean problem decomposition.** The formalization of post-unlearning excess risk as the sum of continual learning excess risk (equation 7) and unlearning loss (equation 6) in Section 2.3 is the paper's clearest conceptual contribution. It correctly captures the tension that reducing one term can worsen the other — a trade-off absent from prior static-setting certified unlearning work.

- **Parameterized trade-off via ρ.** The analysis unifies forgetting and unlearning through a single parameter ρ = λ/(μ+λ) (Theorem 4.1, equation 9), showing that the same mechanism that controls catastrophic forgetting in continual learning also determines unlearning loss. This provides a clean analytical handle on the tension.

- **Novel handling of out-of-order unlearning requests.** The Hessian-based update rule (Algorithm 2, equation 13) addresses the non-trivial challenge that unlearning requests can arrive in arbitrary order and disrupt prior unlearning corrections. The second term in (13) adjusts for interference with previously unlearned tasks, which is a genuine technical contribution beyond straightforward adaptation.

- **Forgetting-enhanced variant (Section 5.3).** The practical heuristic of using Hessian correction only for recent tasks while relying on natural forgetting for older ones is a sensible engineering compromise that follows from the theoretical analysis and reduces storage costs.

## Weaknesses

### Major

- **Theory-experiment assumption gap and overclaimed validation.** The theory (Assumption 2.1) requires the loss to be μ-strongly convex, L-Lipschitz, and M-smooth. The experiments (Section 6, line 288) use cross-entropy loss with a softmax output on a linear model, which is *not* strongly convex — the paper states it "relax[es] its assumption of μ-strong convexity." Yet the abstract, introduction, and conclusion all claim experiments "validate" the theory. The paper provides no argument that the bounds (which depend on μ through ρ = λ/(μ+λ)) carry over to the non-strongly-convex regime. The theoretical bounds become formally vacuous when μ → 0 (ρ → 1 or λ/λ = 1), but the experiments operate precisely in that regime. This disconnect between the theoretical claims and the experimental setup is significant; the claims should be reframed as illustration rather than validation.

- **Thin experimental evaluation.** The empirical component consists of: one dataset (MNIST), one model class (linear with softmax), T=30 tasks, a single unlearning sequence, **no error bars or repeated trials**, and no retraining baseline shown in the key unlearning loss plot (Figure 2(b)). The Hessian-based algorithm's accuracy is compared to perfect retraining only in Table 1 (three λ values), but the natural forgetting algorithm (Alg 1) is excluded from that comparison, making it impossible to evaluate the headline claim that "our Hessian-based adaption algorithm largely outperforms the gradient-based algorithm." The empirical support is insufficient to substantiate the paper's validation claims.

### Minor

- **Unclear notation in Proposition 5.2 (equation 15).** The expression $w_m^{\mathbf{S}_{\leq t} \setminus \{m+1, \dots, t\}}$ uses a set-minus notation in the superscript that is unconventional and difficult to parse without the appendix. The variable $m$ appears both as a time index subscript and inside the set expression in the superscript, making the intended meaning unclear from the main text alone.

- **"First theoretical foundation" framing could be more precise.** The paper adapts existing certified unlearning machinery (Neel et al. 2021; Sekhari et al. 2021) to the ℓ₂-regularized continual learning algorithm (Kirkpatrick et al. 2017), and extends an excess-risk bound from linear models (Lin et al. 2023) to convex models. The core analytical components are inherited. While the *combination* and the analysis of the forgetting–unlearning tension are genuinely novel, the framing as a "first theoretical foundation" could more clearly delineate which parts are inherited vs. new.

### Trivial

None.

## Nice-to-Haves

- The paper could strengthen its empirical contribution by testing the *qualitative* predictions of the bounds — for instance, does the approximation error decay exponentially with the number of tasks trained after the unlearned task (ρ^(t−s)), as predicted by Theorem 4.1? Such targeted tests would better connect theory and experiments even under relaxed assumptions.
- Adding error bars and at least one more dataset (e.g., Fashion-MNIST or CIFAR-10 with a simple CNN) would substantially improve empirical credibility.

## Removed Points

- **Self-cancelling terms in equation (8):** The reviewer noted terms like $\|w_{\tau_j}^* - w_{\tau_j}^*\|$ and $\rho^{\tau_j - \tau_j}$. These are parser artifacts (broken subscripts) — the original submission almost certainly had $\rho^{\tau_j - \tau_i}$ and $\|w_{\tau_j}^* - w_{\tau_i}^*\|$. Removed per hard rules on formatting artifacts.
- **Table 2 not shown in main text:** The parser strips appendix content from all papers. Removed per hard rules.
- **Storage cost impracticality:** The paper already acknowledges the O(td² + 2td) storage cost and proposes the forgetting-enhanced variant to reduce it. This is not an overlooked weakness.
- **Missing related works / existing methods not discussed:** Per hard rules, not permissible to mention based on reviewer knowledge gaps.
- **General speculation about confounders or unverified assumptions:** Stripped per filtering discipline — only concrete, paper-grounded criticisms are retained.

## Novel Insights

None beyond the paper's own contributions. The reviews corroborate the paper's central contributions (the decomposition, the ρ-parameterized trade-off, and the Hessian-based algorithm's handling of out-of-order requests) while identifying gaps in experimental support and theory-experiment alignment.

## Suggestions

1. Reframe the experimental section as *illustrative* rather than *validating*, and transparently acknowledge the assumption gap. Add a small ℓ₂ regularizer to the loss to approximately satisfy strong convexity, or provide an argument for why the bounds approximately apply under the relaxed setting.
2. Add error bars (multiple random seeds/initializations), a retraining baseline to Figure 2(b), and at minimum a second dataset. Include the natural forgetting algorithm's accuracy alongside the Hessian-based algorithm in the quantitative comparison.
3. Fix the notational issue in Proposition 5.2 (equation 15) for clarity in the main text.

## Score and Decision

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>
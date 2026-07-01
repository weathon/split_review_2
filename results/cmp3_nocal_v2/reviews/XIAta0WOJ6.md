## Summary

This paper proposes a family of fully first-order methods (F²SA-*p*) for stochastic bilevel optimization under the standard nonconvex-strongly-convex setting. The key conceptual contribution is reframing the existing F²SA method as a forward-difference approximation of the hyper-gradient, which naturally generalizes to higher-order finite-difference schemes. Under a *p*th-order smoothness assumption in the lower-level variable **y** only, the authors prove an SFO complexity of \(\tilde{\mathcal{O}}(p\epsilon^{-4-2/p})\) that interpolates from the known \(\tilde{\mathcal{O}}(\epsilon^{-6})\) (\(p=1\)) to near-optimal \(\tilde{\mathcal{O}}(\epsilon^{-4})\) as \(p\) grows, and provide an \(\Omega(\epsilon^{-4})\) lower bound via a clean separable construction.

## Strengths

1. **A genuine conceptual reframing.** Connecting the penalty-based F²SA method to finite-difference approximation of hyper-gradients (Eqs. 8–9 and the derivation around line 171) is the paper's key insight. This makes the generalization to higher-order finite differences natural rather than ad hoc, unifying the algorithm family under a single analytic framework.

2. **Clean complexity interpolation.** Theorem 3.1 gives \(\tilde{\mathcal{O}}(p\epsilon^{-4-2/p})\) that smoothly connects \(\tilde{\mathcal{O}}(\epsilon^{-6})\) for \(p=1\) to near-optimal \(\tilde{\mathcal{O}}(\epsilon^{-4})\) as \(p\) grows. The intermediate values (e.g., \(\tilde{\mathcal{O}}(\epsilon^{-5})\) for \(p=2\)) are genuine predictions, and this interpolation is what a good theory should provide.

3. **Valid lower bound with clean construction.** The separable construction (Section 4) with \(g(x,y)=\mu y^2/2\) satisfies all the paper's smoothness assumptions and reduces bilevel to single-level optimization, cleanly inheriting the \(\Omega(\epsilon^{-4})\) lower bound from Arjevani et al. (2023). The simplicity of the construction is a virtue, avoiding issues with prior constructions (Dagré et al. 2024, Kwon et al. 2024a).

4. **Tighter analysis for existing results.** Remark 3.2 identifies an improved Lipschitz constant for the \(p=2\) case compared to Chen et al. (2025b), and Remark 3.3 improves the \(p=1\) \(\kappa\) dependence from \(\kappa^{12}\) to \(\kappa^{11}\).

## Weaknesses

### Fatal

None.

### Major

1. **Experiments measure the wrong quantity and conflate compute budget with algorithmic improvement.** The paper's central claim is about **SFO complexity** (Theorem 3.1), yet the experiments report test loss and test accuracy vs. **outer-loop iterations** (Figure 1). Since F²SA-*p* with larger even *p* solves *p* parallel lower-level SGD trajectories per outer iteration, F²SA-10 uses 5× more gradient calls per step than F²SA (\(p=1\)). The advantage visible in Figure 1 may be entirely an artifact of higher per-iteration compute rather than the finite-difference scheme itself. The paper states it "conduct[s] numerical experiments to verify our theory," but the presented evidence does not test the theory's core prediction.

2. **No statistical reporting for stochastic experiments.** The paper reports no error bars, standard deviations, or information about the number of random seeds for any method. For stochastic optimization where both gradient oracles and algorithm states are random, single-trace comparisons are uninterpretable.

### Minor

3. **Hyperparameter search not transparent.** The paper states that hyperparameters (\(\eta_x, \eta_y, \nu\)) were searched on "a logarithmic scale with base 10" but provides no search ranges and no final selected values. This makes it impossible to assess whether the comparison is fair across methods.

4. **Fixed inner-loop length mismatches theory.** The inner-loop length is set to \(K=10\) uniformly for all methods. Theorem 3.1 prescribes \(K \asymp \frac{\kappa^2\sigma^2}{\nu^2\epsilon^2}\log(\dots)\), which varies with *p* because \(\nu \propto \epsilon^{1/p}\). The experiments do not follow the theoretical prescriptions.

5. **Normalized gradient step is a departure from practice.** Algorithm 1 uses \(x_{t+1} = x_t - \eta_x \Phi_t / \|\Phi_t\|\) rather than a standard gradient step. Remark 3.1 acknowledges this is "for analytical convenience" and asserts that standard steps would work, but the analyzed algorithm differs from what one would implement. This is a small theoretical gap.

6. **"Almost for free" claim is conditional.** The paper states that F²SA-2's benefits come "almost for free" (line 257) because it solves the same number of lower-level problems as F²SA. However, the improvement requires second-order smoothness (Assumption 2.5 with \(p\geq 2\)); without it, the error guarantee degenerates to first-order. The caveat is present in the text, but the headline phrasing overstates the unconditional benefit.

### Trivial

None.

## Nice-to-Haves

- Replace the per-iteration plots with plots of gradient norm vs. SFO calls (or wall-clock time with matched resources), including error bars over multiple seeds. This would directly verify whether the theoretical SFO improvement manifests empirically.
- Add an ablation comparing F²SA-2 with 2 lower-level solves vs. F²SA with 2 lower-level solves under identical total inner-loop budget, to isolate the effect of central vs. forward differencing.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **Faà di Bruno proof in appendix (Critical Issue 2 from the input).** The critic questioned the claim that only **y**-direction high-order smoothness suffices, noting the proof uses the high-dimensional Faà di Bruno formula and is relegated to the appendix. **Removed per hard rule:** the parser stripped the appendix from all papers; the proofs exist in the original submission. This is a trust issue that would be resolved by the full paper, not a weakness of the paper as submitted.

- **L\(_0\)-Lipschitz assumption restrictiveness.** The critic noted that Assumption 2.4 assumes \(f\) is \(L_0\)-Lipschitz in **y**, which excludes some practically relevant losses. **Removed:** this is a standard assumption in the F²SA literature, not specific to this paper's contribution.

- **\(\eta_y\) \(\nu^2\) dependence.** The critic noted that \(\eta_y\) has a \(\nu^2\) dependence that varies with \(p\). **Removed:** this is simply describing a consequence of Theorem 3.1, not a weakness.

- **Lower bound independent of \(p\).** The critic noted the \(\Omega(\epsilon^{-4})\) lower bound does not tighten as \(p\) increases. **Removed:** the paper openly acknowledges this gap and discusses it as an open problem.

- **Large condition number dependency.** The critic noted \(\kappa^{9+2/p}\) is large. **Removed:** the paper discusses the \(\Omega(\kappa^9)\) condition number gap as an open problem in the same paragraph.

## Novel Insights

None beyond the paper's own contributions. The reviews do not surface an independent novel observation about the paper that is not already articulated in the paper or in the strengths/weaknesses above.

## Suggestions

1. **Refocus the experiments on SFO complexity.** Plot gradient norm (the quantity the theory guarantees) vs. total SFO calls, including error bars over ≥5 random seeds. This would directly test the paper's core theoretical prediction.
2. **Report hyperparameter search details.** Disclose the search ranges and final selected values for all hyperparameters (\(\eta_x, \eta_y, \nu\)) for each method.
3. **Soften the "almost for free" claim** or attach the conditionality more prominently.

## Score and Decision

This is a solid theoretical paper. The core insight — that F²SA can be interpreted as a forward-difference hyper-gradient approximation, and that higher-order finite differences yield provably better complexity under higher-order smoothness — is genuine and well-executed. The complexity interpolation from \(\tilde{\mathcal{O}}(\epsilon^{-6})\) to near-optimal \(\tilde{\mathcal{O}}(\epsilon^{-4})\) is a clean result, and the lower bound is rigorous. The experimental section is the weakest part, but the paper's contribution is primarily theoretical, and the experimental flaws do not invalidate the theory.

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>
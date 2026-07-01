## Summary

This paper studies stochastic bilevel optimization in the nonconvex-strongly-convex setting. It reinterprets the existing F²SA method as a forward-difference approximation of the hyper-gradient, then generalizes this to a family of methods (F²SA-p) using p-th-order finite differences. Under a higher-order smoothness assumption on the lower-level variable, the paper proves improved SFO complexity of Õ(p ε^{-4-2/p}), interpolating between ε^{-6} (p=1) and ε^{-4} (p→∞), and provides an Ω(ε^{-4}) lower bound showing near-optimality for large p. The paper is primarily a theoretical contribution with illustrative experiments on a logistic regression hyperparameter tuning problem.

## Strengths

1. **A clean conceptual reinterpretation of F²SA (Section 3.1).** The connection between F²SA's penalty reformulation and forward-difference approximation of the hyper-gradient (Eqs. 8–9) is genuinely insightful and opens the door to higher-order generalizations. The derivation is precise and well-explained.

2. **A non-trivial generalization to arbitrary p (Lemma 3.2, Theorem 3.1).** Generalizing from p=1 to arbitrary p∈ℕ₊ requires the Faà di Bruno formula (Lemma 3.2) to bound the Lipschitz constant of ∂^{p+1}/(∂ν^p ∂x) ℓ_ν(x). The complexity improves monotonically with p, interpolating between Õ(ε^{-6}) at p=1 and Õ(ε^{-4}) as p→∞, which is exactly what one would hope for. The tightening for p=2 (Remark 3.2, improving κ⁶ to κ⁵) is also a concrete technical improvement over prior work.

3. **A valid and clean lower bound (Theorem 4.1).** The separable construction f(x,y)≡f_U(x), g(y)=μ‖y‖²/2 cleanly reduces bilevel to single-level optimization while respecting all smoothness assumptions. The paper correctly identifies how prior constructions by Dağrü et al. (2024) and Kwon et al. (2024a) inadvertently violated smoothness assumptions. The bound Ω(Δ L₁ σ² ε^{-4}) matches the single-level lower bound exactly.

4. **Honest framing and open problems (Section 1, Section 6).** The paper clearly states what it does not solve: the gap for small p, the condition number gap of Ω(κ⁹), and the extension to nonconvex-nonconvex settings. This intellectual honesty is valuable for the community.

## Weaknesses

### Fatal

None.

### Major

None. The theoretical contributions are sound, and the experiments, while limited, do not undermine the paper's core claims.

### Minor

1. **Experiments do not report the quantity the theory guarantees (Section 5, Figure 1).** The theory concerns finding an ε-stationary point measured by ‖∇φ(x̂)‖ ≤ ε, but the experiments report test loss and test accuracy versus outer-loop iterations. The paper claims to "conduct numerical experiments to verify our theory" (line 278), yet the reported metrics do not directly measure gradient stationarity. While it is common for theory papers to use illustrative proxy metrics, reporting at least an approximation of ‖∇φ(x)‖ (e.g., using the finite-difference estimator itself) would substantially strengthen the connection between theory and experiment.

2. **Fixed inner-loop budget K=10 without justification or ablation (Section 5).** The theory (Theorem 3.1) prescribes K ∝ (κ²σ²)/(ν²ε²)·log(·), which depends on problem parameters. The paper sets K=10 for all methods and provides no discussion of whether this is sufficient, nor any ablation over K to verify that the inner-loop approximations are accurate. Without such validation, it is unclear whether the observed performance ordering is driven by the finite-difference improvement or by other factors.

3. **No variance reporting or multiple-seed analysis (Section 5).** The experiments do not report error bars, confidence intervals, or any indication of multiple runs. Since all methods are stochastic, single-run comparisons risk being driven by randomness. This limits the reliability of the empirical comparisons.

4. **Results plotted against outer iterations, not total SFO calls (Section 5, Figure 1).** The per-iteration cost differs across methods: F²SA-p with p=10 requires solving 10 lower-level problems per outer iteration, while standard F²SA and F²SA-2 require only 2. Plotting against outer iterations hides this cost difference and may give a misleading impression of relative efficiency. A plot against total SFO calls or wall-clock time would be more informative.

### Trivial

None.

## Nice-to-Haves

- An ablation on the inner-loop budget K (e.g., K ∈ {5, 10, 20, 50}) to verify robustness to this hyperparameter.
- An empirical comparison of the normalized gradient step used in Algorithm 1 against a non-normalized variant, which Remark 3.1 speculates would also work.
- Practical guidance on choosing p, since the theoretical condition p = Ω(log(κ/ε)/log log(κ/ε)) depends on unknown quantities.

## Removed Points

These points are flagged to be removed; treat them with caution:

- **"The lower bound is not informative for the paper's own problem class."** The reviewer noted that the construction makes g independent of x, so the problem decouples. However, the paper is transparent about the construction being "fully separable" (line 275) and explicitly acknowledges the κ gap as an open problem (lines 48–49). The lower bound is valid for the problem class and achieves its stated purpose; the observation does not identify a flaw in the paper.
- **"Cannot verify Lemma 3.2 without the appendix."** Removed per the hard rule: the parser strips appendix content; the original submission contains the proofs.
- **"K=10 is likely far from the theoretical requirement."** The speculation about actual constants for the 20 Newsgroup problem is not verifiable from the paper as written. The fixed-K concern is kept in Minor above as a concrete observation; the speculation about specific values is removed.
- **"No discussion of how to choose p in practice"** and **"The deterministic setting is not discussed."** These address topics outside the stated scope of the paper (stochastic optimization, theory-focused) and are suggestions for future work rather than weaknesses.

## Novel Insights

None beyond the paper's own contributions. The valid critical observations about the experiments (mismatch between theoretical quantity and reported metric, fixed K without ablation, no error bars, per-iteration cost not accounted for) are standard evidential gaps rather than novel methodological insights.

## Suggestions

1. In a revision, add a plot of estimated gradient norm (e.g., using the finite-difference estimator itself) over iterations for different p values. This directly connects the experiments to the ε-stationarity guarantee of Theorem 3.1.
2. Add an ablation over K to show whether the method's performance is robust to the inner-loop budget.
3. Run multiple seeds (e.g., 5) and report error bands or standard deviations on the loss/accuracy curves.
4. Report results against total SFO calls in addition to outer iterations to give a fair per-iteration cost comparison.

MY FINAL SCORE: <score>8.0</score>
MY FINAL DECISION: <decision>Accept</decision>
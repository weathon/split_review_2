**Note on access**: The file was successfully read in full earlier. The partial read error above is a technical limitation of sub-range access; the full content is already available.

Now writing the final review.

## Summary

This paper proposes SCaSML, a framework that combines a pre-trained surrogate model (PINN or GP) with Monte Carlo simulation (Multilevel Picard iteration) to correct the surrogate's error at inference time. The core idea is to derive a "defect PDE" for the approximation error that retains the semi-linear structure of the original problem, enabling solution via stochastic simulation. The authors provide theoretical analysis suggesting a product-form error bound and improved convergence rate, and empirical results on high-dimensional PDEs up to 160 dimensions.

## Strengths

1. **The core idea is genuinely interesting and well-motivated.** Combining defect correction (a classical numerical analysis concept) with modern ML surrogates is a creative synthesis. The intuition—that the surrogate handles smooth/low-frequency components and the Monte Carlo correction handles the high-frequency residual—is physically sensible and connects to spectral bias in neural networks (Rahaman et al., 2019). This is articulated clearly in Section 2.1.

2. **The theoretical framing (Theorem 2.5) targets the right question.** The claim that the final error is bounded by the *product* of surrogate error and simulation error captures a genuinely synergistic relationship: the cost of correction decreases as the surrogate improves. This provides a concrete framework for understanding when the hybrid approach helps.

3. **The range of test problems is appropriate and challenging.** Linear convection-diffusion, viscous Burgers, HJB from LQG control, and diffusion-reaction with oscillatory solutions span from textbook linear to strongly nonlinear, from smooth to oscillatory, and from d=10 to d=160. SCaSML consistently achieves lower error than the surrogate alone across all 20 problem-dimension combinations in Table 1.

4. **The paper acknowledges the control variate interpretation** in the conclusion (Section 4, line 328: "our framework uses the machine learning model as a control variate in stochastic simulations"), showing awareness of the method's relationship to established techniques.

## Weaknesses

### Fatal

None.

### Major

1. **Unequal clipping thresholds compromise the empirical comparison in 3 of 4 experiments.** For the Viscous Burgers, HJB/LQG, and Diffusion-Reaction experiments, SCaSML and the naive MLP solver use substantially different clipping thresholds (e.g., 0.01 vs. 1.0 for Burgers, 0.1 vs. 10 for HJB, 0.01 vs. 10 for DR). Clipping directly constrains the solution values, and giving SCaSML a 100× tighter threshold provides a significant advantage. The paper's justification ("reflecting the smaller magnitude of the defect," line 250–251) partially presumes the conclusion it is trying to demonstrate. This concern is partially mitigated by the LCD experiment (Section 3.1), where both methods use the *same* threshold (0.5(d+1), line 234) and SCaSML still achieves 20–56.9% error reduction—but this single clean comparison is not sufficient to allay concerns about the other three experiments.

2. **The main results do not normalize for substantially unequal compute budgets.** SCaSML is 10–134× more expensive than the surrogate alone in runtime (e.g., LCD 60d: 37.59s vs. 0.28s; VB-GP 80d: 60.69s vs. 1.69s). The headline claim of "20–80% error reduction" is presented without contextualizing the additional compute cost. The paper states that "fixed-budget efficiency comparisons" are in Appendix G.7, but the main text's presentation of results (Table 1, Section 3) frames the comparison primarily in terms of error without cost normalization, which can give a misleading impression of the method's practical efficiency.

3. **Overselling of the "Structural-preserving Law of Defect."** The derivation (Fact 2.3) is direct algebraic rearrangement: subtracting the surrogate's PDE from the original yields a new PDE for the error. The paper's claim that this is "the first derivation that preserves the semi-linear structure essential for high-dimensional Monte Carlo solvers" (line 31) overstates what is a straightforward algebraic consequence—subtracting two semi-linear PDEs always yields a semi-linear PDE. The real contribution is the *application* of this observation (using the defect PDE to enable Monte Carlo correction), not the derivation itself.

### Minor

1. **The main text's convergence heuristic mixes incompatible resource measures.** The "Intuition for Faster Convergence" box and Section 2.4 state: if the surrogate error scales as m^−γ *from m training points*, and one averages *m new Monte Carlo paths*, the error becomes m^−γ−1/2, totaling "2m function evaluations." This treats training points and Monte Carlo paths as fungible computational units and ignores the per-step cost of evaluating the surrogate and its gradients (which require forward *and* backward passes through the neural network at every simulation step). While the paper labels this as "Intuition" and references rigorous proofs in the appendix (Appendices F and E), the informal argument in the main text would benefit from caveating the strong simplifying assumptions.

2. **Naming inconsistency.** The method is referred to as SCaSML, SCaML (Figure 1), SCA²SM¹ (Table 1, Corollary 2.6), and SCSML (Figure 3) across the paper. This makes the paper harder to follow.

### Trivial

- None beyond the naming inconsistency noted above.

## Nice-to-Haves

- A compute-normalized comparison (error vs. total wall-clock time for all methods) in the main text rather than deferred to the appendix. This would directly address the efficiency question.
- For the experiments with different clipping thresholds, an ablation showing sensitivity to the clipping choice would strengthen confidence in the results.
- A more explicit discussion of *when* the method is expected to provide large vs. small improvements (the error reduction varies from 6.6% to 80% across problems).

## Removed Points

These points were raised in the harsh review but are removed with justification:

- **"Inference-time scaling framing is rhetorically misleading"** — Removed because the paper's conclusion (line 328) explicitly acknowledges the control variate interpretation: "our framework uses the machine learning model as a control variate in stochastic simulations." The LLM analogy is a framing device, and the paper does not hide the method's relationship to established techniques.
- **"Weak baselines (small PINN, few training iterations)"** — Removed. The paper's goal is to show that correction improves an existing surrogate, not to compete with the strongest possible surrogate. The surrogate sizes are a design choice for the experiment, not a flaw in the method.
- **"Proof relegated to appendix"** — Removed per meta-instructions: the parser strips appendices from all papers; the full proofs exist in the original submission.
- **"Convergence rate not derivable from information presented"** — Weakened from a fatal claim to a Minor note because (a) the paper states rigorous proofs are in Appendices F and E, and (b) the main text's argument is labeled as "Intuition."
- **"The defect PDE is not structurally easier to solve"** — Removed. The claim is not that the defect PDE is "easier" in an absolute sense, but that its residual magnitude is smaller (due to the surrogate's accuracy), which reduces Monte Carlo variance. This is the central mechanism of the method.

## Novel Insights

The reviews surface a key tension that the paper does not fully resolve: the method's efficiency claim depends on the surrogate error being small enough that the defect PDE's residual is significantly smaller in magnitude than the original source term. When this holds, the variance reduction is substantial and the product-form bound in Theorem 2.5 is meaningful. When it does not, the approach reduces to running MLP on a problem with a more complicated nonlinearity (F̃ replaces F) at additional gradient-evaluation cost. The paper would benefit from characterizing this "sweet spot" more precisely rather than presenting the method as universally beneficial.

## Suggestions

1. **Fix the clipping asymmetry.** Use identical clipping thresholds for all methods, or systematically ablate the sensitivity to clipping and report results across a range of thresholds.
2. **Add compute-normalized plots to the main text.** Show error vs. total compute (wall-clock time) for surrogate-only, MLP-only, and SCaSML to clarify the efficiency trade-off.
3. **Tone down the claims about the "Structural-preserving Law of Defect."** Acknowledge more directly that it is a straightforward algebraic consequence, and focus the novelty claim on the application (using it for Monte Carlo correction of ML surrogates).
4. **Unify the naming.** Pick one name (SCaSML) and use it consistently throughout.
5. **Add a "when to use" discussion.** The error reduction varies dramatically (6.6% to 80%). A principled explanation of this variation would strengthen the paper significantly.

## Score and Decision

MY FINAL SCORE: <score>5</score>
MY FINAL DECISION: <decision>Reject</decision>
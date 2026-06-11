## Summary
# Final Review Report

## Summary

This paper presents a theoretical and empirical study claiming that neural (nonlinear) policy ensembles are inherently sub-optimal compared to linear policy ensembles. The authors develop three main theorems: (1) neural ensembles are sub-optimal on linear systems under diversity, nonlinearity, and complexity conditions; (2) time-varying neural ensemble weights can cause instability even when base policies are individually stable; and (3) non-convex (neural) mixing of optimal linear policies is sub-optimal compared to convex mixing. Experiments on multi-regime LQR systems and nonlinear benchmarks (Pendulum, CartPole/van der Pol) are presented to support these claims.

**Core assessment:** The paper addresses a potentially important question about the fundamental limitations of neural policy ensembles. The theoretical framework is well-structured and the intuition about temporal coupling breaking ensemble averaging is compelling. However, the manuscript suffers from several critical issues: (a) a central empirical claim ("2 orders of magnitude" gap) is contradicted by the paper's own reported numbers (~1.85x gap); (b) the mixing experiments contain contradictory results that may actually disprove a core theorem (neural mixing outperforms convex mixing on a nonlinear system); (c) the mathematical definition of the nonlinearity measure (κ) has well-definedness issues; (d) empirical validation of the stability theorem is missing key measurements; and (e) there are naming inconsistencies that raise reproducibility concerns. External novelty verification was not possible in this run (Retrieval-Disabled Mode), so novelty conclusions are deferred for manual verification. The paper has strong potential but requires substantial revision before publication.

## Strengths
**S1. Important and under-explored question.** The paper addresses a fundamental issue: whether the success of ensemble methods in supervised learning (classifier ensembles) carries over to sequential decision-making (policy ensembles). The central intuition — that temporal coupling in closed-loop systems can break the variance-reduction mechanism of ensemble averaging — is insightful and worth formal investigation.

**S2. Clean theoretical framing.** The paper sets up a rigorous mathematical framework with clear definitions (admissible policies, value functions, HJB equation, nonlinearity measure). The three theorems address distinct but related aspects of sub-optimality (ensemble performance, stability, mixing), providing a reasonably comprehensive theoretical treatment. The use of CLF theory for stability analysis (Theorem 2) is a principled approach.

**S3. Multi-faceted experimental design.** The experiments cover multiple dimensions: (i) performance comparison on linear systems, (ii) switching pattern analysis, (iii) diversity scaling, (iv) stability on nonlinear benchmarks, and (v) policy mixing effects. This breadth demonstrates an attempt to validate the theory from multiple angles.

**S4. Reproducibility effort.** The paper includes source code, well-defined seeds, and a reproducibility statement. The use of multiple seeds (5) and trials (10) for statistical averaging is appropriate. The Appendix includes AI usage disclosure and reproducibility details.

**S5. Practical motivation.** The paper connects its theoretical findings to practical domains (RL, Mixture-of-Experts, agentic AI), making the work relevant to a broad audience. The discussion of safety-critical systems as a key application area is well-placed.

## Weaknesses
**W1. [CRITICAL] "2 orders of magnitude" claim is unsupported by reported data (Page 1 – Abstract, Page 1 – Introduction).**
The Abstract and Introduction repeatedly claim that neural ensembles underperform linear ensembles "often by 2 orders of magnitude" (i.e., ~100x). However, the primary experimental data in Figure 1 shows a gap of only ~1.85x (Neural Ensemble cost = 432.21 vs LQR Ensemble cost = 234.06). The optimality gaps (51.5 vs 249.6) show a ~4.8x ratio, still far from 100x. This is a factual overclaim that misrepresents the empirical evidence. If the 2-orders claim refers to a different experiment not shown in the main paper, that experiment must be included. This issue undermines the credibility of the entire empirical narrative. **(Annotation ID: a99652c8)**

**W2. [CRITICAL] Mixing experiments contradict Theorem 3 (Page 1 – Section 6, Figure 5).**
The policy mixing experiments contain results that directly contradict the paper's central claim that neural (non-convex) mixing is sub-optimal. For the Soft_Pendulum system, Figure 5(a) shows Neural Non-Convex Mixing achieving Mean Episode Count ≈ 1500, while Linear Convex Mixing achieves only ≈ 500. If "Mean Episode Count" is higher-better (common for RL metrics like "episodes until success" where lower is better, or "total reward" where higher is better — the paper does not specify), this is a 3x advantage for neural mixing, disproving the claim that convex mixing is universally optimal. If lower-is-better, the figure labeling is misleading. Furthermore, subplots (b) and (d) both labeled "Convexity Violation" show contradictory patterns for Soft_Pendulum — (b) shows a large violation for neural mixing while (d) shows near-zero for all methods. These internal contradictions must be resolved. **(Annotation ID: 4ef978b6)**

**W3. [MAJOR] Definition 10 (Nonlinearity Measure) is mathematically problematic (Page 1 – Section 3.1).**
The nonlinearity measure κ defined as sup_{x≠y} sup_λ ||π(λx+(1-λ)y) - λπ(x) - (1-λ)π(y)|| / ||x-y|| has several technical issues. The denominator ||x-y|| means that for smooth nonlinear functions (e.g., π(x)=x^2), the numerator scales as O(||x-y||^2) while the denominator is O(||x-y||), making the ratio O(||x-y||) which blows up as x→y, potentially making κ infinite even for well-behaved functions. For piecewise-linear functions (ReLU networks), κ is zero within linear regions and only non-zero at region boundaries, meaning the sup may be dominated by boundary artifacts. This undermines the applicability of Theorem 1's condition (2) to commonly used neural network architectures. A constructive replacement or a clear discussion of well-definedness is needed. **(Annotation ID: 577e76d5)**

**W4. [MAJOR] Theorem 1 condition (3) mixes incommensurate quantities without justification (Page 1 – Section 3.1).**
The "Sufficient Complexity" condition L_f κ_0 δ > ρ combines the Lipschitz constant of system dynamics (L_f) with the nonlinearity measure (κ_0), policy diversity (δ), and the discount rate (ρ). These quantities have different units/dimensions, and their product inequality is presented without physical interpretation, scaling analysis, or examples showing when it is satisfied. The non-constructive nature of ε (the theorem only proves existence, not a value) further limits practical utility. The paper should at minimum discuss dimensional consistency, provide parameter ranges for realistic systems, and offer a constructive lower bound for ε. **(Annotation ID: 7d019285)**

**W5. [MAJOR] Empirical validation of Theorem 2 lacks critical measurements (Page 1 – Section 5).**
Theorem 2 provides a specific bound for instability: β > min_i α_i / (2 max_i ||V_i||_∞). However, the empirical stability study (Section 5) does not report any of the quantities needed to verify this bound — not β (weight variation rate), not α_i (Lyapunov decay rates), and not ||V_i||_∞ (Lyapunov function bounds). The experiments show that neural ensembles are less stable, but this is a weaker claim than what Theorem 2 predicts. The theory-empirical gap means the stability theorem is not empirically corroborated in a falsifiable way. **(Annotation ID: b1f6c596)**

**W6. [MAJOR] Stability experiment has naming inconsistency (Page 1 – Section 5.1 vs Figure 4 caption).**
The text in Section 5.1 states the neural ensemble was tested on "Pendulum and vadDerPol" systems, while Figure 4's caption and description consistently refer to "Pendulum and CartPole tasks." CartPole and van der Pol are fundamentally different dynamical systems. This inconsistency makes it impossible for readers to know which environments were actually tested, severely undermining reproducibility. **(Annotation ID: 966f5b68)**

**W7. [MAJOR] Statistical significance reporting is incomplete (Page 1 – Section 4.4).**
The paper claims "p < 10^{-5}" with "extremely strong statistical significance" but does not report which test was used, the test statistic value, degrees of freedom, sample size, or effect size. For the mixing experiments, Cohen's d is mentioned but without the actual value. Incomplete statistical reporting prevents verification of the significance claims. **(Annotation ID: 8cd40a92)**

**W8. [MAJOR] Introduction overclaims with categorical impossibility statement (Page 1 – Introduction).**
The statement "nonlinear function approximators are inherently unsuitable for ensemble control methods, regardless of how sophisticated the ensemble design becomes" is a categorical impossibility claim that is not supported by the paper's evidence. The theorems only apply to convex-weighted ensembles of independently trained neural policies on linear systems. A single counterexample (e.g., a Lipschitz-constrained neural ensemble with stabilizing regularization that closes the gap) would disprove this claim. The language should be bounded to the specific setting studied. **(Annotation ID: 17f96a95)**

**W9. [MAJOR] Conclusion introduces new unsupported concepts (Page 1 – Section 8).**
The Conclusion introduces "trajectory manifold mismatch" and "temporal error amplification" as central insights, but these concepts are not defined, derived, or measured anywhere in the paper. The "key insight" about "diversity in the linear subspace" is presented as a proven finding rather than a speculative research direction. The conclusion should only consolidate what has been demonstrated. **(Annotation ID for Conclusion paragraph)** *(Note: The Conclusion spans lines 470–488 and was annotated in annotation #12 pending)*

**W10. [MAJOR] Abstract and Introduction lack clear gap statement (Page 1 – Abstract & Introduction).**
The Abstract does not follow the standard 4-5 sentence structure (problem → gap → method → result) — it jumps directly to the claim without clearly articulating why existing ensemble methods fail specifically for policies. The Introduction's second paragraph restates the 2-orders claim without providing a concrete gap in prior work that this paper fills. Readers unfamiliar with the specific literature cannot understand what makes this work novel. **(Annotations: 48837f08, 8ac6d90e)**

**W11. [MAJOR] Contributions list mixes proven and empirically demonstrated claims without differentiation (Page 1 – Section 1.1).**
The Contributions list uses "prove" for all bullet points, but the evidence strength varies: Theorems 1-3 are theoretical claims that depend on specific assumptions, while the "Empirical validation" bullet is entirely experimental. Readers cannot distinguish rigorously proven results from empirically demonstrated ones. Each claim should be qualified by its key assumptions and evidentiary basis. **(Annotation ID: 79d98ab9)**

**W12. [MAJOR] Covariate shift / train-test setup is not clearly described.**
The paper says both linear and neural ensembles are "trained from identical data" but does not specify: (a) how the neural policies are trained (online RL? behavioral cloning from optimal controller? system identification?); (b) whether the training data distribution matches the test-time distribution; (c) whether both ensemble types use identical training budgets and hyperparameter tuning. Without this information, the comparison may not be fair.

**W13. [MINOR] Related work section is list-style and lacks comparison axes (Page 1 – Section 7).**
The Related Work is organized as a chronological summary rather than around thematic comparison axes (e.g., ensemble methods for control, theoretical optimality results, MoE stability). The section does not explicitly state how this paper differs from the closest prior work.

**Novelty & External Retrieval Note:** External paper search was not available in this run (Retrieval-Disabled Mode). All novelty and comparison-based conclusions are therefore deferred for manual verification. The paper's claims about prior work coverage and the novelty of its theoretical framework (Theorems 1-3) should be independently verified against the existing literature by the authors and reviewers.

## Score
**Final Score: 4/10**

**Rationale:** This paper tackles an important and timely question about the fundamental limitations of neural policy ensembles, and its theoretical framework (intuition about temporal coupling, three theorems covering sub-optimality/stability/mixing) has the potential to make a meaningful contribution. However, the manuscript in its current form has several critical weaknesses that severely undermine its credibility:

1. **Factual overclaim:** The central quantitative claim of "2 orders of magnitude" improvement gap is not supported by the paper's own experimental data (actual gap is ~1.85x), which constitutes a serious misrepresentation of results.

2. **Contradictory experimental evidence:** The policy mixing experiments contain results that appear to directly contradict Theorem 3 (neural mixing outperforming convex mixing on Soft_Pendulum), along with internal inconsistencies between subplots.

3. **Mathematical rigor issues:** The Nonlinearity Measure (Definition 10) has well-definedness problems that may invalidate Theorem 1's applicability, and the key condition mixing incommensurate quantities lacks justification.

4. **Theory-empirical disconnect:** The stability theorem's predictions are not directly validated — the reported experiment shows a weaker claim than the theorem's specific bound.

5. **Inconsistent reporting:** Naming inconsistencies in stability experiments (vadDerPol vs CartPole) and incomplete statistical reporting reduce reproducibility.

The paper has a solid core intuition and a well-structured theoretical setup, but these issues must be addressed before the claims can be trusted. The score reflects significant revision required rather than fatal flaws — the core idea is salvageable with careful correction of the overclaims, resolution of experimental contradictions, and tightening of the mathematical definitions.

**Recommendation:** Major revision. The authors should (a) correct the "2 orders of magnitude" claim to match actual data, (b) resolve contradictions in mixing experiments and clarify which interpretation is correct, (c) fix the Nonlinearity Measure definition, (d) add direct empirical validation of Theorem 2's bound, (e) fix naming inconsistencies, and (f) complete statistical reporting. Novelty verification against related work should also be strengthened.
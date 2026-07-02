## Summary
# Final Review Report

## Summary

This paper develops a decision-theoretic framework for acting on partially calibrated forecasts in a robust minimax sense. The core idea is to treat a forecaster's predictions as constraints on the set of possible outcome distributions (the "ambiguity set" Q) rather than as point estimates to be blindly trusted or ignored. The paper first characterizes the minimax-optimal decision rule for any finite-dimensional ℋ-calibration guarantee via a duality argument (Theorem 3.1), yielding a tractable two-step procedure: compute an adversarial belief q*(v) via convex optimization, then best-respond to it. The paper then identifies a sharp transition: when ℋ contains the decision-calibration indicators (a weak, tractable condition requiring only |A| test functions), the adversarial tilt collapses and the optimal robust rule reduces to the plug-in best response, recovering the same "trustworthiness" semantics as full calibration (Theorems 4.1–4.2). For settings where decision calibration is unavailable, the paper derives robust policies from pipeline-induced calibration properties (self-orthogonality under squared loss, bin-wise calibration). Empirical evaluation on two regression datasets confirms that the robust policy outperforms naive best-response under calibration-preserving distribution shifts.

The paper makes a solid theoretical contribution to the intersection of calibration and decision theory. The results are clean, well-structured, and the sharp transition finding is genuinely insightful. However, the experimental validation is thin (two datasets, no variance reporting, no multiclass experiments) and the practical applicability is bounded by the linear utility assumption and finite action set requirement. Overall the paper presents novel theoretical insights that advance understanding of how decision-makers can reliably use partially calibrated forecasts.

## Strengths
1. **Clean theoretical framework.** The ℋ-calibration formalism elegantly unifies a spectrum of calibration guarantees, from no information (ℋ = ∅) to full calibration (ℋ = all functions). The duality-based characterization in Theorem 3.1 provides a principled and computationally tractable approach to minimax-optimal decision-making under partial calibration.

2. **Sharp transition insight.** The finding that decision calibration (a weak, tractable condition requiring only |A| test functions) suffices to recover plug-in best-response optimality is genuinely surprising and theoretically significant. It upgrades the previously known swap-regret guarantee of decision calibration to a stronger minimax-optimality claim. The "collapse" of the hierarchy of robust policies (Figures 1-2) is a clean conceptual contribution.

3. **Practical bridge from training pipelines.** Proposition 4.4 (self-orthogonality under squared loss) connects standard regression training to ℋ-calibration without any additional algorithmic intervention, demonstrating that the framework applies to widely used models (linear regression, neural networks with linear heads trained via MSE). This practical grounding is valuable.

4. **Elegant exposition.** The paper is well-structured, with clear notation, helpful schematic figures, and an intuitive conceptual arc. The connection between the ambiguity set Q and the extreme cases (full calibration vs. no information) is explained accessibly before the technical derivation.

## Weaknesses
### W1. Experimental validation is insufficient (Major)

**Evidence:** Section 5 presents experiments on two regression datasets (Bike Sharing, California Housing) with only one model type (2-layer MLP). Table 1 reports only mean utilities without any variance/confidence intervals.

**Root cause:** The experiments are designed as a proof-of-concept rather than a rigorous empirical evaluation. Key limitations include:
- No multi-seed variance or statistical significance reporting. Utility differences are small (0.004–0.019), and readers cannot assess whether these are statistically reliable.
- Only two policies compared (a_BR vs a_robust). No comparison with the constant minimax policy (a_minimax) or post-hoc recalibrated baselines.
- The adversarial distribution construction method is not described, hindering reproducibility.
- No experiments with d > 1 (multiclass or multi-output), which is the paper's primary motivation (full calibration is intractable in high dimensions).
- Only two datasets, both relatively small and low-dimensional.

**Impact:** The empirical claims are weakly supported. While the theory is sound, readers cannot assess how the robust policy performs under realistic conditions without proper statistical reporting and broader evaluation.

**Recommended fix (Must):** (1) Report mean ± std over ≥10 random seeds in Table 1. (2) Describe adversarial distribution construction (algorithm or equations). (3) Report empirical ℋ-calibration error on the calibration split to quantify how closely the calibration condition is met. (4) Add at least one experiment with d > 1.

**Recommended fix (Nice-to-have):** Compare with a_minimax baseline and at least one post-hoc recalibration approach (e.g., isotonic regression).

---

### W2. Linear utility assumption restricts practical scope (Major)

**Evidence:** Assumption 2.1 (Page 4) states that u(a,v) is linear in v. The paper acknowledges this excludes risk-averse utilities but does not quantify how limiting this is.

**Root cause:** The entire framework (Theorem 3.1, Theorems 4.1–4.2) depends on linearity in v for the convexity/concavity structure that makes the minimax problem tractable. Many practical decision-makers are risk-averse, especially in the high-stakes domains (healthcare, finance) that motivate the paper.

**Impact:** The paper's applicability is limited to risk-neutral expected-utility settings. The claimed practical relevance for "high-stakes decision making" is partially undercut by this restriction, since risk aversion is common in such settings.

**Recommended fix:** Add a quantitative discussion of how risk-averse utilities (e.g., concave in v) would change the results. Note that the robust optimization literature often handles convex/concave utilities, and this extension is a natural next step. The current one-sentence acknowledgment in the Conclusion understates the limitation.

---

### W3. Theorem 3.1 lacks formal compactness/convexity justification for saddle-point existence (Moderate)

**Evidence:** Theorem 3.1 (Page 4-5) states the minimax problem admits a saddle point but does not cite a specific minimax theorem or justify compactness/convexity of the relevant spaces.

**Root cause:** The action policy space is a space of measurable functions, and Q is a set of functions satisfying linear moment constraints. Establishing saddle-point existence in infinite-dimensional spaces requires compactness in an appropriate topology or convexity/concavity plus Slater-type conditions.

**Impact:** While the result is likely correct for finite ℋ (since the dual reduces to a finite-dimensional problem), the proof sketch in the main text glosses over technical conditions. This may concern theoretically oriented readers.

**Recommended fix:** Add a brief justification in the main text (or proof sketch) citing Sion's minimax theorem or a suitable infinite-dimensional generalization, noting that the objective is convex in q (linear in q, hence convex) and concave in a (since u is linear in a's argument), and that Q is convex and weakly compact under appropriate conditions.

---

### W4. Self-orthogonality claim assumes population-level stationarity (Moderate)

**Evidence:** Proposition 4.4 (Page 7) assumes the model is trained to a first-order stationary point of the *expected* squared loss. In practice, models are trained on finite samples via SGD, and neural networks may not reach exact stationary points.

**Root cause:** The moment conditions E[z_φ(X)(Y-f_θ(X))^⊤] = 0 and E[f_θ(X)(Y-f_θ(X))^⊤] = 0 hold exactly only at population-level first-order optimality. For finite-sample training, these conditions hold only approximately, with error bounded by the gradient norm at convergence.

**Impact:** The paper acknowledges "approximately satisfies" in the experiments but does not state this caveat explicitly in Proposition 4.4. A reader may overestimate the precision of the self-orthogonality guarantee.

**Recommended fix:** Add a caveat to Proposition 4.4: "In practice, models are trained on finite samples and may not reach exact stationarity; the resulting calibration error is bounded by the gradient norm at convergence, which is typically small."

---

### W5. Decision calibration practicality is asserted without evidence (Minor)

**Evidence:** The Conclusion (Page 9) states decision calibration is "a natural requirement whenever the decision-maker can influence the training pipeline" without providing sample complexity or empirical demonstration.

**Root cause:** The paper cites the multicalibration literature (Hébert-Johnson et al., Noarov et al., Gopalan et al.) for achieving ℋ-calibration, but does not demonstrate decision-calibration training in experiments. Section 5 uses self-orthogonality, not decision calibration.

**Impact:** A reader may question whether decision calibration can be achieved at practical sample sizes for realistic problems, especially when A is moderately large (e.g., |A| = 20).

**Recommended fix:** Add a brief quantitative remark: "Decision calibration requires O(|A|/ε²) samples to achieve ε-calibration error, which is manageable when |A| is small (≤ 10)." Also note the limitation for continuous action spaces.

---

### W6. Related work is organized as a paper list, not a thematic taxonomy (Minor)

**Evidence:** Section 1.2 (Pages 2-3) presents three paragraphs, each summarizing a cluster of related work, but the organization is paper-by-paper rather than by comparison axes.

**Root cause:** The authors chose a narrative style that highlights individual contributions rather than a structured taxonomy. This makes it harder for readers to quickly locate where this paper differs from the closest competitors.

**Impact:** Minor readability issue. The content is informative, but restructuring would improve navigation.

**Recommended fix:** Reorganize into two thematic streams: (A) "Calibration for Decision-Making" (Foster & Vohra, Rothblum & Yona, Zhao et al., Noarov et al., Kleinberg et al., Roth & Shi, Hu & Wu, Okoroafor et al.) and (B) "Robust/Minimax Decision-Making" (Wald, Gilboa-Schmeidler, Hansen-Sargent, Manski, Ben-Tal-Nemirovski, Duchi-Namkoong, Carroll, Andrews & Chen, Kiyani et al.).

---

### W7. Framework assumes finite action set A (Minor)

**Evidence:** The decision-calibration class size equals |A|, and the paper focuses on finite A throughout. Corollary 4.3 (simultaneous optimality across multiple decision problems) requires the union over finite A_j.

**Root cause:** The paper does not discuss how the framework extends to continuous action spaces, where the decision-calibration class becomes uncountably infinite.

**Impact:** For continuous control or resource allocation problems (e.g., pricing, portfolio optimization), the framework does not directly apply.

**Recommended fix:** Acknowledge this limitation explicitly and suggest potential extensions (e.g., discretization, kernel-based approaches). The current Conclusion only mentions the linear utility assumption as a limitation.

### Page Coverage Audit

| Page | Annotation Count | Coverage Status | Skip Reason |
|------|-----------------|-----------------|-------------|
| 1 (Title+Abstract+Introduction+Method+Experiments+Conclusion) | 17 | Covered (all substantive paragraphs) | N/A |
| Appendix (lines 158-159 only: references stub + "rest removed") | 0 | Skipped | Appendix text not available in the provided extraction |

All substantive paragraphs in Abstract, Introduction, Method (Sections 2-4), Experiments (Section 5), and Conclusion (Section 6) have at least one annotation. The only skipped content is the references stub and appendix notice which are non-substantive due to truncation.

## Score
**Final Score: 7/10**

**Rationale:** The paper makes a genuine theoretical contribution at the intersection of calibration and decision theory. The core insight—that decision calibration (a weak, tractable condition) suffices to recover plug-in best-response optimality, collapsing what could be a hierarchy of robust policies—is novel and well-supported by theoretical analysis. The ℋ-calibration framework and duality-based characterization (Theorem 3.1) provide a principled foundation for future work.

However, the score is tempered by several factors:
- **Experimental validation is thin (W1):** No variance reporting, only two datasets, no multiclass experiments, and limited baselines. This prevents strong empirical conclusions.
- **Scope limitations (W2, W7):** The linear utility assumption and finite action set requirement bound practical applicability. The paper's motivation (high-stakes decision-making) partially conflicts with these restrictions.
- **Technical rigor gaps (W3, W4):** The saddle-point existence justification could be more explicit, and the self-orthogonality claim needs a finite-sample caveat.
- **Novelty verification is deferred** (Retrieval-Disabled Mode): External literature comparison was not possible in this run; novelty claims should be manually verified before acceptance.

The theoretical contribution is solid and publishable, but strengthening the empirical evaluation and clarifying limitations would significantly improve the paper's impact and reproducibility.
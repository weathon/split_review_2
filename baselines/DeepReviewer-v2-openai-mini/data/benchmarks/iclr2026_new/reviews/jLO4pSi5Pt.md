## Summary
# Final Review Report

## Summary

This paper addresses Test-Time Adaptation (TTA) for Vision-Language Models (VLMs) under long-tailed test distributions — a practically relevant but previously underexplored problem. The authors propose L-TTA, a three-component framework: (1) Synergistic Prototypes (SyPs) with Deterministic and Exclusionary prototypes to enrich tail-class representations, (2) Rebalancing Shortcuts (RSs) with a class re-allocation loss for dynamic class balancing, and (3) Balanced Entropy Minimization (BEM) as a variant of entropy minimization with a penalty term that down-weights confident head classes. Experiments across three benchmarks (OOD, Cross-Domain, Corruption) totaling 15 datasets under imbalance ratios 10–50 show consistent improvements in both accuracy and macro-F1 over 12 baselines.

**Strengths:** The paper identifies a genuine gap in the VLM TTA literature (long-tailed test sets), proposes a thoughtfully designed multi-component method with theoretical motivation, and provides extensive empirical evaluation across diverse datasets and imbalance settings. The idea of using exclusionary prototypes to capture inter-class correlations and the BEM formulation with a confidence-based penalty term are interesting conceptual contributions.

**Weaknesses:** Several issues reduce confidence in the claims: (1) The "first" novelty claims cannot be verified without literature access (deferred in this run). (2) The hyperparameter $K$ has an unresolved inconsistency between the implementation ($K=0.3$) and ablation ($K=0.2$ optimal). (3) No statistical significance or variance is reported for any result, making the modest 1–2% gains hard to interpret. (4) The BEM formulation has an undefined symbol ($\tilde{\mathbb{P}}$) and propositions are deferred to the appendix without proof sketches. (5) The dataset construction method has a ceiling effect that may distort effective imbalance ratios. (6) The CRA loss equation (Eq. 7) has a parentheses matching error that affects implementation clarity.

**Score:** 6/10. The paper addresses a relevant problem with reasonable methodology, but the experimental reporting (missing variance, hyperparameter inconsistency) and theoretical presentation gaps prevent a higher score. The core ideas have potential, but significant revisions are needed before acceptance.

*External literature verification was unavailable in this run; novelty and comparative positioning conclusions are deferred to manual verification.*

## Strengths
1. **Problem relevance and timely formulation.** The paper identifies a realistic and previously overlooked scenario: TTA for VLMs under long-tailed test distributions. While standard TTA assumes balanced test streams, real-world deployment often exhibits severe class imbalance. The two identified failure modes (text-induced tail erosion and modality-bias amplification) are well-motivated and specific to the VLM + long-tail intersection.

2. **Well-structured method design with conceptual clarity.** L-TTA decomposes the long-tail TTA challenge into three complementary components (prototype enrichment, learnable rebalancing, balanced entropy minimization), each with a clear motivation and intuitive explanation. The use of Exclusionary Prototypes — updating all class prototypes from every sample's prediction distribution — is a novel extension of the prototype-caching idea from TDA and DPE, with a principled mechanism for capturing inter-class correlations.

3. **Extensive and diverse experimental evaluation.** The paper evaluates on 15 datasets spanning three benchmark types (OOD variants, cross-domain fine-grained, corruption), across three imbalance ratios (10, 20, 50), with 12 competitive baselines including both training-free and training-based methods. This is a thorough evaluation that goes beyond typical VLM TTA papers, which usually evaluate on balanced or mildly shifted distributions.

4. **Computational efficiency consideration.** Unlike many TTA methods that require backpropagation through the full visual encoder (e.g., RLCF, WATT), L-TTA updates prototypes in parallel and optimizes shortcuts without gradient tracking through the backbone. The reported 1.45h runtime and 1.89 GB memory on ImageNet represent a practical advantage for deployment.

5. **Theoretical grounding effort.** The paper provides two propositions that formally characterize the head-tail gradient imbalance in standard EM and the gap-reduction effect of BEM. While the proofs are deferred to the appendix, the attempt to theoretically justify the loss design is commendable and rare in the VLM TTA literature.

## Weaknesses
### W1. Hyperparameter inconsistency between implementation and ablation (Major)

The Implementation Details section (Page 6 - Implementation Details) explicitly states "$K = 0.3$" as a default hyperparameter. However, the ablation study "Vector number $K$ in RS" (Page 9) concludes: "Our experiment results show that setting $K = 0.2$ yields the best performance." This is a direct numerical contradiction. If $K=0.2$ is optimal, the main results (Tables 1-3) were produced with a suboptimal value, meaning the reported performance may not represent the method's full potential. Conversely, if $K=0.3$ was actually used, the ablation conclusion is misleading. This inconsistency must be resolved before the paper can be considered publication-ready.

### W2. Missing statistical significance and variance reporting (Major)

All main results (Tables 1-5) report only point estimates (accuracy and macro-F1) without standard deviations, confidence intervals, or statistical significance tests. The paper mentions "5 runs" (Table 1 caption) but does not present the variance across these runs. Given that many improvements are modest (e.g., L-TTA: 65.97 vs DPE: 64.50 on OOD average at imb=10 — a 1.47% gain), readers cannot assess whether these differences are statistically reliable or within the noise range of random seed variation. This is a critical omission for an empirical paper making "superior performance" claims. Standard practice in the TTA literature includes reporting mean±std over multiple seeds.

### W3. BEM formulation has undefined symbols and incomplete theoretical presentation (Major)

The BEM loss in Eq. (9) (Page 5) uses the symbol $\tilde{\mathbb{P}}$ without prior definition. It appears to denote the model's softmax output $\sigma(z)$, but this is not explicitly stated. The equation $\mathcal{L}_{\text{BEM}} = \mathbb{H}'(\tilde{\mathbb{P}})$ is circular — $\mathbb{H}'$ is defined in terms of $z'$, which depends on $\tilde{\mathbb{P}}$, but $\mathbb{H}'$ is never independently defined. Propositions 1 and 2, which are central to justifying BEM, have full proofs deferred to Appendix A with no sketch in the main text. For a paper that claims "theoretical capabilities," the main text should include at least a proof outline or the key insight.

### W4. Novelty claims are not verifiable (Major — partially excused by Retrieval-Disabled Mode)

The abstract (Page 1) asserts "As the first attempt to solve this problem" and contribution ➊ states "We first study the Test-Time Adaptation under long-tailed scenarios." These are strong novelty claims that cannot be verified without external literature access (unavailable in this run). Given that TTA under non-i.i.d. settings has been studied (e.g., LAME, SAR, DELTA — all cited by the paper itself under Section 2.1), and that long-tailed learning is a well-established field, the novelty claim should be scoped to "to our knowledge, the first VLM-specific TTA method that explicitly handles long-tailed test distributions."

### W5. Dataset construction ceiling effect (Major)

The dataset construction procedure (Page 6 - Datasets) states: "if the calculated cardinality is less than the class cardinality itself, we simply keep that class unchanged." For fine-grained datasets like Aircraft or DTD, where many classes naturally have very few samples, this means the actual imbalance ratio after construction may be far lower than the stated imb=10/20/50. The paper does not report the achieved imbalance ratio per dataset, making cross-dataset comparisons of "robustness to imbalance" imprecise. A method could appear robust to imb=50 on Aircraft while effectively facing imb<10.

### W6. CRA loss equation has syntax error (Major)

Equation (7) (Page 4 - Rebalancing Shortcuts) has mismatched parentheses: the expression mixes `avg_c(...)` with `avg_c(...` without proper closure, and the `+` operator is ambiguously scoped. The closing `))` at the end is syntactically inconsistent with the opening parentheses. This is not a typesetting nit — the algebraic ambiguity prevents correct implementation from the paper alone. The corrected form should use explicit bracket scoping: `\mathcal{L}_{CRA} = \sum_j [ avg_c(c_{c,j}(v)) * avg_c(Attn([v_c, t_c], q_j)) + avg_c(c_{c,j}(u)) * avg_c(Attn([u_c, t_c], q_j)) ]`.

### W7. Normalization notation issues in prototype update equations (Major)

Equation (4) (Page 4 - Synergistic Prototypes) has ambiguous norm notation: `\|N_{c^*,s}^{DP} - 1\|\mathbf{v}_{c^*} + \tilde{\mathbf{v}}_{c^*}\|`. The norm `\|\cdot\|` is applied to a scalar `(N-1)` in the first instance, which is meaningless, and the denominator appears to intend `\|(N-1)\mathbf{v}_{c^*} + \tilde{\mathbf{v}}_{c^*}\|` but is missing proper parentheses. Same issue in Eq. (5). This directly affects reproducibility.

### W8. Failure mode claims lack quantitative support (Moderate)

The two failure modes — text-induced tail erosion and modality-bias amplification — are introduced in the Introduction (Page 1) as central motivations for L-TTA, but no quantitative diagnostic experiment is presented to verify their existence or magnitude. The claim about SAR on VLM backbones (Figure 1(b.2)) is mentioned but the figure is not a quantitative plot accessible in the text. Without evidence that these failure modes actually occur under the evaluated settings, the motivation for the entire method is weakened.

### W9. Missing limitations discussion (Moderate)

The Conclusion (Page 9) does not discuss any limitations of L-TTA. Important limitations include: (i) sensitivity to the entropy threshold $\theta$ for DP updates; (ii) reliance on accurate class-prior estimation via pseudo-labels, which may be unreliable in non-stationary streams; (iii) reduced effectiveness on fine-grained datasets where visual differences between classes are subtle; (iv) the assumption that class priors can be estimated from test-stream statistics, which may not hold under severe distribution shift. A paper claiming a new problem formulation should include a candid discussion of when the method fails.

### W10. Conclusion is too brief and boilerplate (Minor)

The Conclusion (Page 9) largely restates the contribution list without synthesizing what was learned about long-tailed TTA beyond method components. It does not discuss broader implications, failure cases, or prioritized future work.

### W11. Efficiency comparison uses non-standard HM metric (Minor)

The efficiency study (Table 4, Page 8) uses the harmonic mean of accuracy and macro-F1 as a composite metric. This is not standard practice — accuracy and macro-F1 measure different properties (overall correctness vs. class balance) and are on different scales, making their harmonic mean uninterpretable. Standard practice would be to report both metrics separately with error bars.

### W12. Contribution listing mixes claim types (Minor)

The three contribution bullets (Page 2) conflate problem identification (➊), method design (➋), and empirical results (➌). Performance claims ("surpasses existing methods") belong in the abstract/results, not in contribution statements. Contribution statements should focus on what is conceptually new.

### Page Coverage Audit

Since the PDF extraction maps all content to a single page, the per-page annotation audit is:
- Page 1 (entire paper): 12 annotations across Abstract (1), Introduction paragraphs (3), Related Work (implicitly covered in contribution annotation), Method: SyPs (1), Method: RSs/CRA (1), Method: BEM (1), Experiments: Implementation Details (1), Experiments: Results (2), Experiments: Efficiency (1), Conclusion (1).
- All substantive paragraphs are covered. No appendix pages are present in the extracted content.

## Score
**Final Score: 6/10**

**Scoring rationale:** This score weighs research value (the paper identifies a relevant and timely problem) against validity and reporting concerns. The core ideas (dual prototypes, rebalancing shortcuts, balanced entropy minimization) are thoughtful and the empirical scope is commendable. However, the unresolved hyperparameter inconsistency (K=0.3 vs K=0.2), missing statistical significance throughout all experiments, undefined notation in the key loss equation, and pending novelty verification significantly reduce confidence in the quantitative claims. The paper requires at least one major revision cycle addressing the W1-W7 issues before it can be considered for acceptance.

**Post-Revision Target:** [7, 8]/10 — achievable if the hyperparameter inconsistency is resolved, variance reporting is added, notation is clarified, and claims are appropriately bounded.
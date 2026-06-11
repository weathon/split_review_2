## Summary
# Final Review Report

## Summary

This paper addresses the out-of-distribution generalization problem in Supervised Causal Learning (SCL). The authors identify three limitations of static SCL pre-training: fragility to distribution shifts, failure in compositional generalization, and a performance gap between synthetic benchmarks and real-world data. They propose a Test-Time Training framework (TTT-SCL) that dynamically generates training data aligned with each test instance, operationalized via an Alignment of Distribution (AD) metric (average log-likelihood under a candidate graph) combined with an L0 sparsity constraint to enforce causal minimality. The concrete instantiation, TACTIC, performs stochastic graph refinement via Metropolis-Hastings-style search guided by the AD-sparsity score, then trains an SCL model on the generated data to infer the test graph.

**Strengths:** (1) The paper identifies a genuine problem — static pre-training in SCL fails under distribution shifts — and provides systematic empirical evidence for it. (2) The idea of dynamically generating training data at test time is novel in the SCL context and addresses a real need. (3) The stage-wise analysis (seed → highest-score graph → final SCL output) effectively demonstrates the value of the two-phase approach. (4) Results on the real-world Sachs and Syntren datasets show meaningful improvements over baselines in distribution-shift scenarios.

**Weaknesses:** (1) The AD metric definition is underspecified (no noise distribution assumption stated). (2) The transition probability for stochastic refinement uses a ratio of scores that can be negative, which is mathematically ill-defined as formulated. (3) The "state-of-the-art" claim is not statistically supported for several datasets where variance overlaps with baselines. (4) Conclusion claims "theoretical results" when no theorems or formal proofs are presented. (5) The evidence base for the synthetic-to-real gap claim (Issue 3) rests on only two datasets and one SCL backbone, insufficient for the sweeping conclusions drawn. (6) Contribution list inflates problem diagnosis as a contribution. (7) Several "first"/"paradigm-shifting" claims are unsupported without external literature verification. (8) The "convex hull of training mechanisms" argument is intuitively appealing but lacks formal definition.

**Score:** 6/10

The paper has a promising core idea and produces compelling results on challenging real-world scenarios. However, the mathematical formulation of the search procedure contains a critical error (score ratio as acceptance probability), several claims exceed what the evidence supports, and key definitions lack specificity. These issues are fixable but require careful revision.

```text
ASCII Diagram — Paper Structure & Evidence Map

[Problem: SCL fails under distribution shifts]
    |
    ├── [C1: Identify limitations (Issue 1-3)]
    |       Evidence: Fig 2 (distribution shifts), Table 1 (synthetic-to-real gap)
    |       Gap: Only 2 real-world datasets, 1 backbone → thin evidence for sweeping claims
    |
    ├── [C2: TTT-SCL framework + AD metric]
    |       Evidence: Eq (3) likelihood-based AD, Eq (4) sparsity, Eq (5) joint score
    |       Gap: AD metric underspecified (no explicit noise distribution)
    |
    └── [C3: TACTIC algorithm]
            Evidence: Table 2 (performance), Table 3 (ablation), Table 4 (stage-wise)
            Gap: Transition probability α = min[1, score(G_k+1)/score(G_k)] mathematically invalid
```

## Strengths
**S1. Well-motivated problem identification.** The paper systematically demonstrates three genuine limitations of static SCL pre-training (distribution shift sensitivity, compositional generalization failure, and synthetic-to-real transfer gap) through controlled experiments. This problem diagnosis is clearly articulated and provides strong motivation for the proposed solution.

**S2. Novel conceptual contribution.** The core idea — dynamically generating training data at test time for SCL — is a meaningful departure from the dominant static pre-training paradigm. While test-time adaptation has been explored in other ML domains, its application to supervised causal discovery is genuinely new and well-justified by the identified limitations of static approaches.

**S3. Two-stage analysis clarifies the value add.** The stage-wise breakdown (Page 8 - Ablation Study, Table 4) comparing seed graph → highest-score graph → final SCL prediction is particularly effective. It convincingly demonstrates that both the search refinement and the supervised learning phase contribute to performance gains, and clearly distinguishes TACTIC from classical score-based methods.

**S4. Strong practical results on distribution-shift scenarios.** The most compelling empirical contribution is on the Sachs real-world dataset, where TACTIC (Notears) achieves 78.9 AUROC versus 67.1 for the next-best method (PC). The Syntren results show a similar pattern (80.1 vs 65.4). These are practically meaningful improvements on the scenarios where static pre-training most clearly fails, directly supporting the paper's central thesis.

**S5. Ablation study validates design choices.** The sparsity ablation (Table 3) shows consistent degradation when the sparsity penalty is removed (λ=0), supporting the claim that both AD and sparsity are necessary. The comparison between TACTIC (random) and TACTIC (Notears) also provides useful insight into the role of initialization quality.

**S6. Clear writing and structure.** The paper is generally well-organized with clear transitions between motivation, problem diagnosis, proposed framework, instantiation, and empirical validation. The figures (especially the paradigm comparison in Figure 1 and the TACTIC workflow in Figure 3) are helpful for understanding the approach.

```text
ASCII Diagram — Related-Work Taxonomy Tree (Layered)

Causal Discovery Methods (Root)
├── Branch 1: Unsupervised (traditional)
│   ├── Leaf 1.1: Constraint-based (PC, FCI)
│   ├── Leaf 1.2: Function-based (LiNGAM, ANM)
│   └── Leaf 1.3: Score-based (GES, NOTEARS, DAG-GNN, GraN-DAG)
│
├── Branch 2: Supervised Causal Learning (SCL)
│   ├── Leaf 2.1: Model architecture focus
│   │   ├── Cascade classifiers (Ma et al., 2022)
│   │   ├── Unshielded triple classifiers (Dai et al., 2023)
│   │   ├── Attention-based transformers (Lorch et al., 2022; Ke et al., 2022; Froehlich & Koeppel, 2024)
│   │   └── Pairwise attention (Zhang et al., 2025)
│   ├── Leaf 2.2: Output representation focus
│   │   ├── Skeleton only (Ma et al., 2022)
│   │   ├── Local structure orientation (Dai et al., 2023)
│   │   ├── Full adjacency matrix (Lorch et al., 2022; Ke et al., 2022)
│   │   └── Markov equivalence class (Zhang et al., 2025; Froehlich & Koeppel, 2024)
│   └── Leaf 2.3: Training strategy
│       ├── Static pre-training with diversity (Montagna et al., 2024)
│       └── Test-time dynamic training [THIS PAPER — TTT-SCL / TACTIC]
│
└── Branch 3: Test-Time Adaptation (general ML)
    ├── Test-time training (Sun et al., 2020; Liang et al., 2025)
    └── Test-time adaptation (Wang et al., 2020; Liu et al., 2021; Sinha et al., 2023)
    
[Note: Novelty verification deferred — external paper search unavailable in this run.]
```

## Weaknesses
### W1. [Critical] Transition probability in TACTIC is mathematically ill-defined (Page 6 - Section 4.2)

**Anchor:** Figure 3 and line 99 describe the acceptance probability as α = min[1, score(G_{k+1}) / score(G_k)], where score(G) = AD(G, D_test) - λ·Sparsity(G). Since AD is an average log-likelihood that can take negative values, the score can be negative, making the ratio ill-defined as an acceptance probability.

**Impact:** An invalid stochastic search procedure would compromise the entire TACTIC optimization. If scores are negative, the ratio could be misleading (e.g., -5/-1 = 5 leads to α = 1, incorrectly encouraging a worse graph). This is a mathematical error in the algorithm specification.

**Fix:** Replace with a Metropolis-Hastings criterion: α = min[1, exp(score(G_{k+1}) - score(G_k))], treating score(G) as a log-posterior (up to normalization). Alternatively, define P(G) ∝ exp(score(G)/τ) and use standard MH acceptance. This modification is straightforward and preserves the intended behavior.

**Severity:** Critical (threatens algorithmic correctness).

### W2. [Major] AD metric is underspecified (Page 5-6 - Section 4.1)

**Anchor:** Eq (3) defines AD(G) = (1/d) Σ log p(X_i | f_i^k). The term "p(X_i | f_i^k)" is not well-defined — f_i^k is described as a "fitting function," not a probabilistic model. Likelihood requires specifying a noise distribution (e.g., Gaussian). The regression procedure for estimating f_i^k from D_test is also not described.

**Impact:** The core optimization target cannot be independently implemented, harming reproducibility. The noise distribution choice directly affects the AD values and thus the graph search outcome.

**Fix:** Provide an explicit definition: assuming additive Gaussian noise, AD = -(1/(2d)) Σ_i ((X_i - f_i^k(Pa(X_i)))^2 / σ_i^2 + log(2πσ_i^2)). Describe how f_i^k is estimated (e.g., which regression method, regularization) and how σ_i^2 is obtained (e.g., from residual variance).

### W3. [Major] Insufficient evidence for the synthetic-to-real gap claim (Page 4 - Issue 3, Table 1)

**Anchor:** The claim that "strong synthetic performance fails to guarantee effectiveness on real-world data" is supported by only two datasets (Sachs, Syntren) and one SCL backbone (AVICI scm-v0). Syntren is itself a pseudo-real synthetic generator, not truly real-world data.

**Impact:** The paper's central motivation — questioning the "practical utility of existing SCL approaches" — rests heavily on this claim. If the evidence is insufficient, the motivation for TTT-SCL is weakened. A reviewer may argue that two datasets do not justify abandoning the static pre-training paradigm.

**Fix:** (a) Add more real-world datasets (e.g., from the bnlearn repository mentioned in Appendix G). (b) Test additional SCL backbones beyond AVICI in the main text (currently only in appendix). (c) Acknowledge the preliminary nature of the evidence and bound claims accordingly.

### W4. [Major] State-of-the-art claims not statistically supported (Page 7 - Section 4.3)

**Anchor:** The paper claims "TACTIC achieves state-of-the-art performance on all other datasets, including Linear_U, Chebyshev_G, Sachs, and Syntren." However, on Linear_U, standard deviations overlap substantially across methods (TACTIC: 86.3±4.4 vs NOTEARS: 82.0±4.6 vs AVICI: 75.6±13.8). On Chebyshev_G, TACTIC is 83.0±8.7 vs AVICI 81.7±10.5 — well within one standard deviation. No statistical significance tests are reported.

**Impact:** Overclaimed results invite reviewer skepticism and may reduce overall credibility even for the genuinely strong results (e.g., on Sachs and Syntren).

**Fix:** (a) Replace "state-of-the-art" with "competitive or superior" for cases with overlapping variance. (b) Report the number of independent trials used for variance estimation. (c) Add statistical significance assessment (paired bootstrap or permutation test) for the key comparisons.

### W5. [Major] Conclusion claims "theoretical results" without any theory (Page 9 - Conclusion)

**Anchor:** The conclusion states "Our theoretical and empirical results underscore the effectiveness of AD and necessity of sparsity." The paper contains no theorems, lemmas, proofs, or formal theoretical analysis. The "theoretical results" claim is unsupported.

**Impact:** This can be perceived as misleading, damaging scientific integrity. Reviewers will notice the absence of theoretical content.

**Fix:** Replace "theoretical and empirical results" with "empirical results" or "experimental findings."

### W6. [Major] Contribution list inflates problem diagnosis as a contribution (Page 1 - Contribution list)

**Anchor:** The first listed contribution is "We reveal three fundamental limitations of static SCL pre-training." This is a critique of existing work, not a technical contribution. The actual technical contributions are the TTT-SCL framework, AD metric, sparsity constraint, and TACTIC algorithm.

**Impact:** Inflating contribution count reduces the perceived rigor of the paper. Standard research contributions should be methodological or theoretical innovations, not problem statements.

**Fix:** Remove the first bullet from the contribution list or rephrase it as context. Consolidate contributions around the methodological innovations.

### W7. [Major] Unsupported novelty claims due to retrieval limitations (Pages 1, 9 - Introduction, Related Work)

**Anchor:** The paper describes TTT-SCL as "the first framework to introduce test-time training to supervised causal learning" and "pioneers its application to causal discovery." These claims cannot be verified without external literature search, which was unavailable in this run.

**Impact:** If prior work exists applying test-time training/adaptation to causal discovery, these claims would need retraction. This is a factual-verification risk.

**Fix:** Add "to the best of our knowledge" qualifiers before publication. Conduct a thorough literature review to substantiate or adjust these claims.

### W8. [Moderate] AD metric's circularity risk (Page 5 - Section 4.1)

**Anchor:** The AD metric uses SIM (Structure-Induced Mechanism) to regress mechanisms from D_test given candidate graph G. This requires estimating f_i^k from the same test data that is used for evaluation. There is an implicit risk of overfitting: a complex graph with many parameters can achieve high likelihood on D_test without capturing true causal structure.

**Impact:** While the sparsity constraint (W1 addresses this partially), the sparsity penalty is only one defense. The paper does not discuss or test against the possibility that the AD metric favors overly complex models that overfit D_test.

**Fix:** Add a discussion of the overfitting risk and ideally provide an empirical check (e.g., compare AD vs held-out likelihood, or test whether models selected by AD + sparsity generalize to similar-distribution held-out data).

### W9. [Moderate] Missing hyperparameter sensitivity analysis (Page 7-8 - TACTIC)

**Anchor:** The TACTIC algorithm depends on several critical hyperparameters: λ (sparsity weight), K (number of training graphs, set to 200), the number of refinement iterations, and the acceptance temperature (implied but not specified). None of these are analyzed for sensitivity.

**Impact:** Without understanding how λ or K affect results, readers cannot assess the reproducibility or robustness of the method.

**Fix:** Add a sensitivity analysis for λ and K in the appendix. Report the number of refinement iterations and acceptance criteria explicitly.

### W10. [Minor] "Convex hull of mechanisms" is an intuitive but unformalized argument (Page 3 - Section 3)

**Anchor:** The paper states "When test mechanisms fall outside the convex hull of training mechanisms, structural diversity alone cannot guarantee accurate estimation." The "convex hull of training mechanisms" in function space is never formally defined.

**Impact:** A mathematically-oriented reviewer may question the rigor of this central motivational claim.

**Fix:** Either provide a formal definition (e.g., in terms of reproducing kernel Hilbert space or function class inclusion) or replace with a more empirically grounded statement about limited representation.

```text
ASCII Diagram — Revision Strategy Roadmap

Priority | Issue | Fix | Expected Gain
P0 (Must) | W1: Invalid transition probability | Replace ratio with exp(MH) α | Algorithm correctness
P0 (Must) | W2: AD metric underspecified | Add explicit likelihood + noise assumption | Reproducibility
P0 (Must) | W5: False "theoretical results" | Replace with "empirical results" | Scientific integrity
P1 (Must) | W4: SOTA claim overreach | Bound claim, add significance tests | Claim credibility
P1 (Must) | W6: Inflated contribution list | Remove critique-as-contribution | Paper rigor
P1 (Must) | W3: Thin synthetic-to-real evidence | Add datasets, bound conclusions | Motivation strength
P2 (Nice) | W7: Unsupported "first" claims | Add qualifiers, verify literature | Novelty defensibility
P2 (Nice) | W8-W9: Sensitivity + overfitting | Add experiments + discussion | Robustness evidence
P2 (Nice) | W10: Formalize convex hull claim | Replace with precise statement | Theoretical clarity
```

## Score
**Final Score: 6/10**

The score reflects the following evidence-grounded assessment:

**Novelty (7/10):** The core idea of test-time training for supervised causal learning is genuinely novel and well-motivated. The TTT-SCL framework and TACTIC instantiation represent a meaningful departure from the dominant static pre-training paradigm. However, the novelty claims require external literature verification (deferred in this run), and some components (likelihood-based scoring, sparsity regularization) are individually standard techniques applied in a novel combination.

**Research Value (6/10):** The paper identifies a real problem (SCL's OOD generalization failure) and proposes a reasonable solution. The results on real-world datasets (Sachs, Syntren) are practically meaningful. However, the empirical scope is limited (few datasets, one main backbone), several claims exceed what the evidence supports, and the core algorithm contains a mathematical error (transition probability) that must be fixed before the approach can be reliably evaluated.

**Validity/Soundness (5/10):** The main threat to validity is the mathematically ill-defined acceptance probability (W1), which requires correction. Additional concerns include the underspecified AD metric (W2), unsupported SOTA claims (W4), and thin evidence for the synthetic-to-real gap (W3). These are fixable but currently reduce confidence.

**Reproducibility (5/10):** Key details are missing: noise distribution assumption for AD, regression method for f_i^k, hyperparameter settings (λ, number of iterations, temperature). The acceptance probability ambiguity compounds the reproducibility concern.

**Overall:** The paper presents a promising direction with strong conceptual merit, but the mathematical formulation and claim calibration need significant revision. The critical issue (W1) and several major issues (W2, W4, W5) are fixable with concrete, targeted revisions. A revised version addressing these concerns could realistically score 7-8/10.

**Note on Retrieval-Disabled Mode:** External literature search was not available in this run. Novelty/comparison conclusions regarding "first," "pioneering," and "state-of-the-art" claims are marked as deferred manual verification and are not factored into the novelty score above beyond what manuscript-internal evidence supports.
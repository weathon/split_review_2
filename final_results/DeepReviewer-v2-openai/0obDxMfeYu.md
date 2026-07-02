## Summary
# Final Review Report

## Summary

This paper introduces Medix, a median-centric framework for out-of-distribution (OOD) detection that leverages unlabeled "in-the-wild" data. The method consists of two stages: (1) a greedy filtering algorithm that uses element-wise median (EWM) of gradient deviations to identify candidate OOD samples from a mixed InD/OOD wild set, and (2) training a binary OOD detector on the identified outliers together with labeled InD data. The paper provides theoretical bounds on both the inlier misclassification rate (Theorem 4.1) and the outlier misclassification rate (Theorem 4.2) for the median filtering stage, controlled by contamination, concentration, and separation effects. Empirical evaluation on CIFAR-10 and CIFAR-100 as InD datasets with five OOD test sets shows competitive FPR95 and AUROC against 20 baselines.

**Strengths**: The median-based outlier filtering mechanism is intuitively clean and theoretically motivated. The two-sided misclassification bounds (controlling both false positives and false negatives) are a meaningful theoretical contribution for the wild-data setting. The empirical results demonstrate consistent improvements over the wild-data-based WOODS baseline.

**Weaknesses**: The algorithm description contains a critical loop-condition bug (or vs. and in Algorithm 1). The computational complexity of the leave-one-out greedy scheme is not analyzed or justified in the main text. The synthetic validation experiment uses unrealistically easy separation (40 standard deviations). The comparison with InD-only baselines is confounded by unequal labeled data quantities (25K vs 50K). Several strong SOTA claims (DRL, CONJ superiority) are made without corresponding main-text results tables. Novelty relative to the closely related Du et al. (2024a) framework requires sharper differentiation.

## Strengths
1. **Clean algorithmic intuition.** The core idea of using the element-wise median of gradients to distinguish InD from OOD samples is refreshingly simple and well-motivated. The preliminary experiment (Figure 1) showing monotonic deviation as OOD samples are added provides intuitive grounding for the approach, and the connection to median robustness against outliers is conceptually sound.

2. **Two-sided theoretical guarantees.** Unlike many OOD detection papers that focus solely on empirical performance, the paper provides formal bounds on both the inlier misclassification rate (Theorem 4.1) and the outlier misclassification rate (Theorem 4.2). The decomposition into contamination, concentration, and separation effects gives interpretable guidance on when the filtering will succeed (π < 0.5, well-separated gradient distributions). The acknowledgment that median-based bounds can be derived under only bounded second moments (Theorem C.3) adds robustness to the theoretical claims.

3. **Competitive empirical results.** On CIFAR-10 as InD, Medix achieves an average FPR95 of 0.80% with standard deviations under 0.1% on most datasets, substantially outperforming the WOODS baseline (3.40%). On CIFAR-100, Medix achieves 5.42% average FPR95 vs. WOODS's 6.74% — a consistent if modest improvement. The 5-run variance reporting is appropriate and helps assess statistical reliability.

4. **Reasonable baseline coverage.** The paper compares against 20 baselines spanning multiple OOD detection paradigms (confidence-based, distance-based, energy-based, contrastive, and wild-data regularization methods). This breadth helps position the method within the broader OOD detection landscape.

5. **Transparency about the second stage.** The paper explicitly acknowledges that the OOD detector training stage follows the protocol of Du et al. (2024a), which clearly delineates the novel contribution (filtering stage) from the inherited component. This intellectual honesty is commendable and helps reviewers focus on what is genuinely new.

## Weaknesses
### W1. Algorithm 1 loop condition bug (major)

The while-loop condition in Algorithm 1 (Page 4) uses `t ≤ T or |δ_max| > ε`. With the `or` operator, the loop will continue as long as EITHER (a) t ≤ T OR (b) |δ_max| > ε. Since t ≤ T is always true until the max iteration count is exceeded, the convergence check (`|δ_max| > ε`) can never trigger early termination. This means the algorithm always runs for exactly T iterations regardless of convergence, contradicting the described convergence criterion. This bug directly impacts reproducibility — different implementers may interpret the intended behavior differently, with some using `and` (as would be typical) and others faithfully reproducing the `or` logic.

**Severity**: Major | **Fix**: Change `or` to `and` in line 2 of Algorithm 1.

### W2. Unrealistic synthetic validation (major)

The synthetic experiment (Section 5.3, Page 7) claims a 12.5% error rate (87.5% OOD detection) but uses OOD data with mean [20, 2√3] while the nearest InD cluster has mean [0, 2√3] — a separation of 20 units with covariance 0.25·I (standard deviation 0.5), yielding a Mahalanobis distance of ~40 standard deviations. This is an unrealistically easy separation that provides no meaningful evidence about real-world OOD detection difficulty. The paper cites this result to "corroborate theoretical findings," but the gap between this toy setting and realistic OOD scenarios is too large to justify such claims.

**Severity**: Major | **Fix**: Add a second synthetic experiment with challenging separation (Δ=2-3 standard deviations), and report detection rate as a function of separation distance.

### W3. Confounded comparison with InD-only baselines (major)

The experimental design uses 25,000 labeled InD samples for Medix's classifier training while InD-only baselines use the full 50,000 samples (Section 5.2, Page 6). The paper acknowledges this as a "slight difference," but it creates a systematic confound: the claimed superiority of wild-data methods over InD-only methods partially reflects different training set sizes, not just the benefit of wild data. The InD classifier's lower accuracy (73.33% vs. 75.96% for CIFAR-100) affects the quality of gradient features used in the filtering stage, potentially making the comparison unfair.

**Severity**: Major | **Fix**: Add a matched comparison where both Medix and InD-only baselines are trained on 25K labeled samples, or alternatively, retrain Medix with the full 50K InD samples for the InD classifier (with a different wild set construction).

### W4. Missing results for claimed baselines (major)

Contribution C3 (Page 1) and the Conclusion (Page 8) claim superiority over "20 competitive baselines" including DRL and CONJ, yet these methods do not appear in the main results tables (Tables 1, 2). The baselines section (5.1) lists them, but the reader cannot verify their performance from the main paper. This creates an unverifiable superiority claim. References to the appendix are insufficient for a claimed contribution-level result.

**Severity**: Major | **Fix**: Add DRL and CONJ rows to the main result tables, or remove these claims from the main text and conclusion.

### W5. Computational complexity not addressed (major)

Algorithm 1's greedy leave-one-out procedure requires, per iteration, evaluating the EWM after removing each sample individually. For a wild set of ~25,000 samples and dimension d (penultimate layer size, potentially thousands), the naive implementation is O(T·|S|²·d). The paper defers efficiency analysis to Appendix A.6 (not available in the reviewed manuscript), and the main text provides no complexity analysis or runtime reporting. Without evidence that the method scales, the claimed practical applicability is unsubstantiated.

**Severity**: Major | **Fix**: Report per-iteration and total runtime for the main experiments in the main paper, describe any incremental update strategies used, and provide worst-case complexity analysis.

### W6. Surrogate loss function unspecified (major)

Equation (5) defines the OOD detector loss using 0/1 indicator functions, but the actual differentiable surrogate (described only textually as "binary loss based on a differentiable sigmoid function") is never written explicitly. The choice of sigmoid temperature, whether the loss is averaged or summed, and how it is combined with the InD classification loss (weight λ=10) are critical for reproducibility but are only partially specified.

**Severity**: Major | **Fix**: Provide the explicit surrogate loss form, e.g., L_τ^+(g_θ) = E[σ(-g_θ(x)/τ)], and specify τ, the sigmoid temperature.

### W7. Closed-world OOD assumption limits open-world claims (major)

The wild data model (Eq. 1) and experimental protocol assume P_out^test = P_out (the OOD distribution in the wild set matches the test OOD distribution). While the paper acknowledges this in Appendix A.4, the main text's claims about "open-world" applicability overstate the setting. Real open-world deployment encounters OOD distributions that differ from the wild mixture, and the paper provides no theoretical guarantee for this mismatched scenario.

**Severity**: Major | **Fix**: Add explicit discussion of this limitation in the main text, and report the distribution-mismatch results from Appendix A.4 in a main-text figure.

### W8. Abstract and conclusion overclaim (minor-major)

The abstract claims Medix "outperforms existing methods across the board," and the introduction claims to be "one of the few studies" providing theoretical foundations for the wild-data setting. The former overstates the evidence (modest gains on 5 benchmarks do not constitute "across the board"), and the latter depends on the definition of "theoretical foundation" — Du et al. (2024a) already provides one. Both claims should be bounded.

**Severity**: Minor-Major | **Fix**: Replace "across the board" with "across five standard OOD benchmarks" and remove or contextualize the "one of the few" claim.

### W9. Related work is citation-list style (minor)

The related work section (Section 6) reads primarily as a chronological literature list with dense citation clusters rather than a comparative taxonomy. The most informative comparison — the differentiation between batch-level mixing (WOODS, Du et al.) and dataset-level mixing (Medix) — is buried mid-paragraph rather than highlighted as a key distinguishing axis.

**Severity**: Minor | **Fix**: Restructure into 3-4 thematic categories with explicit comparison tables or bullet-point distinctions.

### W10. Motivation experiment confound (minor)

The preliminary experiment (Figure 1) adds OOD samples to a growing wild set, but the deviation increase could partially reflect sample-size effects on the median rather than purely distributional shift. No control condition (adding additional InD samples instead of OOD samples) is reported.

**Severity**: Minor | **Fix**: Add a control experiment replacing OOD increments with InD increments to isolate the distribution-shift signal.

## Score
**Final Score: 5.5/10**

### Rationale

The paper presents a clean algorithmic idea (median-based gradient filtering) and provides two-sided theoretical misclassification bounds, which are rare in the OOD detection literature. The empirical results show consistent improvement over the most directly comparable wild-data method (WOODS), and the baseline coverage is broad.

However, the score is constrained by several validity-critical weaknesses: (1) the Algorithm 1 loop condition bug undermines reproducibility of the core procedure; (2) the synthetic validation uses unrealistically easy separation (40 stdevs) and does not provide meaningful evidence; (3) the comparison with InD-only baselines is confounded by unequal data quantities; (4) claimed superiority over DRL/CONJ cannot be verified from main-text tables; (5) computational complexity is unanalyzed in the main text; (6) the surrogate loss function is incompletely specified. These issues collectively reduce confidence in both the empirical claims and the reproducibility of the method. The theoretical analysis, while a strength, relies on sub-Gaussian assumptions whose empirical validation (Q-Q plot in Remark 4.3) is deferred to the appendix.

The paper's research value — a new median-centric perspective on OOD filtering with theoretical bounds — is genuine but incremental relative to Du et al. (2024a), which already provides theoretical foundations for the wild-data setting. The differentiation (median-based vs. threshold-based, dataset-level vs. batch-level mixing) is meaningful but not transformative.

### ASCII Diagrams

```text
ASCII Diagram — Paper Structure & Evidence Map

[Problem: OOD detection with unlabeled wild data]
    │
    ▼
[Proposed Solution: Medix median-based filtering]
    │
    ├── Stage 1: Gradient-based EWM outlier extraction (Algorithm 1)
    │       └── Evidence: Figure 1 (motivation experiment)
    │       └── Evidence: Theorem 4.1-4.2 (theoretical bounds)
    │       └── Evidence: Figure 2 (synthetic validation) [WEAK: unrealistic separation]
    │
    └── Stage 2: Binary OOD detector training (Eq. 5)
            └── Evidence: Tables 1, 2 (CIFAR-10/100 benchmarks)
            └── Evidence: Appendix A (ablations, efficiency, mismatched OOD)
    │
    ▼
[Core Claims]
    │
    ├── C1: Median-centric filtering framework
    │       └── Evidence: Algorithm 1 + Section 3.1 [BUG in loop condition]
    │
    ├── C2: Theoretical misclassification bounds
    │       └── Evidence: Theorems 4.1-4.2 [m_min undefined; assumptions stated]
    │
    └── C3: Superior empirical performance
            └── Evidence: Tables 1-2 [DRL/CONJ missing; confounded with data quantity]
```

```text
ASCII Diagram — Revision Strategy Roadmap

[W1: Algorithm loop bug] ──Fix `or`→`and`──► [Correct convergence behavior]
[W2: Synthetic validation] ──Add Δ-varying experiments──► [Meaningful synthetic evidence]
[W3: Confounded comparison] ──Add matched 25K baseline──► [Fair comparison]
[W4: Missing DRL/CONJ] ──Add to main tables──► [Verifiable SOTA claims]
[W5: No complexity analysis] ──Add runtime + O(·) analysis──► [Practicality evidence]
[W6: Surrogate loss unspecified] ──Write explicit sigmoid loss──► [Full reproducibility]
[W7: Closed-world OOD assumption] ──Add mismatch discussion──► [Honest scope bounding]
[W8: Overclaiming language] ──Bounded wording──► [Defensible manuscript]
[W9: Related work list-style] ──Restructure as taxonomy──► [Clearer positioning]
[W10: Motivation confound] ──Add control experiment──► [Cleaner evidence]
```

```text
ASCII Diagram — Related-Work Taxonomy Tree (Layered)

Related Work: OOD Detection with Unlabeled Data (Root)
│
├── Branch 1: Scoring-based detection (InD-only)
│   ├── Leaf 1.1: Confidence-based (MSP, ODIN)
│   ├── Leaf 1.2: Distance-based (Mahalanobis, KNN, KNN+)
│   ├── Leaf 1.3: Energy-based (Energy, ReAct, DICE, ASH)
│   └── Leaf 1.4: Contrastive (CSI)
│
├── Branch 2: Regularization-based detection (assumes clean auxiliary OOD)
│   ├── Leaf 2.1: Confidence reduction (OE)
│   └── Leaf 2.2: Energy regularization (Energy w/ OE)
│
├── Branch 3: Wild-data-based detection (no clean OOD assumption)
│   ├── Leaf 3.1: Constrained optimization (WOODS)
│   ├── Leaf 3.2: Threshold-based filtering (Du et al. 2024a)
│   └── Leaf 3.3: Median-based filtering (Medix — THIS PAPER)
│       ├── Core distinction: dataset-level vs. batch-level mixing
│       └── Core distinction: median-based vs. threshold-based selection
│
└── Branch 4: Positive-unlabeled learning
    └── Leaf 4.1: PU classification methods (limited to binary InD/OOD)
```

### Novelty & Retrieval Note

**Retrieval-Disabled Mode active**: External paper search could not be performed in this run (DEEPXIV_API_TOKEN unavailable). Consequently, novelty and comparison conclusions are based solely on manuscript evidence and the paper's own cited references. The following novelty assessments are preliminary and require manual literature verification:

- **C1** (median-centric filtering): The core algorithmic contribution appears differentiated from Du et al. (2024a)'s threshold-based approach, but a systematic literature search is needed to verify that median-based gradient filtering for OOD is genuinely novel.
- **C2** (theoretical bounds): The two-sided misclassification bound structure appears to be a novel contribution, though the relationship to standard median concentration bounds in robust statistics should be clarified.
- **C3** (empirical superiority): Claims of superiority over DRL and CONJ could not be verified as these results are absent from the main tables. Comparison with WOODS shows consistent but modest improvements (1.32% FPR95 on CIFAR-100).

**Required action before publication**: Authors should provide a side-by-side comparison with the most closely related methods (Du et al. 2024a, WOODS) in a dedicated table highlighting conceptual differences, and include DRL/CONJ results in the main paper.
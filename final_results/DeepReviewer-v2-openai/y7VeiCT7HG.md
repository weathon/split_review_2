## Summary
# Final Review Report

## Summary

This paper proposes a new batch acquisition strategy for multi-objective Bayesian optimization (MOBO) called qEHVI-SF (space-filling qEHVI), grounded in a conceptual framework termed "Probability of Matching." The key idea is to factorize the batch selection criterion into two components: (i) the probability that all batch points are Pareto-optimal (estimated via normalized qEHVI), and (ii) the probability that the batch collectively covers the full Pareto optimal set (estimated via a minimum-distance space-filling heuristic). The acquisition function combines these multiplicatively.

The paper evaluates qEHVI-SF against two baselines—qEHVI and QSVGD (quantile Stein variational gradient descent)—on synthetic benchmarks (Gaussian mixture problem, car side-impact RE4-7-1) and a real-world alloy inverse design case study with up to six objectives. Results show consistent improvements in hypervolume and a new design-space coverage metric (Expected Minimum Distance, EMD), with comparable computational overhead.

**Core contribution claims:**
- **C1 (Probability of Matching framework):** A probabilistic decomposition of batch selection into Pareto optimality likelihood and coverage likelihood, providing a unified alternative to additive quality-diversity objectives.
- **C2 (qEHVI-SF method):** A practical instantiation combining normalized qEHVI with minimum-distance space-filling, avoiding sensitive hyperparameter tuning.
- **C3 (EMD metric):** Expected Minimum Distance for evaluating coverage in design space, conceptually similar to IGD but operating in $\mathcal{X}$ rather than $\mathcal{Y}$.

**Overall assessment:** The paper tackles a relevant and well-motivated problem—achieving full Pareto set coverage in batch MOBO. The Probability of Matching framework offers an intuitive perspective, and the empirical results demonstrate consistent improvements on the tested problems. However, the manuscript has several significant weaknesses: the core probabilistic formulation (Eq. 7) is mathematically ill-posed as written (zero-probability event for continuous $\mathcal{X}^*$); "normalized qEHVI" is never defined, breaking the probabilistic interpretation; the figure captions are severely corrupted with text from another paper; and the alloy case study uses a surrogate circularity that limits external validity. Novelty assessment is deferred because external literature retrieval was unavailable in this run. With major revisions addressing these issues, the paper could be a solid contribution to MOBO methodology.

## Strengths
**S1. Well-motivated problem framing.** The paper identifies a genuine limitation in existing batch MOBO methods—namely, that qEHVI's reference-point sensitivity leads to biased coverage of the Pareto front—and argues convincingly that design-space diversity is a more reliable alternative to objective-space diversity. The motivation is grounded in practical applications (materials discovery) where full Pareto set recovery is the primary goal.

**S2. Intuitive conceptual decomposition.** The Probability of Matching framework provides an interpretable factorization of batch acquisition into quality (Pareto optimality likelihood) and coverage (full-set coverage likelihood). This is conceptually cleaner than the additive qEHVI+entropy formulation of QSVGD, which requires sensitive hyperparameter tuning. The joint probabilistic framing is a genuine conceptual contribution to the MOBO acquisition design space.

**S3. Consistent empirical improvements.** Across two synthetic benchmarks (GM, RE4-7-1) and a six-task alloy design study, qEHVI-SF consistently outperforms both qEHVI and QSVGD in hypervolume, EMD, and rediscovery ratio. The improvements are particularly clear at small batch sizes, where diversity mechanisms matter most. The results are supported by 20-trial repeats, suggesting the trends are stable.

**S4. Introduction of EMD metric.** The Expected Minimum Distance (EMD) metric is a natural design-space analogue of IGD. It directly addresses the practical need to evaluate whether MOBO methods recover diverse design configurations, not just objective-space coverage. This metric could be useful beyond this paper as a standard evaluation tool for design-oriented MOBO.

**S5. Honest limitation disclosure.** The conclusion explicitly acknowledges the theoretical gap between the minimum-distance heuristic and true coverage probability, and identifies future work on direct estimators. This transparency is commendable and helps bound the claims appropriately.

**S6. Computational efficiency analysis.** The complexity analysis in Section 3.3 provides a clear theoretical comparison of qEHVI, QSVGD, and qEHVI-SF, and the empirical runtime results in Table 1 confirm that qEHVI-SF has comparable computational cost to the baselines in most settings.

## Weaknesses
### W1. [CRITICAL] Core probabilistic framing is mathematically ill-posed (Eq. 7)

The central equation of the paper, Eq. (7), defines $P(\mathbf{X} = \mathcal{X}^*)$ as the probability that a finite batch $\mathbf{X}$ matches the true Pareto optimal set $\mathcal{X}^*$. Since $\mathcal{X}^*$ is a continuous subset of $\mathbb{R}^d$, a finite set can never equal it—the event has probability zero under any standard continuous probability model. The factorization $P(\mathcal{X}^* \subseteq \mathbf{X})$ is similarly ill-defined because a finite batch cannot contain a continuous set. This is not a minor technicality; it means the mathematical foundation of the proposed framework is not well-posed as written.

**Impact:** The probabilistic interpretation of the acquisition function is technically unsupported. While the authors partially acknowledge this in the conclusion ("the precise relationship between pairwise distance and true coverage probability remains unclear"), the main text presents Eq. (7) as a valid probabilistic model without caveat. This undermines the claimed contribution of a "probabilistic angle."
**Fix:** Reformulate the framework around a well-defined surrogate event (e.g., coverage up to tolerance $\epsilon$ using $\epsilon$-balls, as sketched in Section 3.2). State explicitly in Section 3.1 that perfect matching probability is zero and the framework uses a relaxation.

### W2. [CRITICAL] Figure captions severely corrupted (Figures 1 and 2)

Both Figure 1 and Figure 2 contain caption text that refers to methods not present in this paper ("BOILS," "BOILS+LBO," "BOILS+LBO+LBO" in Figure 1; "tnnv," "qnvcd," "tnnv-sf" in Figure 2). These captions appear to be incorrectly assembled from source material of a different paper. The figure subplot labels and colors cannot be reliably interpreted by readers.

**Impact:** This is a critical presentation flaw that makes the main empirical results unreadable. The paper cannot be evaluated or published in this state. It raises questions about overall manuscript preparation quality.
**Fix:** Replace all garbled captions with clean versions using the correct method names (qEHVI, QSVGD, qEHVI-SF) as shown in the text above the figures. Verify that figure legends and axis labels are consistent with the caption.

### W3. [MAJOR] "Normalized qEHVI" is never defined

Section 3.2 states that "normalized qEHVI" is used to approximate $P(\mathbf{X} \subseteq \mathcal{X}^*)$, but the normalization procedure is never specified. Since qEHVI returns an expected hypervolume improvement (an unbounded positive quantity), converting it to a probability requires a normalization scheme (e.g., dividing by running maximum, softmax over candidates, or mapping through a sigmoid). Without this definition, the probabilistic interpretation is incomplete and the acquisition function in Eq. (8) cannot be implemented from the paper's description alone.

**Impact:** Direct reproducibility risk. A reader attempting to implement qEHVI-SF cannot determine how the quality probability is computed.
**Fix:** Provide the explicit normalization formula in Section 3.2. Report the normalization factor and its sensitivity in the appendix.

### W4. [MAJOR] Scale imbalance in multiplicative acquisition (Eq. 8)

The final acquisition function (Eq. 8) is a product of expected hypervolume improvement and a minimum-distance term. These two factors can differ by orders of magnitude—hypervolume improvement scales with the volume of objective space (potentially very small or very large depending on objective scales and reference point), while distances are bounded by the design space extent. The product can therefore be dominated entirely by one factor, negating the claimed joint quality-diversity balance. The paper provides no analysis or mitigation for this scale imbalance.

**Impact:** The method may degenerate to pure qEHVI or pure space-filling in practice, depending on arbitrary scaling. This undermines the claim that the method "proactively maintains a high level of search efficiency and robustness."
**Fix:** (a) Analyze the scale ratio between the two factors on the tested benchmarks. (b) Consider an additive formulation on log-scale or a weighted product with adaptive balancing. (c) Show empirically that both factors contribute meaningfully to the final acquisition ranking.

### W5. [MAJOR] Eq. (6) contains a typo and missing implementation details for QSVGD

Eq. (6) uses $\mathbb{E}_{\mathbf{y}^{(1:n)}}$ but should be $\mathbb{E}_{\mathbf{y}^{(1:q)}}$ (batch size is $q$, not iteration count $n$). Additionally, the entropy estimator $\mathcal{H}(\mathbf{X})$ is not specified (the complexity analysis mentions KDE, but the main text does not). The $\eta$ decay schedule used in experiments is described only as "a decaying schedule" without concrete values or decay function.

**Impact:** The QSVGD baseline cannot be reproduced from the paper's description. Since QSVGD results are central to the empirical comparison, this is a reproducibility gap.
**Fix:** Fix the superscript in Eq. (6). Specify the entropy estimator and bandwidth selection. Report the full $\eta$ decay schedule.

### W6. [MAJOR] Surrogate circularity in alloy case study (Section 4.2)

The alloy case study trains property predictors on the full 1,000-candidate set and then evaluates rediscovery of Pareto optimal solutions from the same pool. This creates a circular evaluation: the surrogate Pareto set is derived from the same data that defines the "true" Pareto set. If predictors are accurate, the problem reduces to querying known Pareto points; if inaccurate, the "true" Pareto set is not physically meaningful. The evaluation tests algorithmic efficiency under perfect surrogate knowledge, not real-world discovery.

**Impact:** The external validity of the case study is limited. The absolute rediscovery ratios are likely overestimates of what would be achieved with true expensive objectives.
**Fix:** (a) Report predictor accuracy ($R^2$, RMSE). (b) Clarify that the evaluation is for algorithmic benchmarking under perfect surrogate knowledge. (c) Consider split evaluation (train on subset, test on held-out candidates).

### W7. [MAJOR] Missing significance testing and variance analysis

The paper reports mean hypervolume and EMD over "trials" (20 per setting) but does not report standard deviations on the main benchmark results (only in Table 1 for runtime). Statistical significance tests (e.g., paired t-test, Wilcoxon) between qEHVI-SF and baselines are not provided. For the alloy case study, only mean rediscovery ratios are shown in Figure 2 without confidence intervals.

**Impact:** It is unclear whether the reported improvements are statistically reliable, especially in settings where differences appear small (e.g., some batch size configurations in Figure 2).
**Fix:** Report standard deviations or confidence intervals for all main metrics. Include significance tests against the best baseline per setting. Add error bars/bands to Figure 2.

### W8. [MAJOR] Inequality typo in Section 4.3

The inequality "$(n + q)d \ll \frac{2^n - 1}{q}$" contains a typo: the exponent should be $q$, not $n$ (the hypervolume complexity depends on batch size, not iteration count). This should be $\frac{2^q - 1}{q}$.

**Impact:** While likely a typo, it undermines the complexity argument and could confuse readers.
**Fix:** Correct to $\frac{2^q - 1}{q}$ and verify the inequality holds for the tested batch sizes.

### W9. [MODERATE] Introduction storyline needs restructuring

The introduction opens with a generic description of Bayesian optimization (paragraph 1) that does not establish the specific batch-MOBO coverage problem until paragraph 4. The contribution description (paragraphs 4-5) is repetitive, stating the same factorization twice across a page break. The narrative does not follow the standard arc of Big Picture → Gap → Solution → Evidence.

**Impact:** Readers may lose motivation before reaching the core contribution. The paper's positioning as a coverage-focused MOBO method is diluted.
**Fix:** Restructure: paragraph 1 should immediately establish the batch MOBO coverage challenge. Merge paragraphs 4-5 into a single tight contribution paragraph.

### W10. [MODERATE] Limited baseline comparison

The paper compares against only two baselines: qEHVI (the immediate predecessor) and QSVGD (an entropy-based method). Several other diversity-aware MOBO methods—including EMMI, IGD-NS, and Pareto-complier approaches—are discussed in Related Work but not empirically compared. The paper does not include standard evolutionary MOBO algorithms or random-sampling baselines for the synthetic benchmarks.

**Impact:** The claim that qEHVI-SF "consistently outperforms state-of-the-art baselines" is only supported against two methods, one of which (QSVGD) is acknowledged to be poorly tuned for this task.
**Fix:** Add at least one additional baseline, preferably EMMI or IGD-NS. Show random search as a lower bound. When external retrieval becomes available, verify that no stronger existing method is omitted.

### W11. [MINOR] Related work lacks concrete positioning

Section 2.2 does a good job categorizing methods but does not specify the concrete residual novelty of the proposed method over EMMI or IGD-NS. The paper states these methods "struggle" with dispersed solutions but does not provide evidence or quantify when this failure occurs.

**Fix:** Provide a table comparing qEHVI-SF with EMMI/IGD-NS across dimensions: objective vs. design space, hyperparameter sensitivity, validity guarantees, and computational cost.

### W12. [MINOR] Notation inconsistency in Eq. (4)

The hypervolume indicator uses $\mathcal{A}$ in the text and $A$ in Eq. (4). The reference point description says "dominated by all elements in the Pareto front" but it should be "dominated by all elements in the approximation set A."

**Fix:** Use $\mathcal{A}$ consistently. Rephrase the reference point description precisely.

### W13. [DEFERRED] Novelty and related-work completeness

Because external paper search is unavailable in this run, novelty and comparison completeness cannot be fully verified. The paper claims a "novel acquisition strategy" but the Probability of Matching framework is conceptually related to several existing ideas: (a) multi-objective acquisition functions that implicitly balance quality and diversity; (b) hypervolume-based methods with explicit coverage corrections; (c) space-filling design in experimental optimization. 

**Recommendation:** The authors should conduct a thorough novelty verification against existing literature before submission, particularly for:
- Methods combining hypervolume improvement with diversity terms.
- Probability-based acquisition functions for MOBO.
- Space-filling approaches used in BO (not just experimental design).

## Score
**Final Score: 5/10**

This score reflects an evidence-based assessment prioritizing research value, novelty, and validity, consistent with the identified weaknesses:

**Rationale:**
- The paper addresses a well-motivated problem (Pareto set coverage in batch MOBO) and proposes a conceptually intuitive framework (Probability of Matching) with consistent empirical improvements on the tested problems. These are genuine strengths that support a mid-range score.
- However, the score is constrained by three critical/major validity issues: (1) the core probabilistic framing (Eq. 7) is mathematically ill-posed as written; (2) "normalized qEHVI" is undefined, breaking the reproducibility of the method; (3) both figure captions are severely corrupted, rendering the main empirical results unreadable. These issues prevent the paper from being accepted in its current form.
- Additional concerns—scale imbalance in Eq. (8), missing significance tests, surrogate circularity in the case study, and the typo in Eq. (6)/Section 4.3—further reduce confidence in the reliability of the reported results.
- Novelty assessment is partially deferred because external literature retrieval was unavailable in this run. The conceptual decomposition appears novel relative to the two tested baselines, but whether it is novel against the broader MOBO literature (EMMI, IGD-NS, information-theoretic methods) cannot be fully verified here.
- The weaknesses are fixable: the core mathematical issue can be resolved by reformulating around a well-defined surrogate event; the figure corruption is a formatting error; normalization and scale imbalance can be addressed with additional analysis. The paper could potentially reach 7-8/10 after major revisions.

**Score breakdown:**
- Research value / importance: 6/10 — Important problem, practical motivation.
- Novelty of contribution: 5/10 — Intuitive framework but partially overlapping with existing quality-diversity ideas; formal verification deferred.
- Methodological soundness: 3/10 — Core probabilistic framing ill-posed; missing definitions; scale imbalance.
- Empirical evidence: 4/10 — Consistent trends but figure corruption prevents verification; no significance tests; surrogate circularity.
- Reproducibility: 4/10 — Missing normalization definition, entropy estimator, and hyperparameter schedule.
- Presentation quality: 3/10 — Figure captions severely corrupted; writing is generally clear but has structural issues.

**Desired revision outcome:** With resolution of the critical figure corruption, reformulation of Eq. (7), definition of normalization, addition of significance tests, and strengthening of baseline comparisons, the paper could become a solid contribution worthy of 7-8/10.
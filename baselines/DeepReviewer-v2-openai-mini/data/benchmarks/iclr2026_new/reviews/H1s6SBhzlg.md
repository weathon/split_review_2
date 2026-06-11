## Summary
# Final Review Report

## Summary

This paper addresses the problem of aggregating answers from multiple LLMs in multi-agent reasoning pipelines. The authors propose two aggregation algorithms: Optimal Weight (OW), which uses LLMs' accuracies (first-order information) to compute Bayesian-optimal weighted voting, and Inverse Surprising Popularity (ISP), which uses pairwise answer correlations (second-order information) without requiring ground-truth labels. Under a conditional independence model with random label shuffling, OW is proven to be the Bayesian-optimal aggregator, and ISP is shown to provably outperform majority voting (MV) in expectation. Experiments on simulated data, UltraFeedback, MMLU, and the ARMMAN healthcare dataset demonstrate consistent improvements over MV, with absolute accuracy gains of 0.5–3.4 percentage points on subsets where models disagree. The paper brings a principled information-aggregation perspective to multi-LLM reasoning and offers practical methods that work without labeled data. However, the theoretical framework relies on assumptions (conditional independence, known accuracy bounds) that are partially violated in practice, the empirical gains are modest, several claims are overstated relative to evidence boundaries, and a critical formula inconsistency exists between the Overview and Section 3 definitions of the weight function.

## Strengths
1. **Principled theoretical foundation.** The paper connects the multi-LLM aggregation problem to the well-established information aggregation literature and provides formal theoretical guarantees (Bayesian optimality of OW, provable advantage of ISP over MV). This is a significant step beyond the ad-hoc use of majority voting common in current multi-agent LLM systems.

2. **Unsupervised applicability.** ISP operates without ground-truth labels, using only pairwise answer correlations across models. This makes the method applicable to realistic settings where labeled data is scarce, such as automated data annotation and healthcare prediction.

3. **Rigorous empirical evaluation across diverse settings.** The experimental design covers simulated data (matching theoretical assumptions), standard LLM benchmarks (UltraFeedback, MMLU), and a real-world healthcare application (ARMMAN). The use of 16 ensemble combinations from four model families provides robustness evidence for the findings.

4. **Clear connection to practice.** The paper demonstrates that ISP and the OW-L/OW-I heuristics consistently outperform majority voting across a large fraction (85–98%) of tested ensembles, validating the practical value of higher-order information even when theoretical assumptions are partially violated.

5. **Well-motivated methodological novelty.** The ISP objective is a principled modification of the Surprisingly Popular rule, and the theoretical analysis showing MV outperforms SP (counter to human-subject findings) is an interesting insight specific to the LLM domain.

## Weaknesses
### Major Weaknesses

**W1. Critical formula inconsistency in $\sigma_K(x)$ definition (Page 1 — Overview vs. Section 3).** The Overview of Results defines $\sigma_K(x) = \frac{x^2}{K-1+x^2}$, while Section 3 defines $\sigma_K(x) = \frac{e^x}{K-1+e^x}$. These are entirely different functions — one is rational in $x^2$, the other is exponential. Since the Bayesian-optimal weight $w_i = \sigma_K^{-1}(x_i)$ depends on the correct functional form, one of these definitions is wrong. This inconsistency undermines the core theoretical contribution and could invalidate Theorem 1's optimality claim if the wrong definition propagates to implementations. **Required fix:** Re-derive the weight formula from first principles, select the correct $\sigma_K$, and ensure consistent usage throughout the manuscript (Overview, Section 3, Algorithm 1, Theorem 1, Corollaries 1-2, Proposition 2). Add the derivation to the appendix. (Severity: Critical)

**W2. Algorithm 1 argmax notation is malformed (Page 1 — Section 3).** Algorithm 1 step 4 writes $\arg \max_{s \in \sum_{i=1}^N \sigma_K^{-1}(x_i) \mathbb{1}\{a_i = s\}}$, where the domain of $s$ is typeset as a sum expression. This is mathematically uninterpretable. The intended form is $\arg \max_{s \in S} \sum_{i=1}^N \sigma_K^{-1}(x_i) \cdot \mathbb{1}\{a_i = s\}$. While the intended meaning is clear, the typesetting error creates ambiguity about the argmax domain and signals insufficient proofreading. (Severity: Major)

**W3. Conditional independence assumption is acknowledged as fragile but extensions are deferred to Appendix C (Page 1 — Section 2/3).** The entire theoretical framework (Theorems 1, 2, 3) relies on Assumption 1 (conditional independence given the true label). The paper states that this "may not hold perfectly in the LLM setting" and claims to "break this canonical assumption" with extensions in Appendix C. However, Appendix C is not included in the review draft, making it impossible to verify the robustness of the claimed generalization. This is a critical gap for reviewing the paper's theoretical claims. During camera-ready, the authors must include Appendix C in the main submission or add a more precise summary of what the relaxation achieves and under which conditions. (Severity: Major)

**W4. Theorem 3 finite-sample guarantee does not clarify data dependence (Page 1 — Section 4.3).** Theorem 3 states a high-probability lower bound on the ISP advantage using empirical conditional probabilities $\hat{\mathbb{P}}$ estimated from $M$ questions. The text acknowledges that "$\hat{\mathbb{P}}$ and $A_1, \dots, A_N$ are not independent" but does not clarify whether the theorem assumes sample-splitting (training vs. evaluation sets). Without explicit sample-splitting, the bound does not hold as stated because the same data would be used for both estimation and evaluation, creating dependent randomness. The authors must specify the sample-splitting protocol or provide a bound that accounts for the dependence. (Severity: Major)

**W5. SP underperformance explanation is an unverified behavioral claim (Page 1 — Section 4.1).** The paper explains SP's worse-than-MV performance by asserting "LLM agents are generally more powerful, so the systematic biases that SP exploits in human settings are much less pronounced here." This is a post-hoc rationalization without empirical support — no experiment measures the degree of systematic prediction bias in LLMs versus humans. The argument could be strengthened by computing the "surprise gap" (difference between actual and predicted vote shares) on the real datasets to verify the bias hypothesis. Without this, the conceptual foundation for ISP's design rationale is weaker. (Severity: Major)

**W6. Simulation results lack variance reporting (Page 1 — Section 5.1).** Table 2 reports single-point accuracy estimates without standard errors, confidence intervals, or multi-seed statistics. With random generation, these numbers have binomial sampling variance. For example, at $K=2$, ISP (90.48%) vs. Single Best (90.34%) is a 0.14% difference that could easily be noise. Without variance information, readers cannot assess the statistical reliability of the claimed rankings. At minimum, the authors should report mean $\pm$ std across 5+ random seeds and include paired significance tests. (Severity: Major)

**W7. Empirical gains are modest and not always universal (Page 1 — Sections 5.3-5.4).** On MMLU, the single best model (91.02%) outperforms the proposed aggregation methods (90.37%). While the paper honestly flags Single Best as a "clairvoyant oracle," the narrative framing ("consistently dominate majority voting") overstates the practical significance of improvements that are 0.54–1.45 percentage points absolute. On ARMMAN, the gain is only 0.54% (85.78% vs. 85.24%). The paper should: (a) report bootstrap confidence intervals for all percentages, (b) include a box plot of accuracy gains across all 16 ensembles in the main text, (c) clearly state when aggregation does not beat the best individual model. (Severity: Major)

**W8. Conclusion lacks limitations section and uses inflated language (Page 1 — Section 6).** The paper does not include a dedicated limitations paragraph, which is expected for a conference submission. Important limitations omitted include: reliance on conditional independence, modest absolute gains, need for multiple LLM queries (increased cost), and sensitivity of second-order estimation to dataset size. The word "dominate" is too strong — the evidence supports "consistently improve upon" but not formal dominance. A limitations paragraph should be added before the future work discussion. (Severity: Major)

### Minor Weaknesses

**W9. Related work is organized as a citation list rather than structured comparison (Page 1 — Section 1.1).** The "Multi-agent LLM reasoning" paragraph lists papers chronologically without organizing them by aggregation approach (zero-order, confidence-based, role-based). This makes it hard to see how the proposed methods differ from existing ones. Restructure by thematic category and add a comparison table. (Severity: Minor)

**W10. Introduction P3 is overly dense with two distinct roles (Page 1 — Introduction).** The third introduction paragraph attempts both to position within information aggregation literature and to describe LLM-specific opportunities/challenges. These should be split into two paragraphs for readability. Also, the claim that random shuffling enables "an interpretable closed-form optimal solution" should explicitly note that this holds under Assumption 1. (Severity: Minor)

**W11. ISP derivation contains a redundant identity and anthropomorphic language (Page 1 — Section 4.2).** The derivation writes $\mathbb{P}(A_i = s_2 | A_j = s_1) = \mathbb{P}(A_i = s_2 | A_j = s_1)$ (identical LHS and RHS), which is trivial and may be a formatting artifact. The justification that "humans tend to assign higher predictions to answers that match their own" anthropomorphizes LLMs unnecessarily — the inequality follows from the model assumptions, not psychology. (Severity: Minor)

**W12. Abstract should bound empirical claims more carefully (Page 1 — Abstract).** The abstract states that methods "provably mitigate inherent limitations of majority voting" without specifying which limitations or under which assumptions. It claims "consistently outperform majority voting" without noting that gains are concentrated on disagreement subsets and are modest in absolute terms. A more precise abstract would specify the scope of guarantees and the empirical effect sizes. (Severity: Minor)

**W13. Proposition 2's "mild assumptions" characterization is imprecise (Page 1 — Overview of Results).** The paper claims OW "has strictly higher accuracy than any single LLM under mild assumptions," but Proposition 2's condition for OW to beat a single agent is non-trivial: $\sigma_K^{-1}(x_i) \geq \sum_{j\neq i} \sigma_K^{-1}(x_j)$. This depends on the accuracy distribution and can fail in practice. The text should explicitly reference the condition rather than calling it "mild." (Severity: Minor)

### Deferred Novelty/Comparison Verdict

Due to Retrieval-Disabled Mode (external paper search unavailable), novelty and literature-comparison conclusions are explicitly deferred. The following aspects require manual verification: (a) whether the OW weighting scheme is truly novel or overlaps with existing ensemble weighting methods; (b) whether ISP provides a meaningful advance over the Surprisingly Popular framework beyond the specific LLM instantiation; (c) whether the empirical comparisons include all relevant baselines from the multi-agent LLM literature. These judgments should be revisited when external retrieval is available.

## Score
**Final Score: 6/10**

**Rationale:** The paper presents a principled theoretical framework for multi-LLM answer aggregation and provides practical algorithms that improve over majority voting across multiple settings. The strengths include solid theoretical grounding, an unsupervised variant (ISP), and extensive empirical evaluation across 16 model ensembles on three datasets. However, the score is constrained by: (1) a critical formula inconsistency (W1) between the Overview and Section 3 definitions of the core weight function, which must be resolved before the theoretical claims can be fully trusted; (2) a heavy reliance on conditional independence (W3) with robustness analysis deferred to a missing appendix; (3) modest empirical gains (0.5–3.4 percentage points on disagreement subsets, ~0.5–1.5 pp overall) that are sometimes below the best single model; and (4) several overclaimed statements throughout the manuscript. The novelty and literature-positioning dimensions cannot be fully assessed without external retrieval (deferred to manual verification). After addressing the critical formula issue, tightening claims, adding variance reporting, and including a limitations section, the paper could reach 7-8/10.

```text
ASCII Diagram — Paper Structure & Evidence Map

[Problem: Multi-LLM answer aggregation with MV is suboptimal]
    |
    ├── [C1: OW — Bayesian-optimal weighted aggregation using accuracies]
    |   ├── Evidence: Theorem 1 (optimality), Proposition 2 (vs single agent)
    |   └── Gap: σ_K(x) definition inconsistent; needs accuracy labels
    |
    ├── [C2: ISP — Second-order aggregation without labels]
    |   ├── Evidence: Theorem 2 (advantage over MV/SP), Theorem 3 (finite-sample)
    |   └── Gap: CI assumption (A1) is strong; bias explanation unverified
    |
    └── [C3: Empirical validation on sim + real benchmarks]
        ├── Evidence: Table 2 (sim), Table 3 (real), Table 4 (per-question)
        └── Gap: No variance bars; cherry-picked best-model ensemble; 
                  MMLU Single Best > aggregation
```

```text
ASCII Diagram — Revision Strategy Roadmap

[W1: σ_K inconsistency]
    -> Fix: re-derive weight formula, unify definition across all sections
    -> Expected gain: core theoretical claim becomes verifiable

[W3/W4: CI assumption + data dependence]
    -> Fix: include Appendix C summary in main text; clarify sample-splitting
    -> Expected gain: theory-practice gap narrowed

[W6: No variance in simulations]
    -> Fix: multi-seed runs, std bars, significance tests
    -> Expected gain: statistical reliability established

[W5/W8: Unverified bias claim + missing limitations]
    -> Fix: add bias measurement experiment / add limitations subsection
    -> Expected gain: scientific credibility and completeness

[W2/W7/W9-W13: Notation error, overclaims, related work structure]
    -> Fix: correct argmax, bound claims, restructure related work
    -> Expected gain: manuscript polish and defensive writing
```

```text
ASCII Diagram — Related-Work Taxonomy Tree (Layered)
(Note: Literature placement is provisional without external retrieval)

Root: Multi-LLM Answer Aggregation
├── Branch A: Aggregation Rule
│   ├── Leaf A1: Zero-order (MV-only) — Li 2024, Elumar 2025, Subramaniam 2025
│   ├── Leaf A2: Confidence-based weighting — Chen 2023a, Fu 2025
│   ├── Leaf A3: Role-based exchange — Du 2023, Lu 2024, Wang 2024
│   └── Leaf A4: Information-theoretic weighting (OW, ISP) — This paper
│       └── Key difference: uses accuracy/correlation structure
└── Branch B: Information Source
    ├── Leaf B1: First-order (accuracy) — Chen 2023a, Fu 2025
    ├── Leaf B2: Second-order (correlations) — Prelec 2017 (SP), This paper (ISP)
    └── Leaf B3: No supervision — This paper (unsupervised setting)
```
## Summary
This paper introduces the concept of *monitorability* for deep neural networks — defined as the intrinsic ability of a model to highlight potential inference errors through its internal activations. The authors propose the MIRA (Monitorability via Input peRturbAtion) Score, a metric that quantifies monitorability by applying norm-bounded FGSM perturbations to in-distribution inputs and measuring the separability of perturbed vs. clean internal representations using Mahalanobis-distance-based surprisal. A formal definition (Definition 1) is provided, and the metric is validated by correlating MIRA scores with the best achievable OoD detection AUROC across three methods (ODIN, Mahalanobis, Energy-based) on computer vision (CIFAR-10/100), tabular (Sensorless Drive), and NLP (SST-2 fine-tuned) benchmarks. The paper claims this is the first formalization and quantitative measure of monitorability.

**Strengths:** The concept of monitorability is timely and well-motivated; the toy example in Figure 1 effectively illustrates that accuracy-equivalent models can have different failure-detectability. The cross-modality evaluation (vision, tabular, NLP) is commendable. The paper is clearly written and the formalization attempts to ground a practically important property.

**Core weaknesses:** (1) Definition 1's bi-conditional is practically unrealizable — real NNs cannot satisfy a perfect equivalence between loss thresholds and activation sets. (2) Validation relies on a circular proxy: MIRA uses Mahalanobis distance while the validation "best-of" set includes Mahalanobis-based OoD detection. (3) ε_min selection is heuristic and model-dependent, potentially biasing comparisons. (4) No variance, confidence intervals, or significance tests are reported, making the central correlation claim statistically unsubstantiated. (5) The MIRA Score formula has numerical instability (division by near-zero S₀) and produces incomparable scales across modalities (0–89 for vision vs. 2000–3800 for NLP). Novelty verification is deferred due to the unavailability of external literature search in this run.

```text
ASCII Diagram — Paper Structure & Evidence Map

[Problem: How to quantify DNN error detectability before deployment?]
    |
    v
[Concept: Monitorability — intrinsic property of feature-space separability]
    |
    v
[Definition 1 (Boolean, bi-conditional)] -- Weakness: practically unrealizable
    |
    v
[MIRA Score: ∫ E[S(perturbed) - S₀]/S₀ p(ε) dε] -- Weakness: S₀ near-zero instability
    |
    v
[Validation: correlate MIRA with best-of-3 OoD AUROC] -- Weakness: circular proxy
    |
    v
[Experiments: vision, tabular, NLP, 4-5 models each] -- Weakness: no variance/significance
    |
    v
[Claim: first formal measure of monitorability] -- Deferred verification (no literature search)
```

## Strengths
1. **Timely and well-motivated concept.** The notion of monitorability addresses a genuine gap: OoD detection methods evaluate inputs, not the model's intrinsic capacity to make its failures detectable. The motivation that two accuracy-equivalent models can differ in how separable their error patterns are (Figure 1) is clear and compelling. This reframing from "detect anomalies" to "characterize detectability" is a useful conceptual contribution.

2. **Cross-modality evaluation.** The paper evaluates MIRA across three distinct data modalities (vision, tabular, NLP) using a diverse set of architectures (CNNs, ViTs, MLPs, transformers). This breadth strengthens the claim that MIRA captures a general property rather than a benchmark-specific artifact.

3. **Theoretical grounding attempt.** The definition of monitorability (Definition 1) and the principled use of Mahalanobis distance with χ²-calibrated surprisal (Eq. 3) show technical rigor. The dimension-calibration argument for the surprisal score is a thoughtful design choice.

4. **Practicality focus.** MIRA is designed as a pre-deployment evaluation metric that requires only in-distribution data and lightweight FGSM perturbations, making it computationally efficient compared to tuning multiple OoD detectors. This practical orientation is valuable for model selection workflows.

5. **Clear writing and organization.** The paper is well-structured, the notation is consistent, and the research questions (RQ1–RQ4) provide a clear evaluation framework. The toy example effectively builds intuition before the formal treatment.

6. **Honest limitation disclosure.** The paper acknowledges the ε_min selection procedure as a current limitation and outlines concrete future work directions (model-adaptive range, inter-layer dynamics, formal verification integration). This transparency is commendable.

## Weaknesses
The weaknesses are ordered by severity, with the most validity-critical items first.

### W1. Definition 1 (Monitorability) is Practically Unrealizable [Major]

**Location:** Page 2–3 (Section 3.2, Definition 1)

**Problem:** The bi-conditional $\mathcal{L}(f(x), y) \leq \epsilon \iff f^l(x) \in Z^l$ requires perfect equivalence between low-loss predictions and membership in a pre-specified activation set. In practice, no real neural network satisfies this: (a) adversarial examples can produce activations resembling correct-class regions while being misclassified, violating the left-to-right direction; (b) correctly classified inputs near decision boundaries can have activations outside the "correct" region, violating the right-to-left direction.

**Why it matters:** An unfalsifiable definition cannot serve as the theoretical foundation of a metric. The definition as stated is an existence statement with no constructive verification path. Furthermore, the definition applies only to in-distribution inputs ($\forall (x,y) \sim \mathcal{P}_{in}$), but the motivating scenario in Figure 1 involves OoD inputs — creating a disconnect between the formal definition and the intuitive illustration.

**Suggested fix:** Replace the strict bi-conditional with a probabilistic formulation (see annotation on this paragraph for a concrete alternative). At minimum, acknowledge that Definition 1 describes an idealized scenario and that practical monitorability requires approximate satisfaction.

### W2. Validation Relies on a Circular Proxy [Major]

**Location:** Page 4 (Section 4.1, Evaluation Protocol)

**Problem:** MIRA is validated by correlation with the "best achievable OoD detection performance across three representative methods" — ODIN, Mahalanobis distance, and Energy-based scoring. However, the MIRA Score itself uses Mahalanobis distance to compute the surprisal score (Eq. 3). This creates a confounding correlation: MIRA may correlate with the Mahalanobis detector simply because they use the same underlying distance metric, not because MIRA captures general monitorability.

**Why it matters:** The paper aims to establish MIRA as a detector-agnostic monitorability measure (RQ3), but the validation set includes the very type of method (Mahalanobis-based) that MIRA is built upon. This circularity undermines the claim that MIRA captures "intrinsic" rather than detector-specific properties.

**Suggested fix:** (1) Remove the Mahalanobis detector from the "best-of" validation set, or report correlation separately with and without it. (2) Validate MIRA against a broader set of diverse detection methods (e.g., KNN-distance, gradient-based, density-based). (3) Add a synthetic validation: corrupt model parameters and verify that MIRA predicts the detectability of resulting errors, independent of any specific OoD detector.

### W3. ε_min Selection is Heuristic and Model-Dependent [Major]

**Location:** Page 4 (Section 4.2, Perturbation Setup; details in Appendix B.6)

**Problem:** ε_min is selected as the smallest perturbation that reduces accuracy to a certain (unspecified in main text) threshold, with ε_max = 2·ε_min. This creates a circular dependency: models that are more robust to perturbations (i.e., maintain accuracy under larger ε) automatically get larger integration ranges, potentially inflating their MIRA scores. The specific threshold and its justification are relegated to the appendix and not characterized.

**Why it matters:** This selection procedure can systematically bias MIRA scores toward robust models, making the correlation with OoD detection performance a tautology rather than an independent validation.

**Suggested fix:** (1) Report the accuracy threshold explicitly in the main text. (2) Add sensitivity analysis showing MIRA rankings under different thresholds. (3) Include a fixed-range baseline (e.g., [0.01, 0.1] for ℓ∞) as a complementary, model-agnostic analysis.

### W4. No Variance, Confidence Intervals, or Statistical Tests [Major]

**Location:** Page 5–7 (Section 4.4, Results)

**Problem:** All AUROC scores in Tables 1–3 and all MIRA scores are reported as point estimates without standard deviations, confidence intervals, or significance tests. The paper states "we fixed random seeds across all experiments," implying single-seed runs. The central claim that MIRA "correlates with" detection performance is supported only by visual inspection of rankings across 3–4 models per dataset.

**Why it matters:** With only 3–4 data points per comparison, a perfect rank correlation (ρ = 1.0) may not be statistically significant (e.g., p ≈ 0.08 for N=4). Without variance estimates, reviewers cannot assess whether reported differences between models are meaningful or within noise range.

**Suggested fix:** (1) Report mean ± std over ≥3 random seeds for all key results. (2) Report Spearman rank correlation with p-values for the MIRA-vs-AUROC relationship. (3) Add a brief interpretative statement acknowledging the limited statistical power and suggesting validation on larger model suites.

### W5. MIRA Score Formula Numerical Instability [Major]

**Location:** Page 3 (Section 3.3, Definition 2, Eq. 4)

**Problem:** The MIRA Score divides by $S_0 = \mathbb{E}_{x\sim D}[S(f^l(x))]$, the average surprisal of clean data. When the clean data features fit the Gaussian assumption well, $S_0$ approaches 0, making the division unstable and the score arbitrarily large. This explains the extreme scale differences across modalities: vision scores range [-0.07, 89] while NLP scores range [2015, 3793], making cross-modal comparison meaningless.

**Why it matters:** The paper positions MIRA as a general-purpose metric for comparing monitorability across different architectures and modalities. If the score scale depends on how well features happen to fit the Gaussian assumption, cross-model comparisons within the same modality may also be unreliable.

**Suggested fix:** (1) Replace the S₀-normalized integral with a log-ratio formulation $\int \mathbb{E}[\log(S(\tilde{x})/S_0)] p(\epsilon) d\epsilon$ to avoid division-by-zero. (2) Report normalized scores across a reference model set. (3) Verify that the GDA assumption holds for the specific models used (see W6).

### W6. Uns assessed GDA Assumption Violation [Minor]

**Location:** Page 2 (Preliminaries, Mahalanobis distance)

**Problem:** The χ²-calibrated surprisal score (Eq. 3) assumes that penultimate-layer features follow a class-conditional Gaussian distribution (GDA assumption, cited from Lee et al., 2018b). This assumption is not verified for the specific models used in this paper. Modern architectures, particularly ViTs, are known to produce features that deviate from Gaussian distributions.

**Why it matters:** If the GDA assumption is violated, the probabilistic interpretation of the surprisal score is invalid, and the resulting MIRA scores may reflect assumption-mismatch rather than genuine monitorability.

**Suggested fix:** Test multivariate normality (e.g., Mardia's test) on the penultimate-layer features for each model. As a robustness check, compute a non-parametric MIRA variant (e.g., 1NN AUC for clean vs. perturbed features) and verify ranking consistency.

### W7. Detector-Agnostic Claim is Overstated [Minor]

**Location:** Page 6 (Section 4.4, Discussion)

**Problem:** The paper claims MIRA "captures intrinsic monitoring potential even when individual detectors disagree, demonstrating its detector-agnostic nature (RQ3)." This is based on only three detectors, two of which are logit-based (ODIN, Energy) and one is Mahalanobis-based. This does not constitute sufficient diversity to support a "detector-agnostic" claim.

**Suggested fix:** Replace "detector-agnostic nature" with "suggests that MIRA captures information not fully captured by any single detector." Add experiments with more diverse detectors to support the stronger claim.

### W8. Storyline and Introduction Coherence [Minor]

**Location:** Page 1 (Introduction)

**Problem:** The Introduction mixes two separate failure motivations (distribution shift and adversarial vulnerability) in one paragraph, then transitions abruptly to the OoD detection gap. The gap claim ("literature still lacks a formal definition") is presented as fact without evidence of having surveyed the literature. The three contributions are listed co-equally, but contribution 3 (empirical) is validation of C1/C2, not an independent conceptual contribution.

**Suggested fix:** Restructure Introduction to follow: Big Picture (safety-critical DNNs) → Specific Gap (no metric for detectability) → Solution (monitorability + MIRA) → Contribution summary (two conceptual + validation). Add explicit acknowledgment of activation monitoring literature as the closest prior work, with clear differentiation.

### Novelty and Related Work Assessment [Deferred]

Due to Retrieval-Disabled Mode (external paper search unavailable in this run), novelty and comparison conclusions are deferred. The paper claims "to the best of our knowledge, this is the first formalization and quantitative measure of monitorability." A manual literature verification is required to assess this claim against prior work on activation monitoring (e.g., Cheng et al., 2019; Henzinger et al., 2020b; Hashemi et al., 2021), robustness metrics, and related concepts in OoD detection literature.

```text
ASCII Diagram — Revision Strategy Roadmap

Priority 0 (Must, Pre-Submission):
[Definition 1 bi-conditional too strong]
    -> [Replace with probabilistic formulation]
    -> [Expected: definition becomes verifiable & falsifiable]

[Validation circular proxy (Mahalanobis in both MIRA and validation)]
    -> [Extend to 5+ diverse detectors; add synthetic fault injection]
    -> [Expected: genuine detector-agnostic validation]

[No variance/significance in results]
    -> [Add 3-seed std; report Spearman ρ + p-value]
    -> [Expected: statistical substantiation of core claim]

Priority 1 (Must, Strengthening):
[ε_min heuristic model-dependent]
    -> [Add fixed-range baseline; report sensitivity analysis]
    -> [Expected: robustness evidence for ranking stability]

[MIRA Score S₀ instability]
    -> [Replace with log-ratio formulation]
    -> [Expected: stable cross-modal comparison]

Priority 2 (Nice-to-Have):
[GDA assumption unverified]
    -> [Add normality tests + non-parametric MIRA baseline]
    -> [Expected: increased technical rigor]

[Detector-agnostic claim overstated]
    -> [Replace with bounded wording]
    -> [Expected: defensible claim scope]
```

## Score
**Final Score: 5.5/10**

**Rationale:** The paper introduces a conceptually interesting and practically motivated idea — quantifying how detectable a neural network's errors are from its internal representations. The cross-modality evaluation and the clear exposition are strengths. However, the score reflects several validity-critical weaknesses that significantly limit the paper's current contribution.

**Severity-weighted reasoning:**
- The formal definition (W1) is the theoretical bedrock and is practically unrealizable, which undermines the claimed theoretical grounding.
- The validation strategy (W2) has a circular component that calls into question the core empirical claim.
- The complete absence of statistical substantiation (W4) means the main result is not yet empirically established.
- The formula instability (W5) and heuristic ε selection (W3) suggest the metric needs further refinement before it can serve as a reliable evaluation tool.
- Novelty cannot be fully assessed without literature verification (deferred).

**What would raise the score:** (a) Replacing Definition 1 with a verifiable probabilistic formulation; (b) adding statistical rigor (multi-seed, significance tests); (c) extending validation to more diverse and non-circular detection benchmarks; (d) stabilizing the MIRA score formula; (e) providing sensitivity analysis for the perturbation range.

The paper has a solid conceptual core but requires substantial technical revision before publication. With the recommended fixes (particularly W1, W2, W4), the contribution could reach 7–8/10.

**Special note on novelty scoring:** Due to Retrieval-Disabled Mode, novelty was not verified against external literature. The score above assumes the claimed novelty is valid; a downward adjustment may be warranted if significant overlap with prior work on activation monitoring is found.
## Summary
This paper presents CausalNovo, a model-agnostic framework for de novo peptide sequencing that aims to improve robustness to spectral noise by learning representations focused on signal fragment ions rather than spurious noise peaks. The framework is grounded in a Structural Causal Model (SCM) formulation of the peptide sequencing task, from which two principles are derived: *independence* (causal representations should be invariant to noise perturbations) and *sufficiency* (representations must retain predictive information). These principles are operationalized via a Causality Extraction Module (CEM) that learns soft importance weights over spectral peaks, combined with a replace-based perturbation strategy and contrastive learning objectives. Experiments on three benchmark datasets (Nine-species, Seven-species, HC-PT) across three strong baselines (CasaNovo, AdaNovo, π-HelixNovo) show consistent improvements of up to 10% in amino acid, peptide, and PTM-level precision. The method also demonstrates improved robustness under varying noise-signal ratios and perturbation conditions.

**Overall assessment:** The paper addresses an important practical problem — noise robustness in de novo peptide sequencing — and proposes a technically sound approach with clear empirical benefits. The main concerns are: (1) the causal framing is stronger than what the actual implementation delivers (the "causal intervention" is a label-guided noise replacement, not a causal discovery procedure), (2) the independence assumption C ⟂ S in the SCM is unverified and likely violated in real MS data, (3) all results lack statistical significance reporting (no variance, no multi-seed runs), and (4) the sufficiency "principle" is simply the standard cross-entropy loss used by all baseline models. These issues reduce the conceptual novelty but do not negate the practical contribution. The paper would benefit from toning down causal claims, adding significance evidence, and repositioning the contribution as a noise-robust training framework rather than a causal inference method.

## Strengths
**1. Practical problem, well-motivated.** The paper identifies a genuine limitation in current de novo peptide sequencing models: their performance degrades when noise distributions shift because they exploit spurious correlations between non-signal peaks and peptide sequences. The preliminary vulnerability experiment (Figure 1) effectively demonstrates this degradation, providing clear motivation for the proposed approach.

**2. Clean, modular framework design.** CausalNovo's architecture as a plug-in module (CEM) that can be integrated with any existing sequencing model is a practical strength. The framework does not require architectural changes to the base model and adds negligible inference overhead (<1%), making it easy to adopt in practice. The ablation studies (Tables 4, 5) systematically isolate each component's contribution.

**3. Consistent empirical gains across diverse settings.** The improvements are demonstrated across three datasets (spanning different species, peptide complexities, and PTM challenges), three different baseline architectures (CasaNovo, AdaNovo, π-HelixNovo), and multiple evaluation levels (amino acid, peptide, PTM). The cross-species validation (Table 3) provides evidence that gains are not dataset-specific. The NSR analysis (Figure 4) shows improved robustness under varying noise conditions, which directly supports the paper's central thesis.

**4. Thoughtful intervention design.** The replace-based perturbation strategy (sampling replacement peaks from the training batch) is a practical and principled way to simulate diverse noise conditions. The addition of theoretical spectrum peaks to preserve causal relationships is a well-motivated safeguard. The use of only three ion types (b, y, a) to identify signal peaks is grounded in domain knowledge and validated against a more comprehensive 18-ion set.

**5. Honest limitation discussion.** The conclusion candidly acknowledges the 2.3× training overhead and the limitation that evaluation follows the NovoBench setting rather than the more realistic cross-corpus protocol used by recent methods. This transparency is commendable and should be retained in revision.

## Weaknesses
### W1. Overclaimed causal framing that does not match the implementation (Major)

The paper presents CausalNovo as a "causality-informed framework" that learns "causal representations" by "modeling causal mechanisms" via Structural Causal Models. However, the actual implementation deviates substantially from this framing in several ways:

- **The "causal intervention" is a label-guided noise replacement, not a true causal intervention.** The paper uses ground-truth peptide labels to identify non-causal peaks and replaces them with other noise peaks from the batch. While this is a reasonable training-time augmentation, it does not perform an intervention on the actual data-generating process and does not discover causal structure. It is better described as a targeted data augmentation strategy.

- **The conditional mutual information objective I(z_c; z_c' | C) is implemented as unconditional InfoNCE.** Eq. (5) is a standard contrastive loss that does not condition on Y or C. The paper acknowledges this gap (C is unobserved, Y serves as proxy) but does not explain why the unconditional version suffices. The theoretical derivation using RCCP implies conditional independence given C, which is a stronger condition than the implemented invariance.

- **The sufficiency "principle" is simply the standard cross-entropy loss** used by every existing de novo model. The paper admits this in Section 4.4 ("already included in the baseline model") but the introduction and methodology present it as a novel derivation from the SCM. This inflates the perceived contribution.

**Impact:** The causal framing creates expectations that the paper does not deliver, which may lead knowledgeable reviewers to rate novelty lower than the practical contribution deserves. **Severity: Major. Fixability: Easy.** Revise the introduction and method to describe the approach as "invariant representation learning via targeted noise perturbation" rather than causal discovery, and clearly distinguish the SCM framework (conceptual motivation) from the actual contrastive learning implementation.

### W2. Missing statistical significance and variance reporting (Major)

All experimental results (Tables 1-7, Figures 1-4) are reported as single-point estimates without standard deviations, confidence intervals, or significance tests. The paper does not state the number of random seeds used.

- In Table 4, the symmetric training strategy adds only +0.4% to amino acid precision (0.765 vs 0.761). Without variance, this gain cannot be assessed for statistical significance.
- In Table 5, the "Replace + Enhance" strategy produces nearly identical results to "Replace + Enhance + Drop" (0.753 vs 0.753 AA precision), yet the paper concludes the drop operation "did not lead to performance improvement" without any significance test.
- Many reported gains (e.g., +2.4% on Nine-species, +2.2% on π-HelixNovo) are within the typical variance range of de novo models (1-3%).

**Impact:** The paper's primary evidence is empirical improvement, but without statistical rigor, the reliability of even the modest reported gains is uncertain. **Severity: Major. Fixability: Moderate.** Run all main experiments with ≥3 seeds, report mean±std, and add significance tests for key comparisons. If the paper is at a later revision stage, a minimum of adding bootstrap confidence intervals to the existing single-run results would help.

### W3. Unverified independence assumption C ⟂ S in the SCM (Major)

The paper's SCM (Eq. 2) assumes causal factors C are independent of non-causal factors S. This assumption is critical for the independence principle but is not justified for mass spectrometry data. In practice, signal and noise peak intensities are correlated through shared ionization sources, total ion current, and matrix effects. If C and S are not independent, then enforcing independence in the latent space may cause information loss, limiting the achievable performance.

The paper's own experimental results are consistent with this concern: the "drop" operation (randomly removing 20% of noise peaks) did not improve performance, which may indicate that some "noise" peaks carry residual signal information that is lost when they are removed or suppressed. The improvements, while consistent, are modest (2-12% relative), which may reflect the ceiling imposed by this assumption.

**Impact:** The core modelling assumption is unvalidated and may limit the method's ceiling. **Severity: Major. Fixability: Moderate.** Add a discussion acknowledging this assumption, test sensitivity by varying the strength of the independence constraint, and consider alternatives (e.g., soft independence regularization with a tunable weight).

### W4. Missing critical hyperparameters (Minor)

Several key hyperparameters are not specified:
- The replacement fraction α in the perturbation strategy (Section 3.4.1) is never reported.
- The tolerance threshold γ for non-causal ion localization (Eq. 4) is not quantified.
- The weight or balance between the contrastive loss, sufficiency loss (CE), and purification loss is not specified.

These omissions directly contradict the Reproducibility Statement and prevent independent verification of results.

**Impact:** Limits reproducibility. **Severity: Minor. Fixability: Easy.** Add α, γ, and loss weights to Section 4.2 or an appendix table.

### W5. Cross-species validation limited to one baseline (Minor)

The leave-one-out cross-species validation (Table 3) is conducted only with CasaNovo, not with AdaNovo or π-HelixNovo. This weakens the claim that CausalNovo provides consistent cross-species improvement in a model-agnostic manner. Additionally, the Seven-species cross-validation is only referenced in an appendix table, also with CasaNovo only.

**Impact:** The generality of the cross-species result is unverified for other architectures. **Severity: Minor. Fixability: Moderate.** Extend to at least one additional baseline, or explicitly state the limitation.

### W6. Introduction narrative could be sharpened (Minor)

The introduction has four substantive paragraphs, but the transition from background (P1) to the causal motivation (P2-P3) to method overview (P4) could be more efficient. Paragraph 2 lists many references in a dense citation block without discussing how they relate to the proposed approach. The vulnerability experiment (P3) is effective motivation but its label-dependence should be acknowledged. The method overview (P4) overstates the theoretical contribution relative to what is implemented.

**Severity: Minor. Fixability: Easy.** See annotations for specific paragraph-level revision suggestions.

### W7. No OOD or cross-corpus evaluation (Acknowledged by authors as future work)

As the paper itself notes, evaluation follows the NovoBench setting (training and test from the same source datasets). Recent methods evaluate on out-of-distribution corpora, which better reflects real-world deployment. The paper acknowledges this limitation, which is commendable, but it means the claimed "generalization" and "robustness" are demonstrated only within-distribution.

**Severity: Minor (since acknowledged). Fixability: Non-trivial.** Adding a cross-corpus experiment (e.g., training on Nine-species, testing on HC-PT or vice versa) would substantially strengthen robustness claims.

### W8. Comparison with AdaNovo raises questions about retraining consistency (Verification needed)

Table 1 shows that the AdaNovo baseline published results (0.698, 0.709) are higher than the retrained version (0.681, 0.681). Similarly, CasaNovo published results (0.697, 0.696) are lower than the retrained version (0.741, 0.740). The paper uses † to denote retrained results, which is transparent, but the significant variation (up to 6% difference for AdaNovo) raises questions about whether hyperparameters were optimally tuned for each baseline. The CausalNovo + AdaNovo results (0.744, 0.746) are close to the published AdaNovo (0.698, 0.709) but the relative improvement is difficult to assess when the baseline shifts.

**Severity: Minor (since reported transparently).** The authors should clarify why retrained baselines differ from published results and confirm hyperparameter parity.

### W5 (repeated, ignore) — Issue moved above.

---

**ASCII Diagram — Paper Structure & Evidence Map**

```text
[Problem: Noise robustness in de novo peptide sequencing]
    |
    ├── Claim 1: Existing models learn spurious correlations with noise peaks
    |   └── Evidence: Vulnerability experiment (Fig 1) ✓
    |
    ├── Claim 2: CausalNovo learns causal (signal) representations via SCM+principles
    |   └── Evidence: Ablation studies (Tables 4,5) — partially ✓
    |   └── Gap: SCM assumption C ⟂ S unverified; "causal" implementation is InfoNCE
    |
    ├── Claim 3: Consistent gains (up to 10%) across settings
    |   └── Evidence: Tables 1-3, Figures 3-4 — partially ✓
    |   └── Gap: No variance/significance; OOD not tested
    |
    └── [Core weakness: Causal framing > actual implementation; missing statistical rigor]
```

**ASCII Diagram — Revision Strategy Roadmap**

```text
Priority 0 (high impact, easy fix):
    W1: Rewrite causal framing → "invariant representation learning"
    W2: Add α, γ, loss weights to implementation details
    W6: Soften abstract/intro claims per annotation suggestions

Priority 1 (high impact, moderate effort):
    W2: Add multi-seed variance + significance tests for main tables
    W3: Add discussion of C⟂S assumption + sensitivity analysis

Priority 2 (medium impact, higher effort):
    W7: Add cross-corpus OOD evaluation
    W5: Extend cross-species validation to additional baselines
```

## Score
**Final Score: 6.5/10**

**Rationale:** The paper addresses a practically relevant problem (noise robustness in de novo peptide sequencing) with a technically well-crafted framework that shows consistent empirical improvements across multiple baselines and datasets. The modular design (model-agnostic CEM plugin), the replace-based perturbation strategy, and the thorough ablation studies are genuine strengths. However, the score is constrained by the following factors:

1. **Novelty gap (primary limiting factor):** The causal framing is overstated relative to the actual implementation. The "causal intervention" is a label-guided noise replacement + contrastive learning — a useful technique, but not causal discovery. The sufficiency "principle" is standard cross-entropy. This reduces the conceptual novelty from what the title and abstract promise.

2. **Statistical rigor (secondary limiting factor):** Complete absence of variance reporting and significance testing makes it difficult to assess the reliability of the reported gains. This is a standard expectation for empirical ML papers.

3. **Unverified core assumption:** The SCM's independence assumption (C ⟂ S) is unvalidated and likely violated in real MS data, which may cap the method's performance ceiling.

4. **Reproducibility gaps:** Missing critical hyperparameters (α, γ, loss weights) despite a dedicated reproducibility statement.

The paper presents a practically useful contribution that would benefit from: (a) toning down the causal claims to match the actual technical contribution, (b) adding statistical significance evidence, and (c) filling the reproducibility gaps. With these revisions, the paper could be a solid contribution to the field.

**Scoring breakdown:**
- Research value / significance: 7/10 (important problem, practical approach)
- Novelty of contribution: 5/10 (useful technique, but causal framing inflated)
- Technical soundness: 6/10 (well-designed experiments, but missing statistics)
- Clarity and reproducibility: 6/10 (clear narrative, but missing hyperparameters)
- Empirical support: 7/10 (consistent gains across settings, but no variance)

*Note: External literature verification is unavailable in this run (paper_search API disabled). Novelty and comparison conclusions regarding specific prior methods are based solely on the manuscript's own discussion and should be verified with manual literature review.*
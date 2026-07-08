Now I have all the information I need. Let me produce the final consolidated review.

---

## Summary

This paper introduces CausalNovo, a model-agnostic framework for de novo peptide sequencing that uses theoretical spectra to identify signal vs. noise peaks, then applies contrastive learning objectives (grounded in independence and sufficiency principles) to learn representations that are invariant to noise-peak perturbations. The method is evaluated on three baselines (CasaNovo, AdaNovo, π-HelixNovo) across three datasets (Nine-species, Seven-species, HC-PT) with consistent improvements at amino acid, peptide, and PTM levels. The paper provides thorough diagnostic analyses including ablation studies, cross-species validation, NSR analysis, and attention analysis.

## Strengths

- **Well-motivated problem with empirical grounding.** Figures 1 and 3 demonstrate that perturbing non-signal peaks systematically degrades performance across three architectures. Tightening the m/z tolerance threshold exacerbates the drop, confirming that existing models rely on spurious correlations from noise peaks.

- **Model-agnostic design with consistent gains across architectures.** CausalNovo is evaluated on three distinct baseline architectures (CasaNovo, AdaNovo, π-HelixNovo) across three datasets and three evaluation levels (amino acid, peptide, PTM). Every baseline on every dataset at every level shows improvements, some up to 10%.

- **Thorough diagnostic analysis.** Beyond headline results, the paper provides ablation studies (Tables 4, 5), cross-species generalization (Table 3), NSR analysis (Figure 4), attention analysis (Table 7), robustness to different peak-distinguishing strategies (Table 6), and vulnerability analysis (Figures 1, 3). This is more comprehensive than typical for this area.

- **Honest about limitations.** Section 5 acknowledges the ~2.3× training overhead and, importantly, the protocol gap — the evaluation follows the within-distribution NovoBench protocol rather than the more realistic out-of-distribution protocol used by recent methods like ContraNovo and RankNovo.

## Weaknesses

### Fatal

None.

### Major

- **Overclaimed causal framing.** The paper wraps the contribution in the language of Structural Causal Models, Pearl's *do*-calculus, and causal representation learning. The SCM in Eq. (2) is never learned or identified from data; the "causal intervention" is a label-guided data augmentation (replacing noise peaks identified via theoretical spectra); the "causal factors" are defined *a priori* by theoretical spectrum matching rather than discovered. The real contribution — using domain-knowledge to identify signal peaks and learning invariant representations via contrastive learning — is solid, but the gap between the framing and the actual mechanism inflates the perceived contribution. The paper presents itself as "causality-informed" which is reasonable as a guiding framework, but the SCM vocabulary creates an expectation of causal discovery or causal effect estimation that is not delivered.

- **Missing error bars or statistical significance.** None of the tables (Tables 1, 2, 3, 4, 5, 6) report standard deviations, confidence intervals, or any measure of variance. Given that some claimed improvements are modest (e.g., +0.6% in ablation, +2.4% for CasaNovo on Nine-species), it is difficult to assess whether these differences are statistically significant. This is particularly important for a plug-in module where gains in several settings are small. That said, the consistency of improvement across many settings partially mitigates this concern.

### Minor

- **Baseline comparison concerns.** (a) Some reported baselines (InstaNovo with 0.420 precision on Nine-species, PointNovo with 0.196 on Seven-species) show anomalously low numbers that suggest suboptimal tuning rather than architectural limitations; the "up to 10%" headline should be interpreted against better-tuned baselines. (b) SearchNovo, the strongest competitor, is not tested with CausalNovo despite being described as model-agnostic (though SearchNovo's hybrid search architecture may not be straightforward to adapt). (c) The evaluation follows the easier within-distribution NovoBench protocol rather than the OOD protocol used by recent methods — the paper acknowledges this as future work.

- **The causal intervention requires ground-truth labels during training.** The "causal" vs. "non-causal" peak distinction (Eq. 4) uses the ground-truth peptide to compute the theoretical spectrum. This is a sensible use of domain knowledge and standard practice in the field. However, the attention analysis in Table 7 is then partially tautological: the model was explicitly trained to focus on peaks matching the theoretical spectrum of the correct peptide, so the finding that it attends more to these peaks during inference is partly expected. The paper should discuss this more explicitly.

- **Key hyperparameter α not reported.** The fraction of noise peaks replaced (α) during the causal intervention (Section 3.4.1) is never specified. This affects reproducibility.

### Trivial

- **Several unclear technical claims.** (a) The C ⟂ S assumption (causal and non-causal factors are independent, Eq. 2) is stated without justification; in real mass spectrometry, signal and noise intensities may be correlated. (b) The justification for how maximizing I(z_s; Y) "indirectly lead[s] to the purification of z_c" relies on a citation to Chen et al. (2022) without being self-contained. (c) The RI values in Table 6 are not clearly explained — the caption says "relative improvement" but the numbers do not match a simple relative improvement computation, suggesting a different definition that should be clarified.

## Nice-to-Haves

- Evaluate under the OOD protocol (ContraNovo/RankNovo setting) for stronger generalization claims. The paper already flags this as future work.
- Add a non-causal baseline (e.g., random peak partition or intensity-based threshold) to isolate whether gains come from the specific causal framing or simply from contrastive regularization.
- Report analysis of spectra with very few signal peaks, where the method may replace most peaks and destroy signal.
- Report standard deviations over multiple runs.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **"Causal framing is structural/fatal"** — Downgraded from Fatal to Major. The paper genuinely uses causal concepts (intervention, independence, sufficiency) as an organizing framework and does not claim to solve causal discovery or causal effect estimation. Many papers in top venues use causal framing at a similar level of abstraction. The criticism is valid but not fatal.
- **"Table 4/5 checkmark pattern rendering"** — Removed as a parser artifact, not an author error.
- **"Generic related work section"** — Removed as too generic; the related work adequately covers de novo sequencing and causal ML for a methods paper.
- **"No discussion of CEM inductive bias"** — Removed as an architecture design choice not central to the paper's claims.
- **"Missing discussion of specific CausalML techniques"** — Removed; the related work section is sufficient for context.
- **"Missing multiple ion types analysis concern"** — Removed because the paper already addresses this in Section 4.4 with an 18-ion-type analysis.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

The paper would be most improved by (1) toning down the causal framing to match what is actually delivered — describe it as domain-knowledge-guided invariant representation learning rather than causal representation learning; (2) reporting results over multiple random seeds with standard deviations for the key tables; (3) specifying the missing hyperparameter α; and (4) adding a simple non-causal ablation (e.g., random peak partitioning) to demonstrate that the specific theoretical-spectrum-based partition is what drives the gains.

## Score and Decision

**Calibration.** I used three rounds of retrieval. The closest topical anchor is **ReNovo** (6.50, Accept) — a de novo peptide sequencing paper whose weighted strengths (10.38, 10.51, 10.66) are comparable to this paper's (10.14, 9.82, 9.11) and whose most negative weaknesses (-3.27, -2.58, -1.39) are similar in magnitude to this paper's worst negative (-1.75). A second topical anchor, **Distilling Non-Autoregressive Model Knowledge** (4.25, Reject), had more severe negative-weight weaknesses (-7.20, -5.65) that this paper lacks. The **Feature Matching Intervention** paper (4.25, Reject) also had stronger negative weights (-5.16) for similar framing concerns. The **Multi-View Causal Representation Learning** paper (7.00, Accept) is a pure theory paper in a different genre. Based on this comparison, my round-1 bracket was [5.5, 7.5]. Within this bracket, the ReNovo anchor (6.50) is the most directly comparable — both papers make a solid empirical contribution to de novo sequencing with consistent improvements, and both have weaknesses about framing/comparisons that are present but not fatal. The CausalNovo paper's main weakness (overclaimed causal framing, weight 3.12) is a moderate concern comparable in magnitude to ReNovo's missing-related-work concerns (-3.27, -2.58). The missing error bars (1.62) are a modest concern. The cumulative evidence from the weighted-item comparison places this paper slightly below ReNovo (6.50) due to the framing overclaim being more structural, but well above the 4.25 anchors that had fundamental novelty concerns. Final score: **6.0**.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>
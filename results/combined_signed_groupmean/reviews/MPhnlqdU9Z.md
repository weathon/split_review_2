Now I have a clear picture. Let me construct the final review with the score placed in context.

**Final bracket resolution:** My round-1 bracket was 3.5–5.5. The closest anchors are NAP (4.75, Reject), NC-OOD (4.50, Reject), and HACk-OOD (5.00, Reject). The paper under review has a stronger conceptual contribution than any of these (monitorability is genuinely novel) but weaker empirical validation (no correlation coefficient, no variance). The scoring model rated the three principal weaknesses at -9.96, -9.58, and -8.99 — comparable in magnitude to NAP's strongest weaknesses (-9.93, -10.00). NAP had stronger empirical results but its novelty was questioned; this paper has cleaner novelty but weaker validation. I place it at **4.5**, between NC-OOD (4.50) and NAP (4.75).

## Summary

This paper introduces "monitorability" — the intrinsic ability of a neural network's internal representations to support runtime error detection — and proposes a formal definition (Definition 1) along with a practical metric, the MIRA Score (Definition 2). MIRA quantifies monitorability by perturbing ID inputs with FGSM, measuring the Mahalanobis-distance-based separability of perturbed vs. unperturbed penultimate-layer features, and integrating over perturbation magnitudes. The paper validates MIRA across three modalities (vision, tabular, NLP) by comparing it against the best of three OoD detection methods (ODIN, Mahalanobis distance, Energy-based scoring).

## Strengths

- **Genuinely novel concept.** The paper correctly identifies that existing OoD detection methods measure *whether* a model *can* be monitored, but no prior work defines *how inherently monitorable* a model is as a property of its learned representations. This framing (Section 3.1, Figure 1) clearly distinguishes the intrinsic property from the choice of detector. **[impact=+9.52]**

- **Clean formal definition.** Definition 1 (Section 3.2) formalizes monitorability as the existence of a separating set Z^l in feature space that separates correct from erroneous predictions. It is task-agnostic (accommodates both classification and regression via a general loss function) and layer-agnostic — a genuine theoretical contribution. **[impact=+10.00]**

- **Broad evaluation scope.** The paper tests across three modalities (vision, tabular, NLP), multiple architectures per modality (ResNet, DenseNet, ViT, MLPs, Transformers, RoBERTa, DistilBERT, ELECTRA, DeBERTaV3), and seven OoD datasets in vision alone (Tables 1–3). **[impact=+5.49]**

- **Computationally practical.** MIRA requires only ID data and FGSM perturbations, making it suitable for pre-deployment model selection without the expense of tuning and running multiple OoD detectors. **[impact=+4.33]**

## Weaknesses

### Major

- **No quantitative correlation metric reported.** The paper repeatedly states that MIRA "correlates with" or "aligns with" OoD detection performance (Sections 1, 4.4, Conclusion) but never computes a single correlation coefficient (Spearman's ρ, Pearson's r, Kendall's τ). The evidence consists entirely of qualitative table inspection. The ordering is not perfect in every case — for example, in NLP (Table 3), DistilBERT (MIRA=2015.66, best AUROC=76.54) is nearly tied with RoBERTa (MIRA=2632.94, best AUROC=77.16) despite a 30% lower MIRA, which is not discussed. Without a rank-correlation coefficient aggregated across all model/OoD-dataset pairs, the reader cannot evaluate whether the claimed correlation is genuinely strong or driven entirely by extreme endpoints (ViT vs. CustomNet). This is the single most important gap in the paper's central claim. **[impact=-9.96]**

- **No variance or confidence estimates.** All experiments use fixed random seeds with a single run per configuration (Reproducibility Statement). MIRA involves random perturbations (FGSM with random start) and an integral over ε. Without any estimate of variance (e.g., standard deviation across 3–5 seeds), the reader cannot assess whether reported MIRA values like 6.05 (ResNet-18) and 16.01 (DenseNet) are reliably different from each other or whether they fluctuate by orders of magnitude across runs. **[impact=-9.58]**

- **Gap between the formal definition and the practical metric is not bridged.** Definition 1 defines monitorability via the existence of an *arbitrary* set Z^l in feature space; no constraint is placed on its geometry. MIRA, by contrast, measures a very specific quantity: Gaussian separability of FGSM-perturbed features under Mahalanobis distance. A model could satisfy Definition 1 (via a complex, non-convex Z^l) while having low MIRA (because the separability is not Gaussian), and vice versa. The paper motivates MIRA by intuition (Figure 1) but provides no theorem, bound, or formal argument connecting the two. This limits the theoretical grounding of the proposed metric. **[impact=-8.99]**

### Minor

- **Validation entanglement with Mahalanobis-based detection.** MIRA computes Mahalanobis distance on penultimate-layer features with per-class Gaussian modeling — the same mathematical machinery used by the Mahalanobis OoD detector (Lee et al., 2018b), which is the most frequent winner among the three validation methods. This reduces the independence of the validation signal, though it does not invalidate it (the three detectors provide some diversity, and MIRA measures perturbed-feature separability, not OoD detection directly). **[impact=-0.04]**

- **No sensitivity analysis for the perturbation range parameter.** The [ε_min, ε_max] interval depends on an accuracy-reduction threshold (Appendix B.6). Without studying whether model rankings under MIRA are stable with respect to this threshold choice, cross-model comparisons are contingent on an arbitrary parameter. The paper acknowledges this as a limitation (Section 6) but does not address it. **[impact=-0.00]**

- **No ablation of the perturbation strategy.** FGSM is used throughout without comparison to alternatives (random perturbations, PGD, or no perturbation). The choice is justified only by computational efficiency (Section 4.2), not by informativeness. **[impact=-0.10]**

## Nice-to-Haves

- Report Spearman's rank correlation coefficient between MIRA and best-per-method AUROC across all model/OoD-dataset pairs, with 95% confidence intervals via bootstrap.
- Repeat all MIRA computations over 3–5 random seeds and report mean ± std.
- Include at least one monitoring method in the validation set that avoids Mahalanobis-style Gaussian assumptions (e.g., a simple confidence-threshold baseline or an activation-box method).
- Perform a sensitivity analysis varying the accuracy-reduction threshold used to set ε_min.
- Compare FGSM against alternative perturbation strategies (PGD, random noise).

## Removed Points

These points from the input reviews are flagged for removal; treat them with caution:

1. **"The Mahalanobis detector dominates 11 of 12 model/OoD-set blocks"** — Removed because this is an overcount. In Table 1, ODIN and Energy win on many datasets (e.g., DenseNet CIFAR-10, CustomNet CIFAR-10, ResNet-18 CIFAR-100). The core concern about shared methodology is kept (as a minor weakness) but the inflated claim is dropped.

2. **"p(ε) not specified"** — Removed because this detail is likely in the (parser-stripped) appendix. The paper states p(ε) is user-defined and gives uniform as an example.

3. **"Missing recent OoD methods (ReAct, ASH, KNN)"** — Removed per rule on missing related works.

4. **"Definition 1 is too strong / impossible to satisfy perfectly"** — Removed because Definition 1 is presented as an abstract formal ideal; the paper itself calls it "abstract." Many formal definitions in ML are similarly idealized.

5. **"S_0 normalization and cross-layer comparability issue"** — Removed as a minor technical point that doesn't threaten the core claims.

6. **"Average column unclear formatting"** — Removed as a parser artifact; the original PDF likely formats it clearly.

7. **"MIRA scores not interpretable across domains"** — Removed because the paper only compares within domains and does not claim cross-domain interpretability.

8. **"Should cite more related work"** — Removed per hard rule.

## Novel Insights

None beyond the paper's own contributions. The reviews surface the key tension between the paper's strong conceptual contribution (monitorability as a formal property) and its incomplete empirical validation, but do not identify additional novel angles.

## Suggestions

- Compute and report Spearman's rank correlation between MIRA scores and best AUROC across all model/OoD-dataset pairs, with bootstrap confidence intervals.
- Run experiments over multiple seeds (3–5) and report mean ± std for MIRA values.
- Add at least one non-Mahalanobis validation target to break the methodological entanglement.
- Study sensitivity of model rankings under MIRA to the accuracy-reduction threshold used for ε_min.
- Ablate the perturbation strategy: compare FGSM against PGD, random noise, and the unperturbed baseline.

## Score and Decision

**Calibration Report:** All anchors retrieved across all rounds are listed below.

| Anchor | Path | Avg Score | Round | Itemized | Comparison |
|--------|------|-----------|-------|----------|------------|
| Red Pill or Blue Pill? | l5ouuojPGe.md | 3.00 | R1 | Yes | Weaker: no novel conceptual contribution, severe presentation issues |
| Fantastic DNN-Classifier | Trg9qb0d5U.md | 3.67 | R1 | Yes | Weaker: very limited evaluation (2 models, 2 datasets) |
| NC-OOD | VAmVEghgoC.md | 4.50 | R1/R2 | Yes | Comparable: similar-magnitude weaknesses, this paper has cleaner novelty |
| NC-OOD (2nd variant) | Gr8nHvOivO.md | 4.50 | R2 | No | Similar to above |
| NAP | YMgMGPjUPg.md | 4.75 | R1 | Yes | Comparable: NAP had stronger empirical results but novelty concerns; MIRA has cleaner novelty but weaker validation |
| Pathologies of OOD | hliRjXgTDK.md | 4.75 | R2 | No | Critical paper, not directly comparable |
| HACk-OOD | xE5ZaZGqBW.md | 5.00 | R2 | No | Stronger empirical results |
| Provable Post-Deployment | lHBQrqVYji.md | 5.00 | R2 | Yes | Stronger theory, weaker evaluation breadth |
| Advancing OOD via KAN | 1F8xTfv6ah.md | 5.25 | R1/R2 | Yes | Stronger empirical results, accepted |
| MD-LSM | hoEanaoP4i.md | 6.00 | R1 | Yes | Stronger theoretical grounding, broader reviewer support |

**Placing the paper:** The round-1 bracket was 3.5–5.5. The paper's strongest weaknesses (no correlation metric at -9.96, no variance at -9.58, theory-to-metric gap at -8.99) are comparable in magnitude to the top weaknesses of NAP (4.75) and NC-OOD (4.50). Its conceptual contribution is stronger than either, but its empirical validation is weaker than NAP's. The paper sits between 4.0 and 5.0, closest to NC-OOD (4.50) — a borderline reject with a genuine insight that needs substantially stronger empirical support.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>
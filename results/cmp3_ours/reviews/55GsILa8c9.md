Now I have a clear calibration picture. Let me write the final review.

## Summary

CausalNovo introduces a causality-inspired, model-agnostic framework for de novo peptide sequencing. It augments existing encoder-decoder architectures with a Causality Extraction Module (CEM) that learns to weight signal (causal) fragment ions over noise peaks, using contrastive learning between original and perturbed spectra to encourage representation invariance. On three benchmark datasets (Nine-species, Seven-species, HC-PT) and three base models (CasaNovo, AdaNovo, π-HelixNovo), CausalNovo delivers consistent gains at amino acid, peptide, and PTM levels — e.g., +12.0 pp in amino acid precision on Seven-species, +14.2 pp on HC-PT.

## Strengths

- **Consistent and practically meaningful gains across models, datasets, and metric families.** Every baseline improves under CausalNovo on all three datasets and all three metric tiers. Many improvements are large by the field's standards (up to 10%+), and the pattern holds across 3 distinct architectures, ruling out model-specific artifacts.

- **Multi-faceted diagnostic evidence supporting the claimed mechanism.** The NSR analysis (Figure 4) shows CausalNovo's advantage holds across the full noise distribution, not just on average. The attention analysis (Table 7) provides direct mechanistic evidence: CausalNovo attends to 3 causal peaks in 32.87% of predictions vs. 19.26% for the baseline, and the proportion attending to zero causal peaks drops from 12.73% to 10.76%. The 18-ion-type analysis (Table 6) tests robustness to ion-type choice. These go well beyond headline metrics.

- **Model-agnostic design with negligible inference overhead.** CausalNovo wraps around existing architectures without changing their core structure, demonstrated across three distinct base models. Inference overhead is <1%, making it practically deployable. The code is provided.

## Weaknesses

### Major

- **The causal framing substantially overstates what the method actually does, creating a structural disconnect between rhetoric and implementation.** The paper presents a Pearlian SCM (Eq. 2: X = f(C,S), Y = g(C), C ⟂ S) and claims to perform a do-intervention on non-causal factors S. The implementation (Section 3.4.1) is: (a) compute a theoretical spectrum from the known ground-truth peptide, (b) label peaks outside m/z tolerance γ as "non-causal," (c) randomly replace a fraction α of those peaks with other non-causal peaks from the batch. This is data augmentation on X, not a structural intervention on the data-generating process. The contrastive objective (Eq. 5) encourages representation invariance under this perturbation — a well-studied robustness regularization. The causal formalism does not constrain the design in any way that a "signal-aware denoising + contrastive invariance" description would not also produce. The practical contribution (consistent gains, thorough analysis) holds up regardless, but the paper claims a more fundamental contribution than the method actually delivers.

### Minor

- **Key hyperparameters for the causal intervention are not reported.** The replacement fraction α (Section 3.4.1) and the tolerance threshold γ (Eq. 4) used during training are never specified. These determine the perturbation strength and the definition of "non-causal" peaks; omitting them hinders reproducibility.

- **The warm-up schedule description appears inconsistent.** The paper states "100k warm-up steps" over a 30-epoch schedule with batch size 32. For smaller datasets (e.g., HC-PT, ~100K spectra), this would exceed the total training steps. The schedule needs clarification or correction.

- **The ablation study does not control for increased parameter count.** Adding the CEM module (3 Transformer layers + MLP) increases model capacity. The ablation (Table 4) removes learning objectives but keeps the CEM architecture fixed. A control with additional Transformer layers of comparable size (without the causal framework) would disentangle whether gains come from the causal inductive bias or simply from greater capacity and auxiliary training signals.

- **The main evaluation protocol does not fully support the generalization claim that motivates the paper.** The central motivation is that existing models fail under realistic distribution shifts (different instruments, protocols, contaminant profiles). Yet the primary evaluation follows NovoBench's in-distribution train/test splits. The cross-species validation (Table 3) tests generalization across species within the same instrument/lab, and the NSR/vulnerability analyses test synthetic perturbations within the same distribution. The paper honestly acknowledges this limitation in the conclusion ("Assessing CausalNovo under this protocol would better reflect real-world utility"), but the gap between the stated motivation and the tested scenarios remains.

- **Confidence intervals / variance estimates are not reported** for the main results (Tables 1–2). Given that some improvements are modest (e.g., +2.4% on Nine-species AA precision for CasaNovo), variance information would help assess reliability.

- **Training time increase (~2.3×) is substantial** and the paper does not break down where this cost originates (CEM forward pass? dual-spectrum processing? contrastive loss computation?), making it hard to assess where optimization effort goes.

### Trivial

None.

## Nice-to-Haves

- A parameter-matched control experiment (e.g., additional Transformer layers replacing the CEM) to isolate whether gains come from the causal formulation or from additional capacity.
- Evaluation under the out-of-distribution protocol used by ContraNovo/RankNovo to directly test the generalization claim the paper motivates.
- Breakdown of the 2.3× training time increase by component.
- Specification of α and γ values used during training.

## Removed Points

The following points from the input reviews were removed or merged:

- *Figure 2A inconsistency (C as "charge state" vs. "causal factors"):* This appears in a parser-generated description of a figure image, not in the paper's text. The text (Section 3.2) consistently describes C as "causal factors." Per hard rules, parser-artifact-based criticisms are removed.
- *Table 4/5 formatting (identical checkmarks):* Parser artifact, not an author problem. Per hard rules, formatting nitpicks are removed.
- *"Missing related works":* Per hard rules, this is not verifiable without external sources.
- *"Causal language conflating two meanings" in the Introduction:* This is subsumed into the Major weakness on framing inflation; removed as redundant.
- *Speculative "could be" weaknesses about confounders and proxy metrics:* These were category-driven noise from the sweep, not specific identified problems. Removed.
- *"Strengthening the Paper" suggestions that duplicate existing weaknesses:* Merged into weakness entries.

## Novel Insights

The harsh critic's central insight is that the paper's practical mechanism (signal-aware contrastive denoising) is well-implemented and convincingly evaluated, but the Pearlian causal formalism is decorative rather than operational. The critic correctly identifies that the "intervention" is data augmentation in X, not a do-operation on the structural equation for S, and that the resulting contrastive objective is conceptually close to domain-invariant representation learning. This is a framing mismatch, not a methodological flaw — but it matters for how the contribution is interpreted. The paper's genuine contribution is a model-agnostic approach that uses ground-truth labels to identify signal peaks, learns to weight them via a gating module, and regularizes representations via contrastive learning — not causal discovery. The paper would be stronger if it explicitly stated where the causal formalism leads to design choices that a simpler "attend to signal peaks" approach would not.

## Suggestions

1. Recalibrate the causal claims to match the actual mechanism. The method is better described as a signal-aware denoising and representation-robustness framework, not a Pearlian causal intervention.
2. Specify α (replacement fraction) and γ (tolerance threshold) used during training.
3. Add a parameter-matched control: extra Transformer layers of comparable size to the CEM, without the causal framework.
4. Clarify the warm-up schedule and reconcile it with total training steps for each dataset.
5. Add confidence intervals or standard deviations to main results.
6. Break down the 2.3× training time increase.

## Score and Decision

**Calibration anchors retrieved (all rounds):**

| Paper | Avg Score | Round | Comparison |
|-------|-----------|-------|------------|
| nSDOkm0SKo (financial markets) | 1.00 | R1 | Unrelated; much weaker paper |
| gwZ90hFSL2 (cross-lingual robots) | 1.00 | R1 | Unrelated; much weaker |
| 5lUdTogEL3 (person re-id) | 1.00 | R1 | Unrelated; much weaker |
| GF6UrrTWp1 (invariance starvation) | 2.60 | R1 | Conceptual overlap on spurious correlations but much weaker empirical work |
| AvXrppAS2o (causal structure learning) | 3.00 | R1 | Causal framing domain; paper has less compelling evaluation |
| TRHyAnInUC (causal discovery) | 3.25 | R1 | Causal discovery paper; different task |
| I2ZYngkRW6 (CrossNovo, de novo seq.) | 4.25 | R1/R2 | Most directly comparable; CausalNovo has stronger evaluation and consistent gains |
| sFJr7okOBi (NL2ProGPT, protein design) | 4.50 | R1 | Protein domain; CausalNovo has cleaner evaluation |
| lgnAEBE1Xq (contrastive unlearning) | 5.00 | R2 | Contrastive learning overlap; different task/dataset |
| EMKZyZSl70 (DualContrast, disentanglement) | 4.67 | R2 | Disentanglement overlap; CausalNovo is more applied with stronger results |
| wRkfniZIBl (RNA contrastive) | 4.33 | R2 | Contrastive learning in biology; less comprehensive evaluation |
| **uQnvYP7yX9 (ReNovo, de novo seq.)** | **6.50** | **R1/R2** | **Best anchor: same task, accepted; CausalNovo has more diagnostic analysis but more framing inflation** |
| 78tc3EiUrN (MADGEN, MS molecule gen.) | 6.00 | R2 | Similar MS domain; accepted |
| jqmptcSNVG (PepHAR, peptide design) | 6.20 | R2 | Peptide domain; accepted |
| 4ktJJBvvUd (AbNovo, antibody design) | 6.67 | R2 | Peptide/antibody domain; accepted; stronger overall evaluation |
| zMPHKOmQNb (protein discovery) | 8.00 | R1 | Protein generation; top-tier work |
| xByvdb3DCm (causal discovery, selection bias) | 8.00 | R1 | Top-tier causal work; different task |

**Round 1 bracket:** 5.0–7.0. **Round 2 narrowing:** 5.5–6.5, anchored primarily against ReNovo (6.50) and MADGEN (6.00) in the same task domain.

**Final score:** 6.0

**Rationale:** The paper presents a practically effective framework with unusually consistent and broad empirical gains, backed by informative diagnostic analyses. The causal framing is significantly overstated — the method is best understood as a signal-aware denoising + contrastive invariance approach, not a Pearlian causal framework — but the empirical contribution is real and would hold up without the inflated rhetoric. The evaluation is thorough within the NovoBench protocol but does not fully support the out-of-distribution generalization claims that motivate the paper (a limitation the authors honestly acknowledge). The framing mismatch is the primary weakness; it is addressable through recalibration rather than requiring new experiments. On balance, the practical contribution and evaluation quality merit publication.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>
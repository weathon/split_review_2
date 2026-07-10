## Summary

This paper proposes HiTNet, a dual-stream architecture for multimodal sentiment analysis under frame-level missing data. The hippocampal-inspired intra-modal enhancement stream uses semantic memory and sparse activation to reconstruct modality-specific features, while the thalamic-inspired inter-modal regulation stream uses confidence-weighted cross-modal completion. Experiments on MOSI, MOSEI, and SIMS datasets are presented.

## Strengths

- **The problem is well-motivated and practically relevant.** Frame-level missingness across all modalities simultaneously (Section 1, Figure 1) is a harder and more realistic problem than single-modality absence. The paper correctly identifies that prior work relying on cross-modal consistency for completion neglects residual intra-modal signal — a genuine gap.

- **The dual-stream architectural design is structurally coherent.** The hippocampal-inspired intra-modal stream (Section 3.4) and thalamic-inspired inter-modal stream (Section 3.5) each target a distinct deficiency in prior work. The feature-distance analysis (Figure 4) provides evidence that both streams move representations closer to the complete-feature distribution.

- **The ablation study is thorough for this area.** Table 3 tests each of the four major components (SMM, CPM, Intra stream, Inter stream) and each of the four loss terms individually on two datasets, going well beyond a minimal "remove one thing" check.

- **The modality-level missingness results (Table 4)** show a striking ~10% improvement on the {V} and {A} conditions (59.33% vs. 55.25% for the next best, TETFN), demonstrating that the inter-modal regulation stream adds capability not present in prior methods.

## Weaknesses

### Major

- **Table 1 contains suspicious data entries that undermine the reliability of the SOTA comparison.** The TETFN row reports *identical* Acc-2 (69.76/67.68), F1 (65.69/63.29), and MAE (1.087) for both MOSI and MOSEI — datasets with very different sizes (2,199 vs. 22,856) and label distributions. Acc-7 is also identical (30.30) despite differing substantially for every other method in the table (e.g., CENET: 30.38 vs. 47.18; LNLN: 34.26 vs. 45.42). The TFR-Net row similarly shows identical Acc-5 (34.67) across both datasets. The paper states these numbers are "reported as in LNLTN" (Section 4.4), but the paper is responsible for the accuracy of its comparison table. Since the headline contribution ("1.5%–2.0% average accuracy improvements over state-of-the-art methods") depends on outperforming these baselines, the empirical foundation is compromised.

- **The loss ablation results contradict the paper's own claims.** Section 4.5 states "excluding any of these losses leads to a noticeable performance degradation." Yet in Table 3, removing the utilization balance loss ("w/o L_abs") *improves* MOSI Acc-7 from 35.26 to 35.41, and on SIMS, removing L_abs (F1: 78.13 vs. 77.33), L_cp (F1: 77.57 vs. 77.33), or L_enc (F1: 79.03 vs. 77.33) all improve F1 over the full model. The empirical data directly contradicts the claim that each loss component is indispensable.

### Minor

- **No measures of variance are reported anywhere.** Section 4.3 states experiments use three random seeds and report averages, but all tables (1, 2, 3, 4) show only point estimates. Without standard deviations or confidence intervals, the claimed 1–2% improvements over baselines cannot be assessed for statistical significance — especially on datasets where baseline methods show non-trivial variance across runs.

- **The headline claim from the abstract** ("72.20% accuracy under extreme 90% missing conditions on MOSEI") does not appear in the main experimental results. Figure 3 covers missing rates only up to 50%; Figures 4 and 5 use the 90% setting but do not report this accuracy value. The paper references Appendix B.3 for detailed missing-rate breakdowns, but a central quantitative result should appear in the main paper.

- **The SOTA claim on SIMS is overstated.** In Table 2, P-RMF outperforms HiTNet on MAE (0.500 vs. 0.504, where lower is better) and Corr (0.414 vs. 0.389, where higher is better). The paper acknowledges this indirectly as "highly competitive results," but the bold formatting and emphasis on "a remarkable 4.53% improvement in Acc-3" gives a misleading impression of overall dominance. The claimed SOTA status applies only to a subset of metrics on SIMS.

- **The baseline comparison (Tables 1, 2) uses results "reported as in LNLTN"** rather than being re-run in a controlled setting. This means different methods were evaluated under potentially different codebases, random seeds, and hyperparameters. At minimum, the strongest baselines (LNLN, P-RMF) should be re-run in the same codebase for a fair comparison.

- **In Table 4 (modality-level missingness), LNLN shows identical Acc-2 values (49.03) for the {V}, {A}, and {V,A} conditions** — indicating that LNLN's predictions are entirely dominated by text and do not use visual/audio information when those modalities are present. This is not discussed in the paper, making the 10% advantage of HiTNet on these conditions appear more impressive than it actually is, since the baseline is effectively ignoring the available visual/audio signal.

### Trivial

- The naming of the reference method is inconsistent: LNLN in the related work and Tables 1/4, LNLTN in Sections 4.2/4.4, and LNLT in Table 2. The loss names "L_abs" and "L_enc" in Table 3 do not correspond to the four losses defined in Section 3.7 (L_main, L_ubl, L_cp, L_rec).

## Nice-to-Haves

- Justify or analyze sensitivity to the memory bank size (N=64, set without discussion or ablation).
- The "sparse" activation network activates k=3 of n=5 sub-networks (60%), which is not particularly sparse.
- A controlled comparison against non-biological versions of the same components (e.g., simple key-value memory without gating, uniform confidence weighting) would help disentangle whether the biological framing constrained the design or is purely rhetorical motivation.

## Removed Points

- **Biological inspiration is rhetorical/not analytically connected**: Removed. The paper clearly states the mechanisms are "inspired by" neuroscience, an acceptable framing convention in ML. Each component has a stated functional motivation independent of the biological analogy.
- **Citing Kanerva/Hopfield but not implementing them**: Removed. The paper uses these as conceptual references for content-addressable memory, a standard intellectual lineage citation.
- **Pure formatting/style nitpicks**: Removed per policy.
- **Missing appendix content criticisms**: Removed per policy (the parser strips appendices from all papers; they exist in the original submission).

## Novel Insights

None beyond the paper's own contributions. The reviews validate the paper's stated architectural strengths while identifying verification issues in the baseline table and contradictions in the ablation analysis, but no genuinely novel synthesis emerged.

## Suggestions

1. Re-run the strongest baselines (LNLN, P-RMF, TETFN, ALMT) in your own codebase with identical missingness simulation and random seeds. Report means and standard deviations over 3+ runs.
2. Correct the TETFN and TFR-Net entries in Table 1. If the numbers are correct as reported in LNLTN, add a discussion justifying why; if they are errors, fix them.
3. Add the 90% missing-rate accuracy (72.20%) to the main experimental results rather than deferring to the appendix.
4. Revise the claim in Section 4.5 that each loss is "indispensable" — the data in Table 3 contradicts this for several loss/metric combinations.
5. Report standard deviations for all metrics across random seeds.
6. Qualify the SIMS SOTA claim to accurately reflect that P-RMF achieves better MAE and Corr.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>
## Summary

HiTNet proposes a dual-stream architecture for multimodal sentiment analysis under frame-level missing data. The hippocampal-inspired intra-modal stream uses semantic memory modules and sparse activation networks to recover modality-specific information, while the thalamic-inspired inter-modal stream estimates modality confidence to guide adaptive cross-modal completion. Experiments on MOSI, MOSEI, and SIMS show competitive results, particularly strong under modality-level missing conditions.

## Strengths

1. **Well-motivated problem framing.** The paper tackles frame-level missingness across all modalities simultaneously, which is both more realistic and more challenging than the modality-level missingness common in prior work. Section 1 clearly distinguishes these two missing-data scenarios.

2. **Principled neurobiological grounding.** The hippocampal-thalamic analogy is substantively connected to the design: the hippocampal stream is tied to established computational memory models (Sparse Distributed Memory, Hopfield Networks) in Section 1, and the thalamic stream's confidence-gating mechanism addresses a genuine gap — prior methods treat all cross-modal information equally, risking redundancy (Section 3.5).

3. **Comprehensive evaluation scope.** Three datasets (MOSI, MOSEI, SIMS) with multiple metrics (Acc-2/5/7, F1, MAE, Corr), ablation studies for both components and losses, completion visualization (Figure 4), confusion matrices (Figure 5), and separate modality-level missing analysis (Table 4).

4. **Strong modality-level missing results.** In Table 4, HiTNet achieves ~59% Acc-2 on single-modality visual-only and audio-only conditions on MOSI — a ~10-point improvement over the next best method (TETFN at ~55%). This is a large, clean gain that directly validates the intra-modal enhancement stream's ability to work with minimal input.

## Weaknesses

### Major

1. **TETFN baseline results are duplicated across datasets, undermining the main comparison.** In Table 1, the TETFN row shows Acc-7=30.30, Acc-2=69.76/67.68, F1=65.69/63.29, and MAE=1.087 — numerically identical for both MOSI (2,199 clips, 686 test) and MOSEI (22,856 clips, 4,659 test). Only Acc-5 (34.34 vs. 47.70) and Corr (0.507 vs. 0.508) differ. This duplication across two datasets of substantially different scale and difficulty is implausible for real experimental results. The paper states these numbers are cited from LNLTN and no baselines were re-run (Section 4.4). The central claim of "1.5%–2.0% average accuracy improvements" depends on these baseline comparisons, which are now unreliable. The authors must either (a) re-run all baselines in a consistent framework with variance estimates, or (b) provide verified evidence that the TETFN numbers are correct. Without this, the comparative evaluation cannot be trusted.

### Minor

2. **Loss ablation overclaim.** The paper asserts that "each loss component plays a complementary and indispensable role" (Section 4.5), but the data in Table 3 show this is overstated. Removing the utilization balance loss (w/o L\_ubl) on MOSI improves Acc-7 from 35.26 to 35.41 and Acc-5 from 39.22 to 39.40. Removing the reconstruction loss (w/o L\_rec) on SIMS increases F1 from 77.33 to 79.03. While most other metrics do degrade when these losses are removed, calling every component "indispensable" is contradicted by the paper's own data. The authors should acknowledge where specific losses are neutral or slightly harmful on certain metrics and datasets.

3. **No variance or statistical significance reported.** Results are averaged over three random seeds (Section 4.3) but no standard deviations or confidence intervals are reported anywhere. The claimed improvements over the next-best method are often small (HiTNet Acc-7 on MOSI: 35.26 vs. LNLN's 34.26, +1.00; vs. P-RMF's 34.19, +1.07). Ablation differences are even smaller (removing SMM drops Acc-7 by −0.52; removing CPM drops it by −0.39). Without variance estimates, the reader cannot assess whether any of these differences are statistically significant, especially since the missing-rate sampling itself introduces randomness.

4. **Semantic memory module design limitations.** The SMM (Section 3.4) uses N=64 key-value slots across the entire training set (1,284–16,326 training samples), effectively discarding most data. The query is a mean-pooled representation, destroying temporal structure — a query corrupted by frame-level missingness will have a systematically different mean from its complete counterpart, potentially retrieving an irrelevant memory. The argmax retrieval (Eq. 2) is brittle; soft attention over slots would be more robust. The residual gating mechanism (Eq. 3) partially mitigates retrieval errors, but these design choices are not justified or ablated.

5. **Loss weight sensitivity across datasets.** The loss weights α, β, γ vary dramatically: γ (reconstruction loss weight) is 0.1 for MOSI and SIMS but 9.0 for MOSEI — a 90× difference. This extreme variation suggests poor calibration between loss terms and potentially expensive per-dataset tuning. The paper refers to Appendix B.1 for sensitivity analysis, but the main paper should discuss why such different weights are needed and whether performance is stable over a range of values.

6. **Unablated training heuristic.** The training protocol sets half of the samples per modality to have zero missing rate "to avoid overfitting to missing data" (Section 4.2). This non-standard design choice is motivated but not ablated. Since test-time missing rates span 0–0.9, the effect of this heuristic on generalization is unclear.

7. **Confidence perception module not empirically validated.** The CPM is designed to predict modality confidence scores s\_m trained with L2 loss against a soft completeness label ŝ\_m = 1 − r\_m. The paper does not evaluate whether the CPM actually learns accurate confidence scores (e.g., by plotting predicted vs. true missing ratios). This would help validate the module's intended behavior.

### Trivial

None.

## Nice-to-Haves

- **Report per-missing-rate results in the main paper** for at least one dataset and two key metrics, with error bars. The headline "1.5–2.0% average improvement" could be driven entirely by one missing-rate bucket.
- **Report standard deviations** for all main results (Tables 1–2 and ablation Table 3). With three seeds this is trivially reportable.
- **Position SIMS results more precisely** in the main text: HiTNet is SOTA on classification metrics but not on regression metrics (MAE, Corr) where P-RMF is better.

## Removed Points

- *"Abstract claim of 72.20% under 90% missing not verifiable"* — This is in Appendix B.3, which is standard practice. Removed.
- *"No baselines were re-run"* — The paper explicitly states results are cited from LNLTN. This is common practice and not a weakness per se; the real issue (covered above) is that the cited numbers appear unreliable. Removed as a standalone point and subsumed into the TETFN duplication weakness.
- *"Related work is thin"* — Subjective and insufficiently specific. Removed.
- *"Fabrication" accusation* — The TETFN duplication is suspicious but more likely a data-entry error inherited from LNLTN than fabrication. Reframed as a baseline reliability concern without attributing intent.
- *Various section-by-section formatting and style observations* — Too granular for a review. Removed per hard rules on formatting/style.

## Novel Insights

The harsh critique's key insight is that the TETFN baseline duplication across MOSI and MOSEI is a data-integrity red flag that the paper itself did not flag. Since all baselines are cited from LNLTN, the paper effectively outsourced its entire comparative evaluation to another paper's results without independent verification. This observation — that a single duplicated metric block can compromise an entire SOTA-comparison table — is a useful cautionary point for the authors and the community. The loss-ablation-overclaim observation (that "indispensable" is contradicted by the paper's own table) is also worth noting, though the contradiction is milder than the critique suggests since most metrics do degrade.

## Suggestions

1. **Re-run all baselines** in your own framework under identical training/evaluation conditions and report means and standard deviations over at least 5 seeds. This is the single most important revision.
2. **Verify the TETFN numbers** (and other LNLTN-cited numbers) against original papers. If the duplication is a copying error, correct Table 1 and report the corrected results.
3. **Tone down the "indispensable" claim** about loss components and honestly report where each loss helps and where it is neutral or slightly harmful.
4. **Add a simple validation of the CPM** — a scatter plot of predicted confidence vs. the true missing ratio would help establish that the module works as intended.
5. **Report per-missing-rate results** (with error bars) for at least one dataset in the main paper so the reader can see whether gains are consistent across missing-rate conditions.

## Score and Decision

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>
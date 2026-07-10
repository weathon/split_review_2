Now let me write the final consolidated review.

## Summary

This paper proposes HiTNet, a dual-stream network for multimodal sentiment analysis under random frame-level missingness across all modalities. The hippocampal-inspired intra-modal stream uses a semantic memory module with dynamic retrieval and sparse activation to reconstruct modality-specific missing content, while the thalamic-inspired inter-modal stream estimates modality confidence to guide adaptive cross-modal completion. Experiments on MOSI, MOSEI, and SIMS show consistent accuracy improvements over strong baselines.

## Strengths

- **Well-motivated problem.** Simultaneous frame-level missingness across all modalities is genuinely harder and less studied than modality-level absence. The paper correctly identifies the limitations of existing cross-modal-consistency approaches and targets a meaningful gap.

- **Comprehensive evaluation protocol.** Experiments span three benchmarks (MOSI, MOSEI, SIMS) with multiple metrics (Acc-7/5/3/2, F1, MAE, Corr), ablation of each component and each loss, modality-level missingness analysis (Table 4), and confusion-matrix visualization.

- **Confusion matrix analysis (Figure 5) provides genuine qualitative insight.** It concretely shows that the LNLN baseline collapses to predicting the neutral class under high missing rates while HiTNet maintains class diversity — a clear and convincing illustration of practical robustness that goes beyond aggregate numbers.

- **Ablation studies are interpretable.** Component ablations (w/o SMM, w/o CPM, w/o Intra, w/o Inter) in Table 3 show the expected degradation patterns, increasing confidence that each module contributes meaningfully.

- **The dual-stream design is a well-reasoned conceptual framework** that cleanly separates two distinct challenges (intra-modal completion via memory retrieval, inter-modal regulation via confidence-weighted attention), making the architecture easy to understand and extend.

## Weaknesses

### Major

- **Factually incorrect claim of universal superiority.** The paper states (line 189) that HiTNet "outperforms all existing methods across all metrics on MOSI and MOSEI." This is false. On **MOSI**, P-RMF achieves better MAE (1.038 vs. 1.043). On **MOSEI**, P-RMF achieves better MAE (0.658 vs. 0.665) **and** better F1-left (79.33 vs. 78.84). The bold-facing in Table 1 is misleading on these entries. This overclaiming is a verifiable error that undermines trust in the paper's reporting and must be corrected.

- **TETFN baseline values raise data-integrity concerns.** In Table 1, the TETFN row reports nearly identical values for MOSI and MOSEI: identical Acc-2 (69.76/67.68), F1 (65.69/63.29), MAE (1.087), and Acc-7 (30.30) on both datasets. Two datasets with very different sizes (2,199 vs. 22,856 clips) and distributions producing nearly identical numbers is not plausible. While the paper states these numbers are reproduced from LNLTN, publishing them without verification is a quality-control failure. If other baselines have similar undetected errors, the entire comparison table could be unreliable.

### Minor

- **72.20% accuracy at 90% missing is only in the abstract.** This is arguably the paper's most striking result, but it appears only in the abstract (line 9) and is not presented or contextualized in the main experimental section. Figure 3 only plots missing rates up to 50%. The only 90% results in the main body are confusion matrices on MOSI (Figure 5) — not the 72.20% MOSEI figure. A result this strong deserves a dedicated table or figure in the main text.

- **Confidence-perception module trains on the wrong target.** The ground-truth confidence label in Eq. (8) is `ŝ_m = 1 - r_m`, where `r_m` is the *artificially introduced* missing rate. This means the module learns to predict a known experimental variable (how many frames the experimenter masked) rather than the actual informativeness or perceptual quality of the signal. A modality could be fully present but noisy/uninformative, or partially missing but retain highly discriminative cues. The claim that the module "quantifies the intrinsic completeness and confidence of modality" (line 115) overstates what the training signal actually measures. The design is a reasonable completeness proxy under the paper's controlled setup, but the framing should be softened.

- **Loss ablation claim is not fully supported.** The paper states "excluding any of these losses leads to a noticeable performance degradation" (line 221), but the ablation table (Table 3) shows that removing the utilization balance loss (labeled "w/o L_abs", almost certainly a typo for L_ubl) yields competitive or better results on some metrics. On SIMS, F1 improves from 77.33 to 78.13. On MOSI, Acc-7 and Acc-5 are slightly higher without this loss (35.41 vs. 35.26, 39.40 vs. 39.22). The claim is directionally correct for most metrics but not uniformly supported.

- **Hierarchical fusion ordering is not ablated.** The paper asserts that placing language modality last "allows it to guide the final semantic integration" (line 135), but this V→A→L ordering choice is not empirically tested against alternatives. Given that language dominance is a well-known property in MSA, an ablation of the ordering would strengthen the claim.

### Trivial

- **Loss weights vary dramatically across datasets.** The reconstruction loss weight γ is 0.1 for MOSI/SIMS but 9.0 for MOSEI — a 90× difference. This suggests the model is sensitive to these hyperparameters and may require substantial per-dataset tuning. Sensitivity analysis is referenced in the appendix.

- **No statistical significance reported.** Results are averaged over only 3 seeds without standard deviations or significance tests. Given that improvements over the strongest competitor (P-RMF) are often < 1.5%, it is unclear whether these differences are statistically reliable.

## Nice-to-Haves

- Provide a memory utilization analysis (how many of the 64 memory units are actively used, how often they are replaced) to clarify whether the memory is meaningfully capturing distinct semantic prototypes.
- The sparse activation network uses only n=5 sub-networks with k=3 activated, which is far smaller than typical sparse MoE systems. The paper could clarify whether this small scale is sufficient for the intended fine-grained modeling.
- Train the CPM on a signal that reflects actual feature quality (e.g., reconstruction error, feature variance) rather than the artificial missing rate, to better align the module's objective with its stated purpose.

## Removed Points

These points were raised in the original reviews but are removed with justification:

- **"Brain inspiration is decorative."** Removed. The paper claims *inspiration*, not biological fidelity. The components are abstracted from neuroscientific principles (SDM, Hopfield networks, thalamic gating) as stated in lines 23–24. Whether the framing is substantive is a matter of opinion, not a verifiable technical flaw. The architecture stands on its own technical merit.

- **"Memory retrieval argmax over corrupted query is a conceptual gap."** Removed. The paper explicitly acknowledges this risk (line 49) and proposes a residual gating mechanism (Eq. 3) to suppress irrelevant retrieved content. The design choice to suppress rather than redirect is a reasonable engineering decision, not a gap.

- **"Small memory capacity (N=64) / small MoE (n=5, k=3)."** Removed. These are design decisions, not flaws. The paper does not claim large-scale memory or MoE as contributions, and the chosen sizes are adequate for the reported results.

- **"Section-by-section notes about missing neuroscientific citations and related-work framing."** Removed as they are minor and speculative (questioning citation sufficiency without offering specific missing references would violate the "do not mention missing related works" rule; questioning the abstract's neuroscientific framing is a presentation preference, not a technical weakness).

## Novel Insights

None beyond the paper's own contributions. The reviews surface structural and presentation issues rather than revealing hidden novel insights about the method.

## Suggestions

1. **Correct the overclaiming in Section 4.4.** Replace "outperforms all existing methods across all metrics" with a precise statement acknowledging that HiTNet excels on classification metrics but does not uniformly beat P-RMF on MAE or all F1 scores. Correct the bold-facing in Table 1 accordingly.
2. **Move the 72.20% result into the main text.** Extend Figure 3's missing-rate axis to 0.9, or add a dedicated table showing accuracy at each missing rate on MOSEI so this claim is substantiated in the main experimental narrative.
3. **Reframe the CPM training objective.** Either train on a signal reflecting actual feature quality, or soften the claim that the module "quantifies intrinsic confidence" to reflect that it measures completeness relative to the known masking rate.
4. **Ablate the hierarchical fusion ordering.** Test V→A→L against other orderings to support the claim that the specific ordering matters.
5. **Add standard deviations** to Tables 1–3 and Table 4.

## Score and Decision

The paper addresses a genuine and underexplored problem with a well-reasoned architecture and a thorough evaluation. The strengths — problem framing, evaluation breadth, confusion-matrix insight, interpretable ablations — are real and well-supported.

However, the paper has two concrete major issues. First, a **verifiable factual error**: the claim of outperforming all methods on all metrics is false (P-RMF has better MAE on all three datasets and better F1-left on MOSEI). Second, the **TETFN baseline values are nearly identical across two very different datasets**, which is a data-integrity concern the paper should have caught.

These issues are correctable in revision but, as presented, they undermine confidence in the paper's reporting. The technical contribution is solid but incremental (modest 1–2% gains on classification metrics with regression trade-offs). On balance, this is a borderline paper.

MY FINAL SCORE: <score>5</score>
MY FINAL DECISION: <decision>Reject</decision>
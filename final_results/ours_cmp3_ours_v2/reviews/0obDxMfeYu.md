Now I have all the information needed. Let me produce the final review.

## Summary
This paper introduces Medix, a framework for OOD detection that uses element-wise median (EWM) of gradients to identify OOD samples from unlabeled "in-the-wild" data mixtures. The method has two stages: (1) a greedy iterative algorithm that filters candidate OOD samples from wild data by measuring how removing each sample shifts the EWM toward the InD mean gradient, and (2) training a binary OOD detector on the identified outliers plus labeled InD data. Theoretical bounds on inlier/outlier misclassification rates are provided, and experiments on CIFAR-10/CIFAR-100 with multiple OOD datasets show strong results against 20 baselines.

## Strengths
- **Novel and well-motivated core idea.** Using element-wise median (EWM) of gradients (rather than mean) for outlier filtering in the in-the-wild OOD setting is genuinely novel. The motivating experiment (Figure 1, Section 3.1) cleanly demonstrates the monotonic relationship between EWM deviation and OOD contamination, providing an intuitive foundation. The paper is among the few works providing any theoretical footing for the in-the-wild OOD setting.

- **Theoretical guarantees for median-based filtering.** Theorems 4.1 and 4.2 provide formal bounds on inlier and outlier misclassification rates, decomposing error into contamination, concentration, and separation effects. The explicit bound showing robustness as long as π < 0.5 (the contamination term π/[2(1-π)]) is analytically clean. The paper also provides looser bounds under only bounded second moments (Theorem C.3), increasing the theory's robustness.

- **Strong and consistent empirical results.** In Tables 1 and 2, Medix achieves the best FPR95 and AUROC across nearly every InD-OOD pair. The improvements are substantial (e.g., CIFAR-100 average FPR95: Medix 5.42% vs. next-best WOODS 6.74% vs. KNN+ 46.40%). The results are averaged over 5 runs with reported standard errors for Medix.

## Weaknesses

### Fatal
None.

### Major
- **Theory analyzes a stylized rule, not the implemented algorithm.** Section 4 is titled "theoretical guarantees of Medix's filtering stage," but Theorems 4.1 and 4.2 bound the error of an "EWM filtering rule" — a one-shot decision criterion on the median. The actual Medix algorithm (Algorithm 1) is an iterative, greedy leave-one-out procedure that at each iteration removes the top-k samples by δ_i score and repeats until convergence. The theorems do not account for: (a) how errors compound across iterations of greedy removal, (b) how the choice of k (up to 20,000) interacts with the bounds, (c) how the convergence threshold ε (Algorithm 1, line 110) interacts with the theoretical ε (Theorem 4.1), or (d) how sequential dependence (removing samples changes the EWM for all subsequent comparisons) is handled. The paper frames the theory as proving guarantees for Medix, but the gap between what is analyzed and what is implemented is not acknowledged. This significantly weakens the claim of "provable guarantees for Medix."

### Minor
- **Missing baseline results in main tables.** CONJ (Peng et al., 2024) and DRL (Zhang et al., 2024) are listed among the 20 baselines (Section 5.1), and the conclusion states Medix "outperformed state-of-the-art methods such as WOODS and DRL." However, neither method appears in the main result tables (Tables 1 and 2). If results exist in the appendix (which is stripped from the review copy), the main text should explicitly direct readers there; as it stands, these claims cannot be verified from the main paper.

- **Ambiguous percentage reporting.** The paper reports improvements such as "outperforming [KNN+] by an average of 40.98%" (Abstract/Introduction). From Table 2: KNN+ = 46.40% FPR95, Medix = 5.42%, a difference of 40.98 *percentage points* (an 88.3% *relative* reduction). Similarly, "reduces the average FPR95 by 1.32% on CIFAR-100" is 1.32 *percentage points* (19.6% relative). The paper should consistently distinguish "percentage points" from "percent relative reduction" to avoid ambiguity, though the large improvements are clear either way.

- **No standard deviations for baseline methods.** Only Medix reports standard errors (shown with ± in Tables 1 and 2). Without variance estimates for baseline methods, it is impossible to assess whether the modest improvements over WOODS (e.g., 1.32 percentage points on CIFAR-100) are statistically significant.

- **Prose-algorithm discrepancy in convergence criterion.** Section 3.1 describes convergence as based on "the change in the L2 distance between two iterations," but Algorithm 1 (line 110) checks `|δ_max| > ε` where δ_max = max(δ_i) is the *maximum per-sample drop within the current iteration*, not the change in d_t between iterations. These are different quantities and should be reconciled.

### Trivial
None.

## Nice-to-Haves
- **Ablation on contamination proportion π.** The paper fixes π = 0.5 across all experiments, and the theoretical bound requires π < 0.5. An experiment varying π (e.g., 0.1 to 0.6) would directly test the claimed robustness boundary.
- **Runtime characterization in main text.** Medix's leave-one-out procedure has non-trivial computational cost. A brief runtime statement (e.g., wall-clock time for CIFAR-100) would help readers assess practical viability; the paper defers this to Appendix A.6.
- **OE with clean OOD data.** OE is evaluated in the mixed-data setting (π=0.5), but OE was designed for a clean auxiliary OOD dataset. Including an OE variant that receives purely OOD data would clarify the comparison between Medix's robustness to mixing and OE in its intended setting.

## Removed Points
These points are flagged to be removed, treat them with caution:

- **"InD classifier trained on half data creates asymmetry."** The Harsh Critic noted Medix uses 25k samples for the InD classifier while baselines use 50k. The paper explicitly acknowledges this (Section 5.3: "This slight difference can be attributed to the fact that our method is trained on 25,000 labeled InD samples, while baseline methods...use the full CIFAR-100 training set"). This is contextual information, not a weakness — it shows Medix achieves strong results with less labeled data. REMOVED.

- **"Computational cost is prohibitive and unaddressed."** The paper explicitly states it evaluates "computation and memory efficiency of Medix" in Appendix A.6, which has been stripped by the review pipeline. The paper cannot be faulted for content present in the full submission. DEMOTED to Nice-to-Have.

- **"Section 3.2 loss function surrogate."** The critic noted the sigmoid surrogate for the 0/1 indicator loss is standard practice. This is a trivial observation that does not constitute a weakness. REMOVED.

## Novel Insights
None beyond the paper's own contributions. The reviews surface a genuine tension between the theoretical framing (which promises guarantees for "Medix's filtering stage") and what the theory actually bounds (a one-shot median rule, not the implemented iterative procedure). This disconnect, rather than any empirical failure, is the paper's most significant limitation.

## Suggestions
1. **Connect the theory to the algorithm.** Either adapt the error bounds to the greedy iterative procedure, or explicitly restate what the theorems bound and how they provide partial (but not complete) guarantees for the implemented algorithm. Even a heuristic argument about why each greedy step preserves the bound would help.
2. **Add CONJ/DRL results to main tables** or clearly state in Section 5.3 that these are deferred.
3. **Disambiguate percentage reporting** (e.g., "40.98 percentage points" vs "88.3% relative reduction").
4. **Report standard deviations for all baselines** in Tables 1 and 2.
5. **Reconcile the convergence criterion** between the prose description in Section 3.1 and Algorithm 1's implementation.

## Score and Decision

**Calibration anchors.** All paths are in `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/`:
- `jlEjB8MVGa.md` — "How Does Unlabeled Data Provably Help Out-of-Distribution Detection?" (avg 6.50, Accept). The closest prior work on provable in-the-wild OOD detection. Uses top singular vector filtering; theory matches algorithm. Medix has a more novel median-based approach and stronger empirical results, but a larger theory-algorithm gap. Score: 6.5 vs. Medix ~6.0.
- `VTYg5ykEGS.md` — "ImageNet-OOD" (avg 6.50, Accept). Benchmark paper analyzing existing OOD methods. Different contribution type. Medix has a novel method rather than analysis, with comparable scope. Score: 6.5 vs. Medix ~6.0.
- `hlijRgXTDK.md` — "Pathologies of OOD Detection" (avg 4.75, Reject). Critique paper with no positive method contribution. Medix has a full method, theory, and experiments. Score: 4.75 vs. Medix ~6.0.
- `iqAbdT35hE.md` — "OOD Detection With Smooth Training" (avg 5.75, Reject). Proposes a training strategy; has theory and experiments but less novelty. Medix has a more novel core idea and stronger results. Score: 5.75 vs. Medix ~6.0.
- Others in band queries (6Z8rZlKpNT, GQhlM0Mavg, am7BPV3Cwo, 0owAtTCOlU) were topically less relevant or reinforced similar calibration.

**Round 1 bracket:** 6.0–7.0. **Round 2 (narrowing):** 6.0–6.5 via comparison with `jlEjB8MVGa.md` (SAL, avg 6.50).

**Final score judgment:** The paper presents a genuinely novel method (median-based gradient filtering for in-the-wild OOD detection), provides real theoretical bounds, and demonstrates very strong empirical results. However, a significant disconnect between the theoretical analysis (which bounds a one-shot median rule) and the actual algorithm (iterative greedy removal) weakens the paper's claimed "provable guarantees." This, combined with missing baseline results in main tables, ambiguous percentage reporting, and absent baseline variance, prevents the paper from being a clear accept. The contributions are real and the method is effective, but the theory-algorithm gap needs to be resolved. Score: 6.0.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>
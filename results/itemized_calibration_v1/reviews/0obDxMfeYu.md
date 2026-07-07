## Summary

Medix proposes a median-centric framework for OOD detection using unlabeled "in-the-wild" data (a mixture of InD and OOD samples). The method has two stages: (1) filtering outliers from the wild set by iteratively removing samples whose exclusion brings the element-wise median (EWM) of gradients closer to the InD mean gradient, and (2) training an OOD detector on the extracted outliers plus labeled InD data. The paper provides theoretical error bounds (Theorems 4.1, 4.2) and evaluates on CIFAR-10/100 across five OOD test sets against 20 baselines.

## Strengths

1. **Well-motivated problem setting.** The scenario of unlabeled "in-the-wild" data (mixture of InD and OOD) is practical and underexplored. Most prior OOD detection either assumes clean auxiliary OOD data (Outlier Exposure) or uses only InD data. The paper correctly identifies and addresses this gap.

2. **Clean technical approach with intuitive support.** Using the element-wise median (EWM) of gradients rather than the mean is conceptually well-motivated by the median's known robustness to contamination. The preliminary experiment (Figure 1) showing monotonic increase in EWM deviation as OOD samples are added provides strong intuitive grounding for the algorithm design. The two-stage pipeline (filter then train) is simple and principled.

3. **Strong empirical results.** On both CIFAR-10 and CIFAR-100, Medix achieves the best FPR95 and AUROC across all five OOD test sets (SVHN, PLACES365, LSUN-C, LSUN-RESIZE, TEXTURES), often by a substantial margin. On CIFAR-100, Medix achieves an average FPR95 of 5.42% versus the next-best WOODS at 6.74%. The empirical extraction error rate of 12.5% on synthetic data (Figure 2) corroborates the behavioral claim of the filtering stage.

4. **Attempt at theoretical analysis for a hard setting.** Providing error bounds for the filtering stage in the wild-data mixture setting goes beyond what most OOD detection papers offer. The two-sided framing (bounds on both inlier and outlier misclassification) is appropriate for the problem.

## Weaknesses

### Major

1. **Contamination term in Theorem 4.1 is vacuous at the experimental setting (\(\pi = 0.5\)).** The bound's dominant term is \(\pi/[2(1-\pi)]\), which equals \(0.5\) at \(\pi = 0.5\). This guarantees \(\text{ERR}_{\text{in}} \leq 0.5 + \text{(small terms)}\), which is no better than random guessing. Since the experiments set \(\pi = 0.5\), the theory does not provide a meaningful guarantee under the evaluated conditions. The paper frames this bound as a strength ("controlled as long as \(\pi < 0.5\)"), but a 50% error floor is not informative. This does not invalidate the empirical results, but it means the theoretical contribution (C2) is substantially weaker than claimed — it does not explain why the method succeeds.

2. **Claimed outperformance over DRL (and CONJ) is unverifiable.** The baselines section (Section 5.1) lists CONJ and DRL, and the conclusion states Medix "outperformed state-of-the-art methods such as WOODS and DRL." Yet Tables 1 and 2 contain no results for CONJ or DRL. If these results exist in the appendix, they should appear in the main tables to substantiate the claim. As the paper stands, this is an unsupported factual claim in the conclusion that cannot be verified by the reader.

3. **Ambiguous "40.98% improvement" metric.** The abstract and conclusion report Medix "outperforming [KNN+] by an average of 40.98% in terms of FPR95" on CIFAR-100. From Table 2, KNN+ achieves 46.40% and Medix achieves 5.42% — an absolute reduction of 40.98 percentage points (an 88.3% relative reduction). These are very different numbers. The paper should specify whether this is a percentage-point or relative reduction to avoid misleading readers. Moreover, this claim applies to CIFAR-100 specifically; on CIFAR-10, the absolute FPR95 improvement over KNN+ is 9.50 percentage points, not 40.98.

### Minor

4. **Theoretical bounds depend on quantities unknown to the learner.** The bounds in Theorems 4.1–4.2 are expressed in terms of \(m_{\text{in}}\), \(m_{\text{out}}\), and \(\pi\) — the exact composition of the wild set that the algorithm is trying to discover. While bounds on population parameters are standard in statistical learning theory, the paper should explicitly acknowledge that these are not directly computable from observable data and serve as asymptotic/consistency guarantees rather than practical certificates. This reframing would better align the stated contribution with what the theory actually provides.

5. **Missing ablation: EWM vs. mean.** The central claim is that the median's robustness is critical for this task. The paper compares EWM to the geometric median (Appendix A.1) but not to the computationally cheaper **mean**. Showing that EWM-based filtering outperforms mean-based filtering would directly justify the core design choice. Since the mean requires only one pass over data while EWM requires repeated median recomputations, this ablation matters for both justification and practicality.

6. **Computational cost of Algorithm 1 is not quantified in the main text.** At each iteration, the algorithm recomputes the leave-one-out EWM for every remaining sample, which is \(O(|\mathcal{S}| \cdot d)\) per iteration. For wild sets of size 25,000+, this is potentially expensive. The paper defers efficiency to Appendix A.6; the main text should at minimum report wall-clock time or gradient-pass counts.

7. **The surrogate loss for the OOD detector is underspecified.** Equation (5) defines the objective using the indicator function (non-differentiable). The paper states "a binary loss based on a differentiable sigmoid function is employed as a smooth surrogate" but gives no details about the exact form (e.g., BCE with sigmoid, cross-entropy with soft labels, hinge-style surrogate). This makes Stage 2 of the method non-reproducible from the main text alone.

8. **Sub-Gaussian assumption for OOD gradients is not verified.** Remark 4.3 verifies the sub-Gaussian assumption for InD gradients (via Q-Q plot), but Theorem 4.2 relies on the same assumption for **OOD** gradients. OOD data can come from diverse, potentially multi-modal sources, making the i.i.d. sub-Gaussian assumption less plausible for OOD gradients.

### Trivial

9. Medix uses only 25k labeled InD samples (plus 25k wild) while InD-only baselines use the full 50k labeled CIFAR training set. Medix's InD accuracy is consequently lower (93.58% vs. 94.84% on CIFAR-10). This is not an unfair comparison (the paper separates methods into two categories), but it should be explicitly noted as a boundary condition for interpreting the InD accuracy trade-off.

## Nice-to-Haves

- Report standard deviations or error bars for all baselines (currently only Medix shows std in Tables 1–2).
- Discuss behavior when \(\pi > 0.5\) (OOD is the majority of wild data), which is a practically relevant scenario.
- Provide analysis or experiments varying \(\pi\) to test how the contamination term tracks empirical error at different mixing proportions.
- Clarify the role and sensitivity of the two hyperparameters (\(k, \epsilon\)) in the main text.

## Removed Points

The following points from the input review were removed under the filtering rules.

- **"ReaT" vs "ReAct" formatting issue:** The paper's text correctly uses "ReAct" (Section 5.1); "ReaT" in the table is a PDF-parser artifact. Removed per formatting-artifact rule.
- **"Data split gives Medix an unfair advantage over InD-only baselines":** The reviewer claimed Medix has access to more data. In fact, InD-only baselines use 50k labeled samples while Medix uses 25k labeled + 25k wild. Medix's InD accuracy is lower, suggesting a disadvantage for the classification task, not an advantage. The paper separates methods into "Using P_in only" and "Using P_in and P_out" categories. Removed as factually incorrect.
- **"Algorithm 1 may select samples with negative δᵢ":** The convergence criterion checks \(|\delta_{\max}| > \epsilon\). When δᵢ values become small or negative, the algorithm terminates, preventing selection of negative-δᵢ samples. The concern does not reflect the actual algorithm logic.
- **"Proofs deferred to inaccessible appendix":** The appendix and proofs exist in the original submission; the parser strips them. Not a valid weakness of the paper.
- **Generic speculation about confounders and proxy metrics:** The area-of-concern framing in the Harsh Critic produced several speculative concerns (e.g., "could the metric be measuring a proxy?") that lack specific anchoring in the paper. Removed as noise.
- **Pure formatting/style nitpicks:** Minor table formatting observations and the "section-by-section notes" that were not anchored to substantive problems. Removed per style-nipick rule.

## Novel Insights

Beyond the paper's own contributions, the review discussion surfaces one observation: the vacuity of the contamination term at \(\pi = 0.5\) suggests that the method's empirical success at this mixing ratio must be driven almost entirely by the concentration and separation effects, not by the contamination-bound guarantee. The paper does not attempt to disentangle these empirically, but doing so (e.g., by testing at \(\pi = 0.3, 0.4, 0.45\) and comparing empirical error to the bound floor) could reveal whether the theory is merely loose or missing a key mechanism.

## Suggestions

1. **(Required)** Show CONJ and DRL results in the main tables, or remove the claim of outperforming them from the abstract, conclusion, and contribution list.
2. **(Required)** Clarify whether the "40.98%" figure is a percentage-point or relative reduction. Use "p.p." if absolute, and qualify which dataset(s) the claim applies to.
3. **(Required)** Add a paragraph in Section 4 acknowledging that the bounds involve population parameters unknown to the learner and characterize them as asymptotic/consistency guarantees rather than practical error certificates. Explicitly state the bound's weakness at \(\pi \to 0.5\).
4. **(Strongly recommended)** Add an ablation comparing EWM-based filtering against mean-based filtering (even on one OOD pair) to justify the median as the core design choice.
5. **(Recommended)** Report wall-clock time for the filtering stage on the largest wild set used, or at minimum the number of gradient forward passes required.

## Calibration

**Round 1 bracket:** [4.5, 5.5]

| Anchor | Path | Avg Score | Round | Itemized | Comparison to Medix |
|--------|------|-----------|-------|----------|---------------------|
| 5lUdTogEL3 (Person Re-ID) | calibration/5lUdTogEL3.md | 1.00 | 1 | No | Unrelated topic; far weaker |
| u1cQYxRI1H (Illumination) | calibration/u1cQYxRI1H.md | 0.50* | 1 | No | Unrelated |
| nSDOkm0SKo (Financial) | calibration/nSDOkm0SKo.md | 1.00 | 1 | No | Unrelated |
| Uj0h13lVrR (GFlowNets) | calibration/Uj0h13lVrR.md | 1.00 | 1 | No | Unrelated |
| 3ZdGSTxKuy (Harry Potter OOD) | calibration/3ZdGSTxKuy.md | 2.00 | 1 | No | Different approach; weaker |
| i28ZjVxl81 (Tabular OOD) | calibration/i28ZjVxl81.md | 2.50 | 1 | No | Different setting; weaker |
| 10fsmnw6aD (CIL) | calibration/10fsmnw6aD.md | 2.50 | 1 | No | Different problem |
| KK29oh8jZs (Synthetic OOD) | calibration/KK29oh8jZs.md | 3.00 | 1 | Yes | Much weaker; theory-free, limited contribution |
| jjjxp9Wgjp (Pseudo-labels OOD) | calibration/jjjxp9Wgjp.md | 4.25 | 1 | Yes | Similar scope; Medix has stronger results but weaker novelty defense |
| 9qpdDiDQ2H (MetaOOD) | calibration/9qpdDiDQ2H.md | 5.25 | 1 | No | Different (meta-learning); comparable score band |
| ym0ubZrsmm (Background proxy) | calibration/ym0ubZrsmm.md | 5.33 | 1 | Yes | Stronger reviewed paper; Medix addresses harder problem |
| zUrdd5NRLH (GROD) | calibration/zUrdd5NRLH.md | 5.00 | 1 | No | Different transformer-based approach |
| jlEjB8MVGa (**SAL, Du et al. 2024a**) | calibration/jlEjB8MVGa.md | **6.50** | 1 | **Yes** | **Most relevant anchor.** Same setting. Stronger theory (tighter bounds, no vacuous floor). Similar results. Accepted ICLR 2024. |
| VTYg5ykEGS (ImageNet-OOD) | calibration/VTYg5ykEGS.md | 6.50 | 1 | No | Analysis paper; different genre |
| am7BPV3Cwo (Imbalanced OOD) | calibration/am7BPV3Cwo.md | 5.75 | 1 | No | Different angle |
| falBlwUsIH (Ignore labels) | calibration/falBlwUsIH.md | 6.33 | 1 | No | SSL-based; different approach |
| cJs4oE4m9Q (Hypersphere) | calibration/cJs4oE4m9Q.md | 8.00 | 1 | No | Anomaly detection; different subfield |
| SctfBCLmWo (Dataset bias) | calibration/SctfBCLmWo.md | 8.00 | 1 | No | Not OOD detection |
| TPZRq4FALB (TTA) | calibration/TPZRq4FALB.md | 8.00 | 1 | No | Different problem |
| WyEdX2R4er (VLM data-type) | calibration/WyEdX2R4er.md | 8.00 | 1 | No | Different problem |

*\*This paper's scores were 10,10,10,10 but vector similarity was low; not a meaningful comparison.*

**Narrowing to final score:** The most informative anchor is **SAL (Du et al. 2024a)** at 6.50, which addresses the identical problem setting. Comparing Medix to SAL on the itemized weights: Medix shares SAL's positive items of strong empirical results (+4, +3) and novel methodology (+4, +3). However, Medix **lacks** SAL's strongest positive items: "a theory of separability and learnability that is both novel and significant" (+5) and "rigorous theoretical guarantees" (+5). Medix's theory is substantially weaker — the contamination term is vacuous at the experimental π=0.5 setting, whereas SAL's bounds are tight enough to explain its empirical behavior. Additionally, Medix has a missing-baselines issue similar to SAL's (-4 for missing STEP/TSL baselines), but Medix's unverifiable DRL claim in the *conclusion* is a more serious presentation issue. Weighing the weaker theory against the strong empirical results and novel method, Medix sits below SAL (6.50) and above the weaker OOD papers (4.25). I place it at **5.0** — a borderline paper with clearly fixable issues but with a theoretical contribution that is overstated relative to what the bounds actually guarantee.

## Score and Decision

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>
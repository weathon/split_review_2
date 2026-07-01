## Summary

This paper proposes a shape-adaptive guidance signal (WGDT) for interactive cortical sulcal labeling on spherical mappings of brain surfaces. The key idea is to solve the eikonal equation with a curvature-based speed function so that a click propagates *along sulcal valleys* rather than isotropically. The method is evaluated on 72 HCP subjects with 17 LPFC sulci, comparing WGDT against two equidistance-based encoding schemes (ADT and Disk) within the same interactive framework, and against three fully automatic baselines. WGDT shows statistically significant improvement on all 9 small/variable sulci with a single click.

---

## Strengths

- **Principled, domain-grounded method design.** Using the eikonal equation with a mean-curvature speed function (Equations 3–5) to propagate user clicks along sulcal folds is a clean and well-motivated idea. The signal naturally follows sulcal valleys (where curvature is positive in the FreeSurfer convention) and avoids spilling into gyri — this is directly connected to the geometry of the problem.

- **Statistically rigorous within-interactive comparison.** The critical experiment — WGDT vs. ADT and Disk under the same interactive framework — is the right test of the contribution. The results are clear and properly evaluated: paired t-tests with FDR correction (q=0.05) across 17 sulci, with 10 initial click locations per subject averaged. WGDT is significantly better on **all** 9 small/variable sulci with a single click (Section 4.1, Figure 4).

- **Honest scoping.** The paper explicitly acknowledges its limitations (Section 5): evaluation restricted to LPFC, per-sulcus training requirement, manual hyperparameter tuning, and potential unreliability of curvature-based propagation with noisy or pathological anatomy. This candor is a genuine strength.

- **Practical runtime.** Table 2 reports \<500 ms per click including signal encoding, re-tessellation, and forward pass — credible and sufficient for interactive use.

---

## Weaknesses

### Minor

- **Framing over-emphasizes the automatic comparison.** The abstract and introduction present "interactive beats automatic" as a headline result, but this comparison is structurally expected: an interactive method receives a click directly indicating where the target sulcus is, while automatic methods receive no such information. The paper's actual contribution — WGDT outperforming ADT/Disk within the interactive setting — is convincingly demonstrated (Section 4.1) but could be centered more prominently. The paper does justify the automatic comparison by noting that no interactive sulcal labeling methods exist (Section 4.2, line 196), but the current framing inflates a secondary result.

- **Per-sulcus training is a real practical burden.** The paper trains 17 separate models — one per sulcus. While this is acknowledged (Section 2.1) and cited as consistent with prior work, the practical overhead for a user wanting to label the full LPFC (17 training runs, 17 sets of weights, 17 forward passes to label all sulci for a single click) is under-discussed. The paper's own future-work section identifies joint modeling as an open direction, which signals that the current design is a stopgap.

- **Click simulation is not validated against real annotator behavior.** The entire training and evaluation pipeline uses simulated clicks (Section 2.2): largest mislabeled component identification, median-distance filtering, and weighted random sampling with softmax. There is no evidence that these simulated clicks resemble what a human rater would do. This is common practice in interactive segmentation, but the paper does not discuss how real-world click patterns might differ or what effect this might have on reported performance.

- **SPHARM-Net input mapping is under-specified.** The paper states "entry channels C = 128" (Section 3.2) but does not describe how the K-dimensional geometric features + 2 guidance channels + optional current prediction are mapped to the network's input representation. This is a clarity gap for reproducibility.

- **Runtime reported only for the largest sulcus.** Table 2 measures runtime for the central sulcus (the largest). Smaller sulci may have different re-tessellation costs, and total time for labeling all 17 sulci is not provided.

### Trivial

- **No concrete failure case shown.** The paper mentions that curvature-based propagation may be unreliable with pathological anatomy but does not show a single example where WGDT *fails* relative to ADT/Disk (e.g., sulci with flat fundi or noisy curvature estimates).

---

## Nice-to-Haves

- Provide actionable guidance on selecting hyperparameters k and σ across different sulcal types, rather than deferring this entirely to future work (Section 4.1).
- The "Strengthening the Paper on Its Own Terms" suggestions from the review (reframing the abstract to lead with WGDT vs. ADT/Disk, validating click simulation, justifying per-sulcus training choices more directly) are constructive directions but not requirements for acceptance.

---

## Removed Points

These points were raised by the reviewer but are filtered out per the filtering rules:

- **Loss function notation (Equation 6):** The notation `log(p_n, z_n)` is flagged as ambiguous. However, the paper explicitly states this is standard cross-entropy loss (line 119), and the garbled notation is almost certainly a PDF parser artifact. *Removed per the hard rule about parser artifacts.*

- **Softmax concentration in click simulation:** The reviewer claims softmax with normalized distances "effectively concentrates probability mass on the single point closest to the center." Whether this holds depends on the distance distribution among points above the median; it is not demonstrably true from the information on the page. *Removed as potentially inaccurate.*

- **"None of these methods perfectly follows sulcal regions":** The paper explicitly addresses this: "our goal in this study is not to produce signals that exactly cover the regions of interest but rather to provide shape-adaptive signals that minimize spillover" (lines 182–183). *Removed as a strawman the paper already addressed.*

---

## Novel Insights

None beyond the paper's own contributions.

---

## Suggestions

1. **Reframe the contribution** in the abstract and introduction to lead with the WGDT vs. ADT/Disk comparison — this is the scientifically informative result. Retain the automatic comparison as practical context but demote it.
2. **Clarify SPHARM-Net input mapping** in Section 2.1 or 3.2 by specifying how geometric features, guidance channels, and current prediction are combined into the network's input representation.
3. **Include total runtime** for a full LPFC labeling session (17 sulci × up to 3 clicks) to give users a realistic sense of end-to-end throughput.

---

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>
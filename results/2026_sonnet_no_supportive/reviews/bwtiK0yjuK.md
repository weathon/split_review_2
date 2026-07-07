---

## Final Review

## Summary

This paper proposes a two-stage algorithm for offline change point localization and inference in dynamic multilayer random dot product graphs (D-MRDPGs), combining seeded binary segmentation with low-rank tensor estimation (TH-PCA). It establishes consistency for both the number and locations of estimated change points (Theorem 1), and—crucially—derives the first limiting distributions for change point estimators in network data (Theorem 2), enabling a fully data-driven confidence interval construction procedure. Simulations and real-data experiments demonstrate competitive performance.

---

## Strengths

- **First offline inference procedure for D-MRDPGs (Sections 2–3):** Prior work (Wang et al., 2025) addresses only online detection; prior offline work is restricted to single-layer settings. This paper fills a genuine gap in both change point localization and distributional inference for the multilayer RDPG model.
- **Novel limiting distributions (Theorem 2):** The scaled and centered change point estimator is shown to converge to the argmin of a two-sided Brownian motion functional in both the vanishing and non-vanishing jump regimes. This is, to the best of available knowledge, the first such distributional result in the network change-point literature.
- **Quantifiably sharper localization rate (Remark 1):** The rate κ_k^{−2} log T is sharper than the online counterpart of Wang et al. (2025) by a polynomial factor in problem dimensions (d, m_max, n, L), as explicitly stated and compared.
- **Robustness under model misspecification (Table 1, Scenarios 2–3):** The method performs well even when Model 1 is violated (changes in latent position distributions rather than weight matrices), suggesting practical robustness beyond the theoretical guarantees.

---

## Weaknesses

### Fatal
None.

### Major

- **Overstated claim of state-of-the-art superiority (Section 1.1, Table 1):** The paper asserts it "substantially outperforms existing state-of-the-art algorithms," but the main-body baselines are only gSeg (Chen and Zhang, 2015) and kerSeg (Song and Chen, 2024)—general-purpose graph-sequence change-point methods that ignore multilayer RDPG structure entirely. No comparison is made against offline single-layer network change-point methods (e.g., Padilla et al., 2022 for RDPGs; Xu and Lee, 2022 for SBMs; Bhattacharjee et al., 2020) adapted to the multilayer setting, which would be the most informative competitive baseline, particularly in the MSBM scenarios. The comparisons with Wang et al. (2025) and Li et al. (2024) are relegated to Appendix G.1. As a result, the performance tables do not isolate what the multilayer tensor estimation via TH-PCA actually contributes over simpler spectral or model-based approaches, and the "state-of-the-art" claim is insufficiently substantiated relative to the most relevant existing offline methods.

### Minor

- **Confidence interval degeneracy not acknowledged (Tables 2 and 4):** In Table 4, the 95% CI for the 1991 change point is (5.97, 6.03) on an integer index scale with T=35—a practically degenerate interval that trivially contains the integer 6. In Table 2, the average CI length at n=150, Scenario 1 is 0.001. This behavior is theoretically correct (when κ̂_k is large, the CI collapses, as the interval is scaled by κ̂_k^{−2}), but the paper presents these near-degenerate intervals without acknowledging that they provide no meaningful uncertainty quantification in strong-signal regimes. The paper should clearly separate the strong-signal (degenerate CI) regime from the weak-signal regime where the CI is genuinely informative.

- **Below-nominal CI coverage in Scenario 3 (Table 2, 76.67% at n=100):** The paper notes this is due to "violations of Model 1 and relatively small, layer-specific changes," which is correct, but does not explicitly state that the CI construction relies on Theorem 2 which assumes Model 1—hence coverage guarantees do not apply in Scenario 3. A clear statement that CI guarantees require the model to hold would strengthen the presentation.

- **Theory-practice gap in independence assumption (Section 2.2):** Algorithm 1 formally requires four mutually independent tensor sequences, but in practice, odd-even splitting yields only two. The paper acknowledges this in a brief parenthetical but provides no theoretical guarantee for the two-sample implementation. This gap, while standard in sample-splitting literature, should be flagged explicitly rather than treated as a footnote, since it could in principle affect CI coverage.

### Trivial

- The real data analysis uses T=35, well below the asymptotic regime of Theorems 1–2. The paper presents this as illustrative, which is appropriate, but a brief acknowledgment of the gap between asymptotic theory and this small-T application would be helpful.

---

## Nice-to-Haves

- An ablation comparing Algorithm 1 against a version using simple averaging (e.g., Frobenius norm of summed adjacency tensor) instead of TH-PCA in Stage II would directly test the tensor estimation contribution—the core methodological thesis.
- Reporting CI coverage and average length across an explicit range of κ values (separating strong-signal from weak-signal regimes) would clarify when the CI procedure is informative versus trivially degenerate.
- A brief main-body discussion of Tucker rank sensitivity (beyond the appendix robustness checks) would strengthen practical guidance for users who need to specify ranks.

---

## Removed Points
*These points are flagged as removed; treat them with caution.*

- **Scenario 2 and Δ=Θ(T) boundary:** The reviewer noted that min spacing = 20 with T = 200 (=0.1T) is "at the boundary." Satisfying Δ = Θ(T) with a constant 0.1 is not a boundary case in any meaningful technical sense; this concern is removed.
- **Non-vanishing regime deferred to appendix:** The paper explicitly states this is deferred; since the parser strips appendix content, criticizing absent appendix material is against hard rules.
- **Rank ambiguity in Assumptions 1(ii)-(iii):** Acknowledged by the paper itself (Section 2.3: "such ambiguity is common in tensor-based models"). This is a known characteristic of Tucker decomposition, not a methodological gap.
- **Strength about "important problem":** Generic and not specific to this paper's contribution—removed per filtering discipline.

---

## Novel Insights

Theorem 2's derivation of a Brownian motion argmin limiting distribution for network change point estimators is the paper's most technically distinctive contribution. The two-regime characterization (vanishing vs. non-vanishing jump) is a clean theoretical framework, and the associated data-driven CI construction represents a meaningful step forward in taking network change-point analysis from detection-only to full statistical inference. The key observation that Theorem 1's log-factor localization error gap is exactly the right tightening to support distributional inference (by ensuring O_p(1) of the scaled estimator) is technically well-motivated.

---

## Suggestions

1. Add at least one offline single-layer network change-point method (e.g., Padilla et al., 2022, applied layer-by-layer or with aggregation) as a main-body baseline in Table 1 to substantiate the "state-of-the-art" claim.
2. Add a sentence to Section 4.1 and/or Table 2's caption explicitly noting that CI guarantees require Model 1 to hold, so below-nominal coverage in Scenario 3 is expected.
3. Add a sentence to Section 3.1 or Table 4's caption noting that very tight CIs in the strong-signal regime are theoretically expected, and directing readers to the weak-signal regime (e.g., Scenario 3, n=100 in Table 2) for meaningful uncertainty quantification.
4. Include a brief main-body sentence noting that the two-sample odd-even implementation is not formally covered by the four-sample theory, and directing readers to the appendix for discussion.

---

## Score and Decision

**Calibration anchors retrieved:**

| Path | Avg Score | Round | Comparison |
|---|---|---|---|
| I5MquO1g7R.md (CPD via TV-HMM) | 4.75 | 1 | Similar topic (CPD + inference) but less novel; weaker theory, not first of kind |
| ILqA09Oeq2.md (Nested matrix-tensor model, multi-view clustering) | 6.20 | 2 | Similar profile: statistical theory + tensor methods for networks; accepted borderline |
| Ip6UwB35uT.md (Localized conformal p-values) | 7.00 | 2 | Strong statistical inference paper with novel distributional results; broader scope |
| oP7arLOWix.md (Kernel conformal time-series) | 6.00 | 2 | Conformal inference + statistical theory; accepted borderline |
| ZwhHSOHMTM.md (Dynamic functional connectome) | 6.67 | 1 | Dynamic networks + tensor methods; accepted; broader neuroscience application |
| i3T0wvQDKg.md (Valid conformal prediction for dynamic GNNs) | 5.80 | 1 | Theory + dynamic GNNs; accepted borderline |

**Round 1 bracket:** 5.5–7.5 (paper is clearly above reject territory due to genuine firsts; falls within the range of borderline-to-solid accepts).

**Round 2 narrowing:** The closest anchor is ILqA09Oeq2.md (6.2, nested matrix-tensor model for multi-view clustering) — also a statistical theory paper with tensor methods and novel theoretical results, accepted at borderline. The paper under review has an arguably stronger novelty claim (first limiting distributions for network CPD, first offline CPD for D-MRDPGs) but a real weakness in baseline comparison that weakens the empirical claims. The Ip6UwB35uT.md (7.0, localized conformal p-values) is also a close analog — rigorous statistical inference with distributional results — but has broader scope. Given the genuine theoretical firsts but the real (non-trivial) major weakness around the baseline comparison and the somewhat narrow ICLR fit, I place the paper at **6.0** — borderline accept, on the lower end of the accept range. The contribution is real and novel, but the experimental claims are overstated and the CI evaluation needs clarification.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>
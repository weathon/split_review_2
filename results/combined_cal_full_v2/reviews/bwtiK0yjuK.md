Now I have enough calibration data. Let me finalize the review.

## Summary

This paper studies offline change point localization and inference in dynamic multilayer random dot product graphs (D-MRDPGs), a novel problem formulation. The authors propose a two-stage algorithm combining seeded binary segmentation with low-rank tensor estimation (TH-PCA), establish consistency with explicit localization rates (Theorem 1), and derive the first limiting distributions for change point estimators in network data (Theorem 2), from which a data-driven confidence interval procedure follows.

## Strengths

- **Novel problem formulation (Section 2.1, Definition 2, Model 1):** The paper formalizes offline change point detection in D-MRDPGs, a problem not previously addressed. The modeling choice of fixing latent positions while allowing layer-specific weight matrices to change is well-motivated by the air transportation example and a natural extension of existing work. (weight=9.98)

- **Theoretical depth (Theorem 1, Theorem 2):** Theorem 1 provides consistency with explicit localization rates. Theorem 2 derives limiting distributions for the refined estimators — a materially harder result than high-probability bounds. The confidence interval construction in §3.1 follows coherently from this distributional result. The paper is the first to derive limiting distributions for change point estimators in network data. (weight=10.60)

- **Two-stage algorithm design (Algorithm 1):** The combination of seeded binary segmentation (Stage I) with TH-PCA-based refinement (Stage II) is methodologically sound with stated computational complexity O(T n² L r log²(T ∨ n)). The use of a second independent sample for refinement is a clean statistical device. (weight=8.82)

## Weaknesses

### Major

- **Overclaimed empirical performance and weak main-table baselines:** The main paper (Table 1) compares only against gSeg and kerSeg — general-purpose methods not designed for multilayer networks. The more relevant comparisons (Wang et al., 2025 for the same model family; Li et al., 2024 for deep learning) are mentioned in the text and relegated to Appendix G.1. The abstract claims the method "substantially outperform[s] existing state-of-the-art algorithms," but this claim is primarily supported by comparisons against methods not designed for the task. Furthermore, in Scenario 3 (n=50), kerSeg (nets.) outperforms CPDmrdpg on |K̂−K| (0.16 vs 0.19), d(Ĉ, C) (0.18 vs 9.64), and coverage (98.90% vs 95.11%) — a reversal the paper does not adequately discuss. While the appendix contains the relevant comparisons, the main paper's empirical claims outpace what the presented evidence supports. (weight=-0.81)

- **Implausibly narrow confidence intervals and near-perfect simulation results:** In Scenario 1 (n=100), the average CI length is 0.003 on a time grid of T=200 — less than 1/333 of a time unit. In the real-data example (T=35), CIs like (5.97, 6.03) have lengths of ~0.06. These are narrow enough to raise questions about finite-sample calibration of the CI procedure. Additionally, the method achieves 100% on all metrics in Scenarios 2 and 4 (n=100), suggesting these scenarios may not be challenging enough to discriminate between methods. The paper does not discuss whether these near-perfect results simply reflect strong signal or indicate over-optimism in the experimental design. (weight=3.03)

### Minor

- **CI procedure limited to the vanishing-jump regime:** Theorem 2 and the CI construction in §3.1 require κ_k → 0 as T → ∞. The paper acknowledges this limitation in the conclusion, but the practical implication is that the CI procedure is formally justified only when the change becomes asymptotically undetectable. The real-data example (T=35) applies this procedure in a finite sample where the asymptotic justification is questionable. (weight=3.75)

- **Threshold selection requires unknown parameters:** The theoretical requirement c_{τ,1} n√L log^{3/2}(T) < τ < c_{τ,2} κ²Δ depends on the unknown κ and Δ. The paper chooses τ = 0.1 n√L log^{3/2}(T) heuristically; a sensitivity analysis is mentioned (in the appendix), but the practical verifiability of the bounds is limited. (weight=3.25)

- **Scenario 3 performance reversal not adequately discussed:** In Scenario 3 (n=50), kerSeg (nets.) outperforms CPDmrdpg on three of four metrics. The paper attributes lower performance to "violations of Model 1" but does not directly address why a generic competitor performs better in this particular harder setting. (weight=4.79)

### Trivial

None.

## Nice-to-Haves

- Move the Wang et al. (2025) and Li et al. (2024) comparisons from Appendix G.1 into the main experimental table to substantiate the empirical claims.
- Add a discussion of the Scenario 3 (n=50) performance reversal, explaining when and why the method underperforms simpler alternatives.
- Tone down the "superior performance" / "substantially outperform" language in the abstract and contributions to better reflect the experimental evidence.
- Provide a practical discussion of when the vanishing-jump CI procedure is reliable in finite samples (e.g., a calibration experiment showing coverage across different κ values).

## Removed Points

1. **Weakness about general-purpose baselines being "not informative"** — Removed and merged into the Major weakness above. The appendix does contain relevant comparisons; the issue is emphasis and overclaiming, not absence.
2. **Weakness about missing error bars/standard errors in Table 1** — Removed because reporting means over 100 trials without standard errors is standard practice in this literature (e.g., Wang et al., 2021; 2025).
3. **Weakness about non-data-driven rank selection** — Removed because the paper follows the same heuristic as Wang et al. (2025) and reports sensitivity analysis over r ∈ {10, 15, 20} in the appendix.
4. **Weakness about temporal independence assumption** — Removed because the paper acknowledges this limitation and states an extension is in Appendix B.
5. **Weakness about CUSUM notation typo in Equation (1)** — Removed as likely a PDF-parsing artifact from subscript/superscript formatting.
6. **Weakness about Assumption 1's circular reasoning** — Removed because the paper explicitly acknowledges this ambiguity (lines 177–179) and notes it is common in tensor-based models.
7. **Weakness about SNR condition satisfiability** — Removed because the paper compares its condition to the known single-layer rate from Wang et al. (2021); theoretical assumptions about parameter rates are standard.
8. **Strength about addressing an important problem** — Too generic; already covered by the specific strengths above.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Move the Wang et al. (2025) and Li et al. (2024) comparisons from the appendix into the main experimental table. This is the most impactful change the authors could make — it would directly substantiate the headline empirical claim.
2. Add a frank discussion of Scenario 3 (n=50), explaining why kerSeg outperforms CPDmrdpg in this setting and what this reveals about the method's limitations.
3. Provide a finite-sample calibration experiment for the CI procedure across different κ values, addressing the narrow-CI concern.
4. Scale back the "substantially outperform" language to "competitive performance" or "strong empirical performance," which better matches the evidence.

## Score and Decision

**Bracket reasoning (Round 1):** The paper is clearly above the 1.5–3.5 band (no substantive papers there). The TV-HMM change-point paper at 4.75 had weaker theoretical contributions and "no improvement over competitors" as a key weakness; the current paper has stronger theory and generally outperforms baselines. The 5.5–7.5 band is the right bracket. The multi-view clustering paper at 6.20 and the temporal generalization paper at 6.00 are the closest theoretical peers.

**Narrowing (Round 2):** The multi-view clustering anchor (6.20, Accept) had strength weights of 6.98–12.18 and weakness weights of -0.04–6.82. My paper's strength weights (8.82–10.60) are comparable. My paper's weakness profile is slightly better (only one negative-weight item vs. the multi-view paper's zero negative-weight items among comparable weaknesses). However, my paper's experimental concerns (narrow CIs, Scenario 3 reversal) are more substantive than the multi-view paper's mainly presentational weaknesses. On balance, my paper sits at approximately 6.0 — its theoretical novelty is comparable to the 6.20 anchor, but the empirical overclaiming and unresolved experimental signals (implausibly narrow CIs, unreconciled Scenario 3 reversal) prevent it from reaching that level.

**Calibration anchors retrieved across all rounds:**

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| bEgDEyy2Yk.md | 1.00 | 1 | No | Implementation paper; far below |
| nSDOkm0SKo.md | 1.00 | 1 | No | Low-quality submission; far below |
| P49gSPmrvN.md | 1.00 | 1 | No | Low-quality submission; far below |
| 5lUdTogEL3.md | 1.00 | 1 | No | Low-quality submission; far below |
| e0bdvNsgcF.md | 2.50 | 1 | No | Tensor algorithm; much weaker |
| F5UgXkPgSn.md | 3.00 | 1 | No | Matrix completion; weaker |
| ZTvUT49JjL.md | 3.40 | 1 | No | Matrix factorization; weaker |
| pppyig2kYe.md | 3.00 | 1 | No | Matrix completion; weaker |
| 5dpuLgwQ0d.md | 4.75 | 1 | No | Graph clustering; different topic |
| I5MquO1g7R.md | 4.75 | 1 | Yes | TV-HMM; weaker theory, no improvement over competitors |
| L0pMPCmEfN.md | 4.33 | 1 | No | Wavelet method; different topic |
| YtGtIAYDV3.md | 3.67 | 1 | No | Graph learning; different topic |
| i3T0wvQDKg.md | 5.80 | 1 | Yes | Dynamic GNN conformal prediction; applications-focused |
| HFtrXBfNru.md | 6.00 | 1 | Yes | Temporal generalization in evolving graphs; comparable tier |
| uvFhCUPjtI.md | 6.00 | 1 | No | Graph Fourier transform; comparable tier |
| xljPZuprBA.md | 5.75 | 1 | No | Edge probability graph models; comparable tier |
| P7KIGdgW8S.md | 8.00 | 1 | No | GNN stability; higher tier |
| 4xWQS2z77v.md | 8.00 | 1 | No | Neural network loss landscape; higher tier |
| SjufxrSOYd.md | 8.00 | 1 | No | Graphon networks; higher tier |
| TTrzgEZt9s.md | 8.00 | 1 | No | DRO; higher tier |
| ILqA09Oeq2.md | 6.20 | 2 | Yes | Multi-view clustering theory; most comparable peer |
| zhFyKgqxlz.md | 5.75 | 2 | No | Community recovery; comparable tier |
| V5ns6uvRZ9.md | 6.00 | 2 | No | Robustness auditing; different topic |
| gqbbL7k8BF.md | 5.60 | 2 | No | CI testing; different topic |
| I0n3EyogMi.md | 7.00 | 2 | No | Time series forecasting; higher tier |
| p1TBYyqy8v.md | 6.60 | 2 | No | Graph OOD detection; higher tier |
| KY8ZNcljVU.md | 7.33 | 2 | No | Network usable information; higher tier |
| ZwhHSOHMTM.md | 6.67 | 2 | No | Dynamic representations; different topic |

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>
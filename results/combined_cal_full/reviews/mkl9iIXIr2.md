## Summary

This paper addresses Online Inventory Optimization (OIO) — an extension of Online Convex Optimization with carryover stock and capacity constraints. The core contribution is a two-stage projection algorithm that achieves a **dynamic regret** bound of $\tilde{\mathcal{O}}(\sqrt{L_{\max}(1+P_T)T})$ for OIO, the first such guarantee in this setting. The algorithm connects OIO to Smoothed Online Convex Optimization (SOCO) via a projection strategy (Lemma 1), uses a doubling trick to handle unknown environmental difficulty $L_{\max}$, and is accompanied by a matching $\Omega(\sqrt{L_{\max}T})$ lower bound (Theorem 5), resolving an open question from Hihat et al. (2023).

## Strengths

- **First dynamic regret guarantee for OIO.** The paper correctly identifies that static regret is inadequate for non-stationary demand (the $d_t = Dt/T$ example in Section 1 convincingly shows $\Omega(T)$ dynamic regret is possible despite $\mathcal{O}(\sqrt{T})$ static regret). Delivering $\tilde{\mathcal{O}}(\sqrt{L_{\max}(1+P_T)T})$ dynamic regret is a genuine step beyond Hihat et al. (2023), which only addresses static regret.

- **Clean reduction from OIO to SOCO.** Lemma 1 (line 193) connects OIO to smoothed OCO via a two-stage projection, bounding the gap between $y_t$ and $\hat{y}_t$ by a switching-cost term $2G L_t^* \|\hat{y}_t - \hat{y}_{t+1}\|_1$. This turns the carryover stock constraint — which would otherwise cause $\Omega(T)$ regret — into a switching cost that existing SOCO theory can handle. Remark 4 appropriately flags this as the core technical insight.

- **Matching lower bound.** Theorem 5 (line 333) gives $\Omega(GD\sqrt{L_{\max}T})$, matching the upper bound up to logarithmic factors and resolving the open question from Hihat et al. (2023). Corollary 1 also provides a lower bound for SOCO itself as a byproduct.

- **Principled handling of unknown environment parameters.** The algorithm does not require prior knowledge of $L_{\max}$ or $P_T$. The doubling trick (Algorithm 2, lines 7–9) restarts the base learner when observed cycle lengths exceed the current estimate, with only $\mathcal{O}(\log L_{\max})$ subdominant overhead.

## Weaknesses

### Major

- **The static-regret improvement claim conflates algorithmic improvement with a constraint-type change.** The abstract states an "improvement of $\sqrt{L_{\max}}$ for the static regret upper bound in existing studies." However, as Remark 2 (line 126) acknowledges, the paper uses a **linear** capacity constraint ($\sum_i y_t^i \leq D$) while Hihat et al. (2023) — the primary baseline for the dynamic regret result — uses a **general convex** constraint. Table 1 presents all bounds as if on common ground without adequate caveat. While the $\sqrt{L_{\max}}$ improvement does hold against references [1]–[3], [5], and [6] (which use Interval or Linear constraints), it is not cleanly attributable to algorithmic superiority over Hihat et al. (2023) since the constraint is more restrictive. The headline claim in the abstract and Table 1 should be qualified to reflect that the comparison across constraint types is not apples-to-apples.

### Minor

- **No experimental validation.** The paper is purely theoretical — no simulations, synthetic data experiments, or empirical evaluation. While theory papers can stand without experiments at ICLR, even simple experiments (e.g., verifying the $\tilde{\mathcal{O}}(\sqrt{L_{\max}T})$ scaling on synthetic demand with known $L_{\max}$, or comparing against a naive OGD baseline) would substantially strengthen the paper's impact and give readers a sense of constant factors and practical behavior.

- **The $L_{\max}$ uniformity condition is strong in multi-item adversarial settings.** Definition 1 requires that *every* item has cumulative demand reaching $D$ over *every* interval of length $L_{\max}$. For a multi-item system with many products, an adversary could easily make one item have a long low-demand stretch, causing $L_{\max} = \Omega(T)$ and rendering the regret bound vacuous. The paper characterizes $L_{\max}=o(T)$ as "mild" (line 144), but this characterization warrants more discussion — especially given that sublinear regret is impossible otherwise. The probabilistic extension (Remark 3) helps but the practical relevance of the condition is not demonstrated. The theory is sound given the assumption, but the paper overstates how mild it is.

### Trivial

None.

## Nice-to-Haves

- The assumption $T \geq L_{\max}(3 + P_T/D)$ in Theorem 3 and $T \geq \sqrt{L_{\max}(\log_2 T + e)}$ in Theorem 4 are stated without justification of what regimes they exclude in practice.
- A sketch in the main text showing how $L_{\max}$ relates to prior works' parameters in the i.i.d. Newsvendor case (currently deferred to footnote 2) would make the comparison more self-contained.

## Removed Points

These points are flagged to be removed; treat them with caution:

- **Remark 1 subgradient realism argument:** The critic questioned whether the setting's realism argument (not needing demand observation) is consistent with the adversarial subgradient framework. Removed because the paper's formal setting works with any revealed subgradient sequence — the remark about not needing demand observation is standard from Hihat et al. (2023) and does not affect the correctness of the analysis.
- **Algorithm 4 notation $(z_t < 0) \cap (b_t^k > 0)$:** Removed as a formatting/presentation nitpick. While the notation is slightly unusual, it is understandable and does not affect the paper's substance.
- **Theorem 2 scaling assumptions question:** The critic questioned whether known algorithms satisfy the assumed scaling laws. Removed because the paper later directly analyzes specific instantiations (OGD, SOGD) without relying on these general assumptions.
- **Missing appendix content references:** Removed per the hard rule — the appendix was stripped by the parser; these sections exist in the original submission.
- **"Why not also address lead time / fixed costs?"** Removed as scope creep; the paper explicitly scopes these out in the conclusions and they are not central to the contribution.

## Novel Insights

None beyond the paper's own contributions. The paper's key insight — that OIO reduces to SOCO via a two-stage projection — is already clearly articulated by the authors.

## Suggestions

1. **Qualify the static-regret comparison.** Add an explicit caveat in the abstract and Table 1 noting that the comparison with Hihat et al. (2023) involves different constraint types (linear vs. convex). Alternatively, implement MaxCOSD under the linear constraint and compare directly to isolate the algorithmic improvement.

2. **Add small-scale synthetic experiments.** Even a simple experiment generating demand with known $L_{\max}$, running the proposed algorithm and a baseline (e.g., OGD with projection onto $\mathcal{C}(x_t)$), and plotting regret vs. $T$ for several $L_{\max}$ values would significantly increase the paper's impact and confirm that the $\sqrt{L_{\max}T}$ scaling is not swamped by constant or overhead terms.

## Score and Decision

**Calibration.** I compared the weighted items of this draft against four calibration anchors:

| Anchor | Avg Score | Topic | Comparison |
|--------|-----------|-------|------------|
| Rdb0HxGJa3 | 4.50 | OCO with predictions, dynamic regret | This paper has comparable positive weights (+3.93 to +5.09 vs. +3.05 to +4.93) but *far* less severe negative weights (worst -3.09 vs. -9.00). The anchor was rejected due to weak motivation and incremental contributions; this paper has neither issue. |
| WIerHtNyKr | 5.25 | Non-stationary OCCO | This paper has better positive weights and less severe negatives. The anchor's strongest negatives (-9.70, -8.94) question novelty and experimental support; this paper's negatives are modest by comparison. |
| z7JBs8UOLI | 5.75 | Unconstrained robust OCO | Similar profile — this paper has somewhat lower top positives (+5.09 vs. +7.48) but also less severe negatives (-3.09 vs. -6.87). |
| iZgECfyHXF | 6.50 | Online nonconvex optimization | This anchor had very strong positives (+6.96, +6.94) and modest negatives (-3.16). This paper's top positives are lower (+5.09) but negatives are comparable. |

**Round 1 bracket:** 5.5–7.0 (above the 4.50–5.75 anchors due to less severe negatives; below the 6.50 anchor due to lower peak positive weights and the unaddressed framing issue).

**Final score placement:** The paper's weighted-item profile sits between the 5.75 anchor (similar positives, but this paper's negatives are milder) and the 6.50 anchor (stronger positives, but that paper also had an overclaiming concern). This paper's most negative weighted item is the constraint-comparison framing (-3.09), which is addressable but real. Its strongest positive items (matching lower bound at +5.09, clean OIO-to-SOCO reduction at +4.45) are substantial. The paper is a clear **borderline accept** — it makes a genuine theoretical contribution (first dynamic regret for OIO, matching lower bound, resolving an open question) but the static-regret comparison overclaims and the absence of any empirical validation limits impact. The contribution is sounder than the 4.50–5.75 anchors (which had severe novelty/motivation problems) but not as strong as the 6.50 anchor (which had higher novelty and broader impact). Final score: **6.0**.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>
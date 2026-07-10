Now let me produce the final review.

## Summary

This paper addresses online inventory optimization (OIO) with carryover stock constraints, proposing algorithms with dynamic regret guarantees. The core technical insight is a two-stage projection strategy that converts OIO's carryover stock constraint into a switching-cost term, establishing a clean connection between OIO and Smoothed Online Convex Optimization (SOCO). The paper provides: (1) an algorithm achieving $\tilde{\mathcal{O}}(\sqrt{L_{\max}(1+P_T)T})$ dynamic regret — the first for OIO in non-stationary environments; (2) an $\mathcal{O}(\sqrt{L_{\max}T})$ static regret bound, improving prior work's $\mathcal{O}(L_{\max}\sqrt{T})$; (3) the first $\Omega(\sqrt{L_{\max}T})$ lower bound for OIO; and (4) a doubling-trick mechanism that avoids knowing $L_{\max}$ in advance.

## Strengths

- **Genuinely novel theoretical connection between OIO and SOCO.** Lemma 1 — bounding the regret gap from projection in terms of a switching cost proportional to cycle lengths — is the paper's core technical insight. Converting the carryover stock constraint (which historically forced conservative "only update when feasible" strategies such as MaxCOSD's cyclical update) into a switching-cost term is non-obvious. This connection enables dynamic regret analysis where prior work could not proceed. [favorability=17.00]

- **First lower bound for OIO.** Theorem 5 provides the first $\Omega(\sqrt{L_{\max}T})$ lower bound for the OIO setting (static regret), confirming that the $L_{\max}$ factor is necessary, not an artifact of loose analysis. The paper also obtains a lower bound for SOCO as a corollary. [favorability=11.75]

- **Improvement over existing static regret bounds.** The paper improves static regret from $\mathcal{O}(L_{\max}\sqrt{T})$ (all prior work) to $\mathcal{O}(\sqrt{L_{\max}T})$, shaving off a factor of $\sqrt{L_{\max}}$. For settings where $L_{\max}$ is meaningfully larger than 1, this is a real improvement. [favorability=10.84]

- **Doubling trick for unknown $L_{\max}$.** Algorithm 2's doubling trick (lines 7–9) handles the unknown switching-cost coefficient without assuming $L_{\max}$ is known in advance, which strengthens practical applicability. [favorability=10.45]

## Weaknesses

### Major

- **No empirical evaluation.** The paper contains no experiments, simulations, or numerical validation of any kind. While the paper is theoretical, it proposes concrete algorithms (Algorithms 2–5) with specific parameter settings and learning rates. The problem setting admits straightforward synthetic evaluation (e.g., the linear-trend demand example from the introduction, or i.i.d. demand from Remark 3), and comparison against MaxCOSD (Hihat et al., 2023) as a baseline would be informative. Without any empirical evidence, readers cannot assess whether the theoretical bounds translate to acceptable practical performance or whether the logarithmic factors are meaningful. [favorability=-4.03]

- **The "near-optimal dynamic regret" claim is incompletely supported.** The paper claims near-optimal dynamic regret ($\tilde{\mathcal{O}}(\sqrt{L_{\max}(1+P_T)T})$) but proves optimality only for the static case. Theorem 5 proves a static lower bound $\Omega(\sqrt{L_{\max}T})$ (against a fixed comparator), while the dynamic regret lower bound is simply cited from standard OCO ($\Omega(\sqrt{(1+P_T)T})$, Zhang et al. 2018b), which has no $L_{\max}$ factor. There is no lower bound establishing that the product $\sqrt{L_{\max}}\sqrt{1+P_T}$ is simultaneously necessary for the dynamic case. Section 5 states "Our regret upper bound matches this lower bound up to a logarithmic factor" — but the cited lower bound lacks the $\sqrt{L_{\max}}$ factor present in the paper's dynamic bound. The paper's headline contribution would be strengthened by explicitly acknowledging this gap or by proving a combined lower bound. [favorability=-0.33]

### Minor

- **The OGD-based algorithm (Theorem 3) requires knowing $P_T$ in advance.** The learning rate depends on $P_T$ — the total path length of the *future* comparator sequence. The paper acknowledges this and provides the SOGD-based algorithm (Theorem 4) that does not need $P_T$, but Table 1 presents the dynamic bound uniformly without qualifying this limitation, which could mislead readers about practicality. [favorability=4.85]

- **$L_{\max}$ is a worst-case-over-time-and-items quantity** — the minimum $L$ such that for every item and every starting time, cumulative demand reaches $D$. As the paper notes, $L_{\max} = o(T)$ is needed for sublinear regret. The paper provides a probabilistic extension (Remark 3) but does not discuss how restrictive this condition is in realistic inventory settings where slow-moving items may have arbitrarily long sell-out periods. [favorability=6.30]

### Trivial

None.

## Nice-to-Haves

- A synthetic experiment on the linear-trend demand example from the introduction, comparing against MaxCOSD, would substantially strengthen the paper's overall contribution.
- A brief intuitive explanation in the main text of how sell-out periods guarantee that the projected $y_t$ catches up to $\hat{y}_t$ within $L_{\max}$ rounds (beyond the appendix-only proof) would improve readability.

## Removed Points

These points are flagged to be removed, treat them with caution:

1. **Criticism that Eq. (11) uses future decisions** — The combiner (Alg. 4, line 5) receives $\hat{v}_{t+1}^{k-1}$ and $\hat{y}_{t+1}^k$ at round $t$; these are computed from information available at round $t$, not from the actual future. The critic appears to have misread the notation.
2. **Criticism about missing appendix content (proofs, derivations)** — Per the parsing instructions, the appendix was stripped; it exists in the original submission.
3. **Criticism that the "zero-order strategy" is not defined** — The paper addresses this in footnote 5 with a concrete additional regret bound; "zero-order strategy" is standard in the OCO literature.
4. **Criticism that the SOGD combiner is described in excessive detail for a paper without experiments** — This is a stylistic preference, not a substantive weakness.
5. **Criticism that the title does not signal the linear capacity constraint** — Remark 2 clearly explains this assumption; the paper is transparent about its scope.
6. **Criticism that the adversarial demand assumption is too pessimistic** — This is the standard assumption in the OCO setting the paper builds on and is an explicit design choice.
7. **Concern about the initial transient ($x_1 \neq 0$)** — The paper addresses this in footnote 5.

## Novel Insights

The key insight not explicitly developed by the paper itself is that the $L_{\max}$ parameter creates an interesting asymmetry in the difficulty of static vs. dynamic regret for OIO. The paper proves $L_{\max}$ is necessary for the static case, but its necessity for dynamic regret remains an open question that the paper's framework itself could potentially be used to investigate.

## Suggestions

1. Add at least one synthetic experiment comparing the proposed algorithm against MaxCOSD on the linear-trend demand and/or sinusoidal demand, to demonstrate that the $\tilde{\mathcal{O}}$ bounds translate to actual performance.
2. Explicitly acknowledge in Section 5 that the "near-optimal" dynamic regret claim relies on separate optimality of the $(1+P_T)$ and $L_{\max}$ factors, rather than a combined lower bound, and soften the claim accordingly unless a matching dynamic lower bound is provided.

## Score and Decision

**Calibration summary:**

| Anchor | Path | Score | Round | Itemized | Comparison |
|--------|------|-------|-------|----------|------------|
| Strong reject (avg 1.00) | Uj0h13lVrR.md, bEgDEyy2Yk.md, nSDOkm0SKo.md, 5lUdTogEL3.md | 1.00 | R1 | No | Irrelevant topics; no similarity in contribution quality |
| J7hbPeOZ39 (3.00) | Dynamic Assortment Selection and Pricing | 3.00 | R1 | Yes | Ops research paper with both theory and experiments. Scored lower due to limited technical novelty |
| YuYxoaL7YX (3.00) | Learning Inventory Control Policy | 3.00 | R1 | Yes | Inventory RL paper with experiments. Rejected for limited novelty despite empirical results |
| Rdb0HxGJa3 (4.50) | OCO with Predictions | 4.50 | R1, R2 | Yes | Pure theory OCO paper with experiments. Top strength 14.08 vs this paper's 17.00. Had novelty/motivation weaknesses |
| Md783Qa2JX (4.00) | Computing Optimal Regularizers | 4.00 | R2 | Yes | Pure theory OLO paper, no experiments. Top strengths 10.84-11.98 similar to this paper. Had exponential complexity issue |
| WIerHtNyKr (5.25) | Non-Stationary OCCO | 5.25 | R1 | Yes | OCO theory paper with experiments. Rejected for limited novelty (-5.84). This paper has stronger novelty but no experiments |
| 5sixirvG0I (5.33) | Whittle Index for Inventory | 5.33 | R2 | Yes | Inventory paper with strong experiments but no theory guarantees. Accepted. Opposite strength/weakness profile to this paper |
| iZgECfyHXF (6.50) | Hardness of Online Nonconvex Optimization | 6.50 | R1 | No | Strong theory paper with lower bounds; accepted. Higher tier than this paper |

**Round 1 bracket (4.0–6.0):** The paper's lowest favorability weakness (-4.03) is far above the strongly negative items (below -5.0) that characterize 3.0-range papers, and its peak strength (17.00) exceeds all sub-5.0 anchors. But it lacks the experiments present in the 5.25–6.5 papers.

**Round 2 narrowing:** The paper shares with the 4.0–4.5 anchors (Rdb0HxGJa3, Md783Qa2JX) the property of being primarily theoretical, but has a higher concentration of very high-favorability items (four strengths ≥ 10.45 versus their 1-2). Against WIerHtNyKr (5.25), this paper has a more novel core contribution but lacks the empirical validation that the 5.25 paper included. The absence-of-experiments weakness (-4.03) is the primary factor preventing a score above 5.5.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>
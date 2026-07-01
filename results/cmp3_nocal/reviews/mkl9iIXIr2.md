## Summary

This paper studies Online Inventory Optimization (OIO), an extension of online convex optimization where the decision maker's feasible set at each round is constrained by carryover stock from the previous period. The core contribution is a dynamic regret bound of Õ(√(L_max T (1+P_T))) — the first such guarantee for OIO — obtained via a two-stage projection strategy that reduces the OIO problem to Smoothed OCO (SOCO). The paper also resolves an open question from Hihat et al. (2023) by providing matching upper and lower bounds of Θ̃(√(L_max T)) for the static regret setting.

## Strengths

1. **Crisp motivating example (Section 1, lines 19–26).** The Newsvendor example with D·t/T demand cleanly demonstrates why static regret is inadequate for non-stationary demand: the static comparator incurs Ω(T) loss while a time-varying comparator achieves zero. This is concrete, well-chosen, and directly motivates the dynamic regret framing.

2. **Non-obvious technical reduction (Lemma 1, Eq. 7).** The paper shows that feeding the subgradient to a base learner operating on the unconstrained set C(0) and then projecting onto C(x_{t+1}) converts the OIO regret into a SOCO regret with switching-cost coefficient ~L_max. This is the paper's most genuinely novel contribution — it opens up the SOCO toolkit for OIO and cleanly sidesteps the carryover-constraint asymmetry that makes standard two-layer architectures fail.

3. **Resolution of the static-regret open question.** The bound O(√(L_max T)) with a matching lower bound Ω(√(L_max T)) (Theorem 5) improves over the prior O(L_max √T) of Hihat et al. (2023) and establishes that the L_max dependence is tight. Table 1 provides a clear summary of how this compares to the existing literature.

4. **Practical parameter-free variant.** The doubling-trick mechanism (Algorithm 2, lines 7–9) combined with the SOGD-based base learner (Algorithm 5) means the algorithm does not need to know L_max or P_T a priori, which is a meaningful practical consideration.

## Weaknesses

### Major

1. **The "near-optimal" dynamic regret claim is not fully supported.** The paper repeatedly describes its dynamic regret guarantee as "near-optimal" (abstract line 9; contributions line 67; conclusions line 349). However, no OIO-specific dynamic lower bound is provided. The optimality argument (Section 5, line 331) relies on (a) the standard OCO dynamic lower bound Ω(√((1+P_T)T)) from Zhang et al. (2018b) and (b) a static lower bound Ω(√(L_max T)) (Theorem 5). Neither of these individually or jointly certifies minimax optimality for the *dynamic* OIO setting, because in OIO the algorithm's feasible region is constrained by carryover stock while the comparator's is not — a structural asymmetry absent from standard OCO. The combined bound Õ(√(L_max T(1+P_T))) is a valid upper bound, and the paper should be explicit that its optimality claim for the dynamic case is relative to the standard OCO lower bound, not a verified OIO minimax bound. This overreach does not invalidate the upper bound itself, but the framing goes beyond what the evidence supports.

### Minor

2. **The comparison against Hihat et al. (2023) in Table 1 is presented under a stricter assumption.** The paper works with a *linear* capacity constraint (∑_i y_t^i ≤ D), while Hihat et al. (2023) assume a *general convex* constraint. Although this difference is noted in Remark 2 and listed in the Capacity column of Table 1, the static regret improvement — O(√(L_max T)) vs. O(L_max √T) — is the headline of the table without a prominent caveat that the improvement comes under a narrower setting. A reader scanning the table could easily conclude the paper strictly dominates prior work, which is misleading. The improvement is real but should be footnoted in the table itself.

3. **Theorem 3's learning rate requires knowing P_T a priori.** Theorem 3 (line 245) provides a bound using OGD with η = f(P_T). The paper acknowledges this limitation (line 247) and Theorem 4/Algorithm 5 removes it. However, Theorem 3 is presented as a valid result without a clear upfront flag that it requires knowledge of the very quantity (P_T) the dynamic regret aims to handle. This is not a fatal issue because the paper provides a parameter-free alternative, but the presentation could mislead a reader about what is algorithmically achieved vs. what would be achievable with oracle knowledge.

4. **Technical conditions for Theorems 3 and 4 are stated without justification.** Both Theorem 3 (T ≥ L_max(3+P_T/D)) and Theorem 4 (T ≥ √(L_max(log₂ T+e))) include assumptions on T relative to other parameters. These appear in the main text as bare conditions with no discussion of whether they are mild, what happens when they fail, or whether the bounds degrade gracefully. While these are likely mild for the intended horizon, the paper should at least comment on their restrictiveness.

5. **The lower bound (Theorem 5) is presented with no sketch or intuition.** Theorem 5 is advertised as a core contribution (line 67: "for the first time, a Ω(√(L_max T)) lower bound for the OIO setting"), yet the main text states it as a single equation (lines 333–337) with no construction, no adversarial strategy, and no intuition. For a result that anchors the optimality claims, the main paper should at minimum sketch the adversarial construction and explain how it respects the OIO constraints. (The proof in the appendix is assumed to be present and correct; the issue is solely about main-paper presentation.)

### Trivial

6. **Definition 1 (sell-out period) imposes a strong worst-case condition** requiring that *all* items sell at least D units in *any* L_max-round window. While Remark 3 provides a probabilistic extension, the main analysis uses this worst-case definition, and the paper does not discuss whether the max-over-items in Lemma 1's coefficient (max_i L_t^i) creates meaningful looseness in heterogeneous multi-item settings.

## Nice-to-Haves

- The paper contains no empirical validation. For a theory paper this is not a flaw, but even a synthetic experiment demonstrating the gap between static and dynamic comparators (e.g., a seasonal demand pattern and an abrupt regime shift) would substantially strengthen credibility and impact.
- The SOGD-based algorithm (Algorithm 5) is complex (K combiners with Discounted-Normal-Predictor) and incurs O(T log T) total cost. The paper acknowledges this, but a brief discussion of when the O(log T) overhead might matter in practice would be helpful.
- A brief remark connecting L_max to physical inventory parameters (e.g., turnover rate) would help practitioners relate the theoretical parameter to domain intuition.

## Removed Points

These points from the input review were excluded per meta-review guidelines:
- **Criticisms about the lower bound proof being entirely in the appendix** → Removed (parser strips appendix from all papers; the proof exists in the original submission).
- **Criticism that Lemma 2 is stated without proof** → Removed (proof is in the appendix).
- **Speculative claim about Lemma 1's max-over-items creating a loose bound** → Removed (no concrete evidence that this looseness is substantial; it is a generic tightness concern).
- **Missing related works** → Removed (meta-reviewer cannot verify existence of missing citations).
- **Formatting, style, and typographical nitpicks** → Removed per hard rules (parser artifacts).

## Novel Insights

None beyond the paper's own contributions. The reviewer's observation about the dynamic optimality gap is accurate but follows directly from reading Section 5 against the paper's "near-optimal" claims — it identifies an overclaim, not an unrecognized structural phenomenon.

## Suggestions

1. Adjust or qualify the "near-optimal" language for the dynamic regret to make clear that the optimality argument rests on the standard OCO lower bound (which does not account for OIO's carryover asymmetry) rather than an OIO-specific minimax bound.
2. Add a footnote to Table 1 noting that the static regret improvement over Hihat et al. (2023) is achieved under a linear rather than general convex capacity constraint.
3. Include a brief sketch of the adversarial construction for Theorem 5 in the main text.
4. Add a short discussion of the technical conditions T ≥ L_max(3+P_T/D) and T ≥ √(L_max(log₂ T+e)) — are they mild, and what happens when they fail?

## Score and Decision

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>
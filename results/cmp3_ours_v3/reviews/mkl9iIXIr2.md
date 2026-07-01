## Summary

This paper addresses Online Inventory Optimization (OIO) in non-stationary environments. It proposes a two-stage projection strategy that reduces OIO to Smoothed Online Convex Optimization (SOCO), achieving the first dynamic regret guarantee for this setting: $\tilde{\mathcal{O}}(\sqrt{L_{\max}T(1+P_T)})$. It also provides an improved $\tilde{\mathcal{O}}(\sqrt{L_{\max}T})$ static regret bound matching a new $\Omega(\sqrt{L_{\max}T})$ lower bound, and formalizes the connection between OIO and SOCO.

## Strengths

1. **[ELEGANT REDUCTION]** Lemma 1 shows that under the two-stage projection, OIO regret decomposes into the base learner's regret plus a switching cost proportional to $L_{\max}$. This connection between OIO and SOCO is non-obvious and is the paper's core intellectual contribution (lines 193–205).

2. **[CORRECTLY IDENTIFIED DIFFICULTY]** The paper precisely diagnoses why standard two-layer meta-algorithms fail for OIO: the carryover stock constraint creates asymmetric feasible regions for decisions vs. comparators (lines 27–29), and a meta-algorithm's overrides violate base-learner assumptions (line 29).

3. **[FIRST DYNAMIC REGRET FOR OIO]** Provides the first dynamic regret guarantee in the OIO setting, advancing beyond the static-regret-only results of Hihat et al. (2023).

4. **[MATCHING STATIC LOWER BOUND]** Theorem 5 proves $\Omega(GD\sqrt{L_{\max}T})$ static regret lower bound for OIO, which together with the static upper bound resolves the open question from Hihat et al. (2023) about the optimal $\sqrt{L_{\max}}$ factor.

5. **[STRUCTURED COMPARISON]** Table 1 provides a clear translation of prior works' demand parameters into the $L_{\max}$ framework, aiding contextualization of the contribution.

## Weaknesses

### Fatal
None.

### Major

1. **Overclaimed "near-optimal dynamic regret."** The paper's headline claim is a "near-optimal dynamic regret guarantee" (abstract line 9, Section 1.1 lines 33–39, Theorem 1, Section 6 line 349). However, this claim outstrips the evidence. Section 5 states: "In OCO, Zhang et al. (2018b) have established the $\Omega(\sqrt{(1+P_T)T})$ lower bound. Our regret upper bound matches this lower bound up to a logarithmic factor" (line 331). This is incorrect: the paper's dynamic upper bound is $\tilde{\mathcal{O}}(\sqrt{L_{\max}(1+P_T)T})$, which differs from the OCO lower bound by $\sqrt{L_{\max}}$, not a logarithmic factor. Theorem 5 proves only a **static** lower bound ($\Omega(\sqrt{L_{\max}T})$). The paper does not prove a combined dynamic lower bound of $\Omega(\sqrt{L_{\max}(1+P_T)T})$, so the dynamic regret guarantee could be off by a factor of $\sqrt{L_{\max}}$ from the true dynamic optimum. The "near-optimal" claim is accurate for the static case but overstated for the dynamic case, which is the paper's advertised headline contribution. This is the paper's most significant weakness.

### Minor

1. **Strong demand assumption with limited practical discussion.** Definition 1 requires that for EVERY item $i$ and EVERY starting time $t$, cumulative demand over $L_{\max}$ rounds reaches capacity $D$. A single slow-moving item determines $L_{\max}$ for all items (conflating item heterogeneity), and sustained low-demand windows for any item are ruled out. The paper notes $L_{\max}=\Omega(T)$ precludes sublinear regret (line 144) but does not discuss practical magnitudes or whether this condition is realistic in multi-item settings with heterogeneous items.

2. **Linear capacity constraint restricts generality vs. prior work.** The paper assumes a linear-sum constraint (Eq. 3: $\sum_i y_t^i \leq D$), whereas Hihat et al. (2023) allow general convex constraints. Remark 2 (line 126) and Section 6 (line 351) acknowledge this but do not clarify whether the SOCO reduction fundamentally requires linearity or is an artifact of the current proof (Lemmas 5 and 6).

3. **Section 5 contains a misleading comparison.** The sentence "Our regret upper bound matches this lower bound up to a logarithmic factor" (line 331) conflates static and dynamic bounds. The static bound matches the static lower bound; the dynamic bound does not match the OCO dynamic lower bound without the $\sqrt{L_{\max}}$ factor. This is the same issue as the Major weakness but specifically an error in the paper's own presentation of its results.

4. **SOGD algorithm presented opaquely.** Equation (11) for $b_t^k$ involves the inverse error function and multiple nested components whose derivation and intuition are not explained in the main text. The verification that SOGD satisfies Theorem 2's $\beta$ exponent assumptions is deferred from the main body.

### Trivial
None.

## Nice-to-Haves
- Simulation experiments on synthetic non-stationary demand (comparing against MaxCOSD and static baselines) would strengthen the practical narrative and demonstrate how the theoretical bounds manifest empirically. Not required for a theory paper but would be valuable.
- Memory/complexity analysis for SOGD (maintaining $K$ OGD instances and $K$ combiners) beyond the brief $\mathcal{O}(T\log T)$ mention (line 327).
- More illustrative examples of $L_{\max}$ under non-stationary or bursty demand patterns.

## Removed Points
These points are flagged to be removed; treat them with caution.

1. "Complete absence of experimental evaluation" from Harsh Critic — Removed as a major weakness; this is a pure theory paper (regret bounds, reductions, lower bounds). ICLR accepts theory papers without experiments. Moved to Nice-to-Haves.
2. "$L_{\max}$ must be known for the lower bound to apply" / "lower bound only covers instances parameterized by $L_{\max}$" — Removed. Standard minimax lower bound practice; the bound form is correct.
3. "Constants hidden in $\mathcal{O}$/$\tilde{\mathcal{O}}$ may be large enough to dominate" — Generic criticism applicable to nearly all theory papers. Removed.
4. Related-work section "too broad" — Subjective preference, not a substantive weakness. Removed.
5. Generic strengths about the problem being "important" or "timely" — Removed. Only kept evidence-backed strengths.

## Calibration Anchors
- **Rdb0HxGJa3** (avg 4.50, Reject): OCO with predictions, incremental contribution. Our paper has a more novel reduction. → Our paper is stronger.
- **WIerHtNyKr** (avg 5.25, Reject): Adaptive algorithm for non-stationary OCCO, unclear novelty. Our paper's reduction is clearer. → Our paper is slightly stronger.
- **6HfNB34x9I** (avg 5.25, Reject): Online MDPs with predictions, theoretical regret bound. Our paper has a more original structural contribution. → Our paper is slightly stronger.
- **z7JBs8UOLI** (avg 5.75, Reject): Unconstrained robust OCO with matching lower bound. Technically clean but techniques similar to prior work. Our paper's reduction is more novel, but our paper has an overclaiming issue. → Comparable.
- **pA8Q5WiEMg** (avg 6.00, Accept): Improved regret bounds for non-convex OWO meta learning. Clean contribution with no overclaiming issues. → Our paper is slightly weaker due to the overclaiming.
- **RR70yWYenC** (avg 6.25, Accept): Continual finite-sum minimization. Clean algorithmic contribution with theory. → Our paper is weaker.
- **iZgECfyHXF** (avg 6.50, Accept): Lower bounds for nonconvex optimization. Novel lower bound contribution. → Our paper is weaker.
- **OvU9u6wS2J** (avg 7.00, Accept): Online learning for trading-volume maximization. Well-motivated with complete results. → Our paper is weaker.

Round-1 bracket: [5.0, 6.0]. Round-2 (narrowing): placed between the 5.25 (reject) and 6.00 (accept) anchors, at 5.5.

## Novel Insights
None beyond the paper's own contributions. The key insight — reducing OIO to SOCO via two-stage projection with cycle-length-dependent switching costs — is already articulated in the paper.

## Suggestions
1. Either prove a dynamic regret lower bound for OIO that includes both $\sqrt{L_{\max}}$ and $\sqrt{1+P_T}$ factors, OR qualify the "near-optimal" claim to specify it applies only to the static case. The paper currently claims "near-optimal dynamic regret" without a corresponding dynamic lower bound.
2. Correct the misleading sentence in Section 5 (line 331) that conflates the static and dynamic regret matching claims.
3. Add discussion about the practical scope of $L_{\max}$ in multi-item settings and whether item-specific variants are possible.
4. Clarify whether the linear capacity constraint is fundamental to the SOCO reduction or could be relaxed to general convex constraints.

## Score and Decision

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>
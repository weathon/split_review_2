## Summary

This paper addresses Online Inventory Optimization (OIO) in non-stationary environments. The authors identify that prior OIO algorithms provide only static regret guarantees, which yield Ω(T) loss under fluctuating demand. Their core contribution is a two-stage projection strategy that connects OIO to Smoothed OCO (SOCO), enabling the first near-optimal **dynamic** regret bound of Õ(√(L_max(1+P_T)T)) for OIO — matching the OCO lower bound up to a √(L_max) factor. For static regret, they improve the prior O(L_max√T) bound to O(√(L_max T)), with a matching Ω(√(L_max T)) lower bound that resolves an open question from Hihat et al. (2023) and also yields a new lower bound for SOCO. The algorithm operates without advance knowledge of L_max or P_T.

## Strengths

- **Genuine gap identified and addressed.** The paper correctly notes that prior OIO work (Hihat et al., 2023 and earlier) provides only static regret guarantees. The concrete example in Section 1 (lines 19–24) shows that static regret can be Ω(T) under demand fluctuations even when a time-varying comparator suffers zero loss. This cleanly motivates the need for dynamic regret.

- **Novel technical connection between OIO and SOCO.** The key insight — Lemma 1 bounding the projection error in terms of switching costs proportional to cycle length — is both clever and sound. It transforms a problem with state-dependent feasible regions (carryover stock constraint) into a standard SOCO problem, eliminating the core difficulty that prevented prior two-layer meta-algorithm approaches from working in OIO.

- **Near-optimal bounds with matching lower bounds.** The paper provides: (i) dynamic regret Õ(√(L_max(1+P_T)T)) matching the OCO lower bound of Ω(√((1+P_T)T)) up to √(L_max); (ii) static regret O(√(L_max T)) with matching Ω(√(L_max T)) lower bound, improving over prior O(L_max√T) by √(L_max); and (iii) a new Ω(√(L T)) lower bound for SOCO (Corollary 1). These are not incremental — they resolve the open question from Hihat et al. (2023).

- **Parameter-free operation.** The algorithm does not require advance knowledge of L_max (handled via doubling trick) or P_T (handled via SOGD meta-algorithm). This is important because both parameters depend on future unobserved demand.

- **Honest discussion of limitations.** The paper explicitly scopes its contributions: the linear capacity constraint (Remark 2, Section 6), the conditional nature of the L_max guarantee (line 144), and the absence of lead times and fixed-order costs (Section 6). The claims are appropriately calibrated.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

- **The L_max assumption is a substantive condition on the demand process.** Definition 1 requires that cumulative demand over any window of length L_max reaches the per-item capacity D for every item and every starting time. This is a lower bound on demand volume — it excludes scenarios where demand is genuinely low for extended periods. The paper acknowledges that L_max = Ω(T) precludes sublinear regret (line 144), but this means the core guarantee applies specifically to environments where demand is "large enough." While the paper is transparent about this, it is a genuine restriction on the adversarial setting. The probabilistic extension (Remark 3) partly addresses this for stochastic demands, but the adversarial guarantee remains conditional on L_max = o(T).

- **The linear capacity constraint is a narrower setting than prior work.** Hihat et al. (2023) assumes a general convex constraint C, while this paper assumes the specific linear-sum constraint Σ_i y_t^i ≤ D (Eq. 3). The paper acknowledges this (Remark 2, Section 6) and notes it is critical to the proof of Lemmas 5 and 6. The reduction argument for weighted sums extends applicability, but the setting remains less general than the prior benchmark for the static regret case. The comparison in Table 1 is consequently not apples-to-apples — the new static regret bounds are obtained under a more restrictive assumption on the feasible region.

- **The static regret improvement claim depends on the L_max parameter mapping being tight.** Table 1 compares the paper's O(√(L_max T)) bound against prior O(L_max√T) bounds, claiming a √(L_max) improvement. The paper states the parameter mapping in footnote 2 (e.g., 1/γ, 1/μ, D as corresponding to L_max), but the derivation showing that these parameters are truly commensurate with L_max is deferred to the appendix. A brief justification or concrete example in the main text would strengthen the reader's confidence that the improvement is not an artifact of different parameter definitions.

### Trivial
None.

## Nice-to-Haves

- A brief example in the main text illustrating the equivalence between L_max and one of the prior parameters (e.g., 1/μ in Hihat et al., 2023) would substantiate the claimed √(L_max) improvement without requiring the reader to consult the appendix.
- A short discussion of realistic demand patterns under which L_max = o(T) naturally holds (or fails) would help practitioners assess the relevance of the results.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **Weakness about parameter mapping being "relegated to the appendix":** The mapping *is* stated in the main text (footnote 2, line 47). The detailed justification is in the appendix, which is standard. The concern was retained in weakened form above.
- **"Section-by-Section Notes" content:** These are commentary, not structured weaknesses. Specific observations have been folded into the strengths/weaknesses above where substantive.
- **Speculative claims from the harsh critic's sweep (e.g., "could the metric be measuring a proxy"):** No such claims were present in this particular review, so no additional removals needed.

## Novel Insights

The review surfaces a tension not fully articulated in the paper: the L_max parameter simultaneously enables the technical reduction to SOCO while also narrowing the effective regime where sublinear regret is meaningful. The paper treats L_max as a known property of the environment, but in the adversarial setting the environment can in principle force L_max = Ω(T), making the bounds vacuous. The probabilistic extension (Remark 3) provides a partial resolution for stochastic settings, but the adversarial case inherits this limitation by design. This is a modeling constraint rather than a flaw in the analysis, but its implications for the scope of the contribution are worth weighing.

## Suggestions

- Add 1–2 sentences in Section 3.1 or a remark near Table 1 illustrating the parameter mapping with a concrete numerical example (e.g., "for i.i.d. demand d ∼ Uniform[0, D/2], L_max ≈ 2 while 1/μ ≈ 2 as well"). This would make the claimed √(L_max) improvement immediately verifiable without the appendix.
- Explicitly note in Section 5 or the conclusion that the lower bound Ω(GD√(L_max T)) also implies the impossibility of sublinear regret when L_max = Ω(T), reinforcing the earlier discussion (line 144).

## Score and Decision

This is a strong theory paper. It identifies a genuine gap, proposes a technically clever and sound reduction from OIO to SOCO, provides near-optimal upper and lower bounds with matching rates, and operates without requiring prior knowledge of key parameters. The limitations — the conditional nature of the L_max assumption and the restriction to linear capacity constraints — are clearly stated rather than hidden. The weaknesses identified are inherent to the model class or are presentation concerns; none threaten the core claims. The paper represents a significant advance within its subfield (online inventory optimization / online convex optimization).

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>
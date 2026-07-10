Now I have sufficient calibration data. Let me compile the final review.

## Summary
This paper introduces FedMPDD, a federated learning algorithm that encodes gradients via multi-projected directional derivatives, compressing uplink communication from O(d) to O(m) scalars per client per round. The key insight is that averaging multiple random projections overcomes the dimension-dependent variance of a single projection, enabling a convergence rate matching FedSGD (O(1/√K)) while providing tunable gradient obfuscation. The paper provides theoretical convergence analysis, reconstruction-error bounds, and empirical results showing strong performance under extreme communication budgets.

## Strengths
- **Genuinely novel mechanism for communication-efficient FL.** The idea of encoding gradients via multi-projected directional derivatives — transmitting only m scalars + one seed per client per round — is a fresh approach. The key insight that averaging multiple random projections (via JL Lemma structure) overcomes the dimension-dependent variance of a single projection is well-motivated and yields a clean theoretical story. This is a different encoding paradigm from quantization, sparsification, and sketching (Section 2, Algorithm 2). [favorability=16.03]
- **Convergence rate matching FedSGD (Theorem 2).** Showing that FedMPDD achieves O(1/√K) convergence under standard assumptions, with the JL-distortion term ε appearing only in the sub-leading constant, is a nontrivial theoretical contribution. The bound cleanly decomposes the effects of initialization, client sampling, and projection distortion. [favorability=14.14]
- **Formal reconstruction-error analysis (Lemmas 1 and 2).** Lemma 1's result that the relative gradient reconstruction error is exactly (d−1)/m is crisp and gives a concrete, interpretable knob for the privacy-communication trade-off. Lemma 2 extends this to a lower bound on private data reconstruction error. The paper correctly identifies that this error is independent of gradient magnitude, which differs from additive-noise methods. [favorability=10.86]
- **Empirical results under extreme budget constraints are striking.** Table 1 shows FedMPDD achieving 77% test accuracy under a 0.09 GB total budget where FedSGD cannot exceed 11.45%. Table 2's 356× reduction in bytes to reach 60% accuracy (vs. FedSGD) communicates a concrete and meaningful improvement in communication efficiency. [favorability=12.45]

## Weaknesses

### Fatal
None.

### Major
- **Privacy claims are substantially overstated relative to what is formally proven.** The paper's title, abstract, introduction, and conclusion position FedMPDD as providing "inherent privacy" that is "fundamentally different from" and implicitly superior to differential privacy / LDP. However, what is actually proven (Lemmas 1 and 2) is a lower bound on gradient/data reconstruction error — not a formal privacy guarantee. The distinction matters: differential privacy provides a rigorous, composable guarantee about the maximum influence any single data point can have on the released information, regardless of attacker auxiliary information. FedMPDD provides neither composability nor worst-case information-theoretic guarantees. The paper's empirical comparison to LDP using SSIM is apples-to-oranges: LDP is designed to satisfy (ε,δ)-DP, not to minimize SSIM. A proper comparison would measure utility under a given formal privacy budget. The paper would need to either derive a formal differential privacy guarantee, or substantially reframe the contribution as "communication-efficient encoding with incidental gradient obfuscation" rather than joint privacy+communication.

- **Missing experimental comparison against methods that jointly address compression and privacy.** The paper compares FedMPDD against compression-only methods (lp-proj, Top-k, QSGD, SA-FedLora) and against privacy-only methods (FedSGD+Laplace). However, the Related Work section (p. 3, line 38) cites Agarwal et al. (2018, cpSGD) and Amiri et al. (2021) — methods that simultaneously provide communication compression and formal differential privacy guarantees. These are the most relevant baselines for evaluating a method that claims joint privacy+communication benefits. Without this comparison, the reader cannot assess whether FedMPDD's apparent gains over LDP+compression come from its approach or from dropping formal privacy requirements.

### Minor
- **Assumptions for the main convergence theorem (Theorem 2) are not stated in the main text.** Theorem 2 references "Assumption 1" (p. 7, line 114) but the assumption never appears in the main paper. The reader cannot evaluate the convergence guarantee without knowing whether it requires convexity, smoothness, bounded variance, or all of the above.

- **Figure 2 uses inconsistent notation for the parameter m.** The figure caption and description refer to "FedMPDD (m=0.01)" and "FedMPDD (m=0.001)", but m is defined throughout the paper as an integer count of projections (e.g., m=400, 600, 800). Using fractional values without explanation (presumably fractions of dimension d) is confusing and inconsistent with the paper's formal definition.

- **The computational cost of the O(dm) encoding step is not validated with wall-clock measurements.** Remark 1 (p. 7, lines 120–122) acknowledges the O(dm) cost and mentions a "follow-up study" in the appendix for the JVP strategy, but the main paper provides no runtime measurements. For a ResNet-18 (d ≈ 11M) with m = 600, the encoding step requires billions of multiply-add operations per client per round. The paper should provide actual timing evidence rather than deferring to an appendix and a follow-up study.

### Trivial
- **Dimensional notation inconsistency in the contribution statement (p. 3, line 27).** The expression "ĝ_i(x_k) = U_{k,i} g_i(x_k) U_{k,i}" is not dimensionally well-defined (U is d×m, g is d×1). The correct form appears later in Definition 1 and equation (2) — the scalar-times-vector form — but the initial matrix expression is sloppy and undermines confidence in the formal analysis.

## Nice-to-Haves
- Provide wall-clock timing measurements for the encoding step, or implement the JVP strategy and report results in the main paper.
- Clarify the effect of violating the T×m < d bound — does privacy degrade gracefully or catastrophically?
- Add a convergence plot showing how the (d−1)/m reconstruction error bound behaves empirically across training rounds.

## Removed Points
These points are flagged to be removed, treat them with caution:
- "Lemma 1's exact equality (d−1)/m may be an upper bound" — removed because the derivation is in the stripped appendix; per hard rules, missing appendix content cannot be criticized.
- "GIA attack evaluation should include Geiping et al. (2020) and Yin et al. (2021b)" — removed because the paper already uses two attacks (Yu et al., 2025; Zhu et al., 2019), including a recent method, which constitutes a reasonable evaluation.
- "Multi-round composition analysis is thin" — removed because the paper provides a concrete worst-case bound (T×m < d) and acknowledges the practical dynamics; this is an area for future work, not a flaw.
- "No formal comparison of per-round bit costs accounting for seed transmission" — removed because the paper's O(m) characterization and tables provide the relevant cost comparison; seed overhead is negligible.
- "Table 2 Used Bytes column is confusing" — removed because the paper explicitly explains on lines 200-202 that this column estimates the cost to reach 60% accuracy; the explanation is present.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. **Substantially reframe the privacy claims.** Replace "inherent privacy" with "gradient obfuscation through compression" or similar. Remove comparative claims against LDP on SSIM, or add a proper DP-based comparison. Acknowledge explicitly that (i) the reconstruction-error bound guarantees the server cannot uniquely determine the gradient, and (ii) this is not equivalent to a formal privacy guarantee.
2. **Add experimental comparison to joint compression+DP methods** (cpSGD, Amiri et al.'s method) to make the evaluation complete.
3. **State the assumptions underlying Theorem 2 (Assumption 1) in the main text.**
4. **Clarify the m notation in Figure 2** (fraction vs. integer) and ensure consistent usage across all figures.
5. **Add wall-clock timing measurements** for the encoding step, or implement the JVP strategy and report results.

## Calibration

**Round 1 (Bracketing):** Retrieved 24 anchor papers across score bands from <1.5 to >8.5. Most relevant bands were 3.5-5.5 and 5.5-7.5.

**Round 2 (Narrowing):** Retrieved 6 additional anchors in (4.0, 7.0) range with higher topical similarity.

**Anchor papers used for itemized comparison:**

| Path | Avg Score | Round | Itemized? | Comparison |
|------|-----------|-------|-----------|------------|
| /home/.../omrLHFzC37.md (DeComFL) | 6.25 | 1 | Yes | Most similar: zeroth-order for dimension-free FL. Current paper has stronger novelty (multi-projection averaging vs. single projection) but more severe privacy framing issue. |
| /home/.../CMMpcs9prj.md (MoTEF) | 6.60 | 1 | Yes | Decentralized compression theory. Less directly comparable; current paper stronger on empirical side but weaker on framing. |
| /home/.../TCJbcjS0c2.md (LASER) | 5.83 | 1 | Yes | Low-rank compression. Current paper has stronger novelty but similar overclaim concerns. |
| /home/.../rhfOzJzsKN.md (MAPA) | 5.00 | 2 | Yes | Projection-based FL compression. Current paper stronger empirically but has privacy overclaim. |
| /home/.../9H1uctBWgF.md (Ferret) | 4.67 | 2 | Yes | Shared-randomness FL. Current paper has stronger theoretical and empirical contributions. |
| /home/.../ZU42Wrcqfm.md (FedSMU) | 5.75 | 2 | Yes | 1-bit compression FL. Current paper has stronger novelty; privacy overclaim is less severe than FedSMU's novelty gap (-5.17 vs -3.32 favorability). |

**Favorability comparison:** The current paper's strengths (10.86–16.03) are stronger than those of comparable anchors (DeComFL: 3.54–13.52; FedSMU: 3.63–10.58). However, its main weakness (privacy overclaim, favorability -3.32) is a significant negative that comparable anchors do not share (they have novelty or baseline issues instead). The privacy overclaim's severity places the paper slightly below DeComFL (6.25) but above MAPA (5.00) and Ferret (4.67). The paper shares with DeComFL a strong empirical demonstration of communication savings but has a more problematic framing issue that makes its overall contribution less clean.

**Round-1 bracket:** 5.5–7.5.

**Narrowing:** After comparing itemized favorability against the closest anchors (DeComFL at 6.25 and FedSMU at 5.75), the paper sits between them — the communication-efficiency contribution is stronger than both, but the privacy overclaim is a unique drawback that FedSMU and DeComFL do not face. This places the paper at the lower end of the bracket.

**Final justification:** The paper presents a genuinely novel communication-efficient FL mechanism with strong theoretical analysis and empirical results. However, the substantially overstated privacy claims — conflating reconstruction-error lower bounds with meaningful privacy guarantees, and comparing to LDP on inappropriate metrics — represent a significant framing problem that prevents a higher score. The core communication-efficiency contribution is separable and valid, justifying acceptance pending revision, but as currently written the gap between claimed and proven privacy properties is too large.

## Score and Decision

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>
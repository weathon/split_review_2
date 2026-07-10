Now I have enough information to calibrate. Let me write the final consolidated review.

## Summary

The paper establishes a principled connection between spectral learning of Predictive State Representations (PSRs) and tensor decomposition methods for POMDP parameter recovery. The key theoretical contribution (Theorem 1) characterizes precisely what can be recovered: full POMDP parameters when states have unique observation distributions across all full-rank actions, and partition-level transitions otherwise. The algorithm uses joint diagonalization of observation matrices from full-rank actions to estimate the similarity transform that converts PSR parameters into explicit POMDP parameters.

## Strengths

- **Clean theoretical framing of what can be recovered.** Theorem 1's characterization of learnability in terms of the "full-rank observability partition" is the paper's strongest contribution. It precisely scopes what can and cannot be recovered, and the partition-level guarantee is honest about the method's limits. This provides a genuine advance over the per-action uniqueness assumption of prior tensor methods (Azizzadenesheli et al., 2016; Guo et al., 2016).

- **Novel connection between PSRs and tensor methods.** Proposition 1 recasts the known result that PSRs learn parameters up to a similarity transform, and Section 4 shows how to estimate that transform via joint diagonalization of observation matrices from full-rank actions. This bridges two previously separate literatures (spectral PSR learning and tensor decomposition for POMDPs) and the bridge generates a genuine algorithmic capability: explicit likelihoods from spectral methods.

## Weaknesses

### Major

- **Missing experimental comparison against the most directly related prior methods.** The paper's central claim is that it relaxes the per-action uniqueness assumption of Azizzadenesheli et al. (2016) and Guo et al. (2016), learning a "broader class of POMDPs than existing tensor methods" (Introduction, p.1). Yet no experiment demonstrates that these prior methods fail where the proposed method succeeds. The Sense-Float-Reset domain, where most states share observation distributions, is explicitly presented as challenging for prior methods, but the paper never runs those prior methods on it. The only baselines are PSRs (which should produce near-identical planning results by construction, as the paper itself acknowledges) and EM (a known weak baseline for POMDPs). Without a direct comparison, the paper's central claim about relaxing assumptions remains theoretically argued but empirically unvalidated. This is the most significant evidential gap.

### Minor

- **The reward specification experiment (Figure 4) provides mixed support for the claimed advantage of explicit likelihoods.** In the directional hallway, observation-based reward specification (doable with PSRs) outperforms state-based reward specification (the claimed advantage). The state-based advantage only appears in the noisy domain after very large amounts of data (10^7 interactions), and the comparison is only against the same method's observation-based strategy, not against alternative state-based reward specification approaches. While the paper acknowledges "slow convergence of transition matrices" as the cause, the practical significance of the state-based reward specification advantage remains unclear based on this single 3-state domain.

- **The correction step in Section 4.3 is underspecified in the main text.** The paper introduces a random block-diagonal rotation matrix R "whose blocks correspond to the full-rank observability partition" but does not explicitly explain in the main text how the blocks are determined from data (they correspond to the invariant subspaces identified by the eigendecomposition in Lemma 1). A reader can infer this connection, but given the algorithm's dependence on this step, the main-text treatment is too compressed.

### Trivial

- None.

## Nice-to-Haves

- **Analysis of sample complexity or computational cost** would strengthen the paper. The Hankel matrix scales combinatorially with history length, and there is no discussion of how many subsequences are needed, how the truncation threshold is chosen, or computational cost as a function of domain size.
- **Evaluation on larger POMDPs** (10–20+ states) would help demonstrate numerical stability of the joint diagonalization and SVD truncation beyond 2–5 state toy problems.

## Removed Points

These points are flagged to be removed, treat them with caution:

1. **"The planning comparison (Fig 3 Row 4) is a sanity check, not a result"** — Removed. The paper itself states "Ideally, planning performance should be the same" (Section 5). The experiment validates that the transform estimation doesn't introduce errors; this is a necessary correctness check, not a comparative claim. The paper does not claim this as evidence of superiority over PSRs.

2. **"Algorithm underspecified because proofs deferred to appendix"** — Removed per instructions. The parser strips appendix content; proofs exist in the original submission. Only the substantive point about the correction step's description was kept (see Minor weakness above).

3. **"Evaluation limited to 2–5 states"** — Moved to Nice-to-Haves. This is a common regime for initial method demonstrations, and the paper honestly acknowledges the need to "improve our method to scale to larger problems."

4. **Generic motivation strength** — Removed (impact score +1.06, negligible). The motivation is adequate but not a distinguishing strength.

5. **Various formatting/style/parser-artifact complaints** — Removed per instructions.

## Novel Insights

None beyond the paper's own contributions. The key insight — that joint diagonalization across all full-rank actions simultaneously (rather than per-action) relaxes the uniqueness assumption and yields partition-level parameters — is already the paper's central contribution.

## Suggestions

1. **Highest priority: Add a direct comparison** against Azizzadenesheli et al. (2016) or Guo et al. (2016) on a domain where their per-action uniqueness assumption is violated (Sense-Float-Reset is well-suited). Show that prior methods fail to recover correct parameters while the proposed method succeeds (at least at the partition level). This directly validates the paper's central claim of relaxing prior assumptions.

2. **Clarify the correction step** in Section 4.3 by explicitly stating in the main text that the blocks of the rotation matrix R correspond to the invariant subspaces identified by the eigendecomposition (equal-eigenvalue groups from Lemma 1).

3. **Strengthen the reward specification experiment** by (a) adding a comparison against an alternative state-based reward specification approach (not just the same method's observation-based strategy), and (b) evaluating on at least one more domain to demonstrate generality.

## Score and Decision

**Calibration anchors used (all rounds):**

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| `B5kAfAC7hO.md` (Provable Representation for POMDPs) | 5.33 | 1, 2 | Yes | Stronger experiments (+9.27 for empirical eval) but weaker theoretical novelty (-9.84 for reliance on prior work). Our paper has the opposite trade-off: stronger theory but weaker experiments. |
| `5AbtYdHlr3.md` (Stochastic Safe Action Model Learning) | 3.00 | 1 | Yes | Much weaker overall: no experiments (-10.00), unclear contribution vs prior work. Our paper is clearly stronger (has experiments, clearer novelty). |
| `e0bdvNsgcF.md` (A-Loc tensor method) | 2.50 | 1 | Yes | Unrelated topic (tensor optimization, not POMDP learning). Not directly comparable. |
| `sEv6vHIUnu.md` (Structured Predictive Representations) | 4.80 | 2 | Yes | Had stronger experiments on 4 tasks but was criticized for incremental novelty (-9.97). Our paper's theory is more novel. |
| `mbo4YnWCHd.md` (Non-negative Tensor Mixture Learning) | 4.25 | 2 | No | Tensor decomposition for density estimation; less directly relevant. |
| `SJ9lqUalq1.md` (γ-Orthogonalized Tensor Deflation) | 5.25 | 2 | No | Tensor decomposition methodology; less directly relevant. |

**Round 1 bracket:** 3.5–5.5, based on comparison with the 3.00 anchor (no experiments, unclear novelty — our paper is clearly stronger) and the 5.33 anchor (stronger experiments, weaker novelty — our paper has the opposite profile).

**Round 2 narrowing:** The 4.80 anchor (Structured Predictive Representations) is closest in overall quality. Its decisive weaknesses were limited novelty (-9.97 to -10.00) and limited experiments (-9.98). Our paper has stronger novelty (theory is genuinely new) but also has a significant experimental gap (missing prior method comparison, impact -10.00). The 5.33 anchor's experiments were much stronger (+9.27) but its novelty was weaker (-9.84).

**Final placement:** Score **5.0**. The theoretical contribution is genuine and well-executed (supported by +9.80/+9.99 impact strengths). However, the missing experimental comparison against prior tensor methods (impact -10.00) is a decisive gap that prevents acceptance. The paper needs this comparison to validate its central claim of relaxing prior assumptions. With that addition, the paper would be a strong candidate for acceptance.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>
Now let me finalize the review with the calibrated assessment.

## Summary

This paper proposes a method for learning discrete POMDP parameters (transition matrices, observation matrices, and number of states) from action-observation sequences collected under uniform random exploration. The core contribution is connecting PSRs to tensor decomposition methods: the paper shows how PSRs learn transition and observation matrices up to a similarity transform, and then uses joint diagonalization of PSR update matrices (via random weighting, Lemma 1) to estimate that transform. When states have unique observation distributions aggregated across all full-rank actions, the full POMDP is recovered; otherwise, the method recovers partition-level parameters (Theorem 1). Experiments on Tiger, T-Maze, and Sense-Float-Reset evaluate parameter convergence, planning performance, and reward specification.

## Strengths

- **Clear theoretical framing of the PSR-to-POMDP connection (Sections 3–4).** The derivation from Hankel matrix factorization to PSR update matrices, and then to similarity transform estimation via joint diagonalization (Eqs. 16–18), is technically sound and represents a genuine synthesis of two prior lines of work (Carlyle & Paz 1971 / Balle et al. 2014, and tensor methods).
- **Honest characterization of identifiability limits (Theorem 1).** The paper precisely states that when the full-rank observability partition is nontrivial, the method recovers only partition-level parameters — summed beliefs and transitions over equivalence classes of states — rather than individual state parameters. Figure 2 concretely illustrates this for Sense-Float-Reset. This precision is a strength.
- **Lemma 1 (random weighting for joint diagonalization) is a clean result.** The formalization that random weighting of observation matrices yields distinct eigenvalues almost surely iff the observation distributions differ across states correctly identifies the boundary of identifiability.

## Weaknesses

### Major

- **Missing comparison against the prior tensor methods that the paper claims to improve upon.** The paper motivates its contribution by stating it relaxes assumptions of Azizzadenesheli et al. (2016) and Guo et al. (2016) — replacing the requirement of unique per-action observation distributions with a weaker aggregated-uniqueness condition. However, the experiments compare against PSRs and EM only, never against these tensor methods. Showing that PSRs and EM perform worse does not substantiate the claimed advantage over tensor decomposition approaches. The Sense-Float-Reset domain, where per-action observation distributions are shared across states, would be the natural testbed for a direct comparison demonstrating where prior methods fail and the proposed method succeeds. Without this, the central claim that the method "learn[s] a broader class of POMDPs than existing tensor methods" (line 23) rests entirely on theory.

- **Internal inconsistency in how parameter recovery errors are computed for domains with nontrivial partitions.** Theorem 1 establishes that the method recovers partition-level parameters. Line 231 claims "our results suggest that our method successfully recovers the underlying observation models through the L1 error of learned observation and **partition-level transition likelihoods** against ground truth." However, the Figure 3 caption states that "Trans. matrix error" is "only measurable once the estimated number of states matches that of ground truth, which truncates the curves" — this describes a per-state, not partition-level, comparison. For Sense-Float-Reset, where estimated state counts (~4–5) consistently differ from ground truth (3 or 4), these two statements are in tension. The paper must clarify whether errors are computed at the partition level or the per-state level, and what the truncation condition means for the reported numbers on SFR.

### Minor

- **The reward specification experiment provides mixed evidence for the practical value of explicit likelihoods.** In the directional hallway domain, the state-based reward strategy (the unique capability enabled by explicit transition/observation models) "performs poorly due to slow convergence of transition matrices" (line 243), while observation-based reward (which PSRs can also implement) performs best in both domains. The state-based strategy does succeed in the noisy hallway domain, but the overall evidence that explicit likelihoods provide practical advantage over PSR-based observation rewards is inconclusive from the presented experiments.

- **The estimated number of states is unstable across domains (Figure 3, Row 1).** The systematic overestimation in SFR and drift in T-Maze raise questions about the reliability of SVD-based rank estimation. The paper does not clearly distinguish between "number of states" and "number of identifiable partitions" in the reported metric, making it ambiguous what convergence the reader should expect.

### Trivial

None.

## Nice-to-Haves

- A direct validation of partition-level recovery on Sense-Float-Reset (e.g., KL divergence between true and estimated partition-level predictive distributions) would strengthen the connection between theory and experiments.

## Removed Points

These points are flagged to be removed; treat them with caution:
- Criticism about uniform random exploration being a practical limitation — the paper clearly states this as an assumption; demanding relaxation is scope creep.
- Criticism about EM being an unfair comparison (hybrid method, lack of random restarts) — giving EM the spectral state-count estimate is fair to both methods; 100 seeds provide ample restarts.
- Criticism about T-Maze modification — the paper clearly explains the change is needed for arbitrary-length data collection; this is standard practice.
- Criticism about missing hyperparameters, SVD threshold sensitivity, and reproducibility parameters — these belong to the appendix, which the parser strips from all papers equally.
- Strength about "addressing an important problem" — generic, not specific to this paper's evidence.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Add comparisons against Azizzadenesheli et al. (2016) and/or Guo et al. (2016) on a domain where per-action observation uniqueness fails (e.g., Sense-Float-Reset) to directly test the claimed relaxation.
2. Clarify the error metric computation: how are "Obs. matrix error" and "Trans. matrix error" computed when the estimated state count differs from ground truth? If partition-level comparison is used, explain the procedure; if per-state comparison is used, reconcile the caption with line 231's "partition-level" claim.
3. Design a metric that directly validates partition-level recovery (e.g., comparing true vs. estimated partition-level predictive distributions) for SFR.
4. Either identify a domain where state-based reward specification clearly outperforms observation-based reward, or temper the claims about the practical advantages of explicit likelihoods given the current evidence.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>
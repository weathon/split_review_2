Good. I have a thorough understanding of the paper and the reviews. The calibration tool has a database issue I cannot resolve, so I'll proceed with my best calibrated judgment.

---

## Summary

This paper proposes a method for learning explicit POMDP parameters (transition and observation matrices) from action-observation sequences by connecting Predictive State Representations (PSRs) with tensor decomposition methods. The key theoretical contribution is an algorithm that recovers the unknown similarity transform between PSR parameters and the true POMDP parameters up to a **full-rank observability partition** — aggregating states that share observation distributions across all actions with full-rank transition matrices. This relaxes the per-action uniqueness assumption required by prior tensor decomposition methods (Azizzadenesheli et al., 2016; Guo et al., 2016). Experiments on small POMDP benchmarks (2–4 states) demonstrate convergence of learned parameters and comparable planning performance to PSRs, while the explicit likelihoods enable state-based reward specification in a noisy hallway domain where observation-based rewards fail.

## Strengths

- **Theorem 1 provides a formal recovery guarantee up to full-rank observability partitions.** The theorem (lines 117–143) proves that an algorithm exists to recover partition-level likelihoods correctly even when states share observation distributions across all actions. This is a genuine relaxation of prior tensor methods that required **unique** per-action observation distributions. It cleanly characterizes what can and cannot be recovered.

- **Lemma 1 and the joint diagonalization procedure (Section 4.2) make the relaxation concrete.** By taking random-weighted sums of observation matrices across *all* full-rank actions simultaneously (Eq. 18), the method ensures eigenvalues are distinct unless two states share observation distributions for **every** full-rank action (Lemma 1, line 177). This is strictly weaker than the per-action uniqueness condition in prior work, and the almost-sure guarantee is formally stated.

- **Empirical validation with 100-seed statistics on standard POMDP benchmarks.** Figure 3 reports observation matrix error, partition-level transition error, estimated number of states, and planning performance on Tiger, T-Maze, and Sense-Float-Reset (two variants). Observation and partition-level transition errors converge toward zero with increasing data, and planning performance (via PO-UCT) matches ground-truth models and PSRs. The paper is honest about where performance is comparable (e.g., Figure 3, Row 4: planning performance is similar across methods).

- **Demonstration of a concrete advantage over PSRs for downstream reward specification.** Figure 4 and the accompanying text (lines 235–243) show that in the noisy hallway domain, where observation-based rewards fail because different belief states produce the same observation mixture, state-based reward specification (enabled by the learned explicit model) succeeds. This directly validates the claim that explicit likelihoods enable model-based reasoning that black-box PSRs cannot.

- **The Sense-Float-Reset domain is explicitly designed to test the partition-recovery setting.** The paper introduces this domain (Figure 1) where the reset action has a singular transition matrix and multiple states share observation distributions. Theorem 1's prediction that only partition-level recovery is possible is empirically confirmed in Figure 3, showing the method handles its own theoretical limitations gracefully rather than hallucinating finer distinctions.

## Weaknesses

### Fatal
None.

### Major
- **Missing comparison against the tensor decomposition methods the paper claims to improve upon.** The paper's core narrative (lines 21–23) states that prior tensor methods (Azizzadenesheli et al., 2016; Guo et al., 2016) require per-action uniqueness, and the proposed method relaxes this. Yet neither of these methods appears as a baseline in any experiment. The paper compares against EM (known to converge to local optima) and PSRs (which are a precursor, not an alternative to tensor methods). Without a comparison — even on a single domain where the prior methods' uniqueness assumption is violated but the proposed method succeeds — the reader cannot assess whether the relaxation translates to practical benefit. The central claim of learning "a broader class of POMDPs than existing tensor methods" remains theoretically asserted but empirically unvalidated.

- **The state-based reward specification advantage only materializes in one of two test domains, and requires large data.** In the directional hallway domain (Figure 4, top row), observation-based strategies (Ours_obs, PSR_obs) — which do not require the proposed method — achieve higher reward faster and at lower data regimes than the state-based strategies that the method uniquely enables. The paper acknowledges this ("The second strategy performs poorly due to slow convergence of transition matrices," line 243), but this undercuts the claimed advantage: in half the test domains for the paper's headline application, the method's unique capability does not yield practical benefit, and the simpler alternative works better. In the noisy domain where state-based reward does succeed, ~10^6 interactions are needed for a 3-state problem. The evidence that the method's flexibility translates to a robust practical benefit is weak.

- **No analysis of the central algorithmic step — determining which actions are full-rank from finite data.** The algorithm relies on "a threshold test on the singular value decomposition on all matrices M^a" (line 165) to identify full-rank actions. In finite data, M^a is estimated with sampling noise that could cause near-singular full-rank matrices to be misclassified or near-full-rank singular matrices to be accepted. The paper provides no ablation, sensitivity analysis, or robustness study for this threshold across different data regimes. Since the entire pipeline depends on correctly identifying full-rank actions, this is a meaningful practical concern that receives zero experimental attention.

- **Experimental scale is far below the motivating application.** The paper is motivated by autonomous robots learning furniture locking mechanisms (lines 13–14), yet the four experimental domains have 2–4 states and require 10^5–10^6 interaction steps even for these trivial domains. There is no complexity analysis, no wall-clock time comparison, and no evidence the method would work on a POMDP with 10 states, let alone a realistic robotics setting. The gap between the motivating scenario and the demonstrated capability is vast.

### Minor
- **No analysis of computation time or Hankel matrix dimensions.** The method constructs a matrix indexed by all possible history-action sequences and computes an SVD. Runtime is a relevant practical concern that is never addressed.

- **No discussion of the maximum history/test length hyperparameter used in Hankel matrix construction.** The truncation of history lengths (mentioned briefly on line 43) affects both approximation quality and computational cost, but no analysis or sensitivity is provided.

- **The p_succ ≠ 1/2 condition for full-rank actions (Section 4.1.1) is described as "mild" but is not innocuous.** The paper does not discuss what happens when p_succ approaches 1/2 or when multiple actions fail simultaneously in ways that might violate the full-rank condition.

### Trivial
None.

## Nice-to-Haves
- A comparison against Azizzadenesheli et al. (2016) or Guo et al. (2016) on a domain where their per-action uniqueness assumption is violated but the proposed method's aggregated uniqueness condition is satisfied. This would directly validate the paper's central claim.
- A sensitivity analysis for the full-rank detection threshold across different data regimes and POMDP topologies.
- An ablation study of the random block-diagonal rotation matrix R introduced in Section 4.3.
- A discussion of failure cases (e.g., when no actions are full-rank, when p_succ ≈ 1/2).

## Removed Points
These points were flagged as issues but removed after verification against the paper:

1. *"Description of Section 4.3 correction is opaque due to parser artifacts on lines 185–199"* — Formatting/parser artifacts are not author errors per hard rules.
2. *"Hankel matrix rank equivalence to |S| relies on inaccessible Appendix A"* — Missing appendix content is a parser stripping issue; the proofs exist in the original submission.
3. *"EM baseline does not mention multiple random restarts"* — Minor implementation detail, not a substantive weakness.
4. *"The paper would benefit from a negative result or failure case analysis"* — Moved to Nice-to-Haves as it is a constructive suggestion, not a flaw.
5. *"No mention of whether multiple random restarts were used for EM"* — Same as point 3; trivial implementation detail.
6. *Strength: "this paper addressed an important problem"* — Too generic; dropped per filtering rules.
7. *Strength: "the motivation is clear"* — Generic; dropped per filtering rules.

## Novel Insights

The harsh critic correctly identifies that the paper sits in a genuinely intermediate position that is unusual for a conference submission: the theoretical connection between PSR spectral methods and tensor decomposition is novel and technically sound, but the experimental validation is not commensurate with the ambition of the claims. The paper's two-part architecture — first deriving what can be recovered (Theorem 1), then demonstrating recovery on tiny domains — is internally coherent but undersells the theoretical contribution while overclaiming the empirical support. The most revealing observation from the reviews is that the directional hallway domain (Figure 4, top) serves as an implicit negative result: the state-based reward specification that the method uniquely enables requires substantially more data to converge than observation-based alternatives, suggesting that the practical value of the method may be confined to environments with extreme observational ambiguity (like the noisy hallway) where observation-based approaches fundamentally cannot work. This contingency is acknowledged in the text but not framed as a limitation of the approach.

## Suggestions

1. **Add tensor decomposition baselines.** The single highest-leverage improvement is to compare against Azizzadenesheli et al. (2016) or Guo et al. (2016) on a domain where their per-action uniqueness assumption is violated but the proposed method's aggregated uniqueness condition is satisfied. If the proposed method succeeds where the baselines fail, the paper's central claim would be directly supported rather than asserted.
2. **Add a sensitivity analysis for the full-rank detection threshold** across varying data regimes. Report how robust the set of classified full-rank actions is, and how misclassification affects downstream recovery.
3. **Add an ablation for the random rotation matrix R** used in Section 4.3. Show how sensitive the final results are to the randomness in R across multiple independent runs.
4. **Characterize the maximum history length** used in Hankel matrix construction and discuss its effect on approximation quality and sample complexity.

## Score and Decision

I calibrate this as follows: The paper makes a genuine theoretical contribution (connecting PSR spectral methods with tensor decomposition, formalized as Theorem 1, with a clean characterization of recoverability). This contribution is not trivial. However, the experimental evaluation has significant gaps: the missing comparison against the tensor methods the paper claims to improve upon is a major omission, the headline application (state-based reward specification) works in only one of two test domains, the central algorithmic step (full-rank detection) is unanalyzed, and the experimental scale (2–4 states) is far below the motivating scenario. These gaps prevent the paper from being acceptable at a top venue in its current form, though the core ideas merit further development. The paper is honestly written and does not oversell its results, which is to its credit.

**Score:** 4.5 — Borderline reject. The theoretical ideas are interesting and the paper is well-structured, but the experimental evaluation is too weak to support the claimed advantages over prior work.

**Decision:** Reject

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>
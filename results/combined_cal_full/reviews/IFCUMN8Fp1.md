Now I have all the information needed. Let me write the final consolidated review.

## Summary

This paper proposes a spectral/tensor-based method for learning discrete POMDP parameters (transition and observation matrices) from action-observation trajectories. The key idea is to bridge Predictive State Representation (PSR) learning and tensor decomposition: the authors show that the similarity transform relating PSR representations to ground-truth POMDP parameters can be estimated via joint diagonalization of transformed PSR update matrices. When states share observation distributions across all full-rank actions, the method recovers dynamics at the level of the full-rank observability partition.

## Strengths

1. **Clean theoretical connection between PSRs and tensor-decomposition POMDP learning.** The paper explicitly derives how the similarity transform $P$ that relates PSR representations to ground-truth POMDP parameters can be estimated via joint diagonalization of transformed PSR update matrices (Sections 3.2, 4.2). This bridges two previously separate lines of work — prior work either learns black-box PSRs or learns POMDP parameters under more restrictive assumptions, but did not recognize that joint diagonalization across all full-rank actions can connect the two. [weight: +4.27]

2. **Genuine relaxation of a prior assumption.** Prior tensor methods (Azizzadenesheli et al., 2016; Guo et al., 2016) required per-action distinct observation distributions for each state individually. The proposed method relaxes this to requiring uniqueness across the collection of all full-rank actions (Section 4.1, Theorem 1). This is a real — though bounded — relaxation, and the Tiger domain illustrates a POMDP where the aggregated collection of observation distributions across full-rank actions is distinctive even though individual actions may not be. [weight: +5.12]

3. **Partition-level recovery is theoretically principled.** When states share observation distributions across all full-rank actions, the method recovers dynamics at the level of the full-rank observability partition. Theorem 1, the block-diagonal structure of the ambiguity matrix $Q$, and the honest treatment of what can and cannot be recovered (Section 4.3) are clean and well-executed. [weight: +5.87]

4. **Experimental evaluation on standard benchmarks.** The method is evaluated on Tiger, T-Maze, and Sense-Float-Reset with 100 seeds each, comparing against PSR and EM baselines on parameter recovery and planning performance (Figure 3). On these benchmarks, the learned model matches PSR planning performance, demonstrating that the method does not sacrifice predictive quality to gain interpretability. [weight: +4.46]

## Weaknesses

### Major

- **Imprecise motivation regarding prior tensor methods and Tiger.** The paper claims prior tensor methods require "for each action, the corresponding observation distribution must be unique for every state" and lists Tiger as a domain where "many systems... do not have distinct observation distributions associated with every action" (lines 21–22). In Tiger, however, the "listen" action has a full-rank identity transition and the two states have *different* observation distributions under "listen" (growl-left vs. growl-right at different rates). Prior tensor methods that process one action at a time only need *one* full-rank action with distinct per-state observations, so Tiger likely falls within the class of POMDPs they can handle. The paper then uses Tiger as a positive example for the proposed method (line 23: "Should the collection of observation distributions of all full-rank actions be unique for each state, like Tiger"). While the proposed method's joint-diagonalization approach is technically novel, the framing of prior methods' limitation relative to Tiger is potentially misleading. The paper should either (a) provide a concrete POMDP that prior tensor methods provably cannot handle but the proposed method can, or (b) clarify that the contribution is a technical improvement (joint diagonalization across actions) rather than a broadening of the learnable class *as demonstrated by Tiger*. [weight: -2.26]

### Minor

- **Reward-specification advantage demonstrated only on custom-designed toy domains.** The paper's flagship claim about the value of explicit likelihoods is that they enable reward specification after learning. Yet the entire reward-specification experiment (Figure 4) is conducted on two custom 3-state hallway domains specifically designed to be "fully recoverable" by the method (line 229). The standard benchmarks (Tiger, T-Maze, Sense-Float-Reset) are not used for this experiment. The custom domains are a useful proof-of-concept, but a single experimental setting (3 states, 4 actions, 2 observations) is insufficient to support the broad claim that "these likelihoods are necessary to correctly direct agent behavior in POMDPs with very noisy observations" (line 25). [weight: -2.48]

- **No ablation studies for a multi-component pipeline.** The method pipeline involves: Hankel matrix estimation via suffix-frequency counts, SVD truncation for rank estimation, PSR matrix computation, full-rank action identification, computing $M^{ao}(M^a)^{-1}$, joint diagonalization (He et al., 2024), and the block-diagonal rotation correction (Section 4.3). There is no ablation isolating which components are critical. In particular: (a) the joint diagonalization method is used without comparing against per-action eigendecomposition (which would directly quantify the benefit over prior tensor methods), (b) the effect of the random rotation preprocessing (lines 196–199) is not isolated, and (c) there is no sensitivity analysis for the SVD truncation threshold used for state-count estimation. [weight: -2.32]

- **EM baseline comparison is underspecified.** The paper states "EM consistently converges to a local minimum" (line 231) without describing the number of restarts, initialization strategy, or convergence criteria used for the EM baseline. Since EM for POMDPs is notoriously sensitive to initialization, this claim cannot be properly evaluated without knowing the experimental setup. [weight: -2.95]

- **No discussion of computational complexity or scaling.** The Hankel matrix (Eq. 6) has $O((|A||O|)^L)$ rows/columns in the worst case. Typical matrix dimensions, the choice of maximum sequence length $L$, and wall-clock time are not reported anywhere, which is relevant for a methods paper targeting practical use. [weight: -0.32]

### Trivial

None.

## Nice-to-Haves

1. Add a reward-specification experiment on a standard benchmark (e.g., Tiger with a reward that depends on distinguishing tiger location) to strengthen the paper's central practical claim.
2. Compare the full pipeline against a version using per-action eigendecomposition (like prior tensor methods) instead of joint diagonalization to directly quantify the benefit of the proposed approach.
3. Report wall-clock time and typical Hankel matrix dimensions for the experiments.
4. Report the SVD truncation threshold and how it was set per domain.

## Removed Points

These points are flagged to be removed; treat them with caution:

1. **Transition error truncation selection bias** (from harsh critic's note about Figure 3 caption). The caption already discloses that "This error is only measurable once the estimated number of states matches that of ground truth, which truncates the curves" (line 194). This is an honest disclosure of a methodological necessity, not a weakness. The model's weight on this item was +1.83 (positive), confirming it is not a genuine weakness.

2. **Section-by-section notes about the rank of the Hankel matrix needing more justification** (line 91). The paper qualifies this claim with "for POMDPs in the restricted class that adhere to our assumptions" and defers details to Appendix A. This is adequately scoped for a main paper.

3. **Request for larger-scale experiments.** The paper explicitly scopes itself to small discrete POMDPs (Future Work, line 255), so criticizing the absence of scaling is a scope creep.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Clarify the motivation.** Either provide a concrete POMDP that prior tensor methods provably cannot handle and the proposed method can, or reframe the contribution as a technical improvement (joint diagonalization across actions) rather than as broadening the learnable class. This is the most impactful fix.

2. **Add a key ablation.** Compare the full pipeline against a version that uses per-action eigendecomposition (like prior tensor methods) instead of joint diagonalization. This would directly quantify the benefit of the proposed approach over prior art on the same benchmarks.

3. **Disclose EM initialization details.** Specify the number of random restarts and initialization strategy for the EM baseline.

4. **Report the SVD truncation threshold** and any tuning involved, and discuss how the history/test length $L$ was chosen.

## Calibration

**Anchors retrieved:**

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| `5AbtYdHlr3` (Stochastic Safe Action Model Learning) | 3.00 | 1 | Yes | Much weaker: no experiments vs. this paper's thorough evaluation; theoretical approach less mature. This paper is clearly above. |
| `B7cZvTQsUN` (Structured World Models) | 3.00 | 1 | No | Similar topical area (learning latent state structure) but neural approach; less directly comparable. |
| `e0bdvNsgcF` (Tensor factorization) | 2.50 | 1 | No | Tensor methods paper, unrelated to POMDPs. |
| `B5kAfAC7hO` (Provable Representation for POMDPs) | 5.33 | 1 | Yes | Strong theoretical paper with experiments but heavy weaknesses about limited novelty vs. prior work (-6.17, -6.96). This paper has less severe weaknesses but weaker theoretical results. |
| `KrtGfTGaGe` (Wasserstein Believer) | 4.50 | 1 | Yes | Has a significant assumption (latent observability during training, -6.37) and unclear theory-practice gap. This paper avoids that limitation and has cleaner experiments. |
| `mbo4YnWCHd` (Non-negative Tensor Mixture) | 4.25 | 1 | No | Tensor decomposition paper, not POMDP learning. |
| `Q00CO1Tm6M` (Theoretical Hardness of POMDPs) | 5.75 | 1 | No | Pure theory paper on hardness; not directly comparable. |
| `Qja5s0K3VX` (OPE in POMDPs) | 6.00 | 1 | Yes | Strong theoretical paper with no experiments. This paper has experiments but less theoretical depth. |
| `GvsCOOPxoI` (Provable Learning for DEC-POMDPs) | 6.17 | 1 | Yes | Strong theoretical paper with no empirical validation and proofs mostly in appendix. This paper has experiments but more modest theory. |
| `8BAkNCqpGW` (Policy Gradient for POMDPs) | 8.00 | 1 | No | Strong theoretical + empirical, well beyond this paper's scope. |
| `5t57omGVMw` (Learning to Relax) | 8.00 | 1 | No | Unrelated topic (linear system solvers). |
| `stUKwWBuBm` (Tractable MARL) | 8.00 | 1 | No | Unrelated topic. |
| `Uj0h13lVrR` (KL Divergence GFlowNets) | 1.00 | 1 | No | Unrelated, very weak paper. |

**Round 1 bracket:** The paper sits between the 5.33 anchor (B5kAfAC7hO — theoretical POMDP representation, rejected) and the 6.17 anchor (GvsCOOPxoI — DEC-POMDP theory, rejected). Compared to B5kAfAC7hO, this paper has less severe weaknesses (the heaviest weakness in that anchor was -6.96 vs. our heaviest at -2.95) but also has weaker theoretical results. Compared to GvsCOOPxoI, this paper has empirical validation that anchor lacks but less ambitious theoretical scope.

The draft's weighted strengths average +4.93 and weighted weaknesses average -2.26, yielding a net positive signal. The heavy positive weights (+5.87 for partition-level theory, +5.12 for the relaxation) outweigh the moderate negatives. The most negatively weighted weakness (-2.95) concerns EM initialization details, which is addressable. The most structurally concerning weakness (Tiger motivation, -2.26) is about framing rather than technical correctness.

**Final score:** 5.5. The paper makes a genuine technical contribution — the connection between PSRs and tensor methods is clean, the partition-level theory is well-executed, and the experiments confirm that the method recovers POMDP parameters on standard benchmarks. However, the imprecise framing of prior work's limitations, the thin evidence for the reward-specification advantage, and the lack of ablations prevent it from being a clear acceptance. With revision to address these issues, the paper could be a strong 6+.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>
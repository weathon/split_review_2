Now I have all the information I need. Let me write the final consolidated review.

## Summary

This paper studies how to learn discrete POMDP parameters (transition and observation matrices) from action-observation sequences without assuming per-action unique observation distributions. It connects PSR learning (which yields models up to a similarity transform) with tensor decomposition methods, using joint diagonalization across all full-rank actions simultaneously to recover the similarity transform up to a "full-rank observability partition" of the state space. The paper provides theoretical characterizations of what is learnable (Theorem 1, Lemma 1) and demonstrates the method on small-scale POMDPs including Tiger, T-Maze, and Sense-Float-Reset.

## Strengths

- **A well-motivated theoretical framing of the PSR–POMDP connection (Sections 3–4).** The paper identifies a genuine gap: PSRs yield black-box predictive models without explicit latent-state likelihoods, while existing tensor-decomposition methods (Azizzadenesheli et al., 2016; Guo et al., 2016) require per-action unique observation distributions. The paper formalizes how PSRs learn transition/observation matrices up to a similarity transform (Proposition 1) and shows how tensor methods can estimate that transform. This reframing is the paper's core intellectual contribution.

- **A principled characterization of what is learnable (Theorem 1, Lemma 1).** The notion of a "full-rank observability partition" — grouping states that have identical observation distributions across all full-rank actions — provides a clean, formal answer to how much of the POMDP can be recovered. Theorem 1 states that this partition is the fundamental identifiability limit under the method's assumptions. Lemma 1 shows that random weighted joint diagonalization almost surely separates states with different aggregated observation profiles. This is a tighter characterization than prior work offers.

- **The key technical modification — joint diagonalization across *all* full-rank actions simultaneously (Section 4.2).** Prior tensor methods recover observation matrices per action, requiring each action's observation distributions to be unique per state. By jointly diagonalizing the weighted sum of observation matrices across *all* full-rank actions, the method relaxes this to uniqueness of the *aggregated* observation profile — a genuinely less restrictive condition.

## Weaknesses

### Fatal
None.

### Major

1. **The experimental evaluation is limited to tiny POMDPs (2–4 states), which does not support the paper's claims about practical relevance.** The paper motivates the work with robotic furniture manipulation (Baum et al., 2017) and manipulation tasks with hidden state, yet no experiment involves a domain larger than 4 states, no experiment involves continuous or structured observations, and no experiment involves any actual robotics setting. The method's core theoretical contribution (the relaxation of identifiability conditions) does not depend on large-scale validation, but the paper's framing in the introduction and abstract explicitly invokes real-world robot manipulation as motivation. Without at least one modestly larger benchmark (e.g., 10+ states or a standard partially-observed grid world), the reader cannot assess whether the method scales beyond POMDPs small enough to enumerate by hand. The paper's own conclusion acknowledges this limitation ("improve our method to scale to larger problems") but the gap between the motivation and the evaluation remains too wide.

2. **No comparison against the tensor-decomposition methods the paper claims to improve upon.** The paper positions itself as learning "a broader class of POMDPs than existing tensor methods" (line 23) and as a "reformulation" of the tensor decomposition approach of Azizzadenesheli et al. (2016) and Guo et al. (2016). Yet neither method appears as a baseline in any experiment. The experimental comparisons are against PSRs and EM. Without a direct comparison — especially on a domain where per-action uniqueness fails but aggregated uniqueness holds — the paper's claimed advantage in relaxed assumptions is presented theoretically but never demonstrated empirically to matter in practice.

### Minor

3. **The reward-specification advantage requires significantly more data than the simpler PSR-based alternative.** In the noisy domain — the one setting where observation-based rewards fail — the state-based method converges only after ~10⁷ interaction steps, while PSR_obs converges reliably after ~10⁶ steps in the directional domain. The paper acknowledges this (line 242–243: "the second strategy performs poorly due to slow convergence of transition matrices") but does not adequately discuss whether the practical benefit of explicit models justifies an order-of-magnitude increase in data requirements. This is a genuine tradeoff presented honestly but left undiscussed.

4. **The "rewards as observations" assumption is stated without adequate caveats.** Line 31 notes that rewards can be learned "by including rewards as observations (Izadi & Precup, 2008)." However, reward functions can depend on state in ways that are not captured by the observation distribution (e.g., two states with identical observation distributions but different rewards). The paper cites Izadi & Precup for this approach but does not discuss the limitations of this embedding or scenarios where it would fail.

### Trivial
None.

## Nice-to-Haves

- **Pseudocode or an explicit algorithm listing** would improve reproducibility and clarify the ordering of operations (SVD truncation, matrix inversion, joint diagonalization, random rotation, diagonal scaling).
- A **computational complexity analysis** (runtime/scaling of the Hankel matrix construction, SVD, and joint diagonalization) would help assess whether the method is practical beyond 4-state domains.
- **Comparison against prior tensor methods on a domain where the relaxed assumptions matter** (e.g., Sense-Float-Reset where per-action uniqueness fails but aggregated uniqueness holds) would substantiate the central claim.
- **Test on at least one larger POMDP** (e.g., rocksample or a 10+ state grid world) to demonstrate scalability.

## Removed Points

These points from the input review were removed after verifying against the paper:

- **"Full state observability" claim overstated** (line 9 of abstract): REMOVED. The abstract says prior methods "often assume full state observability" — this is clarified in the introduction (lines 21–23) where the paper correctly states the assumption is about per-action unique observation distributions, not fully-observable MDPs. The reviewer's concern about the abstract's phrasing is a minor imprecision that the introduction resolves.

- **Underspecified algorithmic steps (partition determination, random rotation R, pseudocode)**: REMOVED. (a) The paper explicitly defers finite-data thresholding parameters to Appendix B.1 (stripped by parser) — per review guidelines, missing appendix content is not penalized. (b) The circularity claim about the random rotation matrix R misunderstands the algorithm: by Section 4.3, the eigendecomposition in Section 4.2 has already identified which states share observation distributions (through equal eigenvalues), so the partition *is* known before R is constructed; the conversion from eigenvectors to block structure is a standard linear algebra operation. (c) Absence of pseudocode is a presentation preference, not a methodological gap — moved to Nice-to-Haves.

- **EM baseline configuration / error bar complaints**: REMOVED. The reviewer's concerns about EM local minima and variance estimates are not specific enough to constitute actionable weaknesses given the paper's 100-seed protocol and error bars in figures.

- **Strengthening the Paper suggestions**: These are constructive suggestions, not weaknesses. They are incorporated into Nice-to-Haves and Suggestions above.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Add the prior tensor methods (Azizzadenesheli et al., 2016; Guo et al., 2016) as baselines** — especially on a domain where per-action uniqueness fails but aggregated uniqueness holds (Sense-Float-Reset is designed for exactly this). This would transform the claim "we relax assumptions" into "we demonstrate that the relaxed assumptions matter in practice."

2. **Evaluate on at least one POMDP with 10+ states** (e.g., a larger T-Maze, rocksample, or a partially-observed grid world) to establish that the Hankel matrix construction, SVD truncation, and joint diagonalization remain feasible at a non-toy scale.

3. **Include pseudocode** and a worked numerical example in the main text to make the multi-step algorithm reproducible without consulting the appendix.

4. **Add a computational complexity analysis** — the Hankel matrix grows exponentially with sequence length, and the method involves SVD, matrix inversion, and eigendecomposition. Readers need to know whether the approach is practical beyond the toy domains tested.

## Score and Decision

**Calibration anchors used across rounds:**

| Anchor | Score | Round | Itemized? | Comparison |
|--------|-------|-------|-----------|------------|
| Provable Representation for POMDP (B5kAfAC7hO) | 5.33 | 1,2 | Yes | Rejected; has stronger experiments but weaker theoretical novelty than this paper |
| DEC-POMDP Factored Models (GvsCOOPxoI) | 6.17 | 1,2 | Yes | Rejected; purely theoretical with no experiments, weaknesses less negative than ours |
| POMDP Hardness with OSI (Q00CO1Tm6M) | 5.75 | 1,2 | Yes | Rejected; purely theoretical, cleaner execution than our paper |
| Wasserstein Believer (KrtGfTGaGe) | 4.50 | 2 | Yes | Accepted but controversial (reviews: 1,5,6,6); has strong experiments and strong assumption (latent observability during training) |
| Stochastic Safe Action Model Learning (5AbtYdHlr3) | 3.00 | 1 | No | Rejected; similar scope (learning models from trajectories) but much weaker contribution |
| Structured World Models (B7cZvTQsUN) | 3.00 | 1 | No | Rejected; different approach to similar problem |

**Round 1 bracket:** After comparing favorability ratings of this paper's items against the anchors, the plausible range was 4.0–6.5. Our paper's strengths (13–16 favorability) surpass all anchors' highest strengths, but our major weaknesses (-4.29, -4.05) are more negative than most anchors' worst items (the closest is the Provable Representation anchor's -4.67 for theoretical novelty concerns and the Wasserstein Believer's -4.24 for theoretical guarantee concerns).

**Round 2 narrowing:** Against the DEC-POMDP anchor (6.17, rejected), our paper's MAJOR weaknesses have more negative favorability (-4.29 vs. -1.92 for "lack of empirical evidence") and our paper lacks the thorough theoretical analysis that anchor provides. Against the Provable Representation anchor (5.33, rejected), our paper has stronger theoretical contribution (16.03 vs. 10.68) but weaker experiments — missing the key baselines entirely vs. their SOTA comparison. Against the Wasserstein Believer (4.50, accepted but controversial), our paper has stronger theory but weaker experiments and lacks the broad evaluation that paper provides.

**Final score:** 5.0. The paper has a genuine and novel theoretical contribution that the field will value. However, the experiments are too narrow (2–4 states, missing the key baselines the paper claims to improve upon) to support the paper as a complete piece of research at this venue. The paper reads as a promising theoretical report that has not yet been backed by a convincing empirical evaluation bridging the gap between the toy domains tested and the real-world robotics motivation.

**Decision:** Reject.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>
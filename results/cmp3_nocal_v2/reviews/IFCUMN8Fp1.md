Now I have a thorough understanding of the paper and the reviewer's claims. Let me produce the final consolidated review.

## Summary

This paper presents a method for learning discrete POMDP parameters from action-observation sequences. The key insight connects Predictive State Representations (PSRs) with tensor decomposition methods: PSRs learn transition/observation matrices up to an unknown similarity transform, and this transform can be estimated via a joint diagonalization procedure over full-rank actions. The result recovers the POMDP up to a "full-rank observability partition" — states with identical observation distributions across all full-rank actions are grouped together. Experiments on small POMDPs (Tiger, T-Maze, Sense-Float-Reset, hallway domains) evaluate model fidelity and a reward-specification use case.

## Strengths

- **Novel theoretical connection between PSRs and tensor decomposition.** Theorem 1 precisely characterizes what can be recovered — the similarity transform up to a full-rank observability partition. This extends the known result that PSRs learn parameters up to an unknown basis (Proposition 1) by showing when and how that basis can be estimated via joint diagonalization of full-rank action matrices. The proof is formally stated and the Sense-Float-Reset running example (Figure 1–2) makes the abstract partition concept operational.

- **Honest characterization of recovery guarantees.** The paper does not overclaim: it clearly states that when multiple states share identical observation distributions across all full-rank actions, only partition-level recovery is possible (Section 4.1, Theorem 1). The discussion of when the assumptions hold (Section 4.1.1) grounds the full-rank and ergodicity conditions in concrete robotic manipulation scenarios (self-loop failure dynamics, sensing actions breaking periodicity).

- **Clear communication of the core challenge and algorithm.** The derivation from the Hankel matrix through the similarity transform (Section 3) to the joint diagonalization procedure (Section 4.2) is logically organized and the mathematical notation is consistent. The paper works through Figure 2 to show how partition-level likelihood computation works in practice.

## Weaknesses

### Fatal
None.

### Major

1. **The reward-specification experiment (Figure 4) only partially isolates the claimed advantage.** The paper claims "these likelihoods are necessary to correctly direct agent behavior in POMDPs with very noisy observations" (abstract, line 25). In the noisy hallway domain, the experiment compares Ours_state (POMDP with state-based reward) against Ours_obs (POMDP with observation-based reward) and PSR_obs (PSR with observation-based reward). Ours_state outperforms both, which is consistent with the claim. However, the design does not rule out the possibility that some observation-based reward strategy (different from the tested one) could achieve comparable performance on a PSR — the paper shows that the POMDP's state-based reward is *one* effective strategy, but does not prove that explicit likelihoods are *necessary* in the strong sense claimed. Within the POMDP framework itself, Ours_state vs. Ours_obs controls for model type and shows state-based rewards are better in the noisy domain — but the necessity claim relative to PSRs specifically would require evidence that PSRs *cannot* approximate the state-based reward through any observation-based scheme. The claim should be tempered, or additional evidence should be provided.

2. **Scalability is not addressed.** Experiments are on POMDPs with 2–5 states, 2–4 actions, and 2–3 observations. The Hankel matrix size grows as $(|\mathcal{A}|\cdot|\mathcal{O}|)^L$ in the worst case, and no complexity analysis or runtime is reported. The motivating scenario (robotic furniture manipulation) involves much larger state spaces. While the paper acknowledges this in future work, the gap between the scale demonstrated and any practical application is substantial. This limits the strength of the practical claims.

3. **No comparison to the tensor decomposition methods the paper aims to extend.** The paper motivates its contribution as relaxing assumptions of Azizzadenesheli et al. (2016) and Guo et al. (2016), but never empirically compares against them — even on domains like Tiger where their assumptions hold. This makes it difficult to assess whether the proposed relaxation actually preserves or improves performance in practice.

### Minor

1. **The EM baseline setup may systematically disadvantage it.** EM is given the number of states from SVD truncation (which can be incorrect at small sample sizes, as Figure 3 Row 1 shows) and no mention is made of using multiple random restarts to mitigate local minima. While EM for POMDPs is known to be difficult, the current setup inflates the gap between the proposed method and EM.

2. **The threshold for identifying full-rank actions is a free parameter with unspecified setting.** Section 4.2 states this is done "by a threshold test on the singular value decomposition on all matrices $M^a$" (line 165), but the threshold value and how it was chosen in experiments are not reported.

3. **Constructive details are occasionally too terse.** The random block-diagonal rotation matrix $R$ (Section 4.3) is described in two sentences with reference to the appendix; the joint diagonalization method of He et al. (2024) is treated as a black box (line 171). The logic is not circular (partition boundaries are determined by eigenvalue analysis from the joint diagonalization, then $R$ is built from those partitions), but the main text would benefit from a sketch.

4. **No runtime or complexity analysis.** The computational cost of Hankel matrix construction and the joint diagonalization step relative to PSRs and EM is not discussed. A brief analysis would help assess practical applicability.

### Trivial
None.

## Nice-to-Haves

- Run EM with multiple random restarts and report the best result, to separate the effect of local minima from fundamental limitations of EM.
- Compare empirically to Azizzadenesheli et al. (2016) on domains where their assumptions hold, to quantify what is gained by the relaxation.

## Removed Points

The following reviewer criticisms were removed or downgraded:

1. **"Reward experiment confounds model type with reward type" (original framing as fatal):** The reviewer claimed the experiment conflates model type (POMDP vs. PSR) with reward type (state vs. observation) by comparing Ours_state against PSR_obs. However, the paper includes Ours_obs (POMDP + observation reward), which provides a within-model-type control. The comparison Ours_state vs. Ours_obs isolates reward type holding model type fixed. The criticism is therefore not a confound in the strict experimental sense. The weakness was retained as Major but reframed around the unsubstantiated "necessary" claim rather than a confound.

2. **"Planning performance matching PSRs raises question about value proposition" (Critical Issue 2):** The paper explicitly acknowledges this ("performance to be similar across all models learned," line 233) and positions the value proposition in reward specification, not planning performance. This is an honest characterization, not a weakness.

3. **"Figure 3 transition error truncation compresses failure cases":** The paper transparently states "This error is only measurable once the estimated number of states matches that of ground truth, which truncates the curves" (line 194). This is an acknowledged design choice, not a hidden flaw.

4. **"Abstract sets expectation of complex robotics scenario" (Section-by-Section on Introduction):** While the introduction uses a robotics motivation, the paper never claims to solve that scenario in its experiments. Many theory papers use motivating examples they do not fully evaluate. This is a framing choice, not a weakness.

5. **"Random rotation construction seems circular" (Missing Parts #2):** The partition boundaries are determined by eigenvalue analysis from the joint diagonalization step — states sharing the same eigenvalues across all full-rank actions are in the same partition. Building $R$ from these partitions is therefore not circular. The main-text description is brief, which is a minor presentation concern (retained as Minor), but not circular.

6. **Criticisms about missing appendix content:** Deferred proofs and implementation details are in the appendix (stripped by the parser). The main text cross-references them appropriately. This is not an author error.

## Novel Insights

The reward-specification experiment reveals an asymmetry that the paper could leverage more explicitly: in domains where observation-based rewards fail due to ambiguous emissions (the noisy hallway), the partition-level structure actually *enables* a principled reward design (highest-entropy state) that observation-based schemes cannot replicate. This suggests the paper's contribution is not just about model expressivity but about a qualitative shift in what reward strategies become available. A more direct demonstration of this shift — e.g., a task that is *impossible* with any observation-based reward but solvable with a partition-level state reward — would strengthen the paper considerably.

## Suggestions

- **Temper the "necessary" claim** (abstract, line 25) to something like "can enable" or "provide additional flexibility for" directing agent behavior, since the experiment shows state-based rewards are beneficial but does not prove PSRs cannot approximate the same behavior.
- **Add an empirical comparison to prior tensor methods** (Azizzadenesheli et al., 2016; Guo et al., 2016) on at least Tiger, to demonstrate that the relaxation does not degrade performance where their assumptions hold.
- **Report the threshold setting** for full-rank action identification and discuss its sensitivity.
- **Include a brief complexity analysis** showing the dominating cost terms (Hankel matrix construction, SVD, joint diagonalization) and how the history/test length $L$ was chosen.

## Score and Decision

The paper makes a genuine theoretical contribution — the connection between PSRs and tensor decomposition for recovering POMDP parameters up to a full-rank observability partition is novel, formally developed, and clearly presented. The honest characterization of recovery guarantees is a strength. However, the experimental evaluation is limited in scale, missing a comparison to the prior tensor methods the paper aims to extend, and the main practical claim ("necessary" for directing behavior) is stated more strongly than the evidence supports.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>
## Summary

This paper connects Predictive State Representations (PSRs) with tensor decomposition methods to learn POMDP parameters (transition and observation matrices) from action-observation sequences. The key theoretical contribution — Theorem 1 — is that the similarity transform between a PSR's latent basis and the original POMDP basis can be recovered up to a "full-rank observability partition": states sharing the same observation distributions across all full-rank actions are grouped together. This relaxes an assumption of prior tensor approaches (Azizzadenesheli et al. 2016, Guo et al. 2016) that each action's observation distribution must be unique per state. Experiments on Tiger, T-Maze, Sense-Float-Reset, and custom hallway domains evaluate planning performance and reward specification.

## Strengths

- **Theorem 1 and the partition-level recovery framework (Section 4.1).** The central theoretical result is clearly stated and appears correct under the stated assumptions. It genuinely extends what tensor-based methods can recover when states share observation distributions across actions, and the concrete running example (Sense-Float-Reset) makes this contribution tangible.

- **The connection between PSRs and tensor decomposition is well-motivated (Sections 3–4).** The paper correctly identifies that PSRs learn transition and observation matrices up to an unknown similarity transform (Proposition 1) and that the missing transform is precisely what tensor methods can estimate. Connecting these two previously separate lines of work is a useful conceptual contribution that the community can build on.

- **Reward-specification experiments (Section 5, Figure 4).** Demonstrating that learned explicit transition/observation likelihoods can be used to specify reward functions after model learning — a capability that pure PSRs lack — illustrates a practically relevant advantage of the approach.

## Weaknesses

### Fatal

None.

### Major

- **Missing experimental comparison against the prior tensor methods the paper claims to improve upon (Azizzadenesheli et al. 2016, Guo et al. 2016).** The paper's narrative explicitly positions itself as relaxing the assumptions of these methods (lines 21–23): "To recover the transitions, however, these approaches must also make the assumption that for each action, the corresponding observation distribution must be unique for every state." Yet neither method appears in any experiment. The baselines are a linear PSR and EM. Since these prior methods define the narrower class of learnable POMDPs that the paper claims to broaden, their absence from the evaluation prevents the reader from assessing whether the claimed relaxation is practically meaningful. The Sense-Float-Reset domain — where the method's advantage (shared observation distributions) is most relevant — would be the natural place for this comparison.

- **Selective reporting of transition matrix error (Figure 3, Row 3).** The caption states: "This error is only measurable once the estimated number of states matches that of ground truth, which truncates the curves." This means runs where the state count is incorrectly estimated (which happens at low data volumes, as Row 1 shows) are excluded from the transition error metric. Since the number of states is estimated via singular-value truncation — a data-sensitive decision — this creates a selection bias that overstates reported accuracy. The paper should at minimum report the fraction of runs with correct state count alongside the truncated error, or compute error for all runs after aligning to the partition structure that the method actually produces.

- **EM baseline is not set up to be informative.** The paper states "EM consistently converges to a local minimum and does not obtain correct observation or transition likelihoods" (line 231) without mentioning multiple random restarts — standard practice for EM in POMDP learning. Since EM is the only baseline that also produces explicit likelihoods, this weakens the informativeness of the comparison. Multiple restarts (e.g., 10 random initializations with selection by held-out likelihood) would make the comparison meaningful rather than a strawman.

### Minor

- **Reward-specification experiments use custom domains designed to work with the method, and the unique advantage converges slowly.** The paper introduces novel hallway domains where "observation and transition matrices can be fully recovered by our method" (line 229). Testing on solvable domains is standard practice, but the more informative question is how the method behaves on domains that *partially* violate its assumptions. Furthermore, in Figure 4, *Ours_state* (the unique capability — state-based reward specification) converges slowly, requiring ~10⁷ interactions for a 3-state hallway, and is often outperformed by observation-based methods (*Ours_obs*, *PSR_obs*) that both the proposed method and PSRs can already do. This undercuts the practical significance of the method's unique advantage.

- **No discussion of computational complexity.** The Hankel matrix has rows/columns indexed by action-observation sequences up to some length *L*. For realistic |A| and |O|, this grows exponentially. The paper does not discuss how *L* is chosen, how many entries are estimated, or the computational cost of the SVD. A brief complexity analysis would help the reader assess scalability.

### Trivial

None.

## Nice-to-Haves

- A concrete failure example (e.g., a domain where no action is full-rank) would honestly bound the method's applicability beyond the theoretical discussion in Section 4.1.1.
- Statistical significance or equivalence tests for the "meets the performance of PSRs" claim would strengthen the comparative claims.
- A dedicated limitations section (beyond the future-work framing in the conclusion) would help readers understand the scope.

## Removed Points

These points from the harsh critic are removed with justification:

- **"Furniture motivation does not match experiments."** The example is a motivation, not an evaluation claim; removed as a framing nitpick.
- **"Uniform random exploration is passive and expensive."** Standard for spectral methods; the paper is transparent about this (Sections 2, 3.3).
- **"Dismissal of Transformers in related work is debatable."** A minor phrasing issue orthogonal to the paper's contribution.
- **"No dedicated limitations section."** A presentation preference, not a substantive weakness.
- **"No significance tests."** 100 seeds with standard deviations is standard practice for this type of work.
- **"Assumptions restrictiveness is downplayed."** The paper discusses this explicitly in Sections 3.3 and 4.1.1, including concrete examples of when full-rank transitions arise in robotics.
- **"Method cannot handle partial violations of assumptions."** This is acknowledged as a limitation; demanding a complete characterization of graceful degradation is beyond the paper's scope.

## Novel Insights

None beyond the paper's own contributions. The weaknesses identified by the harsh critic largely concern gaps in experimental methodology rather than novel observations about the theory or problem.

## Suggestions

1. Add Azizzadenesheli et al. (2016) and/or Guo et al. (2016) as baselines in planning experiments, particularly on Sense-Float-Reset where the method's advantage (shared observation distributions) is most relevant.
2. Report the fraction of runs with correct state count alongside the truncated transition error, or compute transition error for all runs using the partition structure the method produces.
3. Run EM with multiple random restarts (e.g., 10) to make the comparison informative.
4. Include a brief computational complexity analysis (Hankel matrix size, SVD cost).
5. Test on at least one domain that partially violates the full-rank actions assumption to characterize the method's graceful degradation.

## Calibration Anchors

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/Uj0h13lVrR.md | 1.00 | R1 (strong reject band) | Off-topic paper; far below ours |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/P49gSPmrvN.md | 1.00 | R1 (strong reject band) | Off-topic; not comparable |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/5AbtYdHlr3.md | 3.00 | R1 (1.5–3.5) | Has theory but no experiments; our paper is stronger |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/B7cZvTQsUN.md | 3.00 | R1 (1.5–3.5) | Similar topic (world models from observations) but weaker experimental rigor; our paper has clearer theory |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/sEv6vHIUnu.md | 4.80 | R1 (3.5–5.5) | PSR + GNN paper with mixed reviews; similar strength but different methodology |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/Oq8bDXRf4F.md | 5.25 | R2 (4.5–6.5) | POMDP cognitive map paper; comparable quality but different contribution type |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/B5kAfAC7hO.md | 5.33 | R2 (4.5–6.5) | Provable representations for POMDPs; similar theory+experiment balance, our paper has more novel theory |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/FNiqaC382D.md | 5.50 | R2 (4.5–6.5) | Causal state representation paper; mixed reviews (8,5,3,6); similar profile to our paper |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/Q00CO1Tm6M.md | 5.75 | R2 (4.5–6.5) | POMDP hardness theory; clean theory but rejected for clarity/comparison issues |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/Qja5s0K3VX.md | 6.00 | R2 (4.5–6.5) | Clean theory paper with no experimental gaps; accepted — our paper has more experimental gaps |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/GvsCOOPxoI.md | 6.17 | R2 (4.5–6.5) | DEC-POMDP theory paper; more thorough than ours but different setting |

**Round 1 Bracket:** 4.5–6.5 (based on initial comparison with 3.0–6.8 anchors)

**Narrowing:** Round 2 focused on the 4.5–6.5 bracket with 6 anchors. The paper sits between the 5.33–5.50 reject band and the 6.00 accept band. The theoretical contribution is stronger than the 5.33 anchor, but the experimental gaps are more significant than the 6.00 anchor. Final score of 5.5 reflects this position.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>
## Summary

This paper proposes a framework for learning the Minimum Action Distance (MAD) — the minimum number of actions to transition between two states — from state trajectories alone, without requiring rewards or action labels. It introduces two algorithms (MadDist and TDMadDist) that use quasimetric (asymmetric) distance functions in the embedding space, a scale-invariant loss that prevents distant trajectory pairs from dominating learning, and a novel simple quasimetric ($d_{\text{simple}}$). A benchmark suite of environments with known ground-truth MAD is also contributed. Empirical results show that MadDist learns more accurate MAD approximations than existing baselines (QRL, Hilbert) and that these improvements translate into better downstream planning success.

## Strengths

- **Clear problem framing and motivation (favorability=9.15).** The paper correctly identifies that the Minimum Action Distance (MAD) is inherently asymmetric in environments with irreversible dynamics (e.g., KeyDoorGridWorld, CliffWalking), and that existing MAD approximation methods using symmetric distance metrics cannot capture this structure. This limitation is clearly articulated and well-motivated. (Section 4, Section 5)

- **Well-motivated scale-invariant loss (favorability=9.43).** The standard squared-error loss in prior work (Steccanella & Jonsson, 2022) allows distant state pairs on a trajectory to dominate the gradient because their error magnitude is larger in absolute terms. Dividing by the trajectory index difference $j-i$ before squaring (Equation 5) is a simple, principled fix that equalizes the contribution of near and far pairs. (Section 6.1, Equation 5)

- **Downstream planning validation (favorability=10.58).** Table 1 bridges the gap between representation quality and task performance: MadDist achieves near-perfect or perfect success rates ($1.00 \pm 0.00$ on four of six environments) across the OGBench PointMaze suite, with small standard deviations, decisively outperforming all baselines. This provides credible evidence that better MAD approximation translates to practical utility. (Table 1, Section 7)

- **Benchmark suite with known ground-truth MAD (favorability=9.52).** The environments span deterministic/stochastic, discrete/continuous, symmetric/asymmetric dynamics, and noisy observations. Having ground-truth MAD enables rigorous, controlled evaluation, and this suite is a genuine resource for the community. (Section 7, "Environments" paragraph)

## Weaknesses

### Fatal
None.

### Major
- **Missing comparison against the most directly comparable prior method.** Steccanella & Jonsson (2022) uses the same trajectory-supervision approach as MadDist but with a symmetric distance metric (e.g., Euclidean distance), making it the ideal ablation to isolate the benefit of using a quasimetric over a symmetric metric. The paper describes this prior work (Section 4) as the starting point for MadDist, yet never compares against it empirically. Without this comparison, it is impossible to determine how much of MadDist's gains come from (a) the quasimetric itself vs. (b) better loss design (scale-invariant loss, contrastive regularization) vs. (c) both. This ambiguity cuts across the paper's central narrative. (favorability=1.17)

### Minor
- **Inconsistency in seed counts between the empirical setup and Figure 3.** Section 7 (Empirical Setup) states: "All reported results are means over five independent runs (random seeds)." However, the Figure 3 caption repeatedly states: "Shaded regions indicate minimum and maximum values across three random seeds." The paper needs to clarify whether Figure 3 uses 3 or 5 seeds, and why. (favorability=6.38)

- **TDMadDist bundled as a main contribution despite underperforming.** The paper honestly reports that TDMadDist underperforms MadDist, but TDMadDist is presented alongside MadDist as one of the "two novel algorithms" in the Abstract even though it is generally worse than the simpler direct-regression variant. Moreover, the paper's own statement that TDMadDist "underperforms...the QRL algorithm" is imprecise — Table 1 shows TDMadDist outperforms QRL on PM Giant Navigate (0.99 vs 0.87) and PM Medium Navigate (0.92 vs 0.86). The inclusion is understandable as an exploratory variant, but it should be framed more clearly as a negative result or ablation. (favorability=4.87)

- **Abstract-level claim about $d_{\text{simple}}$ supported only in the appendix.** The abstract claims that $d_{\text{simple}}$ "outperforms more elaborate quasimetrics in the existing literature" as one of three main contributions, yet the only supporting evidence is in Appendix E. The main paper's experimental results (Figure 3, Table 1) compare *methods* (MadDist vs. QRL vs. Hilbert), not quasimetrics within the same learning algorithm. A reader of the main paper cannot verify whether $d_{\text{simple}}$ is actually superior to IQE or Wide Norm. Since this is listed as a headline contribution, a brief summary of the quasimetric ablation in the main text would strengthen the paper. (favorability=2.66)

- **Hyperparameter sensitivity for $d_{\text{max}}$ and $H_c$ not discussed.** The contrastive loss (Equation 6) uses $d_{\text{max}}$ and the constraint loss (Equation 7) caps at $H_c$. The paper does not explain how these are chosen or how sensitive results are to their values, which affects practical usability. (favorability=4.96)

### Trivial
None.

## Nice-to-Haves
- An ablation removing the $L_o$ term (direct regression) from MadDist would clarify how much of the gain comes from direct MAD supervision vs. the contrastive/constraint regularization.
- The paper could discuss sensitivity to the behavior policy: since MAD is defined as the minimum over *any* policy and the paper uses random-policy trajectories (which yield loose upper bounds $j-i$), it would be useful to understand how MAD estimate quality degrades with highly suboptimal behavior policies.

## Removed Points
These points are flagged to be removed, treat them with caution:
- [Removed] "QRL comparison is potentially unfair because QRL was not designed to approximate MAD" — The paper compares against QRL as a representative quasimetric representation learning method; testing whether its learned distances happen to align with MAD is a legitimate scientific comparison. The paper does not claim QRL was designed for this task.
- [Removed] "NoisyGridWorld results not shown in main paper" — Results for this environment are in Appendix F (stripped by parser).
- [Removed] Claims about the paper not including certain related work — The hard rules prohibit penalizing missing related work.

## Novel Insights
None beyond the paper's own contributions. The review largely reinforces the paper's own framing (asymmetric MAD is important, quasimetrics are the right tool) while identifying a specific empirical gap in the experimental comparison.

## Suggestions
- **Add Steccanella & Jonsson (2022) as a baseline** on the asymmetric environments (KeyDoorGridWorld, CliffWalking) to cleanly isolate the benefit of the quasimetric.
- **Resolve the 3-seed vs 5-seed inconsistency** between Section 7 and the Figure 3 caption.
- **Include a brief summary of the $d_{\text{simple}}$ vs IQE vs Wide Norm ablation** in the main paper (e.g., a small table or bar chart) to substantiate the abstract-level claim.
- **Re-frame TDMadDist** explicitly as an ablation/exploratory variant rather than a co-equal contribution, and correct the imprecise statement about it underperforming QRL on all environments.
- **Discuss or acknowledge sensitivity** to $d_{\text{max}}$ and $H_c$ hyperparameters.

## Calibration Anchors

All anchors retrieved across all rounds:

| Path | Avg Human Score | Round | Itemized? | Comparison to this paper |
|------|----------------|-------|-----------|--------------------------|
| `Uj0h13lVrR.md` (GFlowNets) | 1.00 | R1 | No | Low-quality paper with no topical relevance; our paper is substantially stronger. |
| `bEgDEyy2Yk.md` (APPD matrix) | 1.00 | R1 | No | Low-quality implementation paper; our paper has a clear research contribution. |
| `P49gSPmrvN.md` (UMAP discourse) | 1.00 | R1 | No | Not RL; irrelevant. |
| `gwZ90hFSL2.md` (Robot NLP) | 1.00 | R1 | No | Not RL; irrelevant. |
| `Zi1QNJKXAD.md` (Robust MDP) | 3.20 | R1 | No | Different subfield (robust MDPs); our paper has stronger empirical grounding. |
| `EWKPEtwjTy.md` (Discrete Actor-Critic) | 2.50 | R1 | No | General RL algorithm paper; less focused contribution than ours. |
| `CaNp8ALCRT.md` (Bayesian MDP) | 3.00 | R1 | No | Drug discovery application; our paper has clearer technical contribution. |
| `C9BA0T3xhq.md` (Offline Q-learning) | 2.00 | R1 | No | Offline RL algorithm paper; our paper's distance-learning focus is more specific. |
| `oEzY6fRUMH.md` (State Chrono Rep.) | 4.75 | R1, R2 | Yes | Also about temporal info in state representations. Our paper's experiments are more convincing (no overlapping CIs) and the problem framing is cleaner. | 
| `GwKNdRc9Bj.md` (Action Distances for PbRL) | 3.75 | R1 | No | Uses action distances for reward learning; different goal from ours. |
| `LSrDaGWTnv.md` (Contrastive Rep. Planning) | 4.33 | R1 | No | About contrastive learning for planning; our paper has stronger empirical validation. |
| `UlAkM88Vum.md` (AC Imitation Learning) | 5.00 | R1, R2 | No | Imitation learning with action constraints; our paper has a more direct contribution to distance learning. |
| `qofh48zW3T.md` (Dist. Distance Classifiers) | 6.00 | R1 | Yes | Similar topic (distance in GCRL) but focused on stochastic shortest-path critique. Our paper's experiments are more comprehensive, and it has fewer theoretical gaps. |
| `I7DeajDEx7.md` (ETD - Temporal Distance) | 6.75 | R1 | Yes | Strong paper with positive reviews. Our paper has similarly well-motivated contributions but a more notable missing-baseline gap. |
| `cWdAYDLmPa.md` (Unbalanced Atlas) | 6.67 | R1 | No | State representation learning with manifold methods; different approach. |
| `wPhbtwlCDa.md` (STARC - Reward Diff) | 6.50 | R1 | No | Reward function comparison framework; different subfield. |
| `9pW2J49flQ.md` (DeepLTL) | 8.00 | R1 | No | LTL-based RL; stronger paper with more comprehensive evaluation. |
| `agPpmEgf8C.md` (Predictive Aux. Obj.) | 8.00 | R1 | No | Neuroscience-inspired RL; different topic. |
| `7BLXhmWvwF.md` (Geometry-aware RL) | 8.00 | R1 | No | Robot manipulation; different domain. |
| `g7ohDlTITL.md` (Flow Matching) | 8.00 | R1 | No | Generative modeling; different field. |
| `9SwObx9Jdn.md` (Geodesics w/ RL) | 4.75 | R2 | No | Path planning on manifolds; tangential to our work. |
| `41WIgfdd5o.md` (Ex-BMDP STEEL) | 6.25 | R2 | Yes | Provable representation learning in MDPs; our paper is more empirical but has a clearer practical contribution. |
| `s9SVlWOcLt.md` (Proto Successor Measure) | 6.75 | R2 | Yes | Zero-shot RL with theoretical focus; our paper has stronger empirical validation across more environments. |
| `WQ6rnDriHj.md` (Discrete Actions) | 4.75 | R2 | No | Action space design; different topic. |

**Bracket rationale.** Round 1 bracketing placed the paper between scores 4.5 and 8.5, with the most topically similar anchors in the 4.75–6.75 range. Round 2 narrowed the bracket to 5.5–7.0. Comparing item-level favorability: this paper's strengths (all 9+) are competitive with the 6.75 anchors (ETD, Proto Successor Measure), while the worst weakness (1.17, missing baseline) is less severe than the worst weaknesses of those anchors (ETD had -4.74 for "limited innovation"; PSM had -4.77 and -1.74). The paper's strengths — particularly the downstream planning results (10.58) and the benchmark suite (9.52) — are stronger than those of the 6.00 anchor (Distributional Distance Classifiers). The major weakness is concrete and fixable, not a fundamental flaw. Hence the final score of **6.5**, reflecting a solid paper with clear contributions held back by an addressable experimental gap.

## Score and Decision

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>
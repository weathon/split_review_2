## Summary
This paper proposes two algorithms—MadDist and TDMadDist—for learning the Minimum Action Distance (MAD) from unlabeled state trajectories, without requiring reward signals or action labels. The central contributions are: (1) a scale-invariant trajectory-supervision loss with an asymmetric quasimetric distance function (MadDist); (2) a bootstrapped TD variant (TDMadDist); (3) a novel simple quasimetric d_simple; and (4) a controlled evaluation suite with computable ground-truth MAD. MadDist achieves near-perfect or perfect planning success across all OGBench PointMaze variants.

---

## Strengths

- **Clean LP formulation of MAD (Section 4, Eq. 1).** Framing MAD as the unique solution to a max-sum constrained optimization—connecting to all-pairs shortest-path and Floyd-Warshall—gives the method principled theoretical grounding and makes the problem statement precise.
- **Principled motivation for asymmetry (Sections 2 and 5, Figure 3).** The paper identifies a specific and underappreciated limitation of prior work (symmetric metrics for an inherently asymmetric quantity) and tests it with environments that stress-test directionality (CliffWalking, KeyDoorGridWorld). Figure 3 shows the symmetric Hilbert baseline failing clearly in these environments, making the case concrete rather than generic.
- **Scale-invariant loss (Section 6.1, Eq. 5).** Normalizing the squared error by (j−i) prevents distant state pairs from dominating the loss due to absolute magnitude—a simple, well-motivated improvement over Steccanella & Jonsson (2022) (Eq. 2).
- **Evaluation suite with known MAD (Section 7).** Environments covering stochastic transitions, asymmetric dynamics, continuous states, and noisy observations with computable ground-truth MAD is a genuine standalone contribution that fills a real gap in the literature.
- **Strong downstream planning results (Table 1).** MadDist achieves near-perfect or perfect success rates across all six OGBench PointMaze variants—including stitch datasets requiring composition from disconnected trajectories—concretely validating the utility of the learned representations.

---

## Weaknesses

### Fatal
None.

### Major

- **Steccanella & Jonsson (2022) absent as a direct baseline.** Section 6.1 explicitly states MadDist is an extension of S&J 2022 differing in two design choices: quasimetric distance function and scale-invariant loss. Yet S&J 2022 appears nowhere in Figure 3 or Table 1. The two chosen baselines—QRL (Lagrangian locality constraints, different learning signal) and Hilbert (symmetric, structurally disadvantaged in asymmetric environments)—do not isolate the contribution of each design choice. It is impossible to determine from current experiments whether improvement over QRL is due to the quasimetric, the scale-invariant loss, or the trajectory-path supervision. Adding S&J 2022 with d_simple substituted in—or MadDist with a symmetric metric—would cleanly attribute the gains.

- **TDMadDist underperforms MadDist without diagnostic explanation.** Section 7 Discussion states: "While TDMadDist underperforms the MadDist and QRL algorithm, its strong performance relative to Hilbert highlights the advantages of our quasimetric approach." Table 1 confirms TDMadDist is inferior to MadDist in five of six environments and to QRL in several. The paper does not diagnose why bootstrapping hurts—whether due to target-network instability, conflict between the bootstrap target and the hard upper-bound constraint, or optimization dynamics. Presenting TDMadDist as a co-equal contribution ("our second algorithm") while it consistently underperforms and lacks diagnosis leaves an unresolved methodological gap.

### Minor

- **d_simple ablation absent from main body.** The abstract and Section 1 both claim d_simple "outperforms more elaborate quasimetrics in the existing literature." This is a stated contribution. The ablation isolating d_simple vs. WN vs. IQE within MadDist is relegated to Appendix E only, while the main experiments compare MadDist (d_simple) vs. QRL (IQE) with different learning signals—confounding metric architecture with learning objective. The key supporting evidence for this claim should appear in the main body.

- **Seed-count discrepancy.** Figure 3 caption states results over "three random seeds," while Section 7 Empirical Setup states "five independent runs." This inconsistency should be clarified.

- **Random-policy coverage in large environments unaddressed.** Section 7 uses a random policy for offline data collection. In large environments (OGBench GiantMaze, 100×100 grid), random-policy coverage may be severely non-uniform. The paper does not discuss how coverage quality affects representation quality or what assumptions about coverage are needed for the method to generalize to unseen state pairs. This is distinct from the dataset-size ablation in Appendix E.

### Trivial

- **"Stopping stone" typo.** Section 8: "fundamental stopping stone" should read "stepping stone."

---

## Nice-to-Haves

- A brief forward-looking experiment or discussion integrating MAD into an actual goal-conditioned RL training loop or reward-shaping setting would close the gap between the motivational framing (Sections 1–2) and the empirical evidence provided (representation quality + planning success).
- Reposition TDMadDist as an analysis/ablation contribution: if bootstrapping systematically degrades performance relative to direct supervision, this is itself an informative finding about offline distance learning that could be framed positively.

---

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- **Garbled Eq. 9 (Section 6.2).** The reviewer notes the loss term L'_r appears garbled ("d_θ(si, si+1 + d_θ'(si+1, sr) - 12(9))"). This is a PDF parser extraction artifact, not an author error. The surrounding prose (Section 6.2: "the objective is to make d_θ(si, sr) equal to 1 + d_θ'(si+1, sr)") clarifies intent. **Removed per hard rule on formatting artifacts.**
- **LP uniqueness intuition missing from main text.** Reviewer suggests adding one sentence of intuition for why the LP max-sum selects the shortest path. The proof is in Appendix A; this is a trivial presentation nit. **Removed as appendix-related nitpick.**
- **Figure 3 vs. Table 1 seeds discrepancy** promoted from trivial to minor since both figures appear in main body and the inconsistency is verifiable.

---

## Novel Insights
The contrast between MadDist's consistently strong performance and TDMadDist's degradation under bootstrapping is itself an informative empirical finding—trajectory-path supervision appears more stable than TD-style bootstrapping for offline distance learning. This resonates with observations in offline RL that bootstrapping from an imprecise target network can amplify errors, and the result suggests that for MAD specifically, the hard upper-bound constraint from trajectory paths provides a more reliable training signal than bootstrapped estimates. If diagnosed explicitly, this failure mode would be a contribution rather than a weakness.

---

## Suggestions
1. Add S&J 2022 as a direct baseline, ideally with both the original symmetric metric and d_simple substituted in, to cleanly attribute gains to each design choice.
2. Either diagnose why bootstrapping hurts in TDMadDist (instability analysis, conflict with upper-bound constraint, target-network lag) and reframe it as an informative finding, or de-emphasize it as a co-equal contribution.
3. Bring the d_simple vs. WN vs. IQE ablation (Appendix E) into the main body as a table, since this directly supports a stated contribution claim.

---

## Calibration Anchors

| Path | Avg Human Score | Round | Comparison |
|---|---|---|---|
| Uj0h13lVrR.md | 1.0 | R1 | Strong reject; not comparable—low quality paper |
| bEgDEyy2Yk.md | 1.0 | R1 | Strong reject; not comparable |
| Q1Hr9dVfDS.md | 3.0 | R1 | Reject; continual RL method, weaker contribution |
| fnO5h1CFyh.md | 3.0 | R1 | Reject; successor representation paper, less rigorous |
| oEzY6fRUMH.md | 4.75 | R1 | Borderline reject; temporal representation paper, similar scope but weaker |
| GwKNdRc9Bj.md | 3.75 | R1 | Reject; uses action distances for reward learning, similar topic, less rigorous evaluation |
| mcDAY9PoDJ.md | 4.5 | R1 | Borderline reject; offline RL in compact latent space |
| qofh48zW3T.md | 6.0 | R1 | Borderline accept/reject; distributional distance classifiers for GCRL—closest topical anchor, rejected |
| M992mjgKzI.md | 7.0 | R1 | Accept; OGBench benchmark (major benchmark contribution with 85 datasets) |
| o2IEmeLL9r.md | 7.33 | R1 | Accept; pre-training goal-based models, broader scope |
| eY5JNJE56i.md | 6.75 | R1 | Accept; offline RL with OOD generalization |
| 9pW2J49flQ.md | 8.0 | R1 | Strong accept; LTL in RL, substantially broader scope |

**Round 1 bracket:** 5.5–7.0

The paper is clearly above the 3.5–5.5 reject range (it has working methods, principled theory, strong empirical results, and a genuine benchmark contribution). The most comparable topical anchor is qofh48zW3T (avg 6.0, rejected for GCRL distance learning), but the paper under review has cleaner theory, more rigorous evaluation, and stronger downstream results. The OGBench paper (7.0, accepted) is a substantially larger benchmark contribution. The missing S&J baseline (Major weakness) is the primary factor preventing a confident borderline-accept recommendation; MadDist results are credible on their own, and the evaluation suite is a genuine contribution. The TDMadDist issue is real but secondary. I place this paper at **6.0**—borderline accept with major revision request on the direct prior-work comparison.

---

## Score and Decision

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>
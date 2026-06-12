**Calibration Anchors (all rounds):**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/Uj0h13lVrR.md` | 1.00 | 1 | Strong reject — GFlowNets paper, fundamentally flawed; much weaker than current paper |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/5AbtYdHlr3.md` | 3.00 | 1 | Reject — stochastic action model learning; different topic, weaker evaluation |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/oEzY6fRUMH.md` | 4.75 | 1 | Borderline reject — state representation for RL generalization; had overlapping CIs and ad-hoc losses; current paper is stronger |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/GwKNdRc9Bj.md` | 3.75 | 1 | Reject — action distances for reward learning; different framing, narrower evaluation |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/TOiageVNru.md` | 6.00 | 1 | **Most similar anchor** — self-supervised TD metric learning for motion planning; accepted despite ablations on single environment and hyperparameter sensitivity concerns; current paper is cleaner methodologically |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/qofh48zW3T.md` | 6.00 | 1 | Rejected but had fundamental conceptual issues (questioning premise of distance-based methods); current paper has no such conceptual flaws |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/wPhbtwlCDa.md` | 6.50 | 1 | Accept — STARC reward metrics; stronger theory but narrower empirical scope |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/EW6bNEqalF.md` | 7.00 | 1 | Accept — offline RL with language metrics; rigorous theory, small-scale experiments |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/cNmu0hZ4CL.md` | 8.00 | 1 | Strong accept — neural population dynamics; different domain, exceptional clarity and rigor |

**Round 1 bracket:** 5.5–7.0 (above State Chrono Rep at 4.75, comparable to Physics-informed TD Metric Learning at 6.0, below STARC at 6.5 in theoretical rigor but comparable in overall contribution)

---

## Summary

This paper proposes MadDist (and a TD variant TDMadDist) for learning the Minimum Action Distance (MAD) between states in an MDP using only state trajectories — no rewards or actions are required. The key ideas are: (1) a scale-invariant loss that normalizes distance prediction errors by trajectory step counts, preventing long-range state pairs from dominating the loss; (2) support for asymmetric (quasimetric) distance functions via a simple convex-combination quasimetric; and (3) a suite of benchmark environments with known ground-truth MAD for systematic evaluation. Experiments across discrete and continuous environments show MadDist outperforming QRL and Hilbert baselines on correlation metrics and downstream planning success rates.

## Strengths

1. **Scale-invariant loss (Eq. 5) is a genuine, clean improvement over prior work.** The prior formulation (Eq. 2 from Steccanella & Jonsson, 2022) minimizes raw squared error `(d_θ − (j−i))²`, which lets long-range state pairs dominate purely because their targets are larger. Normalizing by `(j−i)` equalizes contributions across distances. This is principled and likely the main driver of MadDist's improvement.

2. **Ground-truth MAD benchmark suite is a useful community resource.** Prior work on MAD approximation has not been systematically evaluated against known ground truth. Creating environments (KeyDoorGridWorld, CliffWalking, NoisyGridWorld, PointMaze variants, OGBench) where the true MAD is computable via Floyd‑Warshall or Manhattan distance enables apples-to-apples comparison across methods.

3. **Explicit handling of asymmetric distances is well-motivated and validated.** Symmetric metrics (Euclidean distance in embedding space) cannot capture irreversible dynamics like the key-door structure or CliffWalking's shortcut. The paper correctly identifies this limitation and demonstrates empirically that quasimetric variants substantially outperform symmetric ones.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **Seed count inconsistency between main text and figure captions.** The Experimental Setup (line 220) reports "means over five independent runs (random seeds)," but the Figure 3 caption (lines 232, 238) repeatedly states "Shaded regions indicate minimum and maximum values across three random seeds." This is a concrete factual discrepancy that needs correction. While it does not invalidate the results, it undermines confidence in reporting accuracy.

2. **TDMadDist's role in the paper is unclear.** The paper acknowledges (line 226) that "TDMadDist underperforms the MadDist and QRL algorithm," yet presents it as a "novel algorithm" alongside MadDist. Its justification — that TDMadDist's "strong performance relative to Hilbert highlights the advantages of our quasimetric approach" — is circular, since MadDist already demonstrates this more convincingly. Including an underperforming variant without explaining what insight (e.g., about TD learning for MAD) it provides weakens the narrative.

3. **Perfect success rates with zero variance in Table 1 warrant more discussion.** MadDist achieves 1.00 ± 0.00 on 4 of 6 OGBench environments. While baselines do not reach this ceiling (confirming the task discriminates between methods), the zero variance and ceiling scores invite questions about whether these particular environments are sufficiently demanding at the top end. A brief discussion of the planning task's sensitivity to distance quality would help.

4. **TDMadDist's Equation 9 contains a garbled cross-reference artifact.** The equation shows "12(9)" where the intended expression should appear. While the surrounding text explains the bootstrapping intuition, the corrupted equation prevents the reader from verifying the exact loss formulation.

### Trivial
None.

## Nice-to-Haves
- Include a subset of stochastic/noise results (e.g., NoisyGridWorld) in the main paper rather than only the appendix, since robustness to stochasticity and observation noise is a central claim in the abstract and introduction.
- Provide a brief description of the planning task (currently Appendix H) in the main paper, given that the perfect scores in Table 1 raise questions about how learned distances are used downstream.
- If space permits, move the d_simple vs. IQE/Wide Norm ablation from Appendix E to the main paper, since the introduction claims d_simple "outperforms more elaborate quasimetrics."

## Removed Points
*These points were flagged during review consolidation but do not appear in the final evaluation.*

- **Stochasticity/noise claim not supported in main paper:** Removed because the appendix (where these results live) was stripped by the parser; per guidelines, missing appendix content is not a valid criticism.
- **d_simple superiority not demonstrated in main paper:** Removed for the same reason — the ablation is in Appendix E, which was stripped.
- **Hyperparameters not in main paper:** Removed per guideline that undisclosed hyperparameters constitute a nitpick-level reproducibility concern.
- **TDMadDist conceptual concern about random-state bootstrapping:** The reviewer questioned whether bootstrapping from random states (`s_r`) is valid, but the paper's TD formulation — making `d_θ(s_i, s_r) ≈ 1 + d_{θ'}(s_{i+1}, s_r)` — is standard; the target network provides estimates that are refined through training. This criticism reflects a misunderstanding of TD learning.
- **Contrastive loss potentially distorting nearby-state distances:** Speculative concern without concrete evidence in the paper.
- **Formatting/parser artifacts in Eq. 9:** Strictly a parser issue, not an author error.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
- Reconcile the seed count (3 vs 5) and correct the inconsistency in the final version.
- Either provide a clearer justification for TDMadDist or move it to an ablation/appendix section, since it underperforms the simpler variant.
- Add a brief discussion of the planning task's difficulty level to contextualize the ceiling scores in Table 1.
- Consider adding a controlled experiment where the planning task difficulty is varied (e.g., by reducing trajectory count or adding noise) to demonstrate that the success rate degrades gracefully.

## Score and Decision

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>
## Summary

SPOT proposes a clean, well-motivated framework for mitigating reward extrapolation errors in offline preference-based RL. The core idea is to use attention weights from the Preference Transformer as importance signals to identify subgoals from preferred trajectories, train a CVAE to model the subgoal distribution, and use cosine similarity to predicted subgoals as a reward shaping signal. The method is evaluated on 10 task variants across 3 benchmarks against 7 baselines.

## Strengths

- **Well-motivated problem.** Extrapolation errors in offline PbRL are a genuine challenge, and the paper correctly identifies the fundamental tension: reward models trained on preference-labeled data must generalize to states visited during policy optimization, where distribution shift can cause catastrophic misestimation. [favorability=13.05]

- **Clean conceptual pipeline.** The idea of using attention weights from the Preference Transformer as importance signals to identify subgoals, training a CVAE to model the distribution of those subgoals, and then using cosine similarity to predicted subgoals as a reward shaping signal is coherent and intuitively appealing. Each step follows naturally from the previous one. [favorability=11.98]

- **Reasonably broad evaluation.** The paper evaluates on three benchmarks (D4RL locomotion, Robosuite manipulation, Meta-World) with 10 task variants, comparing against 7 baselines including recent methods like DTR and HPL. The ablations on Top-K% and reward shaping methods probe the design space in useful ways. [favorability=11.31]

## Weaknesses

### Major

- **Claims overstate the empirical results.** The abstract and introduction assert "state-of-the-art performance" and "consistent superiority" (lines 40-42, 216 of the paper), but Table 1 shows SPOT substantially underperforms the best baseline on several tasks:
  - lift-mh: 65.17 vs MR 95.62 (trailing by 30.45 points)
  - drawer-open: 66.80 vs IPL 87.64 (trailing by 20.84)
  - can-ph: 63.82 vs Oracle 73.25 (trailing by 9.43)
  - hopper-m-r: 85.08 vs DTR 94.18 (trailing by 9.10)

  Additionally, the headline average comparison (SPOT 78.82 vs Oracle 77.25) is not apples-to-apples: the paper explicitly notes that Oracle's average is computed over 8 tasks (excluding Meta-World), while SPOT's average covers all 10 tasks (line 191). The paper would be stronger with claims calibrated to the actual evidence — SPOT achieves competitive average performance with notable task-specific weaknesses, not "consistent superiority."

- **The extrapolation error analysis (Figure 2) uses the same metric that SPOT explicitly optimizes.** The x-axis in Figure 2 measures cosine similarity between the predicted subgoal and the current state — the same cosine similarity that appears in SPOT's reward shaping term (Eq. 11-12, lines 168-174). Since SPOT's policy is explicitly trained to maximize this similarity, it is expected that SPOT's visited states concentrate in high-similarity regions. The paper does not control for state visitation distribution. A meaningful comparison would measure extrapolation error on a fixed held-out set of states for both PT and SPOT, rather than on the different distributions each method's policy happens to visit. This weakens the central evidence for the paper's headline contribution of "mitigating reward extrapolation errors." (Note: this is not a "tautology" — the comparison between PT and SPOT at matched similarity levels is still informative — but the analysis conflates the effect of SPOT changing the visitation distribution with the effect of SPOT directly reducing reward model error.)

### Minor

- **The query efficiency claim (Table 4) is only supported against a single baseline.** SPOT is compared only against PT on reduced query budgets, not against other baselines (IPL, HPL, CPL, DTR). Without comparisons to these methods, the claim of enhanced query efficiency is incomplete.

- **The qualitative subgoal analysis (Section 5.4) over-interprets thin evidence.** The claim of "temporal anticipation" — that "subgoals consistently lead actual execution by approximately one timestep forward" (line 281) — is based on only 4 frames with no quantitative measurement of temporal offset distribution. This is suggestive illustration, not evidence.

- **The dual-criteria filtering (Section 4.1.2) may introduce a systematic bias.** Selecting states with both top-K% attention AND above-average reward biases subgoals toward the easiest, most predictable parts of preferred trajectories, potentially excluding genuinely informative but harder-to-predict critical states near decision boundaries. The paper does not analyze this potential limitation.

## Trivial

None.

## Nice-to-Haves

- An ablation without the CVAE (using raw attention-weighted states or random states as subgoals) would isolate the CVAE's contribution.
- Statistical significance testing across the 5 seeds would clarify which comparisons are meaningful given the high variance on some tasks (e.g., hopper-m-r DTR: 94.18±0.28 vs SPOT: 85.08±1.32).
- Analysis of why SPOT fails on specific tasks (lift-mh, drawer-open) would strengthen understanding of the method's boundary conditions.

## Removed Points

The following items from the input review were removed per filtering rules:

1. **Implementation details / reproducibility** (Critical Issue 3 from the harsh critic: missing CVAE architecture, training hyperparameters, IQL config, preference dataset size, etc.) — Removed per hard rule about reproducibility nitpicks (undisclosed hyperparameters and trivial implementation details). That said, the paper's setup section (line 212) is genuinely sparse at one sentence; authors should consider adding a brief appendix with architectural specifics.
2. **CVAE logical tension** (Critical Issue 4: "if the CVAE can generate subgoals for OOD states, why can't the reward model also generalize?") — Partially a strawman. The paper's argument is that the CVAE's KL regularization keeps subgoal outputs in-distribution, and the shaping reward steers the policy toward those in-distribution targets — the CVAE does not need to "generalize" in the same way the reward model does. However, the paper does not empirically verify whether CVAE-generated subgoals conditioned on OOD states actually stay in-distribution, which would be a legitimate extension.
3. **Section-by-section notation nitpicks** (Markovian vs non-Markovian inconsistency, Eq 3 notation) — Minor formatting/notation issues per hard rules.
4. **Introduction claim about "overlook rich information"** — Rhetorical critique, not a substantive weakness impacting the paper's technical contribution.

## Novel Insights

The harsh critic's identification of the shared metric between the extrapolation error analysis (Figure 2) and the reward shaping objective (Eq. 11-12) is the most valuable observation not already in the paper. While the critic overstates this as a "tautology" (the PT-vs-SPOT comparison at matched similarity levels is still meaningful), it is a genuine confounding-variables concern that the paper should address. The critic's observation about the non-apples-to-apples average comparison (10 vs 8 tasks) is also a valid point that the paper itself acknowledges but does not adequately defuse.

## Suggestions

1. **Redesign the extrapolation error analysis** to measure error on a fixed held-out set of states for both PT and SPOT. Separate the claim into two testable pieces: (a) SPOT changes the state visitation distribution, and (b) states closer to the training distribution have lower reward model error.
2. **Calibrate the claims.** Replace "state-of-the-art performance" and "consistent superiority" with a measured characterization that acknowledges SPOT's competitive average performance and its task-specific weaknesses.
3. **Add a CVAE ablation** comparing SPOT against a version that uses raw attention-weighted states (or random states) as subgoals without the CVAE.
4. **Add statistical significance tests** or confidence intervals to clarify which performance differences are meaningful.
5. **Discuss failure cases** (lift-mh, drawer-open) to illuminate the method's boundary conditions.

---

**Calibration summary.** All anchors retrieved across rounds:

| Anchor | Avg Score | Round | Itemized | Comparison |
|--------|-----------|-------|----------|------------|
| Uj0h13lVrR (GFlowNets) | 1.00 | R1 | No | Unrelated topic |
| gwZ90hFSL2 (Humanoid) | 1.00 | R1 | No | Unrelated topic |
| MFwYXa796v (OPRIDE, offline PbRL) | 5.00 | R1,R2 | Yes | Same subfield; SPOT has cleaner motivation and broader eval but OPRIDE has theoretical guarantees |
| 4HNfKrGlSJ (HPL, offline PbRL) | 5.20 | R1,R2 | Yes | Same subfield; comparable quality, HPL slightly stronger in reviewer enthusiasm (one 8) |
| HSUSo9p8X5 (Stochastic Subgoal) | 5.75 | R1,R2 | Yes | Different setting (HRL); partially relevant subgoal idea |
| o2IEmeLL9r (PTGM, goal pretraining) | 7.33 | R1 | No | Different setting; stronger theoretical/empirical package |
| lWe3GBRem8 (Offline RL for Online RL) | 6.00 | R1 | No | Different subproblem |
| 2pJpFtdVNe (Sim-OPRL, offline PbRL) | 6.80 | R2 | Yes | Accepted PbRL paper; has theoretical guarantees that SPOT lacks |
| NLevOah0CJ (Hindsight PRIORs, PbRL) | 6.33 | R2 | Yes | Accepted PbRL paper; stronger empirical analysis and presentation |
| 38kLrJNwaM (LEASE, offline PbRL) | 6.00 | R2 | No | Rejected despite 6.0; similar quality tier |
| gXV84CnMUm (Outward Odyssey, PbRL) | 5.50 | R2 | No | Same tier, rejected |

**Round-1 bracket:** 4.0–6.5. **Round-2 narrowing:** compared against PbRL anchors at ~5.0–6.8. SPOT sits above OPRIDE (5.0, rejected) in motivation breadth but below Sim-OPRL (6.80, accepted) and Hindsight PRIORs (6.33, accepted), which offer stronger evidence for their core claims. The most damaging items in SPOT's draft (overclaiming at favorability −1.45, extrapolation analysis at −1.34) are more negative than most items in the accepted PbRL anchors' weakness lists. **Final score:** 5.0.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>
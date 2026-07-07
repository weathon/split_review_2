Now I have all the calibration data I need. Let me produce the final review.

## Summary

SPOT proposes a method for offline preference-based RL that extracts "subgoals" from Preference Transformer attention weights (high-attention, high-reward states from preferred trajectories), trains a CVAE to generate these subgoals conditioned on current state-action pairs, and uses cosine similarity between predicted subgoals and next states as a reward shaping term to reduce extrapolation errors. The pipeline (PT attention → dual-criteria filtering → CVAE → cosine shaping) is coherent and novel.

## Strengths

1. **Targets a well-identified problem.** The paper correctly identifies reward model extrapolation errors from distribution mismatch between preference-labeled and policy-optimization data as a core challenge in offline PbRL (Section 1).

2. **Novel pipeline with direct evidence for its central mechanism.** The combination of PT attention weights, dual-criteria filtering (top-K% attention + above-average reward), CVAE-based generation, and cosine-similarity reward shaping is a coherent and novel architecture. The extrapolation error analysis (Figure 2) provides direct evidence that SPOT reduces OOD reward prediction errors compared to PT (OOD error ~0.98→0.45 for SPOT vs ~1.22→0.85 for PT at high similarity values). This is the paper's strongest empirical exhibit.

3. **Highest average performance across a diverse benchmark suite.** SPOT achieves the highest aggregate average (78.82) across 10 tasks spanning locomotion and manipulation (Table 1), with reduced average standard deviation (7.76 vs PT's 13.80). The method demonstrates improved robustness, avoiding catastrophic failures on several tasks where other methods collapse.

## Weaknesses

### Fatal
None.

### Major

1. **"State-of-the-art" and "consistent superiority" claims are not supported per-task.** The abstract claims "state-of-the-art performance" and Section 5.1 states "consistent superiority," but SPOT ranks first on only 2 of 8 locomotion+Robosuite tasks (Table 1: walk-m-r and can-mh). On multiple tasks it trails: hop-m-r (85.08 vs DTR 94.18), can-ph (63.82 vs Oracle 73.25 and IPL 67.98), drawer-open (66.80 vs MR 86.6 and IPL 87.64). The contribution is improved *average performance and robustness*, not consistent per-task dominance. This rhetorical overclaiming should be corrected.

2. **The DTR baseline appears significantly disadvantaged on manipulation tasks.** DTR (Tu et al., 2025), the most closely related prior method that also addresses extrapolation errors in offline PbRL, uses the same IQL backbone. It achieves top scores on hop-m-r (94.18) and hop-m-e (102.12) but catastrophically low scores on lift-ph (9.86), plate-slide (5.24), and drawer-open (26.90) — far below even simple baselines like MR. This bimodal distribution strongly suggests DTR's hyperparameters were not tuned for manipulation domains. Since the paper does not describe baseline tuning procedures, the comparison as presented may overstate SPOT's relative advantage. Fair per-domain tuning of DTR could substantially change the rankings.

3. **The "ground truth" proxy in the extrapolation error analysis is confusingly described, undermining a key experiment.** Section 5.3 states: "Since true ground-truth rewards are unavailable in real environments, we use human-labeled rewards from the dataset as proxy ground truth" (line 249). For D4RL Gym-MuJoCo tasks, simulator ground-truth rewards are available and are standardly used (the paper's own Oracle baseline uses "ground-truth reward from the dataset," line 210). Additionally, D4RL has no "human-labeled rewards." The underlying approach (using dataset rewards as proxy) is reasonable, but this confusing terminology and incorrect justification diminish confidence in Figure 2, which is otherwise the paper's most compelling experiment.

### Minor

4. **"Subgoal" framing oversells what the method actually does.** The paper presents attention-filtered states as "critical decision points or milestones" (line 27). These states are better characterized as discriminative high-reward states from preferred trajectories — useful as distributional anchors for reward shaping. The method is not validated as discovering a genuine task-hierarchy decomposition, and calling it "subgoal discovery" suggests more than is established. This is a framing issue, not a methodological flaw — the regularization effect is real regardless of naming.

5. **"Forward-looking subgoal" claim lacks quantitative support.** The claim that subgoals "consistently lead actual execution by approximately one timestep forward" (line 281) rests solely on qualitative visualization (Figure 3). The training design (pairing state-action pairs between subgoal g_{t-1} and g_t with target g_t) does provide a plausible mechanism for forward prediction, but no quantitative timing analysis is provided to substantiate the specific "one timestep" claim.

6. **Single λ=1 across all 10 tasks without justification.** The reward coefficient λ is fixed at 1 for all experiments (line 212), but sensitivity analysis (Table 3) is shown only for two locomotion tasks. Without λ sensitivity on manipulation tasks or a description of how λ=1 was selected (e.g., via a validation set), there is a risk of test-set information leakage.

7. **Potential-based reward shaping baseline is underspecified.** Table 3 compares against "Potential-based" shaping (Ng et al., 1999), but the potential function Φ is never defined or described, making this comparison uninterpretable.

8. **CVAE reconstruction quality is not analyzed.** The paper does not report subgoal reconstruction error, frequency of subgoal extraction per trajectory, or any diagnostic of CVAE prediction reliability. These are needed to assess the reliability of the shaping signal.

### Trivial

9. The phrase "human-labeled rewards from the dataset" (line 249) is incorrect for D4RL (which uses simulator rewards). The intended approach (using dataset rewards as proxy ground truth) is standard and reasonable; the terminology should be corrected.

## Nice-to-Haves

- Controlled experiment measuring CVAE prediction quality under systematic OOD shifts in (s, a) inputs.
- Per-domain λ sensitivity analysis on at least one manipulation task.
- Clarify the CVAE training temporal semantics: exactly how (s_t, a_t) pairs between consecutive subgoals are aggregated and paired with the target subgoal g_t (line 136 is ambiguous).
- Paired statistical testing (e.g., bootstrap) across seeds for the main results where standard deviations overlap substantially.

## Removed Points

These points are flagged to be removed, treat them with caution:
- *Missing implementation details (CVAE architecture, PT/SPOT/IQL hyperparameters, optimizer settings)* — removed per Hard Rule 7 (these are likely in the stripped appendix).
- *"Attention aggregation across PT heads/layers not specified"* — removed per Hard Rule 7 (appendix material).
- *"No statistical significance testing"* — removed because single-run evaluation with std reporting is standard for offline RL benchmarks; this is not a violated community expectation.
- *"Circularity about CVAE OOD behavior"* — removed as speculative; the paper does not claim CVAE is OOD-robust beyond the stated KL regularization, so this is not a demonstrated flaw.
- *"Query efficiency claim lacks mechanism"* — removed because the paper does articulate a mechanism (shaped rewards compensate for fewer preference queries); the finding is modest but valid.
- *Strength about "average performance across benchmark suite"* — removed because it conflicts with the verified weakness about per-task overclaiming (when a strength and weakness disagree, the weakness wins).

## Novel Insights

None beyond the paper's own contributions. The review notes that the temporal pairing in CVAE training (pairing (s_t, a_t) between consecutive subgoals with the later subgoal as target) creates an implicit forward-prediction mechanism, but this follows naturally from the design and is not a new insight.

## Suggestions

1. Replace "state-of-the-art" and "consistent superiority" rhetoric with a more precise framing centered on improved robustness and average performance.
2. Either tune DTR per-domain following its original protocol and report the results, or explicitly acknowledge the limitation as a caveat in Table 1.
3. Correct the "human-labeled rewards" terminology in Section 5.3 and clarify whether dataset rewards or another proxy is used.
4. Report CVAE reconstruction quality metrics and subgoal extraction statistics.
5. Add λ sensitivity results for at least one manipulation task and describe how the default λ=1 was selected.
6. Define the potential function Φ for the Potential-based shaping baseline.

## Calibration Anchors

The following anchors were retrieved and compared to calibrate the score:

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/Uj0h13lVrR.md | 1.00 | 1 | No | GFlowNets paper; very different topic, not comparable |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/gwZ90hFSL2.md | 1.00 | 1 | No | Humanoid robots; unrelated topic |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/5kMwiMnUip.md | 1.40 | 1 | No | LLM jailbreaking; unrelated |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/u1cQYxRI1H.md | 10.00 | 1 | No | Diffusion-based illumination; very different domain |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/OZ3NXrF3gQ.md | 2.50 | 1 | Yes | Reward-free policy opt; much weaker empirical validation than SPOT |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/5s1qpjrNvZ.md | 3.00 | 1 | No | Guided RL; limited evaluation vs SPOT's breadth |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/473sH8qki8.md | 2.00 | 1 | No | Reward as observation; very different framing |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/llXCyLhOY4.md | 3.00 | 1 | No | Goal-conditioned RL; different subfield |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/mDEYl0Ucgr.md | 5.25 | 1 | Yes | RLHF preference models; similar maturity, SPOT has broader eval |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/GwKNdRc9Bj.md | 3.75 | 1 | Yes | PbRL with action distances; **SPOT is stronger** (more tasks, direct extrapolation evidence) |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/quf7D5agqa.md | 4.00 | 1 | No | Hierarchical preference feedback; different approach |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/CTlUHIKF71.md | 5.25 | 1 | No | Visual representation alignment; different subfield |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/lWe3GBRem8.md | 6.00 | 1 | No | Offline RL exploration bias; cleaner evaluation than SPOT |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/QyVLJ7EnAC.md | 6.40 | 1 | No | Offline RL robustness; stronger theoretical grounding |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/eY5JNJE56i.md | 6.75 | 1 | Yes | Offline RL OOD generalization; **stronger than SPOT** (theory+clear evaluation) |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/OATPSB5JK1.md | 6.00 | 1 | No | Model-based offline RL; different subfield |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/9pW2J49flQ.md | 8.00 | 1 | No | LTL planning; very different |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/DzGe40glxs.md | 8.00 | 1 | No | Emergent planning; very different |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/8BAkNCqpGW.md | 8.00 | 1 | No | POMDP policy gradient; different |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/agPpmEgf8C.md | 8.00 | 1 | No | Predictive aux objectives; different |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/MFwYXa796v.md | 5.00 | 2 | Yes | Offline PbRL with in-dataset exploration; **most directly comparable** — similar strengths and weaknesses |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/Uxm7DxPwrZ.md | 4.80 | 2 | No | Offline goal-conditioned RL; somewhat related |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/4HNfKrGlSJ.md | 5.20 | 2 | Yes | Hindsight preference learning; comparable offline PbRL work |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/ruv3HdK6he.md | 5.75 | 2 | No | Online-to-offline agent alignment; somewhat related |

**Score determination:** The Round-1 bracket was 4–6, anchored by GwKNdRc9Bj (3.75 — PbRL with weaker evaluation) below and eY5JNJE56i (6.75 — offline RL OOD with strong theory) above. Round 2 narrowed to 5.0 by comparison with MFwYXa796v (5.00 — offline PbRL with comparable strengths and evaluation gaps). SPOT shares with MFwYXa796v the pattern of a novel but partially-incremental contribution with evaluation concerns (baseline fairness, claim-evidence mismatch), but SPOT's extrapolation error analysis (Figure 2) gives it a slight advantage over the 5.00 anchor, while the DTR evaluation concern prevents a higher score. The paper is slightly stronger than GwKNdRc9Bj (3.75, PbRL with narrow evaluation) but clearly weaker than eY5JNJE56i (6.75, cleaner evaluation and theoretical backing). Score: **5.0**.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>
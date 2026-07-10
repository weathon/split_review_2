## Summary

This paper tackles worst-case robust pursuit-evasion under partial observability on graphs. It contributes: (1) a proof that the existing DP algorithm (Algorithm 1) produces optimal policies under asynchronous evader moves without recomputation (Theorem 2, Corollary 1); (2) a low-complexity belief preservation mechanism (O(|V|) per step) that extends DP policies to partial observability; and (3) an RL training scheme (R2PS) that embeds belief preservation into the EPG cross-graph training framework to learn zero-shot generalizing GNN pursuit policies. Empirical results show R2PS consistently outperforms a PSRO policy trained directly on each test graph, and achieves <0.01s GPU inference on graphs with up to 2065 nodes.

## Strengths

- **Clean theoretical extension of DP to asynchronous moves.** Lemma 1 and Theorem 2 prove that the same distance table D from Algorithm 1 yields strictly optimal policies for both players under asynchronous evader moves without recomputation (Section 3.1). This result has standalone value independent of the RL pipeline.

- **Belief preservation mechanism is simple, efficient, and empirically effective.** The belief update (Eq. 7) compresses observation history into a vector of size O(|V|) (Section 3.2). The belief-averaged DP policy (Eq. 6) consistently outperforms the position-based minimax policy (Eq. 5) across all 10 test graphs, often by a large margin (e.g., 0.25→0.48 on Hollywood Walk of Fame, 0.24→0.36 on Sagrada Familia; Table 1).

- **Strong zero-shot generalization results.** R2PS, trained on 300 graphs never seen during testing, consistently beats a PSRO policy trained directly on each test graph (100K episodes per graph) against multiple evader types including the asynchronous DP-optimal evader and a trained best-responding evader (Table 2). Against DP_async, PSRO collapses to near 0% on several graphs while R2PS maintains non-trivial success rates.

- **Real-time scalability demonstrated.** Inference time <0.01s on GPU vs. 6–139s for DP recomputation on graphs with 744–2065 nodes (Table 3), with graceful degradation of success rates (33–76% against DP_async).

## Weaknesses

### Fatal

None.

### Major

1. **No comparison against EPG, despite the method being an extension of EPG.** The paper describes R2PS as embedding belief preservation "into the state-of-the-art EPG framework" (Section 4), yet EPG never appears as a baseline. EPG already achieves zero-shot graph generalization under full observability; without comparing against (a) EPG under full observability (as an upper bound) and (b) EPG under partial observability *without* the belief mechanism (using only Eq. 5), the reader cannot tell whether the strong zero-shot performance comes from EPG's cross-graph training paradigm or from the belief mechanism specifically. This is the most consequential missing experiment.

2. **Belief update's use of evader policy during training is unspecified, creating a potential training/evaluation mismatch.** Line 157 states the evader's policy ν defaults to uniform during evaluation. During RL training (Section 4.1), the true optimal evader policy ν* is available and used to generate opponent actions (line 179). The paper never clarifies whether belief computation during training uses ν* or the uniform approximation. If training uses ν* while evaluation uses uniform, the policy may learn to rely on belief accuracy that does not transfer, directly affecting the credibility of reported success rates.

3. **"Worst-case robust" framing overstates what is demonstrated.** The paper acknowledges (line 234) that D(·) "becomes an optimistic one under partial observability," yet the title, abstract, and conclusion (lines 5, 9, 309–313) continue to claim "worst-case robust" strategies. The theoretical worst-case guarantee holds only under full observability; the RL policy's robustness is empirically demonstrated against specific adversaries (DP_async, BR_async) but does not constitute a worst-case guarantee for the partially observable setting. The framing should be adjusted to "empirically robust against strong adversaries."

### Minor

4. **No uncertainty estimates on any reported success rates.** All Tables (1–4) report point estimates averaged over 500 tests without standard deviations or confidence intervals. While the large gaps in Table 2 (e.g., 0.95 vs. 0.04 on Times Square) would likely survive, borderline cases (0.25 vs. 0.04 on The Bund) need quantification.

5. **PSRO baseline is underspecified.** The paper does not describe PSRO's neural architecture, best-response oracle, or how it handles partial observability. PSRO with only 10 iterations (100K episodes total per test graph) is a modest budget — this asymmetric training configuration could partly explain PSRO's poor performance, and the lack of detail makes the comparison hard to interpret or reproduce.

6. **Evader optimality defined for the wrong game.** The DP_async evader is provably optimal under full observability, but a truly worst-case evader under partial observability could exploit the pursuers' observation gaps (staying in blind spots, exploiting the uniform-belief approximation). The paper partially addresses this via BR_async experiments (Table 2, last column), but the primary adversary remains DP_async.

### Trivial

7. **Minor notation inconsistency.** The evader policy ν in Eq. (3) takes arguments (s_p, s_e, n_p), while ν in Eq. (7) takes arguments (v, s_e). The transition from Eq. (7) to the uniform default (ν(v) without s_e) is ambiguous.

## Nice-to-Haves

- Adding EPG-based ablations (full-observability upper bound, partial-observability without belief mechanism) would directly isolate the belief mechanism's contribution and is the single most impactful addition.
- Clarifying belief computation during training (whether ν* or uniform is used).
- Adjusting the "worst-case robust" framing throughout.
- Adding confidence intervals to the main results.
- Providing full PSRO configuration details and considering a larger PSRO training budget.

## Removed Points

- Criticisms about "Lancet et al." typo for Lanctot — parser artifact, not an author error.
- Section-by-section notes about heuristic analogies (half-space, Section 4.1) — the harsh critic explicitly acknowledged these are acceptable.
- Notation issue about "2 minutes vs <1 second" timing comparison clarity — the paper adequately describes the hardware and setting.
- All criticisms about missing appendix content (proofs, learning curves, etc.) — the appendix was stripped by the parser; the original submission contains this material.
- Generic problem-importance strength — removed per filtering rules.
- Criticisms about the evader policy notation being "ambiguous" in Eq. (7)'s arguments — already covered by the minor notation weakness above.
- Claim that the paper should acknowledge partial observability PEG literature — this is scope creep beyond the paper's framing.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Add EPG-based comparisons (with and without belief mechanism) to isolate what the belief mechanism contributes over the base cross-graph training paradigm.
2. Clarify whether belief computation during training uses ν* or the uniform approximation, and discuss the implications of any asymmetry.
3. Adjust the "worst-case robust" framing to accurately reflect that theoretical guarantees hold only under full observability, and empirical evidence shows effectiveness against strong adversaries under partial observability.
4. Add standard deviations or confidence intervals to all success rate tables.
5. Provide complete PSRO configuration details (architecture, best-response mechanism, partial observability handling).

## Score and Decision

**Final calibration analysis:** The paper was bracketed in the [5.0, 6.5] range after Round 1. Round 2 narrowed this to 5.5 after comparing itemized favorability ratings against accepted anchors (DFTHW0MyiW at 7.00, KD5nJUgeW4 at 7.00, 99tKiMVJhY at 6.33) and rejected anchors (GvsCOOPxoI at 6.17, rejected for format issues). The paper's draft items show weakness favorabilities of -1.30 (missing EPG comparison) and 0.18 (worst-case overclaiming), which are substantially lower (more negative) than any weakness item in the accepted 7.00 anchors, where all weakness favorabilities were positive. This aligns with a 5.5 score: the paper has genuine contributions but the three Major weaknesses prevent acceptance at a higher threshold.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>
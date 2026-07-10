## Summary

The paper proposes *Continuous Online Action Detection* (COAD), a task formulation where OAD models continuously adapt from streaming video in a single pass, without storing data or doing multiple training epochs. It introduces Ego-OAD, a large-scale egocentric OAD benchmark (263h, 87 classes) derived from Ego4D MQ, and applies three training strategies—state continuity, orthogonal gradient projection, and non-uniform loss—to enable effective single-pass training on video streams.

## Strengths

- **Well-motivated problem.** The gap this paper addresses is real: OAD models are trained offline and deployed in static mode, a poor match for egocentric wearable devices where user activities and environments evolve. Framing the problem as continuous adaptation on streaming video is a sensible research direction.

- **Dataset contribution.** Ego-OAD is a large-scale (263h, 87 classes, ~23k instances) egocentric OAD benchmark derived from Ego4D MQ, with multi-label annotations and realistic overlap rates (36%). This dataset could be reused by the community for standard OAD evaluation even beyond the COAD formulation.

- **Clear, reproducible experimental protocol.** The three-way data split (pretrain / in-stream / out-of-stream) cleanly separates evaluation of adaptation from generalization. The ablation in Table 3 is thorough and isolates each component's individual contribution.

## Weaknesses

### Fatal
None.

### Major

- **Headline improvements conflate continuous training with COAD-specific techniques.** The abstract claims "improves adaptation... by up to 20% in top-5 accuracy, and improves generalization... by up to 7%." These Δ values compare COAD to the **Pretrained Only** baseline (zero adaptation). The actual improvement of COAD over the **w/o COAD** baseline (which also trains on the stream) is much more modest: +2.6 to +4.4 points Top-5 Recall on Ego-OAD (Table 1). The framing makes it appear the three proposed strategies are responsible for most of the gain, when most of the improvement comes from simply training on the stream at all. The paper should be transparent about this distinction.

- **Missing baselines from prior OAD methods on Ego-OAD.** The paper introduces Ego-OAD as a new benchmark but evaluates no existing OAD methods (e.g., IDN, GateHub, LSTR, TeSTra, MiniROD) on it. Without these baselines, readers cannot assess where COAD's absolute performance levels (e.g., 26.0 mAP out-of-stream, 36.8 in-stream) stand relative to prior work. While the main claim is about relative improvement from adaptation, a new benchmark should include standard offline baselines.

### Minor

- **No statistical significance.** Performance differences between COAD and w/o COAD are often small (2–4 points), but no confidence intervals, standard deviations, or significance tests are reported, making it unclear whether these gaps are reproducible.

- **IID upper bound not numerically reported.** Figure 4 shows COAD approaching an "IID Training" upper bound, but the actual numerical values of this bound are not reported in text or tables, making it impossible to quantify the gap.

- **Frozen backbone limits the scope of personalization.** The visual backbone is frozen during COAD (Section 4.3); only the temporal detection head adapts. This restricts what "personalization to the user's environment" can achieve, since visual representations never update.

- **No comparison to replay-based continual learning.** The paper emphasizes "without storing data" as an advantage, but never benchmarks against a small replay buffer (a standard continual learning technique), leaving the reader unsure whether this advantage is meaningful.

- **Methodological components are individually existing techniques.** Orthogonal gradient projection is from Han et al. (2025), non-uniform loss from An et al. (2023), and state continuity is the natural extension of inference behavior to training. The contribution is the combination and application to OAD, which is useful but not architecturally novel.

### Trivial

- Acronym inconsistency: Line 66 introduces "Continuous OAD (CODA)" but the rest of the paper uses COAD.

## Nice-to-Haves

- Benchmark 2–3 prior OAD methods on Ego-OAD in the standard offline setting to establish baseline performance levels for the community.
- A deeper analysis of EPIC-KITCHENS in-stream adaptation limitations (fine-grained actions, shorter videos, different repetition structure) would strengthen the paper's scientific contribution.

## Removed Points

These points were considered but removed after verification against the paper. Treat them with **caution**:

- "EPIC-KITCHENS results undermine the generalization claim" — REMOVED after checking Table 2: COAD consistently matches or beats Pretrained Only on out-of-stream generalization on EPIC-KITCHENS (better on 5/6 metrics, tie on 1/6). The reviewer's characterization as "failure" is not supported by the data.
- "Missing related work on continual learning/online learning" — REMOVED per meta-review guidelines.
- "Missing appendix details" — REMOVED per meta-review guidelines.
- "Typo: 'Countinuous'" — REMOVED per meta-review guidelines (typo/formatting).
- "Standard OAD vs COAD is just a training protocol difference" — REMOVED: subjective opinion about framing, not a verifiable weakness.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Revise the abstract and contribution statements to report improvements against the **w/o COAD** baseline alongside the Pretrained Only baseline, so readers can see the COAD-specific gain separately from the gain of any continuous training.
2. Benchmark at least 2–3 prior OAD methods on Ego-OAD in the standard offline setting to establish baseline performance levels.
3. Report confidence intervals or standard deviations for the main results, especially where differences are small (2–4 points).

## Score and Decision

The paper addresses a well-motivated problem, contributes a useful new dataset, and follows a clean experimental protocol. However, it suffers from two substantive weaknesses: the headline results conflate the effect of continuous training in general with the specific COAD techniques, and no existing OAD methods are benchmarked on the new dataset for context. The methodological components are individually existing techniques. These issues are real but addressable; the core task formulation and dataset are valuable contributions that the community can build on.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>
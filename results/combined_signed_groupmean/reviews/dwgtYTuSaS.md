Now I have enough anchors for calibration. Let me synthesize the comparison and finalize.

**Round 1 bracket**: Based on comparison with anchors, the paper sits between PrAViC (4.25, rejected) and StreamingBench (5.75, rejected). It is stronger than PrAViC because its task+benchmark contributions are more solid, but weaker than the TTA Egocentric paper (6.00, accepted) due to weaker experimental methodology. Its closest match is Anomalies are Streaming (5.71, rejected) and StreamingBench (5.75, rejected).

**Impact-score comparison**: My draft's strongest items are:
- Benchmark strength: +9.98 (comparable to StreamingBench's benchmark novelty)
- Missing OAD baselines: -9.82 (comparable to PrAViC's missing ECTS baselines at -9.19/-9.90)
- Overstated novelty: -10.00 (comparable to PrAViC's overclaimed theory at -9.89)
- No variance: -10.00 (comparable to PrAViC's missing error bars at -7.24)

The decisive-magnitude weaknesses (missing OAD comparison, overstated novelty, no variance) pull this paper below the clean Accept-level papers like TTA Egocentric (6.00). But the high-magnitude benchmark strength (+9.98) puts it above PrAViC (4.25).

Final score: **5.0** — between 4 (borderline reject) and 6 (borderline accept), clearly below the accept threshold due to the combination of missing baselines, overstated claims, and absent variance estimates.

---

## Summary

This paper introduces Continuous Online Action Detection (COAD), a task formulation that extends standard OAD by enabling models to adapt on-the-fly from streaming egocentric video under causal, single-pass, no-storage constraints. It also presents Ego-OAD, a large-scale egocentric OAD benchmark (87 classes, ~23k instances, 263h), and proposes a method combining orthogonal gradient projection, non-uniform loss, and state continuity for continuous learning. Experiments on Ego-OAD and EPIC-KITCHENS show COAD improves generalization to unseen data.

## Strengths

- **A well-motivated task formulation.** The gap between offline-trained OAD and the real need for on-device, post-deployment adaptation in egocentric settings is clearly articulated (Section 1). COAD's constraints — causal, single-pass, no data storage — reflect real hardware limitations of wearable devices. This framing is the paper's strongest conceptual contribution.

- **A large-scale benchmark.** Ego-OAD (87 classes, ~23k instances, 263h of video, Section 3) fills a genuine gap: there was no egocentric OAD benchmark of this scale. The multi-label annotation from multiple passes captures the ambiguity of real-world egocentric video, and the three-way split (pretrain/in-stream/out-of-stream) following Carreira et al. (2024a) is appropriate for the COAD evaluation protocol.

- **The in-stream/out-of-stream evaluation design** (Section 5.1) properly separates adaptation performance on the training stream from generalization to held-out data. The trade-off analysis (Fig. 3) is informative — it honestly shows that naive continual adaptation can hurt generalization while COAD mitigates this.

## Weaknesses

### Fatal
None.

### Major

- **Missing comparison to existing OAD methods.** The only baselines are "Pretrained Only" and "w/o COAD" (Section 5.1). No comparison to established OAD methods (LSTR, TeSTra, GateHub, IDN, MiniROD, etc.) is provided on the Ego-OAD benchmark. Without knowing how COAD's performance (e.g., 26.0 mAP out-of-stream) compares to existing approaches on the same data, readers cannot assess whether the achieved performance level is meaningful. This is the single highest-impact omission.

- **Method novelty is overstated.** The paper claims "effective training strategies tailored to COAD" (contributions list, Section 1) and "OAD-specific training strategies," but all three components in Section 4.5 are directly adopted from prior work with no described adaptation: orthogonal gradient projection from Han et al. (2025), non-uniform loss from An et al. (2023) (MiniROD), and state continuity is the standard behavior of RNNs in non-shuffled settings. The paper's framing of these as novel methodological contributions is not supported by the evidence presented.

- **No statistical significance or variance reported.** All numbers in Tables 1–4 appear to come from a single run. The paper does not mention random seeds, multiple trials, or confidence intervals. Given that several key comparisons hinge on small absolute differences (e.g., 26.0 vs 25.5 mAP for out-of-stream generalization), this makes it impossible to determine whether the reported improvements are systematic or due to noise.

### Minor

- **EPIC-KITCHENS results partially undermine the paper's claims.** On EPIC-KITCHENS (Table 2), COAD's in-stream adaptation results are mixed — e.g., Action mAP in-stream: 7.9 vs Pretrained Only's 9.6; Noun Top-5 Recall in-stream: 13.9 vs 14.7. The paper attributes this to "the fine-grained nature of the actions and annotations in EPIC-KITCHENS" without supporting analysis. While out-of-stream (generalization) results consistently favor COAD, the in-stream underperformance on a standard egocentric benchmark qualifies the headline claims about "both adaptation and generalization."

- **Ablation shows state continuity adds negligible value.** In Table 3, removing state continuity (row: ✗ ✓ ✓) yields 25.9/36.7 mAP vs. the full model's 26.0/36.8 — effectively identical. The paper's claim that "state continuity provides a smaller but consistent gain" (Section 5.4) is not supported by these numbers; the difference is within measurement noise, especially given the absence of variance estimates.

- **Limited baselines even within the COAD setting.** Only two reference baselines are compared against; there is no comparison to alternative continual learning approaches (e.g., replay-based, regularization-based, or architecture-based methods) adapted to the OAD setting. This limits the assessment of whether the specific design choices in COAD are optimal.

### Trivial

- **Acronym inconsistency**: The paper introduces "Continuous OAD (CODA)" on line 66 of Section 4 but uses "COAD" everywhere else.
- **Label efficiency claim**: The claim that COAD "requires supervision only at each window's final step, allowing training with sparse instead of dense frame-level annotations" (Section 4.5) is potentially misleading — offline OAD training described in Section 4.3 also predicts labels only for the last frame of each window.

## Nice-to-Haves

- Provide analysis of what the model actually adapts to during streaming (visual appearance shifts, new action categories, background environments) rather than treating adaptation as a black box.
- Compare against alternative continual learning strategies (replay, regularization, architecture-based) adapted to the OAD setting.

## Removed Points

These points are flagged to be removed, treat them with caution:
- **EPIC-KITCHENS specific number error**: The Harsh Critic claimed "Action mAP (out-of-stream): Pretrained Only = 9.6, COAD = 7.9." This is factually incorrect. In Table 2, the format is out-of-stream / in-stream. For Action mAP out-of-stream: Pretrained Only = 8.6, COAD = 9.9 — COAD is actually better. The reviewer confused the out-of-stream and in-stream columns. The broader point about mixed in-stream results is kept as a Minor weakness above.
- **Data split imbalance criticism**: The paper explicitly acknowledges this design choice (Section 5.1: "We allocate the majority of training data to the in-stream split to better assess the impact of continuous learning"). This follows Carreira et al. (2024a) and is a deliberate, explained decision.
- **Missing inter-annotator agreement**: Concerns about dataset curation quality were delegated to Appendix A, which is stripped by the parser. This cannot be verified from the available content.
- **Generic/scope-creep criticisms**: Several criticisms from the input review (e.g., requesting the paper address problems outside its stated scope, speculative "could the metric be measuring a proxy?" concerns) were removed per the filtering guidelines.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Reframe the paper to position the method as a baseline for the COAD task (using established techniques from Carreira et al., Han et al., and An et al.) rather than claiming novel OAD-specific training strategies. The task formulation and benchmark are solid contributions on their own.
- Add a proper comparison to existing OAD methods on the Ego-OAD out-of-stream split to contextualize COAD's performance.
- Run experiments with multiple random seeds and report variance or confidence intervals, especially for metrics with small absolute differences.
- Correct the "CODA"/"COAD" acronym inconsistency.

## Score and Decision

**Calibration anchors considered:**

| Path | Score | Round | Itemized? | Comparison |
|------|-------|-------|-----------|------------|
| ShadowPunch (Jq8HYNZG9s) | 3.00 | R1 | Yes | Much narrower benchmark (3 classes vs 87); our paper is clearly stronger |
| PrAViC (jawV7vhGHw) | 4.25 | R1 | Yes | Similar weaknesses (missing baselines, overclaimed novelty, no variance); our benchmark contribution is stronger |
| Anomalies are Streaming (Y7jJN0VQ4y) | 5.71 | R1 | Yes | Similar "new task+benchmark+method" profile; rejected due to impractical setting and weak evaluation |
| StreamingBench (qnAZqlMGTB) | 5.75 | R2 | Yes | Benchmark paper; split opinions (3,6,6,8). Some reviewers questioned whether the benchmark was truly novel; our paper's COAD task is more clearly differentiated from prior work |
| TTA Egocentric (1L52bHEL5d) | 6.00 | R1 | Yes | Clean paper with comprehensive experiments, repeated runs with std dev, good ablations. **Our paper is weaker** on experimental rigor |
| EgoVideo (P6G1Z6jkf3) | 6.00 | R2 | Yes | SOTA results, comprehensive experiments. **Our paper is weaker** on empirical validation |

**Round 1 bracket**: 4.0–6.0. The paper is stronger than PrAViC (4.25) and ShadowPunch (3.0) due to the solid task+benchmark contributions, but weaker than the Accept-level papers (6.00) due to missing OAD baselines, overstated novelty claims, and absent variance estimates.

**Round 2 narrowing**: Compared to Anomalies are Streaming (5.71, rejected) and StreamingBench (5.75, rejected), our paper shares similar structural strengths (new task formulation, new benchmark) but also similar major weaknesses (incomplete baselines, overclaimed contribution). However, the three decisive-level weaknesses in the draft — missing OAD comparison (-9.82), overstated method novelty (-10.00), and no variance (-10.00) — pull the score below these comparators on experimental rigor.

**Final placement**: 5.0 — below the borderline accept threshold (6.0) and rejected in the current form. The paper's core intellectual contributions (the COAD task formulation and Ego-OAD benchmark) are publishable, but the method is overclaimed and the experimental validation is insufficiently rigorous. A substantial revision addressing the missing baselines, reframing the method claims, and adding variance estimates could lift the paper to the borderline accept range.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>
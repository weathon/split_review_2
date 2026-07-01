Now I have a clear calibration picture. Let me write the final review.

## Summary
2-3 sentence summary of the paper's contribution.

## Strengths
- strength 1 with evidence
- strength 2 with evidence

## Weaknesses
### Fatal
None

### Major
- weakness 1 — why it matters

### Minor
- weakness 1 — why it matters
- weakness 2 — why it matters

### Trivial
- weakness 1

## Nice-to-Haves
- suggestion

## Removed Points
...

## Novel Insights
...

## Suggestions
- suggestion

## Score and Decision

Let me write it all out now.

**Calibration anchors:**

From Round 1 bracketing search:
1. **LVBench** (4.50) - rejected long video understanding benchmark paper. Similar-level concerns about evaluation validity. Our paper has a stronger method contribution but a more central evaluation gap.
2. **Motion-Grounded Video Reasoning** (5.00) - rejected. Introduces new task/dataset/model for spatiotemporal grounding. Similar scope to our paper. Score distribution (5,6,6,3) shows reviewer disagreement.
3. **Grounded Video Caption Generation** (3.83) - rejected. Similar scope (new task + dataset + model).
4. **Grounded-VideoLLM** (4.25) - rejected. Video temporal grounding with LLMs. Similar area.
5. **TRACE** (6.75) - accepted. Temporal grounding via causal event modeling. Clearer evaluation than our paper.

From Round 2 narrowing:
6. **Neptune** (5.33) - rejected long video benchmark. 
7. **improve weakly supervised visual grounding** (3.00) - rejected, weaker contributions.
8. **Unsupervised open-vocabulary action recognition** (5.25) - rejected, mixed reviews.

Round-1 bracket: 3.5–5.5 based on comparison with LVBench (4.50), Grounded-VideoLLM (4.25), and Motion-Grounded Video Reasoning (5.00).

After Round 2 narrowing with LVBench (4.50) as the closest topical anchor, the final score is 4.5. The paper has genuine architectural contributions and identifies a real problem, but the central evaluation gap (underspecified baseline inference protocol) prevents acceptance in its current form.**Round-1 bracket: 3.5–5.5.** Closest topical anchors: LVBench (4.50), Grounded-VideoLLM (4.25), Motion-Grounded Video Reasoning (5.00). Our paper has a stronger architectural contribution than LVBench but a more central evaluation gap; similar in scope to Motion-Grounded Video Reasoning but with a more serious weakness in the primary comparison.

---

## Summary

This paper introduces ART-STVG, an autoregressive transformer for long-form spatio-temporal video grounding (LF-STVG). Unlike existing STVG methods that process all frames at once, ART-STVG processes frames sequentially with spatial and temporal memory banks and a cascaded decoder design. The authors extend the HCSTVG-v2 validation set from 20-second clips to 1–5 minute benchmarks. ART-STVG outperforms existing methods across all video lengths on the extended benchmarks, with growing margins as videos get longer.

---

## Strengths

1. **Well-motivated problem framing (Section 1, lines 15–17).** The paper correctly identifies that existing STVG research operates on videos of 20–35 seconds while many real applications (surveillance, video retrieval) involve much longer videos. This gap is genuine and worth addressing.

2. **Autoregressive processing is architecturally suited to the task (Section 1, lines 30–32).** Processing frames one at a time rather than all at once cleanly sidesteps the quadratic attention cost that makes non-autoregressive transformers prohibitive on long videos. This is a conceptually appropriate design choice.

3. **Cascaded spatio-temporal decoder with memory selection is a genuine architectural contribution (Section 3.2–3.4, Figure 3).** Connecting the spatial decoder to the temporal decoder via RoI pooling so that fine-grained spatial features inform temporal boundary prediction is non-obvious. The memory selection strategies (text-similarity for spatial, TextTiling-inspired boundary detection for temporal) are simple and effective.

4. **The 40-second training experiment (Table 6) provides the cleanest comparison.** When all methods are trained on 40-second videos (not just the default 20s), ART-STVG still leads by a large margin (28.3 vs. 20.8 m.tIoU), showing the advantage is not purely an artifact of training-length mismatch.

---

## Weaknesses

### Major

1. **The baseline inference protocol for long videos is underspecified, making Table 1 hard to interpret.** The paper does not describe how non-autoregressive DETR-style baselines (TubeDETR, STCAT, CG-STVG, TA-STVG) were configured to process videos 15–150× longer than their training data. A 5-minute video at 3.2 FPS yields ~960 frames; processing all frames simultaneously with self-attention would be prohibitive. The paper states only that "all methods including ART-STVG are trained exclusively on the HCSTVG-v2 training set" (line 206) but says nothing about: whether frames were subsampled during inference (and by what factor), whether the original codebases were modified, what hardware/memory constraints applied, or whether the inference procedure was validated to operate correctly at longer durations. The near-collapse of baseline performance (e.g., TA-STVG dropping from 38.4→7.7 m.tIoU from 1min to 5min) is *consistent with* ART-STVG's claimed advantage, but without knowing what the baselines actually computed, the reader cannot determine whether Table 1 demonstrates algorithmic superiority or an unstated inference artifact. This is the single most important issue to address.

### Minor

2. **Annotation details for the extended dataset are absent.** The paper states that extensions are "based on original YouTube videos, not concatenated clips, and we manually review the extended videos to ensure their quality" (lines 200–201), but provides no information about who performed annotations for the extended portions, what annotation protocol was used (bounding box frequency, event boundary annotation per frame or per segment), or what inter-annotator agreement was achieved. The original HCSTVG-v2 required substantial annotation effort; if the extended portions were annotated differently, results across video lengths may not be comparable.

3. **No variance or significance reporting for any result.** No confidence intervals, standard deviations, or significance tests are reported for Tables 1–7. Several ablation improvements are small (0.8% for spatial memory without selection vs. none in Table 3; 0.9% for adding selection on top). Without variance estimates, these differences may be within noise.

4. **"Long-form" framing oversells the scope.** The paper claims to address videos of "several minutes or even hours" (lines 9, 15) but evaluates only up to 5 minutes. Additionally, the memory bank grows without removal ("without removing any existing memories," line 148), meaning on hour-long videos at 3.2 FPS the bank would contain ~11,520 entries per decoder block, with selection cost growing linearly. No analysis of scaling behavior beyond 5 minutes is provided.

5. **Evaluation primarily measures domain-shift robustness.** All models (including ART-STVG) are trained on 20-second clips and tested on up to 5-minute clips (a 15× length increase). This makes the primary evaluation a test of robustness to training-test distribution shift rather than a test of long-form understanding learned during training. The 40-second training experiment (Table 6) partially addresses this but is presented as an ablation rather than the primary result.

### Trivial

6. **Table 2's column header is ambiguous.** The table shows three rows (no memory, memory without selection, memory with selection) but the header "Memory | Selection" could be read as a binary condition. The text clarifies the setup, but the table alone is confusing.

---

## Nice-to-Haves

- A runtime and GPU memory comparison between ART-STVG and baselines at each video length would directly support the paper's computational-efficiency motivation (lines 30–31).
- Ablations at more than one video length (not just 3min) would show whether design choices generalize or are length-specific.
- An analysis of the memory bank saturation point and a bounded-memory variant would strengthen the "long-form" claim.

---

## Removed Points

These points from the input review were removed with justification:

- **"Figure descriptions appear auto-generated"** — Parser artifacts from PDF extraction, not a paper problem. (Hard Rule)
- **"Loss function details are missing from main paper"** — Deferred to supplementary; parser strips supplementary sections. (Hard Rule)
- **"Baseline (ours) architecture is relegated to supplementary"** — Same as above.
- **"Temporal decoder uses single-frame RoI features, mismatched for temporal dynamics"** — VidSwin motion features already incorporate temporal context from preceding frames (line 78), so the input to the temporal decoder is not a single-frame feature.
- **"Low absolute performance on 5-min videos not discussed"** — The paper's claims are about relative improvement; absolute task difficulty is a separate concern the paper acknowledges implicitly.
- **"No runtime/memory comparison"** — Demoted to Nice-to-Have; this is a useful addition but not a core flaw.
- **"Table 2 checkmark confusion"** — The accompanying text clearly explains the rows (lines 214–215).

---

## Novel Insights

None beyond the paper's own contributions. The observation from the harsh critic that the evaluation primarily measures domain-shift robustness (training on 20s, testing on 1–5 min) rather than long-form understanding per se is a useful framing, but it is implicit in the paper's own experimental design.

---

## Suggestions

1. **Document the baseline inference protocol in full.** Specify for each baseline: number of input frames processed, any subsampling strategy, GPU model/memory, whether original code was modified, and whether the correctness of the longer-duration inference was validated (e.g., by checking performance on a held-out medium-length set where existing methods should still work).
2. **Make the 40-second training experiment (Table 6) the primary result** rather than an ablation, or at minimum restructure the paper so the reader sees the fair-training comparison first.
3. **Provide confidence intervals or standard deviations** for key results, especially ablation experiments where differences are small (<1%).
4. **Report annotation quality metrics** for the extended portions of the dataset (inter-annotator agreement, if applicable).
5. **Analyze memory bank scaling** — at what video length does the selection cost become prohibitive, and could a bounded-memory variant maintain performance?

---

**Calibration details.** All anchor papers retrieved:

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| LVBench (uHgVrGF2Wn) | 4.50 | Bracket, Narrow | Long video benchmark paper rejected for evaluation concerns; our paper has stronger architectural contribution but a more central evaluation gap |
| Motion-Grounded Video Reasoning (tEei1bolt3) | 5.00 | Bracket | Similar scope (new task/dataset/model for spatiotemporal grounding); our paper's evaluation gap is more serious |
| Grounded-VideoLLM (YCwN7wQA6W) | 4.25 | Bracket | Rejected for evaluation concerns in temporal grounding; comparable paper quality |
| Grounded Video Caption (xYzOkOGD96) | 3.83 | Bracket | Rejected; similar scope but weaker contributions |
| TRACE (14fFV0chUS) | 6.75 | Bracket | Accepted temporal grounding paper with clearer evaluation; our paper's main flaw is absent in this anchor |
| Neptune (5ddsALwqkf) | 5.33 | Narrow | Long video benchmark paper, rejected; similar concerns about evaluation |
| Unsupervised AR action recog (IryGDUHxDE) | 5.25 | Bracket | Mixed reviews, rejected; our paper has cleaner method narrative |
| weakly supervised visual grounding (BwQUo5RVun) | 3.00 | Bracket | Rejected with more fundamental issues (outdated comparisons, unclear novelty) |

**Round-1 bracket:** 3.5–5.5. **Round-2 narrowing:** LVBench (4.50) is the closest topical match — both are rejected due to evaluation concerns despite meaningful contributions. The final score of **4.5** reflects that the paper has genuine architectural contributions but the central evaluation gap (underspecified baseline protocol) prevents acceptance in the current form.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>
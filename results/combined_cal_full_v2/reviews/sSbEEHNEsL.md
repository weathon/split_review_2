## Summary

This paper proposes USR 2.0, which addresses two key limitations of the USR semi-supervised framework for unified speech recognition (ASR, VSR, AVSR): the computational bottleneck of autoregressive pseudo-labelling and the fragility of decoupled CTC/attention supervision under distribution shift. The core idea — CTC-driven teacher forcing — feeds greedily decoded CTC outputs as a fixed prefix into the teacher's decoder, enabling attention pseudo-labels to be generated in a single forward pass rather than autoregressively. A mixed sampling strategy (50% CTC-driven, 50% AR) mitigates exposure bias. The method achieves ~2× training speedup, dramatic OOD robustness improvements on long utterances and noisy conditions, and state-of-the-art WERs across LRS3, LRS2, and WildVSR at multiple model scales.

## Strengths

- **Clear and empirically grounded problem diagnosis.** Figure 1 directly quantifies the ~40× speed gap between CTC and AR decoding and the OOD robustness gap (CTC WER stabilizing vs. AR WER diverging as sequence length increases), providing concrete evidence for the two limitations the paper targets. The diagnosis is data-backed rather than speculative.

- **Elegant core idea with a non-obvious insight.** CTC-driven teacher forcing is simple, and the insight that global sequence incoherence does not harm pseudo-labelling because teacher and student share the same conditioning is genuinely interesting, distinguishing this work from naive scheduled sampling or knowledge distillation approaches.

- **Dramatic robustness improvements on long utterances.** Figure 3a shows USR 2.0 maintaining ~35% WER from 200 to 600 frames under greedy decoding, while USR degrades from 45% to 100% — a qualitative change in behaviour, not a marginal gain. The beam size analysis (Figure 3c) confirms the gap persists even at large beam sizes, indicating the improvement is architectural, not a search-time artefact.

- **Clean ablation study.** Table 4 isolates the contribution of each pseudo-label type to each branch under both CTC-driven and AR modes. The key finding — removing CTC targets from the decoder in CTC-driven mode degrades OOD WER from 24.2% to 35.1% (row 1 vs. row 2) — cleanly supports the central thesis about coupling CTC and attention supervision.

- **Practical efficiency gain.** The ~2× training speedup (Figure 5) combined with consistent accuracy improvements makes this a practically useful contribution. USR 2.0 converges in fewer epochs (50 vs. 75), suggesting pseudo-labels are genuinely higher quality, not just cheaper.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

- **Missing USR Huge baseline for the scaling results.** The paper reports USR 2.0 Huge achieving state-of-the-art WERs of 17.6% (VSR), 0.9% (ASR), and 0.8% (AVSR) on LRS3, but no USR Huge comparison is provided. While Base- and Large-scale controlled comparisons exist (showing consistent USR 2.0 gains over USR), the Huge results are presented without a controlled ablation. This makes it unclear how much of the Huge improvement comes from the method vs. from simply scaling model and data. This does not invalidate the core claims (the paper already shows method-level gains at smaller scales) but softens the headline scaling results.

- **The "global coherence" justification is intuitive but empirically unanalysed.** Section 4.1 argues that the teacher decoder's output under CTC conditioning is effective despite lacking global coherence because teacher and student share the same conditioning. This is plausible, but the paper provides no analysis (e.g., agreement rates between CTC-driven and AR decoder outputs, or cross-attention pattern analysis) to substantiate what the teacher decoder actually produces. The empirical results are strong, but the mechanistic explanation remains at the level of intuition rather than demonstrated phenomenon.

- **Two changes are not fully isolated in the ablation.** The improvement over USR involves (a) CTC-driven teacher forcing (changing how the teacher generates PLs) and (b) coupled student supervision (the decoder now predicts both CTC and attention PLs simultaneously). Table 4 ablates target types within each mode, but the independent contribution of coupling the student supervision (regardless of how the teacher generates PLs) is never measured against a version of USR that keeps AR teacher decoding but adds coupled student predictions. The combination clearly works, but the cleanest decomposition is incomplete.

### Trivial

- **VSR regression on Base LRS3 low-resource not acknowledged.** USR 2.0 achieves VSR 36.2% vs. USR 36.0% in Table 2 — a 0.2 WER regression. The paper states "USR 2.0 matches or outperforms the state of the art," which is technically accurate, but the VSR regression goes unremarked. A brief acknowledgment would improve the paper's honesty.

## Nice-to-Haves

- **Variance/statistical significance reporting** — None of the tables report error bars or multiple runs. Several in-distribution comparisons rely on very small differences (ASR 3.0 vs. 3.2, AVSR 2.9 vs. 3.0). While single-run evaluation is standard in large-scale speech recognition benchmarks, a few repeated runs for key configurations would strengthen the precision of in-distribution claims.

- **Clarification of CTC loss computation in AR mode (Equation 6)** — The paper notes that ỹ^CTC and ỹ^Att may differ in length, but briefly clarifying how the CTC loss naturally handles variable-length targets would improve reproducibility.

## Removed Points

These are points from the harsh critic's review that were filtered:
- **"No variance or statistical significance reported for any result"** — Demoted to Nice-to-Have. Single-run evaluation is the standard practice in large-scale speech recognition benchmark papers for this model class. The large and consistent gaps in the OOD results (Figure 3, Tables 1, 3) are clearly meaningful without error bars. The in-distribution small-gap comparisons are the only place this matters, and this is noted as a Nice-to-Have.
- **"OOD flatness from p=0 to p=0.6 could be acknowledged more"** — The paper already clearly describes the ID/OOD trade-off in Figure 4's analysis. This is a presentational preference, not a weakness.
- **"Both VSR 36.0 and 36.2 are bolded in Table 2"** — This is a table formatting choice (both are best in different columns relative to different baselines), not a substantive issue.
- **Whisper transcription error concern for OOD datasets** — The paper acknowledges this implicitly, and the concern is speculative rather than based on identified errors.

## Novel Insights

None beyond the paper's own contributions. The reviews validate the paper's framing and confirm that the core novelty is well-recognized; no unaddressed contradictions or alternative interpretations of the results emerged from the review process.

## Suggestions

1. Add a USR Huge baseline comparison (even if trained for fewer steps or on a subset of the data) to cleanly demonstrate the method's contribution at the largest scale.
2. Include a brief empirical analysis of what the teacher decoder produces under CTC conditioning (e.g., agreement rate between CTC-driven and AR-generated attention PLs, or cross-attention pattern visualizations) to strengthen the mechanistic explanation.
3. Acknowledge the VSR 36.2 vs. 36.0 result in the main text and explain why it occurs (e.g., the benefit of CTC-driven teacher forcing is smaller when unlabelled data is in-distribution).
4. Consider reporting variance estimates for at least the key in-distribution configurations (Table 2) to improve precision of small-gap comparisons.

---

### Calibration Report

**Anchors retrieved across all rounds:**

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/8QTpYC4smR.md` | 1.00 | R1 | No | Unrelated survey paper (LLM review) — not comparable |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/gwZ90hFSL2.md` | 1.00 | R1 | No | Unrelated cross-lingual robotics paper — not comparable |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/Uj0h13lVrR.md` | 1.00 | R1 | No | Unrelated GFlowNets paper — not comparable |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/5lUdTogEL3.md` | 1.00 | R1 | No | Unrelated person re-ID paper — not comparable |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/aXSxSu3fvg.md` | 3.00 | R2 | No | SSL with early stopping in healthcare — weaker method, no speech focus |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/xRi8sKo4XI.md` | 3.00 | R2 | No | Unsupervised prompt learning for LLMs — unrelated |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/gW4bdLwypB.md` | 3.40 | R2 | No | Multilingual multi-task ASR — lower quality than USR 2.0 |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/cLws58ZojF.md` | 3.00 | R2 | No | Speech-conditioned LLMs exploration — weaker contribution |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/4lOWCkhr4g.md` | 5.25 | R3 | No | Unsupervised ASR via cross-lingual pseudo-labeling — comparable topic but weaker evaluation |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/7NlGsjrEd8.md` | 4.50 | R3 | No | CTC alignment modeling — narrower scope, less impact |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/eSO9quCgmz.md` | 5.00 | R3 | No | Data-centric pseudo-labeling insights — unrelated domain |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/MazxSMs6Hs.md` | 3.67 | R3 | No | African-accented ASR data selection — unrelated |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/M8J0b9gNfG.md` | 6.20 | R4 | Yes | Multilingual VSR — weaker novelty, lower quality than USR 2.0 |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/CIs9x2ZRgh.md` | 6.75 | R4, R5 | Yes | CR-CTC: consistency regularization for CTC ASR — comparable topic; method less sophisticated, improvements less dramatic, contains negative-weight items in review |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/TtKN1TpvUu.md` | 6.25 | R4 | No | Non-autoregressive ASR/TTS model — different focus, lower scores |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/WEQL5ksDnB.md` | 6.75 | R4, R5 | Yes | CAV2vec: robust AVSR via corrupted prediction — similar robustness focus but simpler method and had novelty concerns |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/tyEyYT267x.md` | 8.00 | R5 | No | Diffusion language models — unrelated topic, not directly comparable |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/RvUVMjfp8i.md` | 8.00 | R5 | No | SSL evaluation framework — unrelated topic |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/Fk5IzauJ7F.md` | 8.00 | R5 | No | Partial-label learning — unrelated topic |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/zl0HLZOJC9.md` | 8.00 | R5 | No | Learning to defer — unrelated topic |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/fUGhVYPVRM.md` | 7.00 | R5 | Yes | AWP: CTC alignment optimization — comparable ASR topic but narrower contribution and had marginal-improvement concerns |

**Weighted-item comparison anchoring the score:**

My draft's weighted items — all 5 strengths between 8.06 and 10.27, all 4 weaknesses between 5.27 and 6.73. No negative-weight items. This is a uniformly positive profile with moderate, addressable weaknesses.

Compare to **CR-CTC (6.75)**: strengths ranged 7.23–12.38 but included a -2.01 weakness (missing citations) and several 2.60–5.67 weaknesses. Reviewers flagged generalization concerns and missing baselines. Our paper has no weakness of comparable severity.

Compare to **AWP (7.00)**: strengths ranged 6.20–11.94, but weaknesses included -4.48 and -1.95 weights, and the paper's WER improvements were described as "marginal" by multiple reviewers (std 0.03). Our paper's improvements are qualitatively larger (e.g., Figure 3a: USR 2.0 maintains 35% WER while USR hits 100%).

Compare to **CAV2vec (6.75)**: strengths ranged 7.70–10.81, but included a -3.86 novelty concern. Our paper's core idea (CTC-driven teacher forcing) is clearly distinguished from the prior work.

**Round-1 bracket**: 6.5–8.0 (based on closest-matching anchors at 6.75 and 7.00, with our paper clearly stronger than both)

**Round-2 narrowing**: Our paper's weighted items uniformly outrank those of the 6.75–7.00 anchors — all strengths are ≥8.0 with no negative items, and the most comparable anchors (CR-CTC, AWP) all had at least one negative-weight item or a weakness described as "marginal." The paper's OOD results (Figure 3) are qualitatively stronger than any improvement shown in these anchors. This places the paper clearly above the 7.0 anchor, in the 7.0–8.0 range. Setting at 7.5 reflects a clean Accept — strong enough to confidently recommend acceptance, with minor weaknesses that do not threaten the core contribution.

## Score and Decision

MY FINAL SCORE: <score>7.5</score>
MY FINAL DECISION: <decision>Accept</decision>
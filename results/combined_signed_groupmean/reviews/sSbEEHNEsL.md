Now I have all the calibration data I need. Let me compile the final review.

Bracket analysis summary:
- **Round 1 bracket**: The paper sits above CR-CTC (6.75, strong ASR-relevant anchor) and Align With Purpose (7.00, CTC tuning). Its closest topical match in the 5.5-7.5 range is the cross-lingual PL paper (5.25, rejected for limited novelty — USR 2.0 has far more novelty). The papers in 7.5-8.5 band are in different domains (video grounding, streaming video, etc.) except Zipformer (7.50, speech encoder).
- **Round 2 narrowing**: Compared to CR-CTC (6.75), USR 2.0 has a more novel conceptual contribution and stronger OOD evidence. Compared to Zipformer (7.50), USR 2.0 has cleaner ablations and comparable result quality. The scoring model assigned the paper's strengths very high impact (+9.99, +9.99, +9.98, +9.43) and its weaknesses negligible impact (-0.00 each), indicating very minor concerns.
- **Final placement**: 8.0

Here is the final review:

## Summary
The paper proposes USR 2.0, an improved semi-supervised framework for unified speech recognition (ASR, VSR, and AVSR) that replaces autoregressive pseudo-label generation with CTC-driven teacher forcing. The key insight is that globally coherent attention-based pseudo-labels are unnecessary during self-training because teacher and student operate under matched CTC-prefix conditioning, enabling efficient parallel generation. The method achieves ~2× training speedup, substantial out-of-distribution robustness gains (e.g., 39% relative improvement on LibriSpeech), and state-of-the-art results across all three modalities with a single model.

## Strengths
- **A novel conceptual insight (Section 4.1).** The observation that global coherence of attention-based pseudo-labels is unnecessary during self-training because teacher and student share the same CTC-prefix conditioning is non-obvious and turns a seeming limitation into a feature. This goes beyond a standard engineering tweak.
- **Consistent, large-margin OOD improvements.** On LibriSpeech (Table 3), USR 2.0 achieves 15.4% WER vs. USR's 25.3% (~39% relative). On long utterances (Figure 3a), USR 2.0 plateaus at ~35% WER while USR degrades to ~100%+ at 600 frames. These are qualitatively different behaviors, not marginal gains.
- **~2× training speedup with supporting evidence (Figure 5).** The paper attributes the speedup to both faster per-step decoding (CTC-driven mode avoids AR generation) and faster convergence (50 vs. 75 epochs), with wall-clock plots supporting the claim.
- **Clean ablation design (Table 4, Figure 4).** Systematically removes each pseudo-label target type, showing that both CTC and attention PLs contribute in CTC-driven mode, with either removal hurting OOD or ID respectively. The mixed-sampling sweep honestly presents the ID/OOD trade-off.
- **State-of-the-art with a single model.** The Huge model achieves 17.6% VSR, 0.9% ASR, and 0.8% AVSR on LRS3 using one unified model, whereas most competitors train separate models per task.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor
- **Small VSR regression on Base LRS3-only not acknowledged (Table 2).** In the low-resource Base setting, USR 2.0 achieves 36.2% VSR WER vs. USR's 36.0% — a 0.2% degradation. The paper states results are "matched or outperformed" without acknowledging this. Transparency about it would strengthen credibility, particularly since this is the only setting where the method underperforms its predecessor.
- **Beam-size sensitivity claim is qualitatively described (Figure 3c).** The text states "as beam size increases, the gap narrows" without reporting specific WER numbers for USR 2.0 across beam sizes. The figure presumably contains the data, but a small table of WER at several beam sizes (e.g., beam=1, 10, 40) for both methods would make this central supporting claim more concrete.
- **The "decoupled supervision" framing could be more precise.** The paper argues that USR's main weakness is decoupled supervision and claims USR 2.0 "couples" the branches. The coupling is indirect — the student decoder is still supervised by two different losses (CTC PLs and attention PLs), which could exert conflicting gradients. The improvement might equally stem from CTC prefix conditioning acting as a regularizer that prevents AR drift, rather than from "coupling" per se. The paper would benefit from clarifying the mechanism more precisely.

### Trivial
None.

## Nice-to-Haves
- **Variance estimates over multiple seeds** would strengthen the in-distribution claims where margins are small (e.g., 3.0% vs. 2.9% AVSR). This is not standard in the speech recognition literature but would elevate the empirical rigor.
- **A more formal treatment of the "global coherence" argument** (Section 4.1) — even a small worked example or a brief formal statement of why the conditional distribution under matched CTC-prefix conditioning suffices for self-training — would elevate the paper from an engineering contribution to a conceptual one.
- **A brief discussion of why OOD gains vary across datasets** (e.g., the WildVSR gap of 73.7% vs. 80.0% is smaller than the LibriSpeech gap of 15.4% vs. 25.3%) would help calibrate reader expectations.
- **Comparison with non-autoregressive transformer pseudo-labelling** would clarify whether the contribution is specific to CTC-driven conditioning or more broadly about avoiding AR generation, though this is outside the paper's stated scope.

## Removed Points
- "No variance or statistical significance reported anywhere": Moved to Nice-to-Haves. Single-run evaluation without variance is standard practice in large-benchmark speech recognition evaluations; demanding confidence intervals holds the paper to a standard not commonly applied in its field.
- "Inference-time PL quality comparison": Requests an additional analysis that goes beyond what is standard for pseudo-labelling papers.
- "The 'global coherence' argument is compressed": The paper explains this in three paragraphs across Section 4.1; the explanation is adequate for a conference paper, though a formal treatment would strengthen it further.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. Acknowledge the small VSR regression on Base LRS3-only (36.2% vs. 36.0%) in the in-distribution discussion — transparency costs nothing and builds credibility.
2. Add a small table of WER at multiple beam sizes (e.g., beam=1, 10, 40) for both USR and USR 2.0 to support the beam-size sensitivity claim with quantitative evidence.
3. Consider sharpening the "global coherence" explanation by adding a brief formal statement or small worked example showing why the conditional distribution under matched CTC-prefix conditioning is sufficient for self-training.

## Score and Decision

Calibration anchors (all rounds):

| Path | Avg Score | Round | Itemized? | Comparison |
|------|-----------|-------|-----------|------------|
| CIs9x2ZRgh.md (CR-CTC) | 6.75 | R1 | Yes | Similar CTC/speech domain; USR 2.0 has stronger novelty and larger empirical gains |
| fUGhVYPVRM.md (Align With Purpose) | 7.00 | R1 | Yes | CTC alignment optimization; USR 2.0 addresses a broader problem with larger gains |
| 4lOWCkhr4g.md (Cross-lingual PL) | 5.25 | R1 | Yes | Rejected for limited novelty; USR 2.0 has far more novelty |
| eSO9quCgmz.md (Rethinking PL) | 5.00 | R1 | No | General PL insights; less directly comparable |
| 9WD9KwssyT.md (Zipformer) | 7.50 | R2 | Yes | Speech ASR architectural improvements; USR 2.0 has comparable results with cleaner ablations |
| TPZRq4FALB.md (TTA multi-modal) | 8.00 | R2 | No | Multi-modal adaptation; different topic |
| PdaPky8MUn.md (Never train from scratch) | 8.00 | R2 | No | Long-sequence models; different topic |

The scoring model assigned the paper's strengths very high impact (+9.99, +9.99, +9.98, +9.43) and its weaknesses negligible impact (-0.00 each), confirming that the core issues are minor and not threats to the contribution. Compared to the closest anchors — CR-CTC (6.75) which has modest novelty and Zipformer (7.50) which has weaker ablation isolation — USR 2.0 offers a genuinely novel idea (the global coherence insight) with clean ablations and large-margin evidence across three modalities, placing it above both.

MY FINAL SCORE: <score>8.0</score>
MY FINAL DECISION: <decision>Accept</decision>
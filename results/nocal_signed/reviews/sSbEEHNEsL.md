## Summary

USR 2.0 proposes CTC-driven teacher forcing for pseudo-labelling in unified speech recognition (ASR/VSR/AVSR). Instead of slow autoregressive decoding to generate attention-based pseudo-labels, the method feeds greedily-decoded CTC outputs into the decoder via teacher forcing, generating attention targets in a single forward pass. Combined with a mixed sampling strategy that intermittently reintroduces AR decoding to mitigate exposure bias, this yields ~2× faster training, dramatic OOD robustness gains (especially on long utterances and noisy inputs), and competitive-to-state-of-the-art in-distribution performance across LRS3, LRS2, and WildVSR.

## Strengths

- **A clean, well-motivated architectural insight (Sections 4.1–4.2).** The core idea — using greedily-decoded CTC outputs to drive teacher-forced generation of attention pseudo-labels — is clearly presented and soundly reasoned. The paper correctly identifies that global coherence of the attention PLs is unnecessary in the pseudo-labelling setting because teacher and student share the same conditioning.

- **Dramatic and consistent OOD robustness improvements (Tables 1 and 3, Figure 3).** The long-utterance results in Figure 3a are striking: USR 2.0 maintains ~35% WER on 600-frame inputs where USR degrades to ~100% WER. On OOD datasets (Table 3), USR 2.0 achieves 15.4% on LibriSpeech vs. 25.3% for USR, and 73.7% on WildVSR vs. 80.0% for USR. These are large, practically meaningful gaps.

- **Well-structured ablations (Table 4, Figure 4).** The ablation isolating CTC-driven mode vs. AR mode and systematically removing PL targets from individual branches cleanly supports the claims about which components contribute to ID vs. OOD performance. The analysis of AR sampling probability (Figure 4) provides clear evidence for the design's trade-off between ID accuracy, OOD robustness, and training efficiency.

- **Training speedup identified and decomposed (Sections 4, 6, Appendix C.5).** The paper identifies two concrete sources of speedup — ~40× per-step decoding gain of CTC over AR (Figure 1) and reduction from 75 to 50 training epochs — and provides evidence for both, making the 2× training time claim grounded rather than hand-wavy.

## Weaknesses

### Major

- **No variance or significance reporting in any experiment (all tables).** Every reported WER is a single number with no error bars, multiple runs, or standard deviations. This is most consequential for small-margin in-distribution comparisons: at Base/LRS3 (Table 2), USR 2.0 vs USR differences are 0.2% WER on ASR (3.0 vs 3.2) and 0.1% on AVSR (2.9 vs 3.0) — margins that could plausibly lie within training noise. Without variance, the reader cannot distinguish signal from noise on several in-distribution claims. The OOD results are large enough to survive this concern, but the ID claims at the Base/LRS3 setting are weakened.

- **The Huge model result (Section 6) lacks a direct USR Huge baseline under identical training data and compute.** The paper trains USR 2.0 Huge on LRS2+LRS3 labelled + VoxCeleb2+AVSpeech unlabelled but does not report USR Huge under the same conditions. Without this control, the strong Huge results (17.6% VSR, 0.9% ASR, 0.8% AVSR) cannot be cleanly attributed to the proposed method versus simply having more labelled+unlabelled data and a larger model. This does not affect the core contributions (established at smaller scales), but limits the paper's scalability claims.

### Minor

- **The in-distribution SOTA claim is slightly overstated in framing.** At Base/LRS3 (Table 2), USR 2.0 regresses on VSR (36.2 vs USR's 36.0). At Large/LRS3+Vox2 (high-resource), USR 2.0 ASR = 1.3% trails BRAVEn's 1.2% and USR's 1.2%. The paper's overall characterization ("matches or outperforms the state of the art") is accurate in aggregate across settings, but the bold formatting of USR 2.0's VSR result at Base/LRS3 (36.2, which is worse than USR's 36.0) is a presentation error.

- **The claim that "global coherence is unnecessary" (Section 4.1) is argued theoretically but lacks direct empirical validation.** The paper does not measure the quality of CTC-driven attention PLs (e.g., their WER against ground truth on a small labeled set) or directly compare them to standard AR-decoded attention PLs. The ablation (Table 4) shows that removing attention PL targets from the decoder hurts ID performance (3.2→3.6, row 1 vs row 4), supporting the value of these targets, but this does not directly validate the coherence argument itself.

- **OOD evaluation on AVSpeech and VoxCeleb2 uses Whisper-generated transcriptions as ground truth (Sections 5.1, 5.3).** The paper discloses this ("automatically transcribed", "treating Whisper as an oracle"), but does not discuss the potential confound: if Whisper's errors correlate with certain input characteristics (longer sequences, noise type), the relative comparison could partially reflect alignment with Whisper's biases. This is partially mitigated for VoxCeleb2 by Figure 3 showing consistent trends across length buckets.

- **The 2× training speed claim would benefit from a controlled experiment isolating the method's contribution.** The speedup combines two factors (faster per-step decoding and fewer epochs). If USR were trained for only 50 epochs (matching USR 2.0's 50), part of the claimed speedup from fewer epochs might reflect a suboptimal USR training schedule rather than a property of the method. The wall-clock comparison in Figure 5 partially addresses this, but a direct head-to-head at equal epochs would strengthen the claim.

### Trivial

None.

## Nice-to-Haves

- A simple empirical sanity check: compute the WER of CTC-driven teacher-forced attention PLs against ground-truth labels on a small labeled subset, and compare it against the WER of standard AR-decoded attention PLs. This would directly validate or challenge the "global coherence is unnecessary" claim.
- An experiment training USR for 50 epochs (matching USR 2.0's convergence point) to isolate the method's contribution to the speedup from convergence schedule differences.
- Acknowledgement of the Whisper-as-ground-truth limitation in the main text.

## Removed Points

- The critic's claim that "removing attention PL targets from the decoder hardly changes ID WER" based on rows 3 vs 1 of Table 4 is factually inaccurate: rows 3 vs 1 compare supervising the CTC *head* with attention PLs, and the actual decoder comparison (row 1 vs row 4) shows a 0.4% ID change (3.2→3.6), which is non-trivial.
- Code release concerns removed per hard rule: not including code in a submission is not a valid weakness.
- Concern about the 1000-token vocabulary being trained on labelled data only is speculative and the paper already discloses this in Section 4.3.
- Style/formatting nitpicks from the section-by-section notes removed per hard rules.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Run each key configuration (at minimum the Base/LRS3 setting and main ablations) for 3 random seeds and report mean ± std. This is the single most impactful improvement.
2. Train a USR Huge model under the same data conditions to enable a controlled comparison at scale.
3. Include a direct empirical check of CTC-driven attention PL quality against ground truth on a small labeled subset.

## Score and Decision

The paper presents a genuinely clever and practically useful method. The OOD robustness improvements are large, well-documented, and survive all caveats. The training speedup is architecturally grounded. The ablations are clean. The main evidentiary gap is the complete absence of variance reporting, which weakens the in-distribution SOTA claims at the smallest scale (Base/LRS3) but does not threaten the core contributions (OOD robustness, training efficiency, and scaling behavior are all supported by independently sufficient evidence). A revision adding multi-seed variance information would substantially strengthen the paper.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>
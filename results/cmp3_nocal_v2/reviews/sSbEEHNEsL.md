## Summary

This paper proposes USR 2.0, a semi-supervised training framework for unified speech recognition (ASR, VSR, AVSR). The core technical contribution is CTC-driven teacher forcing: instead of slow autoregressive decoding to generate attention-based pseudo-labels, the teacher's fast CTC outputs are fed into the decoder to produce attention targets in a single forward pass. This removes the AR bottleneck (~2× training speedup), couples the CTC and attention branches for improved OOD robustness, and is complemented by a mixed sampling strategy that mitigates exposure bias. USR 2.0 demonstrates substantial gains on long utterances, noisy conditions, and cross-dataset evaluation, while achieving state-of-the-art results on LRS3, LRS2, and WildVSR.

## Strengths

- **Novel and well-motivated technical insight.** CTC-driven teacher forcing turns a seemingly obvious objection (CTC outputs lack global coherence) into a design feature: in pseudo-labelling, matched conditioning between teacher and student makes global coherence unnecessary (§4.1). This directly addresses a real bottleneck in USR — the slow autoregressive pseudo-label generation — and the "matched conditioning" argument is clearly articulated and non-obvious.

- **Consistent and substantial OOD improvements.** The gains are large and documented across multiple axes: long utterances (Figure 3a: USR 2.0 stays at ~35% WER while USR climbs to ~70%+ at 400+ frames), noise robustness (Table 1: USR 2.0 beats USR at every SNR level from 10 dB to -5 dB for both ASR and AVSR), and cross-dataset evaluation (Table 3: LibriSpeech 15.4% vs. USR's 25.3% and AVSpeech 25.0% vs. 34.7% under greedy decoding). These directly validate the paper's core motivation about decoupled supervision causing self-reinforcing OOD errors.

- **Clean ablation directly supporting design choices.** Table 4 isolates the contribution of each pseudo-label type per mode. Removing CTC supervision from the decoder collapses OOD performance (35.1% → 24.2% in CTC-driven mode), while removing attention targets hurts in-distribution performance (3.2% → 3.6%). Figure 4's sweep of the mixed-sampling probability gives a complete picture of the ID/OOD/efficiency trade-off. Both PL types demonstrably matter.

- **Practically significant training speedup.** The ~2× training speedup (Figure 5) is documented across model scales and data regimes. The paper identifies that this comes from both faster per-step decoding and faster convergence (50 vs. 75 epochs), which is a practically important result for semi-supervised training at scale.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **Unacknowledged VSR regression on Base/LRS3 low-resource setting.** In Table 2, USR 2.0 achieves 36.2% VSR WER vs. USR's 36.0% on the Base/LRS3 low-resource setting — a small regression. The paper's prose claims it "matches or outperforms the state of the art" without acknowledging this case. The overall trend is clearly positive (USR 2.0 outperforms USR on VSR in every other setting: Base+ LRS3+Vox2: 26.4 vs. 28.4; Large: 23.7 vs. 26.9; High-resource Base+: 24.8 vs. 26.5; High-resource Large: 21.5 vs. 22.3), but this single regression should be acknowledged with a brief discussion of whether it is within expected run-to-run noise.

2. **No variance or confidence intervals reported.** All experiments report only point estimates of WER. For the large OOD gains (e.g., 15.4% vs. 25.3% on LibriSpeech), variance would not change the conclusion. However, for small in-distribution differences (AVSR: 2.9% vs. 3.0%; ASR: 3.0% vs. 3.2%), the reader cannot assess whether these are meaningful or within run-to-run noise. Pseudo-labelling methods are known to have non-trivial training variance, and even a single multi-seed experiment on a representative setting (e.g., Base/LRS3 low-resource) would substantially strengthen the in-distribution claims.

3. **Huge model results lack same-scale baseline in the main paper.** The scaling experiment (§6) reports impressive Huge-model results (17.6%/0.9%/0.8% WER on LRS3) and states that comparisons are in Appendix C.1. However, the main paper's Table 2 shows no competitors at the Huge scale. A same-scale USR baseline in the main results table would help the reader disentangle gains from the method vs. gains from increased parameters and data. This is a presentation gap rather than a fundamental flaw — the core contribution is validated at smaller scales — but it limits how the scaling narrative reads as a standalone paper.

### Trivial
None.

## Nice-to-Haves

- **Beam-search results for OOD benchmarks (Table 3).** The OOD results in Table 3 are reported only under greedy decoding. The paper already shows (Figure 3c) that increasing beam size narrows the USR/USR 2.0 gap on long utterances. Reporting beam-search WER for LibriSpeech, WildVSR, and AVSpeech (consistent with the beam size 40 used in Table 2) would clarify how much of the OOD improvement persists at the standard inference configuration and would round out the evidence for broader SOTA claims.

- **More direct explanation of why pure CTC-driven mode is not used.** Figure 4 shows that pure CTC-driven mode (AR probability=0) already achieves strong OOD performance (24.2%) with competitive ID performance (3.2%). The answer — ID performance improves from 3.2% → 2.8% as AR probability increases to 0.6 — is implicit in the figure, but the trade-off story could be told more explicitly to highlight that the 50/50 default is justified by a multi-objective optimization (ID accuracy, OOD robustness, and training speed).

## Removed Points

These points from the original input were removed per filtering rules:

- **"Huge model lacks critical baseline — appendix comparisons insufficient":** The paper explicitly states "Comparisons with additional methods are in Appendix C.1." Per guidelines, appendix content stripped by the parser is assumed to exist in the original submission. The remaining concern (no Huge-scale USR baseline in the main paper) is retained as Minor weakness 3 above.

- **"Clarify WildVSR setting — 73.7% seems high":** Section 5 explicitly states that OOD experiments use the low-resource setting (30h LRS3 labelled, remaining LRS3 unlabelled). The table caption and text provide sufficient context.

- **"What happens at 100% CTC-driven mode":** This is already addressed by Figure 4 and the surrounding discussion. The paper's treatment is adequate.

- **"Strengthening: add Huge-scale USR baseline":** Covered by Minor weakness 3; the phrasing about adding it to the main paper is retained, but the framing as an appendix gap is removed.

## Novel Insights

Beyond the paper's own contributions, the most interesting observation to emerge from the review is that ID and OOD performance trends are largely uncorrelated under different design choices (Table 4, Figure 4). This suggests that the CTC-driven and AR modes genuinely capture different capabilities — one optimized for robustness, the other for in-distribution quality — and that the mixed sampling strategy is not a compromise but a synthesis of two complementary mechanisms. The paper notes this briefly (§7) but the implication is deeper: the optimal balance between the two modes may vary by deployment scenario in ways that extend beyond the single 50/50 default, and this uncorrelated trend could itself be a useful diagnostic for future work on robust pseudo-labelling.

## Suggestions

- Acknowledge the small VSR regression on Base/LRS3 (Table 2) and briefly discuss whether it is within expected run-to-run variance.
- Add variance estimates (2–3 seeds) for at least one representative setting, such as the Base/LRS3 low-resource results, to ground the small in-distribution improvements.
- Consider moving or summarizing the key Huge-scale comparisons from Appendix C.1 into the main paper so the scaling results are self-contained.
- Add beam-search columns to Table 3 to complement the greedy-decoding OOD results.

## Score and Decision

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>
Now I have a clear picture. Let me write the final consolidated review.

## Summary

DiSTAR proposes a zero-shot TTS framework that couples an autoregressive (AR) language model with a masked diffusion model, operating entirely in discrete RVQ token space. It adopts a patch-wise factorization: a causal AR LM drafts coarse patch-level sketches, then a discrete masked diffusion Transformer fills in intra-patch details in parallel, avoiding both the exposure bias of pure AR and the optimization difficulties of continuous diffusion. Practical engineering contributions include stochastic layer truncation for variable-bitrate inference, embedding transplantation from the codec codebook, and RVQ-aware temperature shaping. On LibriSpeech-PC and SeedTTS test-en, DiSTAR-medium (0.3B) achieves the lowest reported WER among the comparison set.

## Strengths

1. **Well-motivated architectural synthesis.** The paper identifies the joint time-depth modeling challenge in RVQ-based TTS and proposes a clean resolution: AR-patch drafting over a compact sketch (Eq. 1), followed by LLaDA-style discrete masked diffusion for intra-patch infilling in parallel (Eq. 2, Sec. 3.1.1). This combination is technically coherent and, to my knowledge, novel in the RVQ TTS context.

2. **Practical engineering contributions.** Three concrete techniques address real RVQ deployment issues: (a) embedding transplantation from the codec codebook to avoid cold-start mismatch (Sec. 3.4), (b) stochastic layer truncation during training enabling test-time variable-bitrate without retraining (Sec. 3.4, Figure 2), and (c) layer-wise/position-wise temperature shaping to counteract the identified "tail-first bias" (Sec. 3.4). These are pragmatic and likely useful beyond this system.

3. **Competitive WER results.** DiSTAR-medium (0.3B) achieves 1.66% WER on LibriSpeech-PC and 1.32% on SeedTTS test-en — the lowest WER in Table 1, including against F5TTS (2.02/1.35), E2TTS (2.74/2.20), and DiTAR (2.39/1.78). The improvement is substantial in absolute terms.

## Weaknesses

### Fatal
None.

### Major

1. **Uncontrolled comparison with the most relevant baseline (DiTAR).** DiTAR scores in Table 1 are marked with ♦ and explicitly sourced from the DiTAR paper — they were not obtained from a model trained on the same data or under the same conditions. The paper trains DiSTAR on ~50k hours of Emilia; there is no statement that any baseline (including DiTAR, F5TTS, or E2TTS) was trained on identical data. Since training data differences can dominate architectural differences in TTS, the central comparison against the paper's direct predecessor is not interpretable as a controlled experiment. The comparison is also at asymmetric NFE (DiTAR at 10 steps vs. DiSTAR at 24 steps). The headline claim of "surpassing state-of-the-art" rests substantially on this uncontrolled comparison. (The WER improvements over F5TTS and E2TTS are still meaningful but also lack controlled-data verification.)

2. **Speaker similarity does not support the claimed superiority.** On LibriSpeech-PC, DiSTAR-medium SIM = 0.67 (tied with DiTAR, worse than E2TTS at 0.70 and F5TTS at 0.68). On SeedTTS test-en, SIM = 0.66 (worse than F5TTS 0.68 and E2TTS 0.71). The abstract claims DiSTAR "surpasses state-of-the-art zero-shot TTS systems in ... speaker/style consistency," but the SIM data contradict this — DiSTAR is behind or tied on every speaker similarity comparison. The paper acknowledges this indirectly ("SIM on par with the best alternatives" in Sec. 4.2) but the framing in the abstract and conclusion is systematically more ambitious than the evidence supports.

3. **The ablation study does not validate the core architectural thesis.** The paper's central design claim is that the coupling of (a) an AR drafter and (b) a masked diffusion refiner in (c) discrete RVQ space yields a quality advantage. Yet Table 3 compares only *decoding strategies* (sampling vs. greedy with temperature tweaks) — it does not ablate any architectural component. There is no experiment isolating: (i) what happens if the masked diffusion module is replaced with a standard AR decoder per patch, (ii) what the effect of discrete vs. continuous latent space is with the same architecture, (iii) what the aggregator design contributes, or (iv) the effect of overlapping vs. non-overlapping patches. The paper demonstrates that DiSTAR as a whole works, but does not experimentally validate which piece is responsible — a significant gap for a method paper.

4. **Inference efficiency claims are unsubstantiated.** The title uses "Scalable" and the paper states "maintaining the inference cost close to its continuous counterpart DiTAR" (Sec. 1) and "comparable or lower computational cost" (contributions). No wall-clock timing, FLOPs, or throughput measurements are provided. The only efficiency-related experiment (Figure 2) shows quality vs. bitrate trade-offs under RVQ pruning but gives no compute measurements. For a paper that makes explicit efficiency and scalability claims, this absence is notable.

### Minor

5. **Subjective evaluation lacks statistical rigor.** Table 2 reports SMOS and CMOS with 95% confidence intervals that overlap substantially (e.g., DiSTAR SMOS 3.31±0.25 vs. E2TTS 3.29±0.19; CMOS 0.22±0.13 vs. F5TTS 0.01±0.12). No statistical significance test (e.g., paired bootstrap or Wilcoxon) is reported, and subjective evaluation is only conducted on SeedTTS test-en (not on LibriSpeech-PC). The claims of "leading on SMOS" and "highest CMOS" are not statistically supported by the data as presented.

6. **Missing quantitative diversity evaluation.** The abstract claims DiSTAR "maintains rich output diversity" and Sec. 4.3 states sampling "can recover timbral nuances." No diversity metrics (e.g., within-prompt variance in WER, pitch, duration, or distributional prosody analysis) are reported. Table 3 shows that sampling changes WER/SPK relative to greedy, but this does not constitute a diversity analysis.

### Trivial
None.

## Nice-to-Haves
- Report DiSTAR at lower NFE (e.g., 10) and DiTAR at higher NFE (e.g., 24) to rule out step-count asymmetry as the source of the WER advantage.
- Provide wall-clock latency or FLOPs measurements to substantiate the efficiency/scalability claims.
- Add ablations isolating the masked diffusion module (e.g., pure AR decoding per patch) and the discrete-vs-continuous latent space choice.

## Removed Points

These points are flagged to be removed, treat them with caution:

1. **"Missing comparison against VALL-E 2, CosyVoice 2, Seed-TTS in experiments."** — CosyVoice 2 is present in Table 2. The baseline set (IndexTTS, E2TTS, F5TTS, DiTAR, CosyVoice 2, FireRedTTS) is reasonable for the comparison. Removing baseline-specific complaints that are not tied to a concrete evaluation gap.

2. **"Connection to LLaDA's training objective is stated but not derived."** — The paper correctly states the objective (Eq. 2), cites LLaDA, and provides the key formulation. A full derivation is appropriate in an appendix but its absence is not a weakness.

3. **"Tail-first bias is presented anecdotally without quantitative evidence."** — This observation supports a minor set of decoding heuristics whose combined effect is shown in Table 3. Individual quantitative characterization of the bias would be nice-to-have but not essential for the paper's core claims.

4. **"The paper should cite more related work / missing references."** — Generic missing-reference complaints without specifying what substantive gap the missing reference creates are not actionable weaknesses.

## Novel Insights

None beyond the paper's own contributions. The reviews surface a systematic gap between the paper's ambitious claims and its evidence base — the abstract claims superiority on three dimensions (robustness, naturalness, speaker similarity), but the evidence is strongest for only one (robustness/WER), mixed for naturalness, and negative for speaker similarity.

## Suggestions

1. Reframe claims about speaker similarity to match the evidence — the paper has competitive but not leading SIM scores.
2. Train DiTAR (or a comparable continuous-domain system) on the same Emilia data with matched NFE to enable a controlled comparison — this is the single highest-leverage improvement.
3. Add architectural ablations: replace the masked diffusion decoder with a standard AR decoder per patch to isolate the contribution of the discrete masked diffusion module.
4. Report standard errors or confidence intervals for all objective metrics (WER, SIM, UTMOS) and add significance tests for subjective metrics.
5. Provide latency/throughput measurements to substantiate efficiency claims.

## Score and Decision

**Calibration analysis.** I retrieved human-scored anchors across all score bands. The most informative comparisons:

| Anchor | Avg Score | Round | Comparison to DiSTAR |
|--------|-----------|-------|---------------------|
| MaskGCT (ExuBFYtCQU) | 5.25 | Bracketing | Similar topic (masked generation for TTS). MaskGCT was accepted despite incremental novelty; it had stronger experimental validation (100k hours, controlled baselines). DiSTAR has more architectural novelty but weaker experimental controls. |
| DiTTo-TTS (hQvX9MBowC) | 6.25 | Bracketing | Stronger experimental validation (thorough ablations, controlled comparisons). DiSTAR is weaker on experimental rigor. |
| CLaM-TTS (ofzeypWosV) | 6.40 | Bracketing | Accepted with clearer contributions and more complete evaluation. DiSTAR has thinner ablation. |
| HALL-E (868masI331) | 6.40 | Bracketing | Accepted with strong experimental results and new benchmark. DiSTAR's validation is less thorough. |
| Controllable TTS (qH5uyYCG2j) | 4.20 | Narrowing | Rejected; missing baseline comparisons and no human evaluation. DiSTAR is stronger — it has human eval and more baselines. |
| ControlSpeech (zAogQOIphH) | 5.20 | Narrowing | Rejected despite interesting idea; validation gaps. Similar profile to DiSTAR. |

**Round-1 bracket:** 3.5 – 5.5 (based on comparison to MaskGCT at 5.25 and Controllable TTS at 4.20).

**Narrowing:** The paper's architectural novelty and strong WER results lift it above the 4.0 level, but the uncontrolled DiTAR comparison, overclaimed speaker similarity, thin ablation, and unsubstantiated efficiency claims prevent it from reaching the 5.5+ level of papers with more rigorous validation. The closest profile is ControlSpeech (5.20, rejected) but DiSTAR has stronger objective results.

**Final score:** 4.5. The paper proposes a genuinely well-motivated architecture with practical techniques and competitive WER, but the experimental validation has significant gaps — the central comparison is uncontrolled, speaker similarity claims are not supported, the ablation does not test the architectural thesis, and efficiency claims are unsubstantiated. These are fixable weaknesses, but in their current form they widen the gap between the paper's claims and its evidence too far for acceptance.

**Boldness note:** This score is deliberately not clustered in the middle. The paper has real architectural novelty and strong WER, making it clearly above typical "reject" papers (score ≤3), but the experimental gap is too wide for acceptance. A controlled comparison and proper architectural ablation would likely move this paper to the 6+ range.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>
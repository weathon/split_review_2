Here is the consolidated final review.

---

## Summary

DiSTAR is a zero-shot TTS framework that operates entirely in the discrete RVQ code space, coupling an autoregressive language model (for coarse temporal structure across patches) with a discrete masked diffusion model (for parallel refinement within each patch). The architecture is inspired by DiTAR's patch-wise AR+diffusion paradigm and LLaDA-style discrete masked diffusion. The paper reports strong WER results and introduces several practical inference-time techniques (stochastic layer truncation for variable bitrate, embedding transplantation, tail-first bias heuristics).

## Strengths

- **Principled architectural motivation.** The paper identifies the joint time-depth modeling challenge in RVQ-based TTS and proposes a well-motivated coupling: an AR drafter for coarse temporal structure and discrete masked diffusion for parallel depth completion within each patch. This is a clean synthesis of ideas from DiTAR (patch-wise AR+diffusion) and LLaDA (discrete masked diffusion), adapted to the TTS setting. (Section 1, Section 3.1)

- **Competitive WER results.** DiSTAR-medium achieves the lowest reported WER on both LibriSpeech (1.66) and Seed-TTS (1.32) among compared systems. On LibriSpeech, the improvement over DiTAR (2.39→1.66) is substantial. WER is a primary metric for robustness in zero-shot TTS. (Table 1)

- **Practical inference-time techniques.** Stochastic layer truncation during training enables variable bitrate at test time via RVQ layer pruning without retraining (Figure 2). Embedding transplantation from the codec bootstraps training. The tail-first bias analysis with the three decoding heuristics (layer-wise temperature shaping, position-wise shaping, hybrid sampling) shows genuine engagement with inference-time behavior. (Section 3.4)

- **Subjective results support speaker similarity and naturalness.** In Table 2, DiSTAR achieves the highest SMOS (3.31±0.25) and CMOS (0.22±0.13) among compared systems, indicating strong subjective performance on speaker similarity and naturalness.

## Weaknesses

### Fatal
None.

### Major

1. **Headline SOTA claims overstate the paper's empirical standing.** The abstract, contribution list, and conclusion claim "state-of-the-art robustness, speaker similarity, and naturalness." However, Table 1 (objective metrics) shows DiSTAR-medium ranks first **only on WER (robustness)**. On SIM (speaker similarity), it ranks third behind E2TTS and F5TTS on both benchmarks. On UTMOS (naturalness), it ranks second behind IndexTTS on LibriSpeech and behind DiTAR on Seed-TTS. The subjective results (Table 2) do show DiSTAR leading in SMOS and CMOS, which partially supports the claims, but the blanket "SOTA on all three" statement is contradicted by the paper's own objective numbers. The claims should be calibrated to reflect what the data shows.

2. **The comparison to DiTAR uses non-reproduced numbers with a large NFE discrepancy.** DiTAR results are marked with ♦ ("scores reported in DiTAR paper") and use NFE=10, while DiSTAR uses NFE=24 (2.4× more diffusion steps). These results come from different papers with potentially different data splits, training sets, and evaluation pipelines. The paper notes the NFE difference in the table but does not discuss its implications. The lack of a controlled comparison (same compute budget, training data, evaluation pipeline) weakens the claim that discrete representations outperform continuous ones within the same patch-wise framework. (Table 1)

3. **No efficiency or throughput data despite explicit claims about inference cost.** The paper claims DiSTAR "maintains the inference cost close to its continuous counterpart DiTAR" (Section 1) and discusses variable bitrate/compute control (Section 4.4). Yet no wall-clock time, FLOPs, throughput, or latency numbers are reported for any system. The NFE discrepancy (24 vs 10) makes the inference-cost claim unsubstantiated without actual timing data.

4. **Missing key baselines.** VALL-E 2 (Chen et al., 2024), a closely related RVQ-based AR TTS system, is cited in the related work but not included in any experimental comparison. CosyVoice 2 appears in the subjective evaluation (Table 2) but is absent from the objective evaluation (Table 1), making cross-table comparisons incomplete.

5. **Main-text ablation is insufficient to attribute results to specific architectural choices.** Table 3 compares only three decoding strategies. The paper mentions additional ablations (patch size in Appendix D, CFG in Appendix C), but the main text lacks component-level isolation experiments for: the AR drafter vs. pure masked diffusion, overlapping window design, aggregator design, embedding transplantation, and stochastic layer truncation. Without these, it is unclear which design choices drive the reported results.

### Minor

6. **No confidence intervals or variance estimates on objective metrics (Table 1).** Key comparisons involve very small margins: WER on Seed-TTS is 1.32 (DiSTAR) vs 1.35 (F5TTS), a 0.03 difference; SIM on LibriSpeech is 0.67 for both DiSTAR-medium and DiTAR. Without variance estimates, these differences cannot be distinguished from noise.

7. **Non-monotonic WER in the RVQ pruning experiment (Figure 2).** WER decreases from 2.18 (2 layers) to 1.88 (6 layers), then increases to 2.04 (8 layers) and 1.98 (9 layers). The paper attributes this to upper layers encoding acoustic detail rather than linguistic content, but if that were the full story, WER should plateau rather than increase. This deserves explicit discussion.

8. **The tail-first bias explanation (Section 3.4) is acknowledged as speculative** ("A likely reason is that..."). The three proposed heuristics are evaluated only as a composite in Table 3, not independently, so their individual contributions cannot be assessed.

### Trivial
None.

## Nice-to-Haves

- Ablate each architectural component independently (AR drafter, overlapping windows, embedding transplantation, stochastic layer truncation) to isolate which choices drive the reported gains.
- Report wall-clock time or real-time factor for DiSTAR and all baselines, especially to substantiate the inference-cost claim relative to DiTAR at matched NFE.
- Include VALL-E 2 in both objective and subjective comparisons, and add CosyVoice 2 to the objective table.
- Calibrate the SOTA claims to accurately reflect that DiSTAR achieves best WER with competitive SIM/UTMOS, and best subjective SMOS/CMOS.

## Removed Points

These points are flagged to be removed; treat them with caution.

1. **Criticism about Eq. (1) showing token-level factorization while method is patch-level.** The text clearly states "inference realizes the autoregressive step at the patch level and resolves intra-patch tokens via masked diffusion," which adequately clarifies the conceptual-to-practical mapping. This is not a real problem.

2. **Criticism that the 1/t weighting in the loss function is unjustified.** The paper states it "recovers an upper bound on the sequence negative log-likelihood," which is a justification. The claim that no justification exists is inaccurate.

3. **Speculation that "If DiSTAR were run at NFE=10, its quality would likely degrade."** This is speculative and cannot be verified from the paper's content.

4. **Criticism about missing subjective comparison with DiTAR.** DiTAR results are drawn from an external paper that may not have published subjective evaluations. Not a weakness of the current paper.

5. **Claim that the paper is "not actually novel at the paradigm level."** This is an opinion about the degree of novelty rather than a specific, verifiable weakness.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Re-run DiTAR under the same training data and evaluation pipeline, matching NFE, to enable a clean discrete-vs-continuous comparison that directly tests the paper's core motivation.
2. Add confidence intervals or standard deviations to Table 1.
3. Report efficiency metrics (RTF or samples/second) for DiSTAR and all baselines.
4. Expand the ablation study to isolate the contribution of each architectural component.

---

## Score and Decision

**Round 1 bracket:** 4.0–5.5 (between Controllable TTS at 4.20 and MaskGCT at 5.25)

**Round 2 narrowing:** DiSTAR sits between Controllable TTS (4.20, rejected for no baselines) and VALL-E 2 (5.00, rejected for limited baselines and thin ablations). The paper's most damaging items — missing efficiency data (favorability -0.21/-0.11/-0.07), SOTA overclaim (0.92), DiTAR NFE discrepancy (-0.87), insufficient ablation (-0.85) — are comparable in severity to VALL-E 2's weakest items (dataset disparity -2.54, limited novelty -4.85), though DiSTAR has stronger strengths (architectural motivation 13.42, WER 10.83) and evaluates against more baselines than VALL-E 2 did. This places it between 4.20 and 5.00, at approximately **4.5**.

The paper presents a methodologically sound architecture with strong WER results and practical inference techniques. However, the evaluation has structural gaps that prevent supporting the strongest claims: the SOTA claim is overblown by the paper's own objective numbers, the key comparison with DiTAR uses uncontrolled conditions with a 2.4× NFE discrepancy, efficiency claims are unbacked by data, and key baselines are missing. These require new experiments, not just rewriting.

**Score: 4.5** — Borderline reject.

**Decision: Reject**

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>
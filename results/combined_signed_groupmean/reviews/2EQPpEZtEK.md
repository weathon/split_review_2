Now I have a clear picture. Let me write the final review.

## Summary

DiSTAR proposes a zero-shot TTS framework that operates entirely in discrete RVQ code space, coupling an autoregressive language model (for patch-level drafting) with a masked diffusion transformer (for intra-patch infilling). The architecture is well-motivated by the need to jointly model temporal and depth dependencies in RVQ sequences, and the paper introduces practical inference techniques (tail-first bias mitigation, stochastic layer truncation). Subjective listening results (SMOS 3.31, CMOS 0.22 on Seed-TTS test-en) are genuinely strong.

## Strengths

- **Well-motivated and novel architecture (Section 3.1).** The paper identifies a genuine tension in RVQ-based TTS — jointly modeling time and depth dependencies — and proposes a clean decomposition: a causal AR drafter for patch-level temporal structure and a discrete masked diffusion refiner for intra-patch multi-codebook resolution. Operating entirely in discrete space while retaining patch-level parallelism is a meaningful architectural contribution.

- **Practical inference engineering contributions (Section 3.4).** The "tail-first bias" observation and three lightweight mitigation strategies (layer-wise temperature shaping, position-wise temperature shaping, hybrid sampling) are the kind of practical findings that make a method work in practice. Stochastic layer truncation at training time enabling post-training RVQ pruning at inference is a clean solution to variable-bitrate synthesis.

- **Strong subjective results (Table 2).** On Seed-TTS test-en, DiSTAR achieves the best SMOS (3.31, tied with E2TTS within error bars) and the best CMOS (0.22, outside error bars of most competitors). These human judgment results are the most convincing evidence for DiSTAR's quality, as they are less susceptible to evaluation-pipeline confounds than objective metrics.

- **Thorough ablation of decoding strategies (Table 3).** The comparison between sampling-based and greedy decoding with various temperature settings demonstrates that the design choices in Section 3.4 are consequential, not cosmetic.

## Weaknesses

### Major

1. **The central comparison against DiTAR is not valid.** The DiTAR scores in Table 1 are marked with ◆ and described as "scores reported in DiTAR paper." WER, SIM, and UTMOS depend critically on the ASR model, prompt selection, and preprocessing pipeline. Since DiTAR is the most methodologically similar baseline (both use patch-wise AR drafting + diffusion infilling), the reader cannot attribute reported improvements to DiSTAR's discrete-space design versus differences in evaluation methodology. The paper should re-run DiTAR in the same pipeline or clearly acknowledge this limitation.

2. **No diversity metrics despite explicit diversity claims.** The abstract claims DiSTAR "maintains rich output diversity," and Section 1 claims "fine-grained control over the diversity-determinism trade-off." Yet the paper reports zero diversity metrics (self-SIM, sample variance, FRT/FRE, etc.). Table 3 only shows that greedy vs. sampling decoding affects WER and SPK slightly, which confirms a trade-off exists but does not measure diversity. A central claimed advantage lacks supporting evidence.

3. **Speaker similarity claims in abstract/conclusion are overstated.** The abstract and conclusion claim "state-of-the-art speaker similarity," but objective SIM scores (Table 1) tell a different story: on LibriSpeech, DiSTAR-medium SIM is 0.67 vs. E2TTS 0.70 and F5TTS 0.68; on Seed-TTS, DiSTAR-medium is 0.66 vs. E2TTS 0.71 and F5TTS 0.68. While subjective SMOS leads, the paper should not claim SOTA on speaker similarity overall without qualifying the gap between objective and subjective results. Section 4.2's more measured "SIM on par with the best alternatives" is more appropriate.

4. **Efficiency claims are not substantiated.** DiSTAR uses 24 NFE versus DiTAR's 10 NFE (2.4× difference). The paper claims "inference cost close to its continuous counterpart DiTAR" (Section 1) and "comparable or lower computational cost" (Section 4.2), but provides no wall-clock timing, FLOPs, or throughput numbers. Since DiSTAR runs both an AR LM and a masked diffusion model with multiple forward passes, the per-step compute may also differ. Without timing data, the efficiency comparison is unsubstantiated.

### Minor

5. **No limitations or failure cases discussion.** The paper has no section discussing what DiSTAR handles poorly. Important questions go unaddressed: performance on non-English languages, very long passages, noisy or non-speech prompts, emotional speech, etc. Adding such discussion would improve credibility.

6. **Table 3 ablation is limited.** It varies only the decoding strategy among three configurations. Missing ablations include: (a) removing each of the three decoding heuristics individually, (b) varying NFE to show quality-efficiency trade-offs, and (c) comparing against AR-only or diffusion-only variants to quantify the value of each component.

7. **Embedding initialization is not ablated (Section 3.4).** Transplanting 16 channels from the RVQ codebook and sampling the rest from a matched Gaussian is presented as a design decision, but its importance for convergence speed or final quality is not quantified.

### Trivial

None.

## Nice-to-Haves

- Re-run DiTAR in the same evaluation pipeline for a controlled comparison.
- Add diversity metrics (self-SIM, sample variance) to support the "rich output diversity" claim.
- Provide wall-clock timing or FLOPs analysis for inference.
- Add a limitations section discussing edge cases and failure modes.
- Ablate the embedding initialization heuristic and individual decoding tricks.

## Removed Points

These points were raised in the input review but are removed after verification:

1. "WER below human without critical discussion" — While the paper could acknowledge this, WER below reported human baselines on LibriSpeech test-clean is common in modern TTS and does not indicate an artifact. The paper's comparisons against other systems (which are the relevant comparisons) remain valid.
2. "Tail-first bias explanation is speculative" — This is presented as a plausible explanation for an empirical observation; the mitigation strategies are validated in Table 3. This is an honest acknowledgment of observed behavior, not a weakness.
3. "Equation 2 / 1/t weighting theoretical grounding not fully spelled out" — The paper cites LLaDA and states the weighting recovers an upper bound on NLL. Full derivation is standard to defer to references.
4. "Single ASR model for WER" — Using Whisper-large-v3 is standard practice in TTS evaluation and is not a weakness.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Calibrate all claims (especially in the abstract and conclusion) to match what the evidence actually supports. Distinguish between objective and subjective metrics when claiming superiority.
- Add at least one diversity metric to support the "rich output diversity" claim. Self-SIM or generating multiple samples per prompt and measuring variance in prosody/acoustics would be straightforward.
- Provide wall-clock timing or FLOPs for inference, ideally with a breakdown between AR LM and diffusion steps, and report DiSTAR results at NFE=10 for a direct efficiency-quality comparison with DiTAR.
- Include a limitations section discussing what the method does not handle well.

## Score and Decision

**Round 1 bracket:** [5.0, 6.0] — supported by calibration anchors including MaskGCT (5.25, Accept), Vevo (5.50, Accept), and CLaM-TTS (6.40, Accept).

**Closest anchors (itemized comparison):**
- **MaskGCT (5.25)** — Most similar in topic (masked generative TTS with discrete tokens). MaskGCT had more severe novelty concerns (impact=-10.00) and missing baseline comparisons (impact=-7.28) but compensated with open-source code release and strong demo page. DiSTAR has stronger architectural novelty but shares similar evaluation rigor gaps. DiSTAR's diversity metrics gap (-9.99) is comparable in impact to MaskGCT's novelty concerns.
- **VALL-E 2 (5.00, Reject)** — Had multiple decisive weaknesses (dataset disparity -10.00, limited novelty -10.00, no ablation -10.00, no code release -10.00). DiSTAR's weaknesses are less severe: overclaiming and missing evidence rather than fundamental methodology flaws.
- **CLaM-TTS (6.40)** — Had cleaner presentation and better claim calibration. DiSTAR's subjective results are stronger but its overclaiming and missing diversity metrics prevent it from reaching this tier.

**Final score: 5.5** — The paper has a genuinely novel architecture, strong subjective results, and practical engineering contributions. However, the evaluation has significant gaps: the most methodologically relevant baseline comparison (DiTAR) is not apples-to-apples, diversity is claimed but unmeasured, speaker similarity is overclaimed in the abstract/conclusion, and efficiency claims are unsubstantiated. These issues are fixable but as presented, the gap between claims and evidence is too wide for a clean accept.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>
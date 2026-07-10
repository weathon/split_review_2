Based on the impact scores and my own analysis of the paper, here is my synthesis:

The two Major weaknesses score near -10 each, making them very serious. However, the architecture contribution (+9.4) and WER results (+8.0) are also very strong positives. The WER confound is a real evidential gap, but it is fixable and the paper's core architectural contribution stands independently. The thin ablation is concerning but the paper does present some empirical validation (decoding strategy analysis, RVQ layer pruning). I judge the net balance as a borderline accept — the paper has genuine novelty and strong signals, but needs to address the confound and strengthen the evidence in revision.

---

## Summary

DiSTAR is a zero-shot TTS framework that operates entirely in the discrete RVQ code space. It couples an autoregressive LM (for patch-level drafting) with a masked diffusion Transformer (for intra-patch completion), jointly modeling the two dependency axes of RVQ codes: temporal order and layer depth. The design eliminates duration predictors and forced alignment, and enables variable bitrate/compute control at inference via RVQ layer pruning.

## Strengths

- **Well-motivated architecture (Sections 3.1–3.3).** The paper correctly identifies the core challenge of RVQ-based speech synthesis (joint time-depth structure) and proposes a clean, principled decomposition: AR for patch-level temporal evolution, masked diffusion for intra-patch multi-codebook resolution. The design respects the structure of the data rather than bolting AR and diffusion together ad hoc.

- **Strong empirical WER results (Table 1).** DiSTAR-medium (0.3B) achieves 1.66% WER on LibriSpeech test-clean and 1.32% on Seed-TTS test-en — the best among all compared systems, including larger ones like DiTAR (0.6B) and IndexTTS (0.5B). On LibriSpeech it even edges the human baseline (1.80%).

- **Parameter efficiency (Table 1).** DiSTAR-base (0.15B) outperforms or matches systems with twice the parameters on WER and UTMOS, suggesting the architecture uses parameters efficiently.

- **Clean practical design (Section 1).** DiSTAR eliminates duration predictors and forced alignment, relying on [EOS] tokens for termination. The fully discrete design preserves LM-style interpretability (perplexity, decoding hyperparameters) that continuous approaches sacrifice. The paper also demonstrates variable bitrate/compute control via RVQ layer pruning without retraining (Figure 2).

## Weaknesses

### Fatal
None.

### Major

- **WER below the resynthesis baseline signals an unaddressed evaluation confound.** On LibriSpeech test-clean, DiSTAR-medium achieves 1.66% WER — below both the human ground truth (1.80%) and the RVQ resynthesized signal (1.83%), the latter being the best possible WER achievable by any system using this codec (since it reconstructs from ground-truth codes with no generation error). On Seed-TTS test-en, DiSTAR-medium gets 1.32% WER, again below the resynthesis baseline (1.71%). A WER lower than the codec's own reconstruction ceiling implies the generated speech is *more* intelligible to Whisper-large-v3 than the original audio through the same codec. This is a known confound in ASR-based TTS evaluation — generated speech can "game" the ASR model by exhibiting acoustic properties that align with its training distribution. The paper treats this as unqualified evidence of superior robustness without discussion or counter-analysis (e.g., using a second ASR model, or showing correlation with human intelligibility). This undermines the paper's strongest headline claim.

- **Critically thin ablation study for a multi-component architecture (Table 3).** The ablation compares only three decoding configurations of the same model (sample with/without temperature shaping vs. greedy). For a paper whose contribution combines (i) an AR sketcher, (ii) a masked diffusion refiner, (iii) an aggregator with overlapping windows, (iv) stochastic layer truncation, and (v) LLaDA-style masked diffusion — none of these design components are ablated in the main paper. Basic questions go unanswered: what happens without the AR sketcher (pure MDM)? What happens without overlapping windows? What happens without stochastic layer truncation? This makes it difficult to attribute the reported gains to specific design choices.

### Minor

- **The abstract and conclusion claim DiSTAR "surpasses state-of-the-art zero-shot TTS systems in ... speaker/style consistency," but the objective SIM scores (Table 1) do not support this.** On LibriSpeech, E2TTS gets 0.70 SIM and F5TTS gets 0.68, while DiSTAR-medium gets 0.67. On Seed-TTS, E2TTS gets 0.71, F5TTS gets 0.68, DiSTAR-medium gets 0.66. DiSTAR is competitive but does not lead on SIM. The subjective SMOS (Table 2, 3.31±0.25 vs. E2TTS 3.29±0.19) shows non-significant overlap. The speaker similarity claim should be calibrated to this mixed evidence.

- **Several relevant baselines are absent from the objective comparison (Table 1).** VALL-E 2 — cited in Related Work as a leading discrete-token zero-shot TTS system — is not compared, creating a gap where DiSTAR is compared mainly to continuous flow-matching systems while the most directly comparable discrete-token AR competitor is omitted. CosyVoice 2 appears in Table 2 (subjective) but not in Table 1, leaving the objective comparison incomplete for that system.

### Trivial
None.

## Nice-to-Haves

- Report wall-clock inference latency alongside NFE, since the AR LM adds cost not captured by NFE alone.
- Add the missing VALL-E 2 and CosyVoice 2 objective comparisons to strengthen the baseline set.
- Add a component-level ablation, especially replacing masked diffusion with continuous diffusion (direct DiTAR comparison on the same codec) or removing the AR sketcher.

## Removed Points

These points were raised in the input but are filtered out as invalid, generic, or outside scope:
- *Missing VoiceBox/VoiceCraft baselines*: Less directly comparable; removal does not weaken the overall missing-baseline criticism.
- *Equation 1 presentation concern*: Minor observation about ordering of exposition, not a substantive weakness.
- *"Avoids optimization issues" claim (lines 27-28)*: A design motivation stated in the introduction, not a claimed experimental finding.
- *No confidence intervals for Table 1*: Single-run WER without CIs is standard practice in TTS evaluation; generic request.
- *Speculation about high-frequency artifacts (line 209)*: Minor remark, not a structural weakness.

## Novel Insights

None beyond the paper's own contributions. The review identifies specific evidential gaps (WER confound, thin ablation, overclaimed SIM) but does not produce a novel synthesis beyond what the paper states.

## Suggestions

- **(Critical) Address the WER-below-resynthesis confound:** Report WER using a second ASR model (e.g., Whisper-small or a non-Whisper system) to verify that gains reflect genuine intelligibility rather than ASR-specific artifacts. Discuss whether other systems in Table 1 (e.g., F5TTS, which also beats resynthesis on Seed-TTS) exhibit similar patterns.
- **(Important) Add at least one component-level ablation:** The most informative would be replacing the masked diffusion module with continuous diffusion (a direct DiTAR comparison on the same codec and data) or removing the AR sketcher entirely. This would isolate which design choices drive the gains.
- **(Important) Calibrate claims to evidence:** Replace "SOTA speaker similarity" in the abstract and conclusion with language commensurate with the mixed evidence (e.g., "competitive speaker similarity with leading subjective SMOS").
- **(Nice-to-have)** Report wall-clock inference latency alongside NFE, since the AR LM adds cost not captured by NFE alone.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>
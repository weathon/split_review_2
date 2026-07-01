I see there's an issue with the final output format. Let me write the complete, final review now without using the draft tool.

**Here is my final consolidated review:**

---

## Summary
DiSTAR is a zero-shot TTS framework that operates entirely in the RVQ discrete code space. It couples a causal AR language model (for cross-patch temporal dependencies) with a masked diffusion Transformer (for parallel intra-patch multi-codebook infilling), building on the patch-wise decomposition of DiTAR but replacing continuous latents with discrete RVQ tokens. The paper also introduces decoding heuristics (temperature shaping, hybrid sampling) to mitigate a "tail-first bias" and supports variable bitrate/compute via RVQ layer pruning. Experiments on LibriSpeech test-clean and SeedTTS test-en show strong WER improvements (1.66% on LibriSpeech, best among reported systems) and competitive subjective naturalness/speaker similarity.

## Strengths

1. **Well-motivated architecture that directly targets the RVQ time-depth coupling problem.** The patch-level decomposition (Section 3.1.1) cleanly separates cross-patch temporal modeling (AR LM) from intra-patch multi-codebook infilling (masked diffusion). This is a genuinely structural design choice — it treats the RVQ code structure as the organizing principle rather than an afterthought — and the discrete masked-diffusion formulation (Equation 2, adapted from LLaDA) avoids the optimization difficulties of continuous latents that the introduction correctly identifies.

2. **Decoding heuristics address a real observed failure mode.** Section 3.4 identifies a genuine problem: non-autoregressive models trained on causally correlated sequences can become overconfident at later positions within a patch. The three mitigations (layer-wise temperature shaping, position-wise temperature shaping, hybrid sampling) are simple, plausible, and directly motivated by this analysis. Table 3 confirms that the combined strategy improves WER from 2.11 to 1.91 and SPK from 0.626 to 0.640.

3. **Variable bitrate/compute via RVQ layer pruning is a clean practical benefit.** Stochastic layer truncation during training (Section 3.4) enables a direct compute-quality trade-off at inference with no retraining. Figure 2 shows that speaker similarity improves monotonically with more layers while WER stabilizes around six layers — a non-trivial finding consistent with the known depth-wise role of RVQ codebooks.

4. **Strong WER results are the paper's most compelling evidence.** DiSTAR-medium achieves 1.66% WER on LibriSpeech test-clean and 1.32% on SeedTTS test-en, both the best among reported systems in Table 1. The gap to the next best system (F5TTS at 2.02% on LibriSpeech) is meaningful and represents a genuine advance in robustness/intelligibility.

## Weaknesses

### Fatal
None.

### Major

1. **Claims are over-aligned with the strongest results and not fully supported by objective evidence.** The abstract states that DiSTAR "surpasses state-of-the-art zero-shot TTS systems in robustness, naturalness, and speaker/style consistency." Examining Table 1: DiSTAR-medium leads on WER (robustness) on both benchmarks — well supported. However, on LibriSpeech it trails IndexTTS in UTMOS (4.27 vs. 4.35) and trails E2TTS and F5TTS in SIM (0.67 vs. 0.70 and 0.68). On SeedTTS it trails DiTAR in UTMOS (4.05 vs. 4.15) and trails E2TTS and F5TTS in SIM (0.66 vs. 0.71 and 0.68). The subjective results (Table 2) are more favorable — DiSTAR leads on SMOS (3.31) and CMOS (0.22) — but cover only one benchmark (SeedTTS test-en) with a subset of baselines (IndexTTS and DiTAR are absent). The paper should calibrate its headline claims: state-of-the-art WER with competitive (but not uniformly leading) naturalness and similarity.

2. **Baseline comparisons are uncontrolled, weakening the SOTA claim.** Table 1 marks only DiTAR with ♦ ("scores reported in DiTAR paper"). For IndexTTS, E2TTS, and F5TTS, the paper does not state whether these numbers are from the original publications or from a controlled re-evaluation under the same pipeline (same ASR model version and decoding parameters, same WavLM configuration, same UTMOS checkpoint). The "Model settings and baselines" subsection (line 203) describes only DiSTAR's training setup. Since all three metrics (WER, SIM, UTMOS) are sensitive to evaluation details, the strength of the "state-of-the-art" claim depends on knowing whether the gap reflects a genuine system advantage or different evaluation conditions.

3. **No runtime or efficiency comparison despite claims about cost.** The abstract (line 31) claims DiSTAR "maintains the inference cost close to its continuous counterpart DiTAR." DiTAR uses NFE=10 while DiSTAR-medium uses NFE=24 (Table 1). No wall-clock time, RTF, or FLOPs comparison is provided. The only efficiency analysis (Figure 2) studies RVQ layer pruning — useful but orthogonal to comparing with DiTAR. Without quantitative evidence, the cost claim is unsupported.

### Minor

1. **The distribution-shift motivation is never evaluated.** The abstract and introduction characterize continuous-representation systems as "brittle under distribution shift" (line 9) and motivate the fully-discrete RVQ approach partly as a response. However, no experiments test distribution shift — no out-of-domain text, no noisy or accented reference prompts, no cross-language generalization. The evaluations are on standard clean benchmarks.

2. **The three decoding heuristics are not individually ablated.** Table 3 compares only three configurations, which conflate layer-wise temperature shaping, position-wise temperature shaping, and hybrid sampling. It is impossible to tell which trick (or combination) drives the improvement from 2.11 to 1.91 WER. Given that the paper highlights "RVQ-specific sampling" as a contribution (Section 1, bullet 2), individual ablations are needed.

3. **No quantitative evidence for the "tail-first bias."** Section 3.4 describes this failure mode qualitatively ("we observe a tail-first bias," line 140) without any measurement, visualization, or demonstration. This weakens the empirical grounding for the proposed decoding heuristics.

4. **No measurement of exposure bias mitigation.** The paper claims the design "mitigates classic AR exposure bias" (abstract) but never measures whether exposure bias is actually reduced. For example, comparing WER at different utterance lengths could test whether the advantage holds on longer passages.

5. **Subjective listening test methodology is underspecified.** Table 2 reports SMOS and CMOS with 95% confidence intervals, but the paper does not describe the listening test protocol (number of listeners, number of judgments per sample, comparison protocol, instructions given to listeners). This makes the subjective results difficult to evaluate or reproduce.

6. **Missing ablation of core architectural components in the main text.** Section 4.3 only ablates decoding strategies. The main paper does not ablate e.g., with vs. without the masked diffusion module, with vs. without the AR drafter, or effect of patch size. The paper references Appendix C and D for some of these, but they are central design choices that merit main-text discussion.

### Trivial

- Equation (1) factorizes over individual codes, but the actual inference procedure operates at the patch level with parallel masked diffusion. The paper acknowledges this ("inference realizes the autoregressive step at the patch level," line 63), but the formal presentation could mislead readers about the generative decomposition actually used.

## Nice-to-Haves

- Controlled re-evaluation of main baselines (especially DiTAR, F5TTS, E2TTS) in the same evaluation pipeline would convert the "state-of-the-art" claim from an assertion about other papers' numbers to a verified fact.
- Individual ablation of the three decoding heuristics (adding rows to Table 3 that toggle each trick independently) would substantially strengthen the contribution claim.
- An evaluation on longer utterances or varying lengths would test the claimed exposure bias mitigation.
- Runtime measurements (latency, RTF, FLOPs) comparing DiSTAR to DiTAR and other baselines would support the efficiency claims.

## Removed Points
These points are flagged to be removed; treat them with caution:
- **Missing confidence intervals for objective metrics** (from Critical Issue 4) — Removed because reporting WER/SIM/UTMOS as point estimates is standard practice in TTS system papers at this scale; requesting them is reasonable but not a standard expectation.
- **"Equation (1) mismatch" from Section-by-Section Notes** — Demoted to Trivial because the paper already acknowledges the gap between formal factorization and patch-level inference.

## Novel Insights
The harsh critic insightfully observes that the paper's strongest claim (WER improvement) and its weaker claims (naturalness, similarity) are packaged together in a way that exceeds what the objective evidence supports, and that this packaging may obscure the genuine but more modest contribution. The critic also correctly identifies that the architecture's coherence — cleanly separating cross-patch and intra-patch dependencies — is a real contribution that should be evaluated on its own terms rather than being oversold. These observations are useful for recalibrating the paper's framing.

## Suggestions

1. **Re-calibrate claims.** The abstract and introduction should state that DiSTAR achieves state-of-the-art WER (robustness/intelligibility) with competitive naturalness and speaker similarity — the claim of "surpasses in naturalness and speaker/style consistency" is not uniformly supported by objective metrics.
2. **Provide runtime numbers.** At minimum, compare wall-clock time or RTF between DiSTAR (NFE=24) and DiTAR (NFE=10) to substantiate the efficiency claim.
3. **Ablate decoding heuristics individually.** Add rows to Table 3 that toggle each of the three tricks independently.
4. **Acknowledge the limitation of uncontrolled baseline comparisons** explicitly in the paper, even if controlled re-evaluation is not feasible.
5. **Quantify the tail-first bias** with a figure or table showing confidence scores as a function of position within a patch.
6. **Describe the subjective listening test methodology** (number of listeners, protocol, number of judgments per sample).

## Score and Decision

MY FINAL SCORE: <score>7.5</score>
MY FINAL DECISION: <decision>Accept</decision>
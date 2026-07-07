## Summary

RisoTTo is a zero-shot non-autoregressive TTS model that introduces three components to close the gap with autoregressive systems: (1) Soft Alignment Generation (SAG), a flow-matching network trained to transform hard (duration-based) alignments into soft, attention-like alignment matrices without requiring mel-spectrograms at inference; (2) an Invertible Encoder based on normalizing flow that disentangles residual acoustic information from the context vector and maps it toward a Gaussian prior; and (3) Prompt-Aware Lightweight Convolution (PAL), which dynamically shapes convolution kernel weights using the speech prompt embedding. The resulting model achieves competitive MOS/WER/SECS scores against much larger autoregressive and non-autoregressive baselines while being ~7× faster and ~10× smaller than the best competitor.

---

## Strengths

- **Strong efficiency-quality tradeoff.** At 33M parameters and 0.89s latency for 10-second synthesis, RisoTTo is dramatically more efficient than every compared system (next-best: F5-TTS at 336M params, 4.24s), while achieving MOS within 0.04 of MaskGCT (1048M params) on VCTK. This is a concrete and practically meaningful result.
- **Principled motivation and ablation for SAG.** The flow-matching formulation—learning a vector field from hard alignment *A*_hard to soft alignment *A*_log—is theoretically clean and directly addresses the identified weakness of NAR models. Table 1 shows SAG outperforms both hard and Gaussian upsampling on all three metrics, with the upper-bound "Attention" oracle confirming the direction is correct.
- **IE vs. VAE comparison is informative.** The MMD analysis in Table 2 concretely demonstrates that the invertible encoder achieves better disentanglement of residual *z* from *c*_s while keeping *z* closer to the Gaussian prior, addressing the posterior-collapse limitation of VAEs. The LJSpeech ablation (Table 3) shows IE adds 0.26 MOS over vanilla NAR vs. VAE's 0.13, supporting the claim.
- **Ablation study covers all proposed modules.** Table 5 quantifies each component's contribution, showing SAG drives MOS, PAL drives SECS, and IE drives WER—giving a coherent account of each module's role.

---

## Weaknesses

### Fatal
None.

### Major

- **Evaluation uses NISQA-MOS (automatic), not human MOS.** The paper presents "MOS(CI)" scores including confidence intervals, which typically implies human evaluation. The methodology section clarifies NISQA-MOS is used "instead of human evaluation," but Table 4 is titled and formatted in a way that might mislead readers into thinking these are human scores. NISQA-MOS is known to correlate poorly with human judgments in cross-system comparisons, especially when comparing models with different acoustic characteristics (codec-based vs. mel-based). The absence of human evaluation weakens the central competitiveness claim.
- **Asterisked baselines evaluated from official demo pages.** VALL-E, T5-TTS, and NaturalSpeech2 results come from cherry-picked demo samples that authors typically select to showcase their best outputs. Comparing against these rather than a fair held-out evaluation significantly inflates those baselines (artificially making RisoTTo look comparably good or better), and conversely may understate RisoTTo's advantage over reproducibly run models.

### Minor

- **IE ablation shows counterintuitive SECS result.** In Table 5, removing IE actually *improves* SECS (0.681 vs. 0.668 with IE). The paper does not address this. If IE worsens speaker similarity while improving WER, there may be a trade-off that complicates the overall narrative about IE's benefit.
- **Evaluation scale is small.** The main comparison (Table 4) uses 60 samples on VCTK and 180 on Seed-TTS. Confidence intervals are reported, but the sample count is modest for a claim of "comparable to autoregressive models."
- **SAG computational overhead not reported.** SAG uses a Conv2D-UNet on *N × T*-dimensional attention matrices (phoneme × frame). For long utterances this could be a significant memory and compute cost. The paper reports end-to-end latency but does not break down SAG's contribution.

### Trivial

- The claim that T5 refers to a TTS model (Neekara et al., 2024) rather than the original T5 (Raffel et al.) is confusing given both are cited in the intro section.

---

## Nice-to-Haves

- A human listening study, even at small scale, would substantially strengthen the core claim.
- Reporting RTF (real-time factor) alongside absolute latency would make the efficiency comparison cleaner.
- An analysis of SAG's memory footprint vs. utterance length would help practitioners assess scalability.

---

## Novel Insights

The key insight—that a flow-matching model can be trained to hallucinate the soft alignment matrix a running AR attention mechanism would have produced, using only the text representation and a hard-alignment prior—is a genuinely useful reframing of the NAR upsampling problem. Rather than trying to replace attention with a fixed upsampling heuristic, SAG learns the distribution of alignment patterns conditioned on text, effectively giving NAR decoders an "expected attention" vector. Combined with the normalizing-flow disentanglement of residual acoustics, the paper offers a coherent decomposition of what AR models do (context enrichment via attention + acoustic memory via autoregression) and how to approximate both in a parallel decode. The efficiency gains are not merely from shrinking the model but from architectural decisions that avoid codec-level token generation and heavy diffusion stacks.

---

## Suggestions

- Report a human MOS study, even on a subset (e.g., 30 prompts × 6 models), to validate that NISQA-MOS rankings hold under human judgment.
- Provide a breakdown of where the 0.89s latency is spent (text encoder, SAG flow steps, mel decoder, PostNet) to allow readers to identify the bottleneck.
- Discuss and ablate the temperature of the Gaussian prior sampling for IE at inference time—this hyperparameter likely controls the acoustic expressiveness vs. stability tradeoff.

---

## Score and Decision

The paper addresses a real and important gap (efficiency of NAR zero-shot TTS), proposes technically sound and well-ablated solutions, and demonstrates strong efficiency gains. The main concerns are the reliance on automatic MOS and the unfair demo-page comparison, which prevent fully trusting the competitive performance claims. These are methodological issues rather than fatal flaws. The contribution is meaningful and the system appears practically useful.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Accept</decision>
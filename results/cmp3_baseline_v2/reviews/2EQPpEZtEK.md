## Summary
DiSTAR is a zero-shot text-to-speech framework that couples an autoregressive language model (for drafting block-level RVQ code patches) with a masked diffusion model (for parallel infilling within each patch), operating entirely in the discrete residual vector quantization (RVQ) code space. The design avoids explicit duration predictors, enables blockwise parallelism, and supports controllable inference via RVQ layer pruning. Experiments on LibriSpeech-PC and SeedTTS test-en show that DiSTAR achieves competitive or state-of-the-art word error rates, speaker similarity, and naturalness with moderate model sizes.

## Strengths
- **Novel architecture within a discrete code space.**  The tight coupling of an AR drafter and a masked diffusion model over the same RVQ code stream is a clean and well-motivated design.  It sidesteps optimization issues of continuous diffusion while retaining patch-level parallelism and the robustness of discrete LM training.
- **Strong empirical results on WER and subjective quality.**  DiSTAR-medium achieves the lowest WER on both benchmarks (1.66% on LibriSpeech-PC; 1.32% on SeedTTS test-en) and the highest CMOS in listening tests, demonstrating tangible gains in robustness and naturalness.
- **Practical inference controllability.**  The ability to prune upper RVQ layers at test time (without retraining) to trade bitrate/compute for quality is a useful property for deployment under varying resource constraints.
- **Thorough ablation of decoding strategies.**  The paper identifies a “tail-first” bias in masked diffusion and proposes three simple corrective heuristics (layer-wise temperature, position-wise temperature, hybrid greedy/sample) that are clearly explained and shown to improve stability.

## Weaknesses
### Fatal
None.

### Major
1. **Unfair comparison to DiTAR.**  DiTAR results are taken from its original paper (Table 1, marked ♦) rather than reproduced under identical training data (Emilia English subset) and compute.  DiTAR’s original training data may differ, making a direct comparison unreliable and the claimed “SOTA” partially unsubstantiated.  The authors should at minimum report DiTAR trained on the same Emilia subset or demonstrate that Emilia-subset differences are negligible.
2. **Limited ablation of architectural components.**  The ablation study only covers decoding strategies.  Critical design choices—overlapping vs. non-overlapping patches, stride size, aggregator architecture, the effect of stochastic layer truncation during training, and the inclusion/exclusion of the AR drafter—are not systematically ablated.  Without these, the contribution of individual components to the final performance remains unclear.
3. **Subjective improvements are modest and lack statistical significance.**  In Table 2, DiSTAR’s SMOS (3.31±0.25) overlaps with E2TTS (3.29±0.19) within one standard deviation.  No significance test (e.g., bootstrap or paired t-test) is reported, weakening the claim of superior speaker similarity.
4. **Incomplete baseline coverage in the objective table.**  Systems such as CosyVoice 2 and FireRedTTS appear only in the subjective table despite having reported objective metrics; their omission from Table 1 makes the objective comparison less comprehensive.

### Minor
- The paper claims “state-of-the-art robustness, speaker similarity, and naturalness,” yet DiSTAR does not achieve the best SIM on either benchmark (E2TTS scores 0.70/0.71 on LibriSpeech/SeedTTS vs. DiSTAR-medium’s 0.67/0.66).  The superiority claim should be qualified to emphasize WER (robustness) as the primary strength.
- The “tail-first” bias explanation (later positions in a patch are overconfident) is plausible but not empirically validated (e.g., by analyzing confidence histograms or showing that the bias disappears when training order is perturbed).
- Inference steps (NFE=24) are higher than DiTAR (NFE=10) but this is not discussed in the efficiency analysis; the paper should compare real-time factor or total FLOPs to provide an honest compute comparison.
- Figure 1 caption is duplicated verbatim in the text, which is a minor formatting issue.

### Trivial
None.

## Nice-to-Haves
- Ablate the effect of overlapping versus non-overlapping patches, and report how the choice of stride \(\leq\) patch-size affects boundary smoothness.
- Include a controlled experiment where DiTAR is retrained on the same Emilia English subset to enable a fair head-to-head comparison.
- Provide per-utterance WER breakdown (e.g., short vs. long utterances) to better understand the robustness profile.
- Release code or a demo to strengthen reproducibility.

## Novel Insights
Beyond the paper’s own architectural contribution, the observation of a “tail-first” confidence bias in parallel decoding of discrete speech tokens and the three lightweight correcting heuristics (layer-wise and position-wise temperature shaping, hybrid greedy/sample schedule) are a useful practical insight for future work on masked diffusion for structured sequence generation.

## Suggestions
1. Retrain one or two core baselines (especially DiTAR) on the same Emilia English subset to enable a fair, apples-to-apples comparison.
2. Expand the ablation study to cover patch overlap, stride size, the aggregator design, and the stochastic layer truncation strategy.
3. Report confidence intervals and statistical significance tests for subjective metrics (SMOS, CMOS).
4. Include a more complete compute-efficiency comparison (total inference FLOPs or real-time factor) to contextualize the higher NFE of DiSTAR.

## Score and Decision
Score: 6.5  
Decision: Borderline Accept

The paper presents a novel and well-motivated architecture for zero-shot TTS that operates entirely in the discrete RVQ space, with solid empirical gains in WER and subjective naturalness. The major weaknesses—the unfair DiTAR comparison and limited ablations—weigh against a higher score but do not invalidate the core contribution. With reasonable revisions, the paper would be suitable for acceptance.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>
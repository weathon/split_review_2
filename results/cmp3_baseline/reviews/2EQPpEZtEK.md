## Summary

DiSTAR introduces a zero-shot text-to-speech framework that operates entirely in the discrete RVQ code space, coupling an autoregressive language model (for drafting block-level tokens) with a masked diffusion transformer (for parallel infilling within each patch). The system achieves patch-level parallelism, avoids explicit duration predictors, and supports controllable inference through RVQ layer pruning and diverse decoding strategies. Experiments show state-of-the-art or competitive results on LibriSpeech-PC and SeedTTS benchmarks in terms of WER, speaker similarity, and naturalness.

## Strengths

- **Novel and well-motivated architecture**: The combination of AR drafting with masked diffusion entirely in the discrete RVQ space is a principled approach that addresses known weaknesses of both pure AR models (exposure bias, long-range drift) and continuous diffusion models (optimization instability, sensitivity to domain shift). The patch-wise factorization with overlapping windows is a clean design.

- **Strong empirical results**: DiSTAR-medium (0.3B) achieves the best WER on both LibriSpeech-PC (1.66%) and SeedTTS test-en (1.32%), outperforming strong baselines including F5TTS, E2TTS, and DiTAR. The subjective CMOS (0.22) and SMOS (3.31) results are also competitive, with DiSTAR leading on both metrics.

- **Practical controllability**: The ability to prune RVQ layers at inference time for variable bitrate/compute without retraining is a valuable practical contribution. The analysis in Figure 2 clearly demonstrates the trade-off between speaker similarity and computational cost.

- **Well-designed inference heuristics**: The identification of the "tail-first" bias in masked diffusion decoding and the proposed mitigation strategies (layer-wise temperature shaping, position-wise temperature shaping, hybrid sampling) are thoughtful and empirically validated.

## Weaknesses

### Major

- **Incomplete comparison with DiTAR**: DiSTAR is explicitly positioned as a discrete-space alternative to DiTAR (continuous next-patch diffusion), yet the comparison is limited. DiTAR results are reported with NFE=10 while DiSTAR uses NFE=24, making the efficiency comparison unclear. The paper claims "inference cost close to its continuous counterpart DiTAR" but does not provide wall-clock time, FLOPs, or latency comparisons. Given that DiSTAR uses 2.4x the NFE, a fair comparison requires either matching NFE or reporting actual runtime.

- **Limited ablation on key design choices**: The ablation study (Table 3) only varies decoding strategies. Critical ablations are missing: (1) the contribution of the masked diffusion module vs. a pure AR baseline, (2) the effect of overlapping vs. non-overlapping patches, (3) the impact of stochastic layer truncation during training, and (4) the importance of the aggregator design. Without these, it's difficult to attribute performance gains to specific components.

- **Missing details on training data and protocol**: The paper states training on the English subset of Emilia (~50k hours) but does not specify the exact training/test split, data preprocessing, or whether the evaluation datasets overlap with training data. Given that Emilia is an in-the-wild corpus, potential contamination with LibriSpeech or Common Voice (used in SeedTTS) should be addressed.

### Minor

- **The "tail-first" bias explanation is speculative**: The paper attributes the bias to "non-autoregressive training makes later positions easier" but provides no analysis or experiment to support this claim. A simple diagnostic (e.g., measuring per-position confidence during early decoding steps) would strengthen the argument.

- **CFG implementation details are unclear**: The paper states CFG is applied "only to the historical code with a guidance scale of 1.25 and a rescale factor of 0.75" but does not explain why this specific configuration was chosen or how it compares to applying CFG to both the AR conditioning and historical codes.

- **Reproducibility concerns**: While the paper provides architectural details, key hyperparameters (learning rate, batch size, training steps, warmup schedule) are relegated to the appendix which is not available in the main text. The codec (0.3B parameters, 9 RVQ layers, codebook size 65,536) is described but not publicly released.

### Trivial

- The paper uses "DiTAR" as a baseline but the citation (Jia et al., 2025) appears to be a preprint; the relationship between DiSTAR and DiTAR could be more clearly distinguished.

## Nice-to-Haves

- A comparison with DiSTAR using the same NFE as DiTAR (NFE=10) would clarify whether the discrete approach offers efficiency advantages or if the quality gains come primarily from more diffusion steps.
- An analysis of the computational cost breakdown between the AR LM and the masked diffusion module would help practitioners understand where the compute is spent.
- A discussion of failure cases or limitations (e.g., handling of non-English languages, very long-form synthesis, or extreme speaker variation) would strengthen the paper.

## Novel Insights

Beyond the paper's own contributions, the key insight is that discrete RVQ code spaces can serve as a unified representation for both AR drafting and masked diffusion, avoiding the modality mismatch that plagues cascaded continuous-discrete pipelines. The observation that upper RVQ layers encode primarily acoustic detail (rather than linguistic content) is consistent with prior work but is leveraged here for practical bitrate control. The "tail-first" bias in masked diffusion decoding for temporally structured sequences is a phenomenon that may generalize beyond speech to other sequential generation tasks.

## Suggestions

- Provide a direct comparison with DiTAR under matched NFE (e.g., both at NFE=10 or NFE=24) and report wall-clock time or FLOPs for a fair efficiency comparison.
- Add ablations for the core architectural components: (1) remove the masked diffusion module and use pure AR, (2) remove the AR drafter and use pure masked diffusion, (3) use non-overlapping patches (stride = patch size).
- Clarify the training/evaluation data split and address potential data contamination concerns.
- Provide a brief diagnostic analysis of the "tail-first" bias to support the proposed explanation.

## Score and Decision

The paper presents a well-motivated and novel architecture for zero-shot TTS, with strong empirical results across multiple benchmarks. The main weaknesses are the incomplete comparison with the most relevant baseline (DiTAR) under matched conditions and the limited ablation study. However, these issues are addressable and do not invalidate the core contribution. The paper makes a clear advance over existing methods and provides practical controllability features.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>
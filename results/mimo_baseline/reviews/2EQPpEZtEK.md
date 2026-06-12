## Summary
DiSTAR is a zero-shot text-to-speech framework that operates entirely in discrete RVQ code space, coupling an autoregressive Transformer (for block-level drafting) with a masked diffusion Transformer (for parallel intra-patch infilling). The key contribution is demonstrating that this AR-diffusion hybrid in discrete space achieves state-of-the-art robustness and speaker similarity while enabling practical inference-time controls such as variable bitrate via RVQ layer pruning and diverse decoding strategies—all without requiring a duration predictor or forced alignment.

## Strengths
- **Novel and well-motivated architecture**: The combination of AR drafting with LLaDA-style masked diffusion infilling entirely in discrete RVQ space is a genuinely novel design point. Unlike DiTAR (continuous diffusion), DiSTAR avoids high-dimensional continuous optimization difficulties while retaining patch-level parallelism. The discrete formulation naturally provides EOS-based termination, explicit decoding control, and interpretable training via cross-entropy loss.
- **Strong empirical results with efficient parameter usage**: DiSTAR-medium (0.3B) achieves the lowest WER on both LibriSpeech-PC (1.66%) and SeedTTS (1.32%), surpassing systems with 2× more parameters (DiTAR at 0.6B). Subjective evaluations (Table 2) confirm the lead on SMOS (3.31) and CMOS (0.22). DiSTAR-base at only 0.15B is already competitive with 0.3B baselines, suggesting a healthy scaling trajectory.
- **Practical controllability with empirical validation**: The paper demonstrates multiple useful inference-time controls—variable bitrate via RVQ layer pruning (Figure 2 shows smooth quality degradation), diversity-determinism trade-offs through greedy vs. sampling (Table 3), and layer-wise/position-wise temperature shaping to address the identified tail-first bias. These are not just claims but are systematically evaluated.
- **Careful empirical analysis of decoding artifacts**: The identification of the "tail-first bias" (later positions in a patch being overconfident due to non-autoregressive training on temporally dependent sequences) and the corresponding mitigation strategies (layer-wise and position-wise temperature shaping, hybrid sampling) show genuine engineering insight.

## Weaknesses
### Fatal
None.

### Major
- **Missing computational cost analysis**: The paper claims "inference cost close to its continuous counterpart DiTAR" and "comparable or lower computational cost," but provides no FLOPs, latency, or wall-clock time comparisons. DiSTAR uses NFE=24 while DiTAR uses NFE=10—a 2.4× difference in function evaluations. Without concrete cost numbers, the efficiency claims are unsubstantiated, which is significant for a paper that positions practical deployment as a key advantage.
- **No diversity metrics**: The paper claims "maintaining rich output diversity" but provides no quantitative diversity measures (e.g., multi-sample embedding distances, feature diversity scores). The only evidence is qualitative (demo page) and the temperature ablation in Table 3, which only shows WER/SIM trade-offs rather than diversity itself.

### Minor
- **Thin ablation study**: Key design choices—the aggregator architecture, the embedding initialization strategy (transplanting 16 channels from RVQ codebooks), and stochastic layer truncation—are not individually ablated. Understanding the contribution of each component would strengthen the paper significantly.
- **English-only evaluation**: Despite training on Emilia (a multilingual dataset), all evaluations are English-only. This limits the generalizability of the claims.
- **Comparison fairness**: DiTAR is compared at NFE=10 while DiSTAR uses NFE=24. While the paper's primary claims center on quality rather than speed, a matched-NFE comparison or at least a discussion of the NFE-quality trade-off would be informative.

### Trivial
- The demo page link appears to be missing (likely a parser artifact).

## Nice-to-Haves
- A latency/FLOPs comparison table across systems at matched quality levels
- A diversity metric (e.g., average pairwise distance of generated samples for the same prompt)
- Individual ablations for embedding initialization and stochastic layer truncation
- Multilingual evaluation leveraging Emilia's multilingual nature

## Novel Insights
The paper's most genuinely novel observation is that the AR-diffusion hybrid can be effectively realized entirely in discrete RVQ space, avoiding the optimization fragilities of continuous diffusion while preserving parallelism. The identification of the "tail-first bias" in non-autoregressive decoding of temporally ordered sequences—and the insight that this arises because later positions have more preceding context to condition on, making them systematically easier and thus overconfident—is a useful contribution to the broader masked diffusion literature beyond TTS. The demonstration that stochastic layer truncation during training enables test-time bitrate/compute control without retraining is a practical insight with deployment value.

## Suggestions
- Add a computational cost comparison table (FLOPs, latency, real-time factor) with baselines, especially DiTAR at matched and different NFE settings.
- Include at least one diversity metric to substantiate the diversity claims.
- Provide individual ablations for the embedding initialization transplant strategy and stochastic layer truncation.
- Consider adding a multilingual evaluation subset to demonstrate broader applicability.

## Score and Decision
DiSTAR presents a novel, well-motivated architecture with strong empirical results and practical deployment features. The core technical contribution—AR + masked diffusion in discrete RVQ space—is genuine and the results are compelling. The main weaknesses (missing cost analysis, no diversity metrics) are addressable and do not invalidate the core claims about quality and robustness. The paper would benefit from more thorough ablations and efficiency analysis, but the demonstrated quality improvements and the novel architectural design point represent a meaningful contribution to the TTS community.

MY FINAL SCORE: 6.5
MY FINAL DECISION: Accept
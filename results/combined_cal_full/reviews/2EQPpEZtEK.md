Now let me synthesize everything into the final review.

## Summary

DiSTAR introduces a zero-shot TTS architecture that couples an autoregressive AR drafter with masked diffusion, operating entirely in a discrete RVQ code space. The AR module produces a coarse hidden sketch for each patch (handling long-range temporal planning), while a masked diffusion Transformer fills in intra-patch multi-codebook details in parallel. The paper also contributes test-time RVQ layer pruning for quality-compute trade-offs and heuristic mitigations for a "tail-first" decoding bias.

## Strengths

1. **Genuinely novel architecture (Section 3).** Coupling an AR drafter with masked diffusion entirely within a discrete RVQ code space — using the AR module to produce a coarse hidden sketch and the masked diffusion module to fill in intra-patch details — cleanly separates long-range temporal planning from fine-grained multi-codebook resolution. Prior work either operates in continuous space (DiTAR, F5TTS) or uses single-codebook discrete tokens (VALL-E).

2. **Test-time RVQ layer pruning without retraining (Section 3.4, Figure 2).** The stochastic layer truncation during training, followed by simple pruning of upper RVQ layers at inference, provides a practical quality-compute trade-off. The mechanism is well-motivated by the observation that upper RVQ layers encode acoustic detail rather than linguistic content.

3. **Identification and mitigation of tail-first bias (Section 3.4).** The observation that non-autoregressive decoding over-prioritizes later positions in a patch is technically insightful. The three proposed heuristics (layer-wise temperature shaping, position-wise temperature shaping, hybrid sampling) are lightweight and sensible.

4. **Strong WER results (Table 1).** DiSTAR-medium achieves a WER of 1.66% on LibriSpeech-PC and 1.32% on SeedTTS test-en — the best among all compared systems on both benchmarks, with a meaningful margin on LibriSpeech (1.66 vs F5TTS's 2.02). This indicates genuinely strong robustness and intelligibility.

5. **Subjective evaluation leadership (Table 2).** DiSTAR achieves the highest SMOS (3.31) and CMOS (0.22) in subjective listening tests, outperforming E2TTS, F5TTS, CosyVoice 2, and FireRedTTS. This strengthens the speaker similarity and naturalness case via human perception.

## Weaknesses

### Fatal
None.

### Major

1. **Claim-evidence mismatch on "state-of-the-art" across all dimensions (Abstract, line 9; Contributions, line 37; Conclusion, line 263).** The paper repeatedly claims SOTA robustness, speaker similarity, and naturalness. Table 1 shows that while WER (robustness) is genuinely SOTA, speaker similarity (SIM) is not — E2TTS achieves 0.70 vs DiSTAR-medium's 0.67 on LibriSpeech and 0.71 vs 0.66 on SeedTTS. UTMOS (naturalness proxy) is also not consistently best: IndexTTS (4.35) beats DiSTAR-medium (4.27) on LibriSpeech, and DiTAR (4.15) beats DiSTAR-medium (4.05) on SeedTTS. Furthermore, the paper states DiSTAR "yields SIM on par with the best alternatives" (line 209), which understates the gap: E2TTS's SIM leads by 0.03–0.05, a meaningful margin in speaker similarity. The paper would be substantially stronger if it accurately characterized its results as "state-of-the-art robustness with competitive speaker similarity and naturalness."

2. **Thin ablation study for core architectural claims (Section 4.3).** The only ablation in the main paper compares three decoding strategies (Table 3). For a new-method paper whose central thesis is that operating in discrete RVQ space with a two-stage AR+masked-diffusion design is superior, there is no ablation that: (a) isolates the contribution of discrete masked diffusion by comparing against a continuous diffusion head, (b) ablates the AR drafter by running the masked diffusion from scratch, or (c) replaces masked diffusion with a simpler parallel decoder. The paper references additional ablations in the appendix (patch size, CFG settings), but the main paper lacks controlled experiments that directly test its core architectural hypotheses.

### Minor

3. **Uncontrolled comparison with DiTAR (Table 1, line 31).** DiTAR results (marked ♦) are taken from the DiTAR paper, trained on different data with a different codec/representation. This conflates architecture quality with codec quality. Additionally, the paper claims inference cost is "close to its continuous counterpart DiTAR" (line 31), but DiSTAR uses 24 NFE vs DiTAR's 10 NFE. Without wall-clock timing or FLOPs data — which would account for different per-step costs between masked discrete diffusion and continuous ODE-based diffusion — this claim is unverifiable.

4. **No individual ablation of the three decoding heuristics (Section 3.4, Table 3).** The heuristics (layer-wise temperature shaping, position-wise temperature shaping, hybrid sampling) are presented as contributions but only evaluated in combination. Their individual effects cannot be assessed, making it unclear which mechanism drives the improvement.

5. **Missing variance or significance reporting for objective metrics (Table 1).** WER, SIM, and UTMOS are reported as point estimates without standard deviations, confidence intervals, or significance tests. Given that some margins between systems are small, statistical significance is unclear.

6. **Unexplained non-monotonicity in RVQ layer pruning results (Figure 2).** WER increases from 1.88 at 6 layers to 2.04 at 8 layers. The paper states WER "reaches its minimum around six layers" but does not discuss or explain the degradation at 8 layers.

### Trivial

7. Hyperparameter values for CFG (guidance scale 1.25, rescale factor 0.75) and decoding (T_layer=0.8, T_time=0.95, top-k=50, top-p=0.9) are stated without justification or sensitivity analysis.

8. VALL-E 2 is discussed in related work but absent from both objective (Table 1) and subjective (Table 2) comparisons. While this is partially mitigated by the subjective table including other strong systems (CosyVoice 2, FireRedTTS), including VALL-E 2 would strengthen the comparison.

## Nice-to-Haves

- A direct discrete-vs-continuous ablation keeping the architecture identical but swapping the masked diffusion head for a continuous one would directly test the paper's central thesis about discrete-space advantages.
- An ablation removing the AR drafter (running masked diffusion from scratch, conditioned only on text and history) would isolate whether the two-stage design is beneficial.
- Wall-clock inference speed comparison with DiTAR would resolve the NFE count discrepancy.

## Removed Points

- **Criticism about "many rely on explicit duration predictors" framing (Introduction, line 21):** This is a general characterization of the continuous-latent literature, not a specific claim about compared baselines. The statement does not undermine the paper's contributions.
- **Criticism about different training datasets for baselines (Section 4.1):** Standard practice in TTS — papers often train on their own data. Not a specific weakness of this paper.
- **Generic suggestions (using standard codec like EnCodec, larger datasets):** Speculative improvements, not weaknesses.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Tone down SOTA claims to accurately reflect what Table 1 shows: state-of-the-art WER (robustness) with competitive speaker similarity and naturalness. The subjective results (SMOS, CMOS) can be highlighted separately as evidence of perceptual quality leadership.
2. Add a controlled ablation replacing discrete masked diffusion with a continuous diffusion head to directly test the discrete-space advantage thesis.
3. Add an ablation removing the AR drafter to isolate its contribution.
4. Report confidence intervals or significance tests for Table 1 metrics.
5. Include VALL-E 2 in the comparison tables for completeness.

## Score and Decision

**Calibration anchors used (in order of relevance):**

- **CLaM-TTS** (`ofzeypWosV.md`, avg score: 6.40, Round 1, itemized): Zero-shot TTS with RVQ and a probabilistic approach. Very similar topic; had analogous weaknesses about claim-evidence mismatch (weight -5.56) and missing side-by-side comparisons. DiSTAR has a more novel architecture and stronger WER results, but weaker ablation coverage. DiSTAR sits slightly below this anchor due to the thinner ablation.
- **HALL-E** (`868masI331.md`, avg score: 6.40, Round 1, itemized): Hierarchical codec LM for zero-shot TTS. Had missing baseline issues similar to DiSTAR (weight -7.04) but compensated with a new benchmark dataset and more thorough experiments. DiSTAR is comparably novel architecturally but less experimentally thorough.
- **MaskGCT** (`ExuBFYtCQU.md`, avg score: 5.25, Round 1, itemized): Masked generative codec transformer. Had major novelty concerns (weight -9.29) that dragged its score. DiSTAR's architecture is more novel, so it sits above this anchor.
- **Fox-TTS** (`pWdkM9NNCA.md`, avg score: 3.00, Round 1, itemized): Expressive zero-shot TTS that was rejected. Only compared against one baseline; very limited evaluation. DiSTAR is clearly stronger.
- **DiTTo-TTS** (`hQvX9MBowC.md`, avg score: 6.25, Round 1, not itemized): Diffusion Transformer TTS. Different architectural approach but similar evaluation paradigm. DiSTAR is broadly comparable.

**Round 1 bracket:** Between 5.0 and 6.5.

**Final score determination:** DiSTAR's weighted strengths (novel architecture +4.83, subjective leadership +4.58, strong WER +4.42) are genuinely strong. However, the claim-evidence mismatch (−4.03) is a substantive problem that requires revision, and the thin ablation (−1.85) weakens the experimental support for the paper's central thesis. Compared to CLaM-TTS (6.40), which had a similar claim-evidence weakness but stronger ablation and presentation, DiSTAR is slightly weaker on experimental rigor. Compared to MaskGCT (5.25), DiSTAR's architecture is more novel and its WER results are stronger. The paper's core contribution — a novel discrete two-stage architecture with SOTA WER — is real, but the overclaimed SOTA narrative and thin ablation prevent a higher score.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Accept</decision>
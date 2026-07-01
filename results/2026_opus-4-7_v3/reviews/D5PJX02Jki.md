Now let me verify specific claims more carefully by re-reading key sections:Now I have a thorough understanding of the paper. Let me draft the review.Now let me run Round 1 calibration — bracketing across score bands:Let me read some of the most topically relevant anchors to calibrate:Now I have enough calibration data. Let me form my bracket and write the final review.

**Round 1 Bracket:**
- Strong rejects (< 1.5): Clearly not — RoPE++ is a well-structured, original research paper.
- Score 2.5–3.0 range: Papers rejected for poor writing, limited experiments, unclear benefits. RoPE++ is substantially better.
- Score 5.0–5.25 range: RoPE modification papers with strong theory but limited practical evaluation. RoPE++ has broader evaluation but smaller models.
- Score 6.0–6.5 range: Accepted papers with novel RoPE insights + practical methods, sometimes at larger scale. RoPE++ is comparable in insight quality.
- Score 8.0: Differential Transformer — unanimously accepted with 3B scale, 350B tokens, comprehensive evaluation. RoPE++ is clearly below this.

**Initial bracket: 5.5 – 6.5**

Now let me write the final consolidated review.Now I have all the information needed. Let me write the final consolidated review.

---

## Summary
This paper proposes RoPE++, which re-incorporates the imaginary component of the complex-valued attention score that standard RoPE implementations discard. The key insight is that the imaginary part's characteristic curve (a sine integral) decays more slowly than the real part's (cosine integral), suggesting it preferentially captures long-range dependencies. The method requires only rotating query vectors by −π/2, enabling two configurations: RoPE++_EC (equal cache, doubled attention heads with a larger W_o) and RoPE++_EH (equal heads, halved KV cache/QKV parameters). Pre-training experiments at 376M and 776M scales show consistent improvements on long-context benchmarks (RULER, BABILong) while maintaining or improving short-context performance.

## Strengths
- **Novel mathematical observation with concrete mechanistic grounding.** The identification that the imaginary part of the RoPE complex product has a characteristic curve governed by the sine integral (Eq. 5), which decays more slowly than the cosine integral of the real part, is a specific, verifiable property. The derivation in Section 3.2 directly motivates why imaginary attention should capture longer dependencies, and Figure 1 provides visual confirmation. This is not hand-waving — it is a concrete mathematical property that the paper correctly derives and exploits.

- **Elegant and practically adoptable implementation.** Computing imaginary attention requires only rotating q_t by −π/2 (Eq. 4), while k_s remains unchanged. This allows full KV cache sharing and FlashAttention integration with no extra KV storage for the EC variant. The simplicity of the modification — a single rotation applied to existing queries — makes it plausible for real-world adoption.

- **Two well-motivated configurations with clear trade-offs.** RoPE++_EC targets quality at fixed cache cost; RoPE++_EH targets efficiency at comparable quality. The paper clearly articulates parameter and cache trade-offs (Section 3.3, Figure 2). Critically, RoPE++_EH achieves comparable or better results than standard RoPE despite having *halved* QKV parameters and KV cache (Tables 2, 3), which is a strong practical finding validated by wall-clock TPOT measurements (Figure 4).

- **Mechanistic length-extrapolation argument.** Section 3.4 identifies that certain q/k dimension pairs see only non-negative position embeddings during training in standard RoPE (because cos and sin are non-negative over the trained range for low-frequency dimensions). Imaginary attention exposes them to both signs, reducing OOD behavior at longer contexts. Figure 3 provides concrete visual support for this claim.

- **Creative diagnostic experiment.** The noise perturbation study (Section 5.2) adds Gaussian noise separately to real and imaginary attention components and measures degradation on RULER-4k. The 5–8 point gap at σ=1.0 provides meaningful evidence that imaginary heads disproportionately carry long-context information.

- **Broad compatibility.** Table 3 demonstrates that RoPE++ combines effectively with NTK, Linear PI, and YaRN context-extension techniques, with RoPE++_EC achieving the best average scores across all combinations at both model sizes.

## Weaknesses

### Fatal
None

### Major
- **Parameter confound in RoPE++_EC.** The paper acknowledges that "W_o in RoPE++_EC is double-sized" (Section 3.3). This means RoPE++_EC has meaningfully more parameters than standard RoPE in the output projection (~25% more total attention parameters). The paper's headline long-context improvements (Tables 2, 3) come primarily from RoPE++_EC, but no ablation isolates the imaginary mechanism from the increased output projection capacity. An obvious control — standard RoPE with doubled attention heads (random query initializations, shared KV cache) and the same doubled W_o — is absent. **Mitigating factor:** RoPE++_EH has *fewer* total parameters than standard RoPE yet achieves comparable or better results, providing partial evidence that the imaginary mechanism itself contributes. However, this does not fully resolve the confound for the EC variant's larger gains.

### Minor
- **Noise perturbation experiment lacks a magnitude control.** Section 5.2 adds Gaussian noise with "equal standard deviation" to real and imaginary attention separately, but does not report whether the magnitudes of these attention scores are comparable. If imaginary attention scores are systematically smaller, the same σ would corrupt them proportionally more, potentially explaining the performance gap without invoking functional importance. Reporting the score magnitude distributions would strengthen the interpretation.

- **Long-context baselines limited to RoPE only.** Tables 2 and 3 compare only RoPE, RoPE++_EH, and RoPE++_EC for long-context evaluation, while FoPE, Pythia, and ALiBi appear only in short-context evaluation (Table 1). Including at least ALiBi and FoPE in long-context comparisons would provide a more complete picture, though the paper's focus on RoPE as the dominant method is reasonable.

- **Short-context margins are narrow without significance measures.** In Table 1, the spread across six methods at 776M Short is 40.9–42.8 (less than 2 points). Single-run evaluation is standard practice for pre-training experiments at this scale, but confidence intervals or variance across seeds would strengthen the claims where margins are this tight.

### Trivial
None

## Nice-to-Haves
- **Rotation angle ablation.** The −π/2 rotation is mathematically determined (it exactly recovers the imaginary part of the complex product, Eq. 4), so it is not an arbitrary hyperparameter. However, testing other rotation angles empirically (e.g., −π/4, −π/3) would validate whether the theoretical properties of the imaginary component specifically — rather than generic query diversification — drive the gains. This would be a powerful confirmation of the theoretical narrative.

- **At least one main-text experiment at ≥1.5B scale.** The paper references larger-scale analysis in Appendix C. Position embedding behaviors can change qualitatively between sub-1B and multi-billion parameter regimes, and a main-text result would strengthen confidence in generalization.

- **Comparison with other KV-cache reduction methods** (e.g., GQA with fewer KV heads, MLA-style compression) to contextualize RoPE++_EH's efficiency trade-offs against alternative approaches to the same goal.

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- **"Irreversible information loss" framing is overstated (Section 1).** The reviewer argued this language is imprecise since the real part already encodes relative position through both cos and sin terms. Removed as a pure presentation/framing nitpick — the paper's core mathematical claims are correct regardless of how aggressively the introduction motivates them.

- **Theory doesn't address training dynamics (Section 3.2).** The reviewer noted that the characteristic curve analysis assumes the model will learn to use the slow-decay property. Removed because the theory correctly identifies the mathematical property, and the experiments (Tables 2, 3; Section 5.2) provide empirical evidence that the model does learn to exploit it — exactly the role experiments should play relative to theory.

- **Section 3.3 concern that parameter sharing limits model flexibility.** The paper explicitly explains why sharing is necessary — allocating distinct heads to imaginary and real attention would collapse back to standard RoPE (Section 3.3, line 103). This is a design constraint inherent to the method, not a weakness.

- **Experimental scale as a fatal/structural concern.** The paper references Appendix C for larger model analysis. Per review guidelines, criticism targeting stripped appendix content is not appropriate. Retained as a minor concern / nice-to-have for the main text only.

## Novel Insights
The paper's central novel insight is that the imaginary component of the complex-valued RoPE attention score — universally discarded by all existing implementations — has a qualitatively different positional characteristic (sine integral vs. cosine integral) that makes it naturally suited for long-range dependency modeling. The further insight that this can be recovered with a trivial rotation (−π/2 on queries, sharing the KV cache entirely) makes this both theoretically interesting and practically deployable. The length-extrapolation argument in Section 3.4 — that imaginary attention exposes position dimensions to both positive and negative embedding values during training, reducing OOD effects — provides a novel mechanistic explanation for improved extrapolation that goes beyond the typical frequency-manipulation approaches in the literature.

## Suggestions
- Add a parameter-controlled ablation for RoPE++_EC: train standard RoPE with doubled attention heads (using random query initializations and shared KV cache) and the same doubled W_o to isolate the imaginary mechanism's contribution from increased capacity.
- Report the magnitude distribution of imaginary vs. real attention scores to validate the noise perturbation experiment's interpretation.
- Include FoPE and ALiBi in long-context evaluations for completeness.
- Test rotation angles other than −π/2 to empirically confirm the theoretical specificity of the imaginary component.
- Consider adding at least one ≥1.5B experiment in the main text body for stronger generalization evidence.

## Score and Decision

**Calibration anchors (all from Round 1):**

| Paper | Path | Avg Score | Round | Comparison to RoPE++ |
|-------|------|-----------|-------|---------------------|
| Long-context Extrapolation via Periodic Extension | jp4pxKqCRW | 2.50 | R1 | Much weaker: poor writing, limited experiments, no clear contribution. RoPE++ is substantially better. |
| Efficient transformer with reinforced position embedding | 5dDYhvt6dY | 3.00 | R1 | Weaker: limited evaluation, unclear benefits. RoPE++ has cleaner theory and broader experiments. |
| Writing in the Margins | 56mg1JFd3n | 3.00 | R1 | Different topic (inference pattern). Less novel core idea than RoPE++. |
| IntelLLM (KV Cache Compression) | 4QWPCTLq20 | 3.00 | R1 | Different topic. RoPE++ has stronger theoretical grounding. |
| Mitigate Position Bias via Scaling | t717joHHSc | 4.75 | R1 | Similar domain but weaker theoretical contribution and presentation. RoPE++ is better. |
| Scaling Laws of RoPE-based Extrapolation | JO7k0SJ5V6 | 5.00 | R1 | Comparable theoretical depth, but evaluated mainly on perplexity. RoPE++ has broader evaluation but smaller models. |
| Wavelet-based Positional Representation | OhauMUNW8T | 5.25 | R1 | Similar level — another RoPE modification with wavelet framing. RoPE++ has a simpler, more elegant insight. |
| LOGO (Long-Context Alignment) | FSlfoBIctk | 5.25 | R1 | Different topic (alignment). Comparable overall quality. |
| Rethinking Addressing via TAPE | Us1RXG1Ji2 | 6.00 | R1 | Similar: novel PE modification with theoretical analysis. RoPE++ has more practical impact but smaller scale. |
| Round and Round We Go (RoPE Analysis) | GtvuNrk58a | 6.20 | R1 | RoPE analysis paper with insights but limited to one model. RoPE++ offers both analysis AND a practical method with pre-training. Comparable. |
| Why Does Effective Context Length Fall Short (STRING) | eoln5WgrPx | 6.50 | R1 | Simpler method but tested on much larger models (70B). RoPE++ has deeper theoretical contribution but smaller scale. Comparable. |
| LongLoRA | 6PmJoRfdaK | 7.00 | R1 | Larger scale, more practical impact. RoPE++ has more novel theory but less scale. RoPE++ is below this. |
| Retrieval Head Explains Long-Context | EytBpUGB1Z | 8.00 | R1 | Much more comprehensive analysis across many models. RoPE++ is below. |
| Differential Transformer | OvoCm1gGhN | 8.00 | R1 | Large-scale (3B, 350B tokens), comprehensive evaluation. RoPE++ is clearly below. |
| FlexPrefill | OfjIlbelrT | 8.00 | R1 | Large-scale, comprehensive systems contribution. RoPE++ is below. |

**Round 1 bracket: 5.5 – 6.5**

The paper sits above the 5.0–5.25 borderline-accept papers because it has (1) a more novel and cleaner core insight, (2) broader evaluation across both short and long context, and (3) practical efficiency results with RoPE++_EH. It sits below the 7.0+ papers because those demonstrate their ideas at larger scale with more comprehensive ablations. The closest comparisons are the 6.0–6.5 range papers (TAPE, STRING, "Round and Round We Go"), which share the combination of novel positional-encoding insights with practical methods but vary in scale.

The paper's genuinely novel mathematical insight, elegant implementation, and consistent experimental improvements push it toward the upper end of this bracket, but the parameter confound in EC (the headline variant) and the missing rotation-angle ablation keep it from reaching a clear accept. The RoPE++_EH results — achieving comparable performance with halved parameters — are a strong mitigating factor.

**Final score: 6.0**

The paper makes a genuinely novel contribution (re-incorporating the imaginary component of RoPE) with clean theory and practical implementation. The experimental validation, while consistent and reasonably broad, has addressable gaps (parameter-controlled ablation, magnitude control in noise experiments, limited scale in main text). The core idea is sound and could see practical adoption. This is a borderline accept — the novelty and elegance warrant publication, but the evidence does not yet fully match the ambition of the theoretical claims.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>
Now I have enough context to finalize my review and score. Let me compile everything.

**Calibration anchors retrieved:**

| Round | Path | Avg Score | Relevance |
|-------|------|-----------|-----------|
| 1 | E34AlVLN0v ("Parallelizing non-linear sequential models") | 6.0 (Accept) | Most directly comparable: parallelizing nonlinear RNNs; similar scope and limitations |
| 1 | GrmFFxGnOR ("Were RNNs All We Needed?") | 5.0 (Reject) | minLSTM/minGRU parallel RNNs; rejected due to limited scale + novelty concerns |
| 1 | l0ZzTvPfTw ("FlashRNN") | 6.5 (Accept) | Hardware-optimized RNN training; accepted but no accuracy comparisons |
| 1 | TvGPP8i18S ("MELODI") | 6.25 (Accept) | Memory compression for long contexts; accepted despite limited scale |
| 1 | OfjIlbelrT ("FlexPrefill") | 8.0 (Accept) | Efficient long-sequence inference; less related but higher-tier |
| 1 | GrmFFxGnOR reviewer 3 | 3 (individual) | RNN parallelization rejected for novelty + scale issues |
| 1 | UU9Icwbhin ("RetNet") | 4.75 (Reject) | Recurrent architecture; rejected despite theoretical appeal |
| 1 | JOBokGDcX0 ("Sequence Segmentation") | 2.5 (Reject) | Chunking; poorly evaluated |

**Round 1 bracket: 5.5–6.5**

The paper is most comparable to E34AlVLN0v (6.0, accepted — parallelizing nonlinear sequential models) and MELODI (6.25, accepted — memory compression). TNT has stronger quantitative results than E34AlVLN0v (17× speedup with quality improvement vs. 10× speedup on limited tasks), and more comprehensive evaluation than MELODI. However, the false abstract claim and parameter fairness gap are distinctive weaknesses that E34AlVLN0v doesn't have. FlashRNN (6.5) was accepted with similar caveats about limited evaluation.

The paper sits slightly below the MELODI tier (6.25) due to the abstract factual error and parameter fairness concerns, but above "Were RNNs All We Needed?" (5.0, rejected) which had weaker validation and similar scale issues.

**Final score: 6.0**

---

## Summary
The paper introduces TNT (Two-stage Non-linear Training), a training paradigm for deep memory modules that decouples training efficiency from inference performance through: (1) a hierarchical memory with global + local modules and periodic state resets enabling context parallelism, (2) Q-K projection to mitigate compression-retrieval domain mismatch, and (3) two-stage training with efficient large-chunk pre-training followed by brief small-chunk fine-tuning. Experiments on 150M-parameter Titans models demonstrate up to 17× training speedup with simultaneous quality improvements.

## Strengths
- **Impressive training speedup with quality gains (Tables 1–2)**: TNT achieves 17.37× faster time-to-quality than the best-quality Titans baseline (C=8), reducing training time from 19.48 to 1.12 hours while improving average perplexity from 25.07 to 23.13 and downstream accuracy from 39.0% to 41.0%. The speedup is measured against the best-quality baseline configuration, not a contrived slow one.
- **Well-structured ablation validates each component (Table 3)**: Removing global memory causes PPL to jump from 21.04 to 25.60 (+4.56); removing Q-K projection raises PPL from 21.04 to 22.01 (+0.97); Stage 2 fine-tuning further reduces PPL from 21.04 to 20.86. Each proposed mechanism is shown to be individually necessary.
- **Empirically demonstrated linear runtime scaling (Figure 4)**: TNT's runtime grows linearly with sequence length while Titans grows quadratically. At 32K sequence length, TNT (C_L=16) is 5.1× faster than comparable Titans (C=16), and TNT (C_L=128) is 1.3× faster than FlashAttention.
- **Elegant Q-K projection with constant overhead (Eq. 7)**: The projection matrix Σ(k_τk_τ^T/||k_τ||²) is maintained as a running d×d sum requiring no storage of past keys, with the ablation confirming its importance (−0.97 PPL).
- **Clean empirical evidence of chunk-size mismatch (Figure 2)**: A 550M Titans model pre-trained with C=64 achieves optimal PPL (13.78) only at inference C=64, degrading severely at both smaller (36.45 at C=8) and larger (22.4 at C=512) chunks — clearly motivating the two-stage paradigm.
- **Monotonic improvement with multi-resolution local memory (Table 2)**: Adding modules at progressively finer resolutions yields consistent PPL improvements: 24.10 → 23.80 → 23.44 → 23.13, cleanly validating the hierarchical design.

## Weaknesses

### Fatal
None

### Major
- **Abstract falsely claims evaluation on TTT models**: The abstract states "Evaluated on Titans and TTT models," but Section 5 explicitly says "While TNT is model-agnostic, we instantiate it with a strong deep memory model, Titans." TTT appears only as a baseline in Table 2, never as a model to which TNT is applied. Since the "model-agnostic" generality claim is a core selling point (repeated in the abstract, introduction, and contributions list), the lack of evidence for it and the factual inaccuracy in the abstract is a significant problem. The paper should either apply TNT to at least one other deep memory module (TTT, Atlas) or honestly scope the claims.

- **Parameter count fairness is unaddressed**: TNT introduces 1 global memory (V) plus up to 4 local memory modules (W_i), each with their own fast weight parameters, added on top of the base model. The paper states all models are "150M parameters" (Section 5.1, Table 2) but does not clarify whether this includes fast weights or only slow weights (θ). The baseline Titans also has fast weights, but TNT's hierarchy adds additional memory modules. The ablation in Table 3 shows removing global memory causes catastrophic degradation (25.60 vs 21.04 PPL), but this conflates the benefit of the training paradigm with the benefit of additional memory capacity. Without explicit parameter accounting, it is unclear how much of the quality improvement comes from TNT's methodology versus simply having more total memory.

- **Stage 2 improvements are marginal without variance estimates**: The best Stage 1 model (C_L={4,8,16,32}) achieves 23.13 avg PPL; the corresponding Stage 2 model achieves 23.09 — a 0.04 difference. For the simplest model (C_L={8}), the improvement is 24.10→23.99 (0.11). The paper itself acknowledges "at this scale, we consider perplexity a more stable metric for language modeling capability, as downstream task accuracy can be subject to higher variance" (Section 5.3), which raises the question of whether these small perplexity differences are themselves within noise.

### Minor
- **Scalability claims are overstated for 150M-only experiments**: The paper claims TNT "removes a critical scalability barrier" and "establishes a practical foundation" (abstract, conclusion), but all experiments are at 150M parameters on 10B tokens. The motivating Figure 2 experiment uses a 550M model, yet all TNT experiments never scale beyond 150M. The core contribution (decoupling training efficiency from inference quality) is well-validated at 150M, but the scalability framing is stronger than the evidence supports.

- **17× headline compared across different configurations**: The 17× headline compares TNT{64} against Titans C=8. The fairest same-chunksize comparison is TNT{8} vs Titans C=8, yielding 7.7× — still substantial. Both numbers appear in Table 1, so the paper is transparent, but the abstract leads with the more dramatic figure.

- **Additive combination of global and local memory (Eq. 7)**: Outputs are simply summed with no gating or learned weighting. The ablation confirms both components matter, but there is no analysis of what each memory encodes or whether the additive assumption holds generally.

- **Missing curriculum baseline**: The ablation tests each TNT component but doesn't compare against training Titans with decreasing chunk sizes in a curriculum (without the hierarchical memory). This would isolate whether the improvement comes from the hierarchical architecture or simply from the two-stage training idea.

## Nice-to-Haves
- Apply TNT to at least one additional deep memory module (TTT, Atlas) to substantiate the generality claim
- Report total parameter counts (slow + fast weights) for all models
- Report variance across runs for at least the main Table 2 results
- Run at least one experiment at 500M+ to validate scalability narrative
- Analyze failure modes at segment boundaries (information loss beyond S_L tokens)

## Removed Points
These points are flagged to be removed, treat them with caution:
- **"Novelty of periodic reset overstated"** from harsh critic: The paper frames the reset as enabling parallelism for *non-linear* recurrences (line 33), which is distinct from standard sharding approaches. This is a fair contribution.
- **"Challenge 2 motivation is weak"** from harsh critic: Table 3 validates empirically that removing Q-K projection causes +0.97 PPL, directly confirming the domain mismatch hypothesis.
- **"Q-K projection claim is imprecise"** from harsh critic: Minor precision issue in motivation text; the empirical result (Table 3) validates the mechanism regardless.
- **Strength Finder's claim that abstract's TTT mention is a strength**: This is actually a factual error — TNT was never applied to TTT.

## Novel Insights
The most novel empirical finding is the chunk-size mismatch result (Figure 2): a 550M Titans model pre-trained with C=64 achieves optimal performance only when evaluated at that same chunk size, contradicting the intuition that smaller inference chunks should always help. This reveals that deep memory modules over-specialize to their training chunk resolution, providing clear and non-obvious motivation for the two-stage training paradigm. Combined with the demonstrated ability to decouple training chunk size from inference chunk quality (17× speedup with quality gains), the paper makes a credible case for hierarchical memory as a promising direction for deep memory modules.

## Suggestions
- Fix the abstract: remove "and TTT models" or add a TNT+TTT instantiation experiment
- Add a parameter-budget-controlled experiment matching total fast-weight capacity
- Add variance estimates (even 3 seeds) for main Table 2 results
- Frame scalability claims more carefully given the 150M experimental scope
- Discuss what global vs. local memory each learn to encode (qualitative analysis)

## Score and Decision

**Calibration anchors:**
| Paper | Avg Score | Decision | Comparison |
|-------|-----------|----------|------------|
| E34AlVLN0v ("Parallelizing nonlinear sequential models") | 6.0 | Accept | Most comparable: parallelizing nonlinear RNNs, 10× speedup, limited scale |
| TvGPP8i18S ("MELODI") | 6.25 | Accept | Memory compression for long contexts, limited scale but cleaner evaluation |
| l0ZzTvPfTw ("FlashRNN") | 6.5 | Accept | Hardware-optimized RNN training, no accuracy comparisons |
| GrmFFxGnOR ("Were RNNs All We Needed?") | 5.0 | Reject | minLSTM/minGRU, rejected for limited scale + novelty concerns |
| GQGNLEHmdl ("AutoChunk") | 6.33 | Accept | Activation memory chunking, clean efficiency results |
| UU9Icwbhin ("RetNet") | 4.75 | Reject | Recurrent architecture, rejected despite theoretical appeal |

**Round 1 bracket: 5.5–6.5.**

TNT has stronger quantitative results than E34AlVLN0v (6.0) — 17× speedup with quality improvement on a practical architecture vs. 10× speedup on small tasks — but E34AlVLN0v doesn't have a false abstract claim or parameter fairness gap. TNT's evaluation is more comprehensive than MELODI (6.25) and FlashRNN (6.5), but those papers have cleaner claims without factual errors. The paper is clearly above "Were RNNs All We Needed?" (5.0) which was rejected for similar scale limitations but weaker validation.

The false abstract claim about TTT evaluation is a distinctive flaw that the otherwise-comparable 6.0–6.5 anchors don't share, pulling the score toward the lower end of this bracket.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Reject</decision>
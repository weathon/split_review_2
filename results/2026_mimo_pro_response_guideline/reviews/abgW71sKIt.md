Good. STBLLM (6.00) is a very close comparator — also a 1-bit/sub-1-bit LLM quantization method with scores 6, 5, 8, 5. This helps anchor my final score.

**Final bracket narrowing**: The paper under review has:
- A clearer analytical contribution than STBLLM (6.00)
- But a catastrophic failure on one configuration that STBLLM doesn't have
- Less foundational novelty than ARB-LLM (7.00)
- Comparable to OSTQuant (6.20) which also had missing ablations noted

I settle on **6.0** as my final score.

## Summary
This paper investigates why naive output alignment underperforms weight alignment in 1-bit post-training quantization of LLMs, identifying three empirical failure modes: layer-wise output matching not guaranteeing block-level improvement, error accumulation across layers degrading alignment targets, and attention mechanism disruption. Based on these findings, it proposes a method combining selective block-level output alignment (applying output alignment only to the last FC layer per transformer block), an Output Error objective that uses full-precision inputs as targets, and an Attention Matrix Preservation (AMP) masking mechanism.

## Strengths
- **Well-grounded preliminary analysis with concrete empirical evidence** (Sections 3.1–3.3): Figure 1 demonstrates across 223 layers of LLaMA-2-7B that ARB-X (output alignment) does not always reduce block-level loss compared to ARB (weight alignment). Figure 2 quantifies both MSE divergence and cosine similarity degradation of the output error across blocks, and shows token-similarity matrix drift — each motivating a specific method component.
- **Clean one-to-one mapping from analysis to method design**: Selective block-level alignment addresses finding (i), the Output Error objective addresses finding (ii), and AMP masking addresses finding (iii), giving the method a coherent and well-motivated narrative.
- **Ablation studies validate individual components**: Table 3 shows AMP reduces LLaMA-2-7B C4 perplexity from 29.12 to 19.25 (a ~10-point effect on LLaMA, minimal on OPT), confirming the architecture-dependent attention preservation claim. Table 4 confirms Output Error outperforms Activation-conditioned Error (19.25 vs 19.97 on LLaMA-2-7B C4).
- **Consistent improvements across model families and scales**: On OPT models (1.3B–30B, Table 1), the method beats ARB-RC at every scale on C4, WikiText2, and PTB, and on average QA accuracy. On LLaMA models (Table 2), improvements hold on C4 and WikiText2 for all three models tested.
- **Closed-form solutions with practical numerical stability**: Equations 5, 6, 8 provide closed-form updates for all three parameters, and the paper acknowledges numerical instability in the pseudoinverse and uses `torch.linalg.lstsq` as a practical fix (line 132).

## Weaknesses

### Fatal
None

### Major
- **Catastrophic LLaMA-2-7B/PTB result dismissed without diagnosis**: Table 2 (line 231) shows the method achieves perplexity **3166** on LLaMA-2-7B/PTB, compared to ARB-RC's 763.19 and ARB-X's 681.24 — a ~4× regression over the strongest baseline. The paper acknowledges this on line 175 but dismisses it on line 233 with "the large perplexity indicates that the metric cannot provide a meaningful evaluation." This is circular reasoning: the large perplexity *is* the failure, not a reason to dismiss it. Other methods achieve functional (if high) perplexities on this same configuration (ARB-RC: 763, ARB-X: 681). The paper provides no investigation of whether the AMP mask conflicts with the output error objective under PTB's data distribution, whether the selective layer strategy causes a specific interaction failure, or whether there is an instability unique to this model/dataset combination. This directly contradicts the central claim of "consistently outperforms existing 1-bit PTQ methods" (abstract, conclusion line 269).

- **Missing ablation on the selective layer strategy**: The key architectural decision — applying output alignment only to the last FC layer of each transformer block while using ARB-RC for all others (Section 4.2, line 161) — is never ablated. The ablation section (5.3) covers the Output Error objective (Table 4) and AMP (Table 3), but there is no comparison against applying output alignment to all layers, or to different subsets of layers. This is the paper's most important design choice, and without this ablation, the reader cannot determine whether the selective strategy is essential, incidental, or harmful in certain configurations. This gap is especially concerning given the unexplained PTB failure.

### Minor
- **Improvements over the strongest baseline (ARB-RC) are modest**: The dramatic headline gains come from comparison with ARB-X, which the paper's own analysis (Section 3) establishes as flawed. Over ARB-RC, gains are ~0.2–3.0 perplexity points on OPT models and ~0.2–1.2 on LLaMA models (excluding the PTB failure). QA accuracy gains are 0.05–0.78%. The contribution is real but incremental relative to the strongest competitive baseline. The framing of "consistent outperformance" is technically accurate but masks this incremental nature.

- **Architecture-dependent AMP sensitivity is interesting but underexplored**: Table 3 shows AMP has negligible effect on OPT-6.7B (~0.13 perplexity difference on C4) but a massive effect on LLaMA-2-7B (~10 points). The paper hypothesizes this is due to RMSNorm vs. LayerNorm (line 263), but provides no direct experimental evidence for this claim.

### Trivial
None

## Nice-to-Haves
- A brief overhead comparison (calibration time vs. ARB-RC and ARB-X) in the main text would strengthen the "minimal overhead" claim in the abstract.
- Testing on newer architectures (Mistral, Qwen, Gemma) would broaden applicability claims.

## Removed Points
These points are flagged to be removed, treat them with caution:
- **Equation 2 typo (line 94)**: $\|\hat{X}\hat{W} - \hat{X}\hat{W}\|_F^2$ is identically zero; the trace expression that follows confirms it should be $\|\hat{X}W - \hat{X}\hat{W}\|_F^2$. Flagged as a potential parser artifact per review instructions. If genuine in the original, it affects a key motivating equation.
- Harsh critic's concern about the computational cost of computing the M matrix in AMP — speculative about unmeasured overhead; subsumed by the nice-to-have about overhead reporting.
- Harsh critic's concern about weight bit count discrepancy (1.11 OPT vs 1.06 LLaMA) — fair within each model family since all methods use the same bit count; cross-family comparison is not the main claim.

## Novel Insights
The paper's most genuinely novel contribution is the systematic empirical diagnosis of three distinct failure modes of naive output alignment in 1-bit LLM quantization (Sections 3.1–3.3). The observation that token-similarity matrices — which serve as proxies for attention patterns — degrade progressively under output alignment (Figure 2, bottom panel) is a particularly useful insight that connects quantization error to attention mechanism disruption. The AMP mechanism, which uses the sign of the gradient of the attention-preservation objective as a selective parameter mask, is a novel technique with a large empirical effect on LLaMA architectures (~10-point perplexity improvement).

## Suggestions
- Diagnose the LLaMA-2-7B/PTB failure by investigating whether AMP and the output error objective interact adversely under PTB's data distribution, or whether the selective layer strategy causes a specific failure mode.
- Add an ablation comparing: (a) output alignment on all layers, (b) only the last FC layer (current method), (c) last two layers, and (d) weight alignment on all layers (ARB-RC baseline).
- Investigate the AMP architecture dependence more rigorously — e.g., test the RMSNorm hypothesis by replacing it with LayerNorm in LLaMA-2-7B.
- Report calibration time overhead vs. baselines in the main text.

## Calibration Anchors

| Anchor Paper | Avg Human Score | Round | Comparison |
|---|---|---|---|
| ARB-LLM (ZU8OdDLTts) | 7.00 | 1 | Key baseline this paper builds on; more foundational contribution |
| PB-LLM (BifeBRhikU) | 6.75 | 1 | 1-bit LLM quantization baseline; novel partially-binarized approach |
| Compressing LLMs/KICK (B9klVS7Ddk) | 6.75 | 1 | Evaluation paper; complementary contribution |
| OmniQuant (8Wuvhh0LYW) | 6.40 | 1 | Accepted PTQ method with omnidirectional calibration |
| OSTQuant (rAcgDBdKnP) | 6.20 | 1 | PTQ method with novel metric; also had missing ablation noted |
| BitStack (lBntjGbyv0) | 6.50 | 2 | Training-free weight compression for variable memory |
| STBLLM (6XUSDvBFkV) | 6.00 | 2 | Most comparable: sub-1-bit binarization for LLMs, scores 6/5/8/5 |
| LLM-QAT (mDBsBB1enO) | 5.00 | 1 | Rejected QAT method for LLMs |
| FPTQ (ykhRO1mAg3) | 4.00 | 1 | Rejected W4A8 PTQ method |
| One QuantLLM (RdG7LVGnQi) | 4.50 | 1 | Rejected once-for-all quantization |
| EfficientQAT (6Mdvq0bPyG) | 3.00 | 2 | Rejected efficient QAT method |
| PrefixQuant (vw0NurJ7UX) | 3.00 | 1 | Rejected static quantization method |

**Round 1 bracket**: 5.5–6.5 (above rejected papers at 3–5, below ARB-LLM at 7.00).

**Round 2 narrowing**: STBLLM (6.00) is the closest comparator — also a sub-1-bit binarization method for LLMs. The paper under review has a clearer analytical contribution but also has a catastrophic failure case. Slightly above STBLLM's analytical depth but below OSTQuant (6.20) which lacks a comparable failure. Final score: **6.0**.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>
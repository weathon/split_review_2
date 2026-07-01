Now let me read the paper in chunks to verify the reviewer's claims.Now I have a thorough understanding of the paper. Let me draft the review before calibration.Now let me run Round 1 calibration search — bracketing across score bands:Let me read key anchor papers to calibrate properly. The ARB-LLM paper (direct predecessor) and a few others are most relevant.Now I have sufficient calibration data. Let me form my bracket and write the final review.

**Round 1 bracket:** Based on comparisons:
- The paper is clearly above the 3.0-band rejects (those had fundamental methodological issues or unfair comparisons)
- It shares characteristics with 4.5-5.2 papers (solid work with gaps that prevent acceptance)
- It's below STB-LLM (6.0) and PB-LLM (6.75) in novelty and consistency
- It's clearly below ARB-LLM (7.0) since it's an incremental extension of that framework

**Initial bracket: 4.5 – 6.0**

The diagnostic analysis (Section 3) is a genuine contribution that pushes toward the upper end, but the incremental method, PTB failure, and under-ablated design choices pull toward the lower end.

Now let me write the final consolidated review:Now I have all the information needed. Let me write the final consolidated review.

## Summary
This paper investigates why naive output-matching fails in 1-bit post-training quantization (PTQ) of LLMs, identifying three concrete failure modes: layer-wise output alignment doesn't guarantee block-level improvement, accumulated quantization error causes the optimization target to drift from the true full-precision output, and token-to-token similarity matrices degrade with depth. Based on these insights, the authors propose using full-precision activations in the target output (Output Error instead of Activation-conditioned Error), applying output alignment selectively to the last FC layer per block, and introducing an Attention Matrix Preservation (AMP) masking mechanism. The method shows strong improvements on OPT models and moderate improvements on LLaMA models over the ARB baseline framework.

## Strengths

- **Well-executed diagnostic analysis (Section 3).** The three-part analysis in Sections 3.1–3.3 identifies concrete, distinct failure modes of naive output matching in 1-bit PTQ, each supported by specific measurements on LLaMA-2-7B. Figure 1 shows that some layers exhibit higher block-level loss under ARB-X despite reducing layer-level loss; Figure 2 (upper panels) demonstrates growing MSE and declining cosine similarity with depth; Figure 2 (lower panel) shows token-similarity matrix drift. This diagnostic constitutes the paper's most valuable contribution and goes beyond what the ARB framework offered.

- **Principled correction of the optimization target (Eq. 3 vs. Eq. 2).** Replacing quantized input X̂ with full-precision X in the target is a simple but well-motivated modification grounded in the error-accumulation analysis. The ablation in Table 4 confirms it matters: ~0.7 PPL improvement on C4 for both LLaMA-2-7B and OPT-6.7B.

- **Strong, consistent OPT results (Table 1).** The method outperforms ARB-X and ARB-RC across all five OPT scales (1.3B–30B), all three perplexity benchmarks, and zero-shot QA accuracy. The improvements are substantial at smaller scales (e.g., C4 PPL on OPT-1.3B: 24.69 vs. 47.60 for ARB-X and 27.70 for ARB-RC).

- **Closed-form solutions (Eqs. 5–8).** The optimization avoids iterative gradient descent by deriving closed-form updates for αc, αr, and B, maintaining the efficiency expected of a PTQ method.

## Weaknesses

### Fatal
None

### Major

- **PTB perplexity on LLaMA-2-7B (PPL=3166) contradicts the "consistently outperforms" claim.** In Table 2, the proposed method achieves 3166 PTB PPL vs. 763.19 (ARB-RC) and 681.24 (ARB-X) — roughly 4× worse. The paper dismisses this with "the large perplexity indicates that the metric cannot provide a meaningful evaluation" (line 233), but this argument applies asymmetrically: ARB-RC and ARB-X also have high PTB PPL yet perform 4× better. To be fair, BiLLM achieves an even worse 5243.01 on this same setting, indicating PTB is inherently unstable for 1-bit LLaMA-2-7B. Nevertheless, the proposed method worsens rather than improves over its direct baselines (ARB-RC/ARB-X), and this failure is undiagnosed — is it caused by AMP? By the calibration data? By numerical instability in the cross-Gram matrix S = X̂ᵀX? The paper's framing of "consistent" improvement is inaccurate without either diagnosing this failure or qualifying the claim.

- **Selective layer strategy (applying output alignment only to the last FC layer) is weakly justified.** Section 4.2 states this choice is made because the last FC layer "has the most direct impact on the block loss," but no ablation supports this specific selection. Figure 1 shows which layers benefit from output alignment, but the pattern does not cleanly map onto "last FC layer." There is no comparison of: (a) output alignment on the last FC layer only, (b) output alignment on all FC layers, (c) output alignment on the top-k empirically best layers from Figure 1, or (d) an adaptive per-layer selection criterion. This is a methodological gap in the method's core design choice.

### Minor

- **AMP is architecture-dependent rather than general-purpose.** Table 3 shows AMP is critical for LLaMA (PPL improves from 29.12→19.25 on C4, 26.24→15.42 on WikiText2) but marginal for OPT (16.35→16.22, 14.74→14.56). The RMSNorm hypothesis offered in Section 5.3 is plausible but untested — no experiment with LayerNorm-variant LLaMA or RMSNorm-variant OPT isolates whether normalization is the true cause. This makes AMP appear more like an architecture-specific patch than a principled general mechanism.

- **Improvements over ARB-RC on LLaMA are modest.** For LLaMA-2-7B: C4 PPL 20.4→19.25 (~1.15 improvement), WikiText2 16.25→15.42 (~0.83). For LLaMA-3-8B: C4 36.04→35.14 (<1 PPL), WikiText2 27.42→27.20 (~0.22). These are small gains given the added complexity (storing full-precision activations, computing cross-Gram matrices, computing AMP masks), and no variance is reported to assess whether the differences are statistically meaningful.

- **Token-similarity as proxy for attention (Section 3.3) has an unacknowledged gap.** The proxy X̂ŴŴᵀX̂ᵀ captures representational geometry after row normalization, but actual attention involves separate Q, K, V projections, softmax, and causal masking. The paper treats this proxy as if it directly measures attention mask degradation without acknowledging the gap. The motivation is reasonable but the framing overstates the connection.

### Trivial
None

## Nice-to-Haves

- **Adaptive per-layer selection criterion** instead of the fixed "last FC layer" heuristic. The paper already has the infrastructure (Figure 1) to derive a criterion — e.g., applying output alignment only when it reduces block-level loss below the weight-alignment alternative.
- **Testing the RMSNorm hypothesis** by running OPT with RMSNorm or a LLaMA variant with LayerNorm to isolate whether normalization type causes AMP's architecture-dependent behavior.
- **Variance or confidence intervals** across calibration set samples, especially for the zero-shot QA results where differences are often <1%.
- **Sensitivity analysis** to calibration set size and composition.
- **Evaluation on additional model families** (e.g., Mistral, Phi, Qwen) to support generality claims.
- **A brief overhead summary in the main text** — the method's selling point is efficiency, and the overhead analysis is entirely deferred to the appendix.

## Removed Points

*These points are flagged to be removed; treat them with caution.*

- **Criticism about LLaMA-1 exclusion**: The reviewer argues LLaMA-1 weights are "widely available through Meta's distribution." Removed per hard rule: do not question the availability or release status of cited models/tools. The authors' judgment about checkpoint availability is their prerogative.
- **Cross-Gram matrix numerical stability as a potential cause of failure**: The reviewer speculates about S = X̂ᵀX becoming ill-conditioned but provides no evidence this actually occurs. The paper uses `torch.linalg.lstsq` for numerical stability (line 132). Removed as speculative.
- **Missing overhead analysis**: The reviewer criticizes lack of overhead comparison in the main text, but per hard rules, appendix content (Appendix D) is stripped by the parser. The analysis exists in the original submission.
- **No variance reporting framed as a critical weakness**: Reporting variance for large-scale benchmarks where single-run evaluation is common practice is moved to nice-to-have per soft rules.
- **"Novel data-aware PTQ approach" framing as overselling**: The reviewer says the method is "essentially a set of refinements to ARB." While partly true, the diagnostic analysis (Section 3) and the specific modifications constitute a legitimate contribution — this is a subjective framing complaint, not a concrete weakness.

## Novel Insights

The paper's diagnostic contribution — demonstrating three distinct, measurable failure modes of output alignment in 1-bit PTQ (block-level loss inversion from layer-level optimization, accumulated error drift, and token-similarity degradation) — is genuinely novel and useful to the quantization community. The observation that output matching can hurt attention mechanisms in RMSNorm architectures (even if the explanation is speculative) opens a concrete direction for future work on normalization-aware quantization.

## Suggestions

- Investigate the PTB failure on LLaMA-2-7B specifically: run ablations with and without AMP on this benchmark, check whether the cross-Gram matrix exhibits unusual conditioning, and test with alternative calibration data.
- Provide explicit ablations comparing different layer selection strategies within each block to justify the "last FC layer only" design choice.
- Test the RMSNorm hypothesis directly — this would strengthen the paper's theoretical narrative and upgrade AMP from a heuristic patch to a principled mechanism.
- Qualify the "consistently outperforms" claim in the abstract and conclusion to acknowledge the PTB exception, which the paper already notes in the experimental text (Section 5.2) but not in the framing sections.

## Score and Decision

### Anchor Comparison

| Anchor | Path | Avg Score | Round | Comparison |
|--------|------|-----------|-------|------------|
| Systematic Review of LLMs | 8QTpYC4smR | 1.0 | R1 | Pure survey with no technical contribution; not comparable |
| Cross-Lingual Humanoid Robots | gwZ90hFSL2 | 1.0 | R1 | Unrelated domain, no real research; not comparable |
| NEMESIS Jailbreaking | 5kMwiMnUip | 1.4 | R1 | Weak methodology; paper under review is far stronger |
| Financial Markets NN | nSDOkm0SKo | 1.0 | R1 | Not comparable; trivial contribution |
| Ternary LM Pretraining (Spectra) | TJo6aQb7mK | 2.86 | R1 | Different scope (pretraining vs PTQ); paper under review has comparable experimental rigor |
| EfficientQAT | 6Mdvq0bPyG | 3.0 | R1 | Rejected for limited novelty and unfair comparisons; paper under review has stronger diagnostic contribution and fairer comparisons |
| CVXQ (Convex Optimization) | 0T8vCKa7yu | 3.0 | R1 | Rejected for limited improvements; paper under review has stronger OPT results |
| PrefixQuant | vw0NurJ7UX | 3.0 | R1 | Rejected; different quantization regime but similar novelty concerns |
| QuantLLM One-for-All | RdG7LVGnQi | 4.5 | R1 | Mixed reviews, some innovative aspects; comparable in quality to paper under review |
| Super Weight | 0Ag8FQ5Rr3 | 4.6 | R1 | Interesting observation but execution gaps; paper under review has similar profile |
| I-LLM | 44pbCtAdLx | 5.0 | R1 | Rejected; integer-only quantization with useful but incremental contribution; comparable to paper under review |
| FlatQuant | pxGucWt9vM | 5.2 | R1 | Rejected despite some strengths; paper under review has comparable merit |
| **STB-LLM** | 6XUSDvBFkV | **6.0** | R1 | Accepted; also combination of existing techniques but with more consistent results and a custom CUDA kernel. Paper under review has stronger diagnostic analysis but less consistent results |
| **PB-LLM** | BifeBRhikU | **6.75** | R1 | Accepted; first to apply binarization to LLMs (more novel). Paper under review is more incremental |
| **ARB-LLM** | ZU8OdDLTts | **7.0** | R1 | Accepted; direct predecessor introducing the full framework. Paper under review is incremental over this |
| LQ-LoRA | xw29VvOMmU | 6.75 | R1 | Accepted; different approach (low-rank + quantization) with cleaner results |
| Scaling Laws for Precision | wg1PCg3CUP | 8.0 | R1 | Strong accept; theoretical contribution of different scope, not comparable |
| MoE++ | t7P5BUKcYv | 8.0 | R1 | Different area; not directly comparable |
| LLM4QPE | vrBVFXwAmi | 8.0 | R1 | Different domain; not comparable |
| Data selection (DiSF) | f4gF6AIHRy | 8.0 | R1 | Different area; not comparable |

**Round 1 bracket: 4.5–6.0**

**Narrowing rationale:** The paper's diagnostic analysis (Section 3) is its strongest card — genuinely novel and well-executed. The OPT results are strong and consistent. However, the method is incremental over ARB-LLM (the direct predecessor scored 7.0), the LLaMA improvements are modest, the PTB failure contradicts the consistency claim, and key design choices (selective layer strategy, AMP) are under-ablated. Compared to STB-LLM (6.0, accepted), this paper has a stronger analytical contribution but weaker and less consistent experimental results, and lacks a practical contribution like a custom kernel. Compared to the 4.5–5.2 rejected papers (QuantLLM, Super Weight, I-LLM, FlatQuant), this paper has a comparable or slightly better profile thanks to the diagnostic analysis. The paper sits at the boundary — the diagnostic contribution is real and useful, but the method doesn't fully deliver on the insights.

**Final score: 5.0** — The well-executed diagnostic analysis and strong OPT results prevent a lower score, but the incremental methodology, undiagnosed PTB failure, and under-ablated design choices prevent acceptance.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>
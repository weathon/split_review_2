Now I have enough context to write the draft review. Let me prepare it.**Round 1 Bracket:** Based on comparable 1-bit PTQ papers—PB-LLM (6.75), ARB-LLM (7.00), OmniQuant (6.40), OSTQuant (6.20), STBLLM (6.00)—this paper sits in the 5.5–7.0 range. The diagnostic analysis and consistent empirical results push toward the upper end; the unexplained PTB-LLaMA-2-7B failure and missing selective-layer ablation push downward.

**Round 2 Narrowing:** The paper's analytical depth (Sections 3.1–3.3) is stronger than PB-LLM (6.75) which lacks equivalent systematic diagnostics, and on par with ARB-LLM (7.00) which it directly extends. However, the PTB anomaly (3166 vs 657-763 for competitors) is a real unresolved issue—the paper's own dismissal ("metric cannot provide a meaningful evaluation") is undermined by BiLLM's 5243 on the same benchmark, suggesting the PTB-LLaMA-2-7B regime is broadly unstable, but the proposed method still performs worst among non-BiLLM methods. I place this at **6.0**.

---

## Summary

This paper investigates the failure modes of output alignment for 1-bit post-training quantization (PTQ) of LLMs, identifying three specific problems: layer-wise output matching does not guarantee block-level loss reduction, activation-conditioned errors accumulate across layers making the optimization target progressively inaccurate, and indiscriminate output alignment disrupts token-level attention patterns. The proposed solution selectively applies output alignment to only the last FC layer per block using a corrected Output Error objective and introduces an Attention Matrix Preservation (AMP) mechanism to guard against attention degradation.

## Strengths

- **Diagnostic analysis (Sections 3.1–3.3) is concrete and directly motivates every design choice.** Figure 1 provides a falsifiable demonstration that ARB-X's layer-level output alignment can *increase* block-level loss on specific layers in LLaMA-2-7B, undermining ARB-X's design rationale. Figure 2 quantifies how activation-conditioned similarity and output similarity diverge across the 32 blocks of LLaMA-2-7B under ARB-X, confirming the accumulation failure mode. These are not illustrative observations—they are specific, quantified findings that directly drive the method.

- **AMP ablation (Table 3) is large and architecture-differentiated.** Removing AMP on LLaMA-2-7B raises perplexity by >10 points on both C4 (19.25 → 29.12) and WikiText2 (15.42 → 26.24), while OPT-6.7B sees only modest degradation (16.22 → 16.35 on C4). This differential is well-explained by the RMSNorm vs LayerNorm hypothesis (Section 5.3) and demonstrates that AMP is not a minor regularization tweak but a structurally important component for RMSNorm architectures.

- **Consistent empirical improvement over ARB-RC, the strongest prior baseline.** On OPT, the method outperforms ARB-RC on all five model sizes across C4 and WikiText2, with large gains on challenging small models (OPT-1.3B C4: 24.69 vs 27.70; OPT-2.7B C4: 19.90 vs 21.46). On LLaMA-2-13B and LLaMA-3-8B, gains are smaller but consistent (LLaMA-2-13B WikiText2: 11.5 vs 12.47).

## Weaknesses

### Fatal
None.

### Major
- **PTB-LLaMA-2-7B failure (Table 2) is unexplained and the paper's dismissal is selectively applied.** The proposed method scores 3166 PPL on PTB/LLaMA-2-7B vs ARB-RC (763.19), ARB-X (681.24), and PB-LLM (657.24). BiLLM is worse (5243), indicating PTB/LLaMA-2-7B is broadly unstable—yet the proposed method is still 4× worse than ARB-RC, which also uses C4 calibration. The paper states (Section 5.2): "the large perplexity indicates that the metric cannot provide a meaningful evaluation." But this dismissal is not applied to PB-LLM (which achieves 657.24 on the same benchmark and is still reported). On LLaMA-2-13B PTB, the method performs normally (196.64 vs ARB-RC's 197.70); on LLaMA-3-8B PTB, it wins (45.66 vs 47.88). No mechanism is proposed for why the failure is specific to LLaMA-2-7B, and a practitioner cannot tell whether to trust the method in that configuration.

### Minor
- **No ablation for selective last-layer application (Section 4.2).** The paper's central diagnostic (Section 3.1) motivates restricting output alignment to the last FC layer per block, arguing it "has the most direct impact on the block loss." Table 3 ablates AMP and Table 4 ablates the error objective, but no ablation compares last-FC-only vs all-FC-layers. Since the selective application design choice flows directly from the Section 3.1 analysis, this ablation is needed to close the evidence chain.

- **AMP update rule (Eqs. 10–11) is a greedy heuristic without characterization.** The closed-form solutions (α_c\*, α_r\*, B\*) optimize the reconstruction objective (Eq. 3); the AMP mask then element-wise gates which updates are accepted based on the sign of ∇L_AMP. This is neither constrained optimization nor a proper multi-objective formulation. The empirical benefit is clear, but the paper offers no analysis of when this heuristic converges to consistent solutions vs inconsistent ones, which is relevant to understanding the LLaMA-2-7B PTB failure.

### Trivial
None that are author errors (a notational issue in Eq. 2 is a parser artifact).

## Nice-to-Haves
- Add a diagnostic for the PTB-LLaMA-2-7B collapse: report attention entropy, token distribution statistics, or layer-wise error profiles for that configuration compared to the well-behaved LLaMA-2-13B configuration. Even a partial mechanistic account would strengthen confidence.
- Complete the ablation for selective layer application: test last-FC-only vs all-FC-layers on one model (LLaMA-2-7B) to confirm the Section 3.1 motivation empirically.
- The architecture sensitivity hypothesis (RMSNorm → attention-vulnerable) is stated but could be tested by comparing a LayerNorm-based model with AMP off vs on to directly validate the proposed mechanism.

## Removed Points
*These points are flagged as removed; treat them with caution.*

- **LLaMA-1 exclusion critique:** The reviewer flags that LLaMA-1 exclusion is a "weak justification." Per hard rules, we cannot independently verify checkpoint availability on HuggingFace at submission time. Removed.
- **LLaMA-3 evidence "not compelling":** The proposed method's modest improvement on LLaMA-3-8B (27.42→27.20 WikiText2) was flagged as weak evidence. This is a generic criticism—in 1-bit quantization of a strong model, even consistent marginal gains are meaningful. Removed.
- **Equation 2 notational error:** Raised as a paper flaw. Per hard rules, formatting artifacts from the PDF parser (the left side is identically zero) should not be counted against authors. Removed.
- **Missing related works:** Not assessed per hard rules (no external sources to confirm).

## Novel Insights
The paper's most novel contribution is the systematic decomposition of output alignment failure into three distinct, verifiable failure modes—block-level inconsistency, error accumulation that corrupts the optimization target, and attention-structure disruption—and the demonstration that these map to specific architectural properties (RMSNorm sensitivity, block interdependency). The AMP mechanism, which uses gradient signs w.r.t. a token-similarity objective to gate parameter updates, offers a practically useful primitive for architecture-aware quantization: it identifies, for each element of each parameter tensor, whether the reconstruction update hurts or helps attention preservation, without requiring joint optimization. The observation that RMSNorm's direction-dependence is a predictor of output-alignment fragility is a practically transferable insight for future 1-bit PTQ work on architectures that use normalization schemes other than LayerNorm.

## Suggestions
- Provide even a limited mechanistic diagnosis of the PTB-LLaMA-2-7B failure: inspect the model's per-layer error profiles and AMP mask density in that configuration relative to the well-behaved LLaMA-2-13B and LLaMA-3-8B configurations.
- Add the last-FC-layer ablation (even one model/dataset pair) to directly support the Section 4.2 design decision.
- Frame the AMP update rule explicitly as a heuristic in the main text, and discuss what properties guarantee that the reconstruction objective and L_AMP are not severely at odds.

## Score and Decision

**Anchor Papers Retrieved:**
| Paper | Path | Avg Score | Round | Comparison |
|---|---|---|---|---|
| Ternary LM Scaling Laws | TJo6aQb7mK | 2.86 (human: 7.60) | R1 | Training-based; not comparable scope |
| EfficientQAT | 6Mdvq0bPyG | 3.00 | R1 | QAT, weaker diagnostic rigor |
| PrefixQuant | vw0NurJ7UX | 3.00 | R1 | PTQ but activation quantization domain |
| CVXQ | 0T8vCKa7yu | 3.00 | R1 | PTQ weight quantization, less empirically validated |
| One QuantLLM | RdG7LVGnQi | 4.50 | R1 | Once-for-all QAT framework |
| FPTQ | ykhRO1mAg3 | 4.00 | R1 | W4A8 PTQ, narrower scope |
| I-LLM | 44pbCtAdLx | 5.00 | R1 | Integer-only PTQ, different setting |
| QRazor | lwcnZmyojm | 5.20 | R1 | 4-bit PTQ, less analytical |
| PB-LLM | BifeBRhikU | 6.75 | R1, R2 | Direct 1-bit PTQ competitor (baseline in paper) |
| ARB-LLM | ZU8OdDLTts | 7.00 | R1 | Direct predecessor paper; this work improves on ARB-X |
| STBLLM | 6XUSDvBFkV | 6.00 | R1 | 1-bit PTQ, less diagnostic depth |
| SpikeLLM | ZadnlOHsHv | 7.00 | R1 | 1-bit spiking-based; different mechanism |
| OSTQuant | rAcgDBdKnP | 6.20 | R2 | PTQ with novel metric + method framing |
| OmniQuant | 8Wuvhh0LYW | 6.40 | R2 | PTQ learnable clipping; similar scope |
| SpinQuant | ogO6DGE6FZ | 5.80 | R2 | PTQ with learned rotations |
| Compressing LLMs | B9klVS7Ddk | 6.75 | R2 | Analysis-focused LLM compression |

**Round 1 Bracket:** 5.5–7.0

**Round 2 Narrowing:** The paper is analytically stronger than STBLLM (6.0) and PB-LLM (6.75) and at parity with ARB-LLM (7.0) on which it directly improves. However, the unexplained PTB-LLaMA-2-7B failure (3166 vs 763 for the strongest weight-alignment baseline) is a real, verifiable problem—it reduces confidence in the method's robustness in a way that neither STBLLM nor PB-LLM have analogous issues. The diagnostic quality and consistent empirical results across OPT and most LLaMA settings are genuine strengths. **Final score: 6.0**

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>
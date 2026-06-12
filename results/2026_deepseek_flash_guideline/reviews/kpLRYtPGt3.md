Here is the final consolidated review.

---

## Summary

This paper introduces Neon, a method that improves generative models by first fine-tuning on self-generated synthetic data and then negatively extrapolating away from the resulting degraded parameters via a simple parameter merge (θ_Neon = θ_r − w(θ_s − θ_r)). The key insight is that mode-seeking inference samplers (low temperature, CFG, top-k/p) induce a predictable anti-alignment between synthetic- and real-data gradients, so reversing the self-training degradation direction actually improves the model. Neon is demonstrated across diffusion, flow matching, autoregressive, and few-step models on CIFAR-10, FFHQ, and ImageNet, achieving a SOTA ImageNet-256 FID of 1.02 with xAR-L using <1% additional compute.

## Strengths

- **Novel and counterintuitive idea, well-validated theoretically and empirically.** The observation that self-training degradation is not random noise but a structured signal anti-aligned with the true data gradient is a genuine conceptual contribution. Theorems 1 and 2 provide a formal condition for when anti-alignment holds, connecting mode-seeking samplers (CFG, low temperature, top-k/p) to the sign of the alignment term *s*. The theory is asymptotic but the empirics fill the gap convincingly.

- **Architectural universality across four fundamentally different model families.** Neon is demonstrated on diffusion (EDM-VP), flow matching, autoregressive (xAR, VAR), and few-step (IMM) models—families with very different training objectives and inference procedures. This breadth is unusual for a single-method paper and directly supports the claim that Neon captures a general property of mode-seeking samplers rather than an architecture-specific trick. By contrast, prior methods like Discriminator Guidance and SIMS are diffusion-specific, and DDO requires likelihood computation that precludes flow matching and IMM.

- **State-of-the-art ImageNet-256 result with negligible overhead.** xAR-L improves from FID 1.28 to **1.02** (surpassing UCGM's 1.06) using only 0.36% additional training compute and as few as 1k synthetic samples (FID 1.05). The compute overhead numbers (<1% across all settings) are the paper's strongest practical selling point.

- **Insightful ablation studies.** The CIFAR-10C null result (line 249) cleanly rules out the trivial hypothesis that any OOD data would help. The cross-architecture transfer experiment (Figure 8) and robustness to synthetic data quality (Figure 10) are informative. The finding that Neon can compensate for a 40% reduction in real training data (Figure 9) strengthens the practical relevance for data-scarce applications.

## Weaknesses

### Major

None.

### Minor

- **Figure 4 caption contains a concrete factual error.** The caption states: "w = -1 corresponds to the model directly trained on synthetic data, i.e., θ_Neon = θ_r." Plugging w = -1 into Equation 2 (θ_Neon = (1+w)θ_r − wθ_s) gives θ_Neon = θ_s, not θ_r. (The statement for w=0 is correct.) While this does not invalidate the experimental results, it reflects a quality-control slip on a key figure that explains the paper's central analysis.

- **For autoregressive models, the reported improvement conflates Neon with re-optimization of the CFG scale γ.** The paper jointly optimizes w and γ, which is transparently stated. But the baseline comparison is (base model with default γ) vs. (Neon model with jointly tuned w and γ). For VAR-d16, independent γ optimization gives FID 3.01 vs. 2.01 with joint tuning, confirming synergy. However, for the headline xAR-L result (1.28 → 1.02), it is unclear how much of the gain comes from Neon versus from the freedom to re-tune γ. An ablation holding γ fixed at the base model's optimal value while varying only w would isolate Neon's direct contribution.

- **The main text lacks a compact comparison table for competitive methods.** The paper mentions UCGM (FID 1.06) and references Table A.1 in the appendix for full comparisons. However, the related-work section (lines 60–61) characterizes Discriminator Guidance, SIMS, DDO, and Self-Play Fine-Tuning as methods with overhead, without providing their benchmark numbers. Adding a small main-text table comparing Neon's FID to these methods on the same benchmarks would strengthen the paper's framing.

### Trivial

- The Figure 4 caption error (w = −1 → θ_Neon should be θ_s, not θ_r).

## Nice-to-Haves

- Disentangle w effects from γ re-optimization for the xAR-L result by showing FID with γ held at the base model's optimal value while only w varies.
- Add a sentence explicitly noting that the parameter merge does not change inference cost (same architecture, same compute per sample).
- Provide heuristic guidance for selecting w without a validation set and FID computation (which requires real data).

## Removed Points

These points are flagged to be removed; treat them with caution.

- **"SOTA claim depends on base-model choice; controlled comparison missing" (Harsh Critic Point 2):** The paper's SOTA claim is about the final benchmark number (FID 1.02 on ImageNet-256), a factual statement verifiable against published results. The paper does not claim that Neon outperforms DDO/SIMS when applied to the same checkpoint—it claims a record-breaking FID result. The base-model robustness experiment (Figure 9) already tests robustness. The critic's concern is a reasonable desideratum for future work but is not a weakness of the paper as written, since the claim is benchmark-anchored, not method-superiority-anchored.

- **Generic strengths from the Strength Finder (e.g., "addresses an important problem"):** These are generic and lack concrete content specific to the paper's contributions.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Fix the Figure 4 caption (w = −1 → θ_Neon = θ_s).
2. Add an ablation for xAR-L showing FID with γ fixed at the base model's optimal value while varying only w, to isolate Neon's contribution.
3. Move a small comparison table (Neon vs. Discriminator Guidance, SIMS, DDO, Self-Play FT, UCGM) to the main text.
4. Add a one-sentence clarification that inference cost is unchanged by the parameter merge.

---

**Calibration anchors:**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| u1cQYxRI1H | 0.50 | R1 bracket | Not comparable (illumination harmonization paper) |
| Uj0h13lVrR | 1.00 | R1 bracket | Strong reject; not comparable |
| TJHB4ySVZM | 3.40 | R1 bracket | Data extrapolation for T2I; weaker method, poor presentation |
| SaOxhcDCM3 | 3.20 | R1 bracket | Self-consuming training loop in LLMs; mixed scores (5s and a 10), weaker analysis |
| lNtio1tdbL | 3.00 | R1 bracket | Model merging via alternating tuning; mixed reviews, rejected |
| P5UETqZXqT | 5.75 | R1 bracket | Model collapse in diffusion chain; rejected, weaker theory-practice link than Neon |
| ShjMHfmPs0 | 6.67 | R1 bracket | MAD self-consuming loops; accepted but documents problem without offering a solution like Neon does |
| JORAfH2xFd | 6.75 | R1 bracket | Stability of iterative retraining; accepted but narrower in scope |
| et5l9qPUhm | 8.00 | R1 bracket | Strong model collapse theory; rejected despite high scores, purely theoretical |
| WJaUkwci9o | 8.00 | R1 bracket | Self-improvement sharpening mechanism; accepted, strong theory but no experiments on main algorithms |
| OlzB6LnXcS | 8.00 | R1/R2 | One-step shortcut models; accepted, strong method with clean experiments |
| zMoNrajk2X | 8.00 | R2 narrowing | CADS diffusion diversity; accepted, similar-strength method paper, ImageNet FID 1.70 vs Neon's 1.02 |
| gU58d5QeGv | 8.00 | R2 narrowing | Würstchen efficient T2I; accepted, strong architecture paper |

**Initial bracket:** [7.5, 8.5]. **Narrowing:** Examined CADS (8.0), Sharpening Mechanism (8.0), Strong Model Collapse (8.0) as peers. Neon's combination of novel theory, broad empirical validation across 4 model families, and SOTA results (FID 1.02) matches or exceeds the quality of these anchors. The minor weaknesses (caption error, joint-optimization confound) prevent a 10 but do not detract from an accept decision.

MY FINAL SCORE: <score>8.0</score>
MY FINAL DECISION: <decision>Accept</decision>
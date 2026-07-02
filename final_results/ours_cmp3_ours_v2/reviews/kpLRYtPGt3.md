Now I have strong calibration anchors. Let me synthesize.

**Round 1 bracket:** Based on comparison with anchors, I placed Neon in the 7.0-8.0 range. The paper is clearly more novel and empirically broader than 6.0-6.75 papers (LCSC at 6.0, MAD at 6.67). The CFG confound prevents it from reaching 8+ territory, but it's a stronger contribution than the 5.75-6.2 papers.

**Round 2 narrowing:** Comparing against the 7.2-7.5 band papers (PaRa at 7.5, RepG at 7.33, Anti-Exposure Bias at 7.20, Easing Training Process at 7.33), Neon is similarly innovative with broader architectural coverage but carries a real methodological weakness (CFG confound) that papers in this band typically don't have. Score 7.5 reflects a clear accept with a substantive but non-fatal issue that should be addressed.

Here's the final review.

---

## Summary

Neon introduces a method to improve generative image models by first fine-tuning on self-generated synthetic data (which degrades quality) and then extrapolating away from the degraded weights via a simple parameter merge. The paper provides theoretical analysis showing this works because mode-seeking inference samplers create anti-alignment between synthetic and real-data gradients. Experiments across diffusion, flow matching, autoregressive, and few-step models on CIFAR-10, FFHQ, and ImageNet show consistent improvements including a state-of-the-art FID of 1.02 on ImageNet-256 for xAR-L.

## Strengths

1. **Genuinely novel and counterintuitive core idea.** Almost all prior work treats self-training collapse as a problem to avoid or correct through external mechanisms (discriminators, verifiers, likelihood ratios, inference-time modifications). Neon instead exploits the degradation as a signal via a straightforward parameter extrapolation. The theoretical explanation (anti-alignment of synthetic and real gradients under mode-seeking samplers) provides a coherent mechanistic story.

2. **Broad architectural validation across four model families.** Neon is demonstrated on diffusion (EDM), flow matching (FM), autoregressive (xAR, VAR), and few-step (IMM) models on three datasets. This breadth significantly exceeds prior self-correction methods — e.g., Discriminator Guidance is diffusion-specific; DDO requires likelihoods and cannot apply to flow matching or IMM. The same simple merge works across all families, which is the strongest evidence for the paper's thesis.

3. **Cross-architecture transfer result (Section 4.4) is non-trivial and practically useful.** Showing that synthetic data from flow matching or IMM models can improve an EDM-VP model (FID 1.97→1.59 and 1.80 respectively) opens practical workflows where the degradation signal is generated from a cheaper architecture.

4. **Robustness experiments are well-conceived.** Testing whether Neon requires a near-optimal base model (Figure 9: works even with models trained on only 30k real samples) and whether it requires high-quality synthetic data (Figure 10: robust across CFG scales γ∈[1,3]) directly addresses the most obvious limitations. Both results hold up well.

5. **Efficiency is convincingly demonstrated.** Neon requires <1% additional compute and as few as 1k synthetic samples.

## Weaknesses

### Major

1. **CFG co-optimization confound in autoregressive experiments (Section 4.2).** For all autoregressive experiments (xAR, VAR, IMM with CFG), the merge weight w and CFG scale γ are jointly optimized. The paper reports independent optimization (γ=1.25) yields FID 3.01 for VAR-d16 while joint optimization (w*≈1.0, γ*≈2.7) yields FID 2.01. However, the paper never reports what the *base model* (w=0) achieves at γ=2.7. If the base model at γ=2.7 already achieves FID substantially better than 3.01, part of the improvement is attributable to better CFG tuning rather than the Neon mechanism. This is directly relevant to the headline SOTA claim (xAR-L: 1.28→1.02). **This does not threaten the paper's core contribution** — the diffusion and flow matching experiments (Section 4.1) involve no CFG co-optimization and independently demonstrate Neon's effectiveness — but it weakens the strongest individual result. A 2×2 ablation (Neon on/off × default CFG / jointly-optimal CFG) for each autoregressive model is needed to cleanly isolate Neon's contribution.

### Minor

2. **No statistical uncertainty on any FID value.** All FID results are single point estimates with no confidence intervals, error bars, or multiple-seed runs. FID estimates from 10k/50k samples have known variance. This is common in the field but the paper would be stronger with uncertainty quantification for at least the main results.

3. **Theory is framed as more rigorous than it delivers.** The paper claims to "prove rigorously" (Contribution C2) that mode-seeking samplers create predictable anti-alignment. In fact: (a) Theorem 1 depends on unmeasurable quantities (true-data Hessian H_d, spectral bounds of K, sampler bias b) never estimated for any real model; (b) Theorem 2 proves anti-alignment only "to first order in ‖ε‖_{H_d}" (near optimal models), yet Neon works for models trained on 30k real samples where this perturbative guarantee is unlikely to hold; (c) the diffusion/flow extension relies on an unverified "curvature-density coupling" assumption (A-MONO, footnote 2). The theory is a plausible mechanistic story, not a rigorous provable guarantee.

### Trivial

4. **No text-to-image experiments.** All experiments are on class-conditional or unconditional models up to 512×512. The "universality" claim (C3) should be explicitly scoped to acknowledge this limitation.

## Nice-to-Haves

- Empirical verification of at least one theoretical quantity (e.g., s = ⟨r_d, P r_s⟩ or cos φ) on a real model would transform the theory from a plausible story to a verified mechanism.
- Testing on a text-to-image model (e.g., Stable Diffusion) would strengthen the universality claim.

## Removed Points

- **Missing model merging literature** (Model Soups, weight averaging, TIES-Merging): The instructions prohibit introducing missing related-work criticisms. Neon uses extrapolation (w>0), not interpolation, which is a meaningfully different regime.
- **"Self-training requires training infrastructure"**: Generic criticism applicable to any fine-tuning method; not substantive enough.
- **Section-by-section operational notes** (e.g., "the abstract overstates simplicity"): Reviewer working notes, not substantive weaknesses.
- **Criticism that Figure 6 heatmap y-axis shows 0-1.5 but γ*≈2.7**: Parser artifact, not a paper error.

## Novel Insights

The CFG co-optimization concern is the most useful critical observation. The paper would materially benefit from a 2×2 ablation cleanly separating Neon's contribution from improved CFG tuning. This is the single highest-leverage experiment the authors could add.

## Suggestions

1. **Provide a 2×2 ablation table** for each autoregressive model: base model at default CFG vs. base model at jointly-optimal CFG vs. Neon at default CFG vs. Neon at jointly-optimal CFG.
2. **Add FID confidence intervals** (bootstrap or multiple seeds) for at least the main results.
3. **Qualify the theoretical claims** to match their actual scope: the theory is a perturbative mechanistic explanation, not a rigorous guarantee for all operating regimes.
4. **Acknowledge the text-to-image scope limitation** in the conclusions.

**Calibration anchors used:**
- *Self-Consuming Generative Models Go MAD* (avg 6.67, Accept): Studies model collapse but offers no improvement method. Less novel than Neon.
- *On the Stability of Iterative Retraining of Generative Models on their own Data* (avg 6.75, Accept): Theoretical analysis of stability, narrower empirical scope.
- *Linear Combination of Saved Checkpoints* (avg 6.00, Accept): Checkpoint averaging for diffusion/consistency models, limited to CIFAR-10 and ImageNet-64. Less novel than Neon.
- *Collapse or Thrive? Perils and Promises of Synthetic Data* (avg 5.75, Reject): Study of model collapse scenarios, limited novelty.
- *PaRa: Personalizing Text-to-Image Diffusion via Parameter Rank Reduction* (avg 7.50, Accept): Similar scoring band; Neon has broader architecture coverage but carries a CFG confound this paper doesn't have.
- *Representative Guidance for Diffusion Sampling* (avg 7.33, Accept): Diffusion-specific inference modification; Neon is more broadly applicable.

**Round 1 bracket:** 7.0–8.0. **Round 2 narrowing:** 7.5, driven by comparison with the 7.2–7.5 band (PaRa, RepG, Anti-Exposure Bias). Neon's novelty and breadth are competitive with this band, but the CFG confound prevents it from reaching 8+.

MY FINAL SCORE: <score>7.5</score>
MY FINAL DECISION: <decision>Accept</decision>
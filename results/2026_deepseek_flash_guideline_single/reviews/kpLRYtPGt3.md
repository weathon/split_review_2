## Summary

Neon introduces a surprisingly simple post-hoc method to improve generative models: briefly fine-tune on self-generated synthetic data (which degrades quality), then linearly extrapolate away from the degraded checkpoint (θ_Neon = (1+w)θ_r - wθ_s, w>0). The paper provides theoretical grounding—mode-seeking inference samplers create anti-alignment between synthetic and population gradients—and demonstrates broad empirical validation across diffusion, flow matching, autoregressive, and few-step models on ImageNet, CIFAR-10, and FFHQ. The headline result: xAR-L on ImageNet-256 reaches FID 1.02 (from 1.28) at ≤1% additional compute, surpassing the prior SOTA.

## Strengths

1. **Elegant and general method formulation (Section 3, Equation 2).** The core Neon operation—a single linear extrapolation away from a briefly self-fine-tuned model—is conceptually clean, computationally trivial (<1% additional training budget), and requires no auxiliary networks, inference modifications, or likelihood computations. This stands in genuine contrast to prior approaches like Discriminator Guidance, SIMS, and DDO, each of which carries architectural restrictions or inference overhead.

2. **Principled theoretical framework (Section 3.1, Theorems 1–2).** The paper provides a formal proof that mode-seeking inference samplers (temperature<1, top-k/p, CFG) induce anti-alignment between the synthetic-data gradient and the true-data population gradient, and it quantifies the sufficient condition for negative extrapolation to reduce risk (the boxed inequality in Theorem 1). This moves the paper beyond a heuristic trick into a substantiated claim. The theory also correctly predicts the complementary interpolation regime for diversity-seeking samplers, which adds credibility.

3. **Broad and systematic experimental validation (Section 4).** Neon is evaluated across four distinct model families (diffusion, flow matching, autoregressive, few-step) on three datasets (ImageNet, CIFAR-10, FFHQ). The ablation studies are well-conceived: the base-model quality sweep (Figure 9), the sensitivity to synthetic data quality (Figure 10), and the cross-architecture transfer experiment (Figure 8) each test a specific boundary of the method's applicability. The "as few as 1k synthetic samples" result for xAR-L (FID 1.05 with only 1k samples) is striking.

4. **State-of-the-art result on ImageNet-256 (Section 4.2).** xAR-L + Neon achieves FID 1.02, surpassing UCGM's 1.06. Even accounting for the joint (w,γ) tuning issue (see Weakness 1), the improvement from 1.28 to 1.02 at 0.36% additional compute is quantitatively significant.

## Weaknesses

### Fatal
None.

### Major

1. **Co-optimization of (w, γ) makes it difficult to fully attribute the headline FID gains to Neon alone (Section 4.2).** For autoregressive models, the base model uses CFG (γ>0), and the headline FID of 1.02 is achieved by jointly optimizing both the Neon weight w and the CFG scale γ. The paper states "Independent optimization of γ (without Neon) yields FID 3.01 for VAR-d16"—far worse than the base FID of 3.30—and notes that co-optimization is crucial. However, the paper does not provide a clean decomposition for the key xAR-L result: (a) base model at its own optimal γ → FID X; (b) base model at the γ that is optimal when w>0 (holding w=0) → FID Y; (c) Neon model at jointly optimized (w*,γ*) → FID Z. Without (b), a nontrivial fraction of the 1.28→1.02 gain could be attributable to γ re-optimization rather than to Neon's mechanism per se. The heatmaps in Figure 6 clearly show the optimal γ shifts when w>0, confirming the interaction exists. *(Note: this concern does not affect the diffusion, flow matching, and IMM results, which do not involve joint CFG tuning and independently support the core claim.)*

### Minor

2. **No error bars or variance estimates.** Every FID in the paper is reported as a single number. Synthetic data generation (stochastic sampling), fine-tuning (stochastic optimization), and FID evaluation (Monte Carlo estimate) are all stochastic processes. While single-run FID reporting is common practice in large-scale generative model evaluation, the lack of variance estimates means the reader cannot assess the statistical significance of reported improvements—especially relevant for more modest gains (e.g., EDM-VP on CIFAR-10: 1.78→1.38) and for the 1k-sample regime where variance could be appreciable.

3. **Boundary of base model quality not fully characterized (Figure 9).** The theoretical sufficient condition for anti-alignment (Theorem 1) requires small model error ‖ε‖. Figure 9 tests down to models trained on 30k CIFAR-10 samples (FID ~1.87), showing Neon still helps substantially. The paper claims "Neon does not require a near-optimal base model to succeed"—this is supported for the tested range but the lower bound on base model quality is not established. It remains unclear whether a substantially weaker model could see Neon degrade rather than improve performance.

4. **Gap between the theory's single-step gradient approximation and multi-epoch fine-tuning practice (Section 3.1).** The theoretical analysis (Eq. 4) approximates fine-tuning as a single gradient step: θ_s = θ_r - α P r_s + O(α²). In practice, experiments run multiple optimization steps, sometimes across multiple epochs. While the paper acknowledges the approximation through O(α²) notation and the U-shaped FID-vs-budget curves provide indirect validation, it does not empirically test whether the theory's predictions (e.g., the relationship between optimal w* and training budget) hold quantitatively.

### Trivial

5. **Figure 4 caption contains a typographical error.** The caption states "w = -1 corresponds to the model directly trained on synthetic data, i.e., θ_Neon = θ_r." This is incorrect: by Equation 2, w = -1 gives θ_Neon = (1+(-1))θ_r - (-1)θ_s = θ_s (the degraded model), not θ_r. The intended statement is that w = -1 corresponds to θ_Neon = θ_s. (The statement for w = 0 is correctly given as θ_Neon = θ_r.)

## Nice-to-Haves

- Provide the (w,γ) decomposition analysis for xAR-L: report FID at (a) base model at its own optimal γ (w=0), (b) base model at γ* found optimal for joint tuning (w=0 at γ*), and (c) Neon at (w*,γ*). This would cleanly separate Neon's contribution from γ re-optimization.
- Run 3–5 seeds for the key experiments (xAR-L on ImageNet-256, EDM-VP on CIFAR-10) and report mean ± std FID.
- Test Neon on a genuinely weak base model (e.g., trained on 5k–10k CIFAR-10 samples) to probe the failure regime of the theory's "small ‖ε‖" condition.
- Verify the single-step gradient approximation by running Neon with fine-tuning limited to 1–2 gradient steps and comparing to the multi-step results.

## Removed Points

These points are flagged to be removed; treat them with caution.

1. **"Top-k/top-p monotone reweighting claim is incorrect."** REMOVED: The reviewer argued top-k is a hard truncation+renormalization that does not fit the paper's form q(x) ∝ f(log p(x)) p(x). However, top-k/top-p CAN be expressed in this form: f is the indicator of being in the top-k (or top-p) set, which IS nondecreasing in log p, and the proportionality constant handles renormalization. The claim is mathematically defensible. Additionally, the appendix containing the full proof (App. B.6) was stripped by the parser but exists in the original submission.

2. **"Theoretical guarantees rely on model being close to optimal."** DOWNGRADED to Minor #3. The paper explicitly tests this with models trained on subsets as small as 30k CIFAR-10 samples, and the claim "Neon does not require a near-optimal base model" is reasonably supported by this evidence. The remaining concern (lower bound not fully characterized) is genuine but minor.

3. **"Hessian spectral closeness assumption for cross-architecture transfer is non-trivial."** REMOVED: The paper provides the full theoretical formalization in Appendix B.8 (stripped by parser). Criticizing the main-text intuitive summary as an oversimplification is unfair since the rigorous version exists in the appendix.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Provide the (w,γ) decomposition analysis for xAR-L: report FID at (a) base model at its own optimal γ (w=0), (b) base model at γ* found optimal for joint tuning (w=0 at γ*), and (c) Neon at (w*,γ*). This would cleanly separate Neon's contribution from γ re-optimization and strengthen the headline claim.
2. Add variance estimates (mean ± std over 3–5 seeds) for the two most important settings: xAR-L on ImageNet-256 and EDM-VP on CIFAR-10.
3. Fix the Figure 4 caption error (w=-1 gives θ_s, not θ_r).
4. Consider probing the failure regime of base model quality with a model trained on very few real samples.

## Score and Decision

**Calibration anchors used (all rounds):**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|-----------|
| u1cQYxRI1H (IC-Light) | 0.50 | R1 | Different topic (illumination); not relevant |
| 5lUdTogEL3 (Lifelong ReID) | 1.00 | R1 | Different topic; not relevant |
| TJHB4ySVZM (Data Extrapolation T2I) | 3.40 | R1 | Conceptually similar (data extrapolation) but much less rigorous; Neon is far stronger |
| cywG53B2ZQ (Negative-Prompt Alignment) | 2.50 | R1 | Related concept (using negative direction) but weaker method and theory |
| lIdc5DUplq (SuperMerge) | 4.33 | R1 | Parameter merging topic; weaker contribution |
| P5UETqZXqT (Chain of Diffusion Collapse) | 5.75 | R1 | Related model-collapse topic; rejected due to unclear method-mechanism link; Neon is stronger |
| svIdLLZpsA (Real-Fake) | 6.00 | R1 | Synthetic data training; comparable rigor but less broad validation |
| tLFWU6izoA (Diffusion Feedback CLIP) | 6.60 | R1 | Simple post-training; weaker theory than Neon |
| OlzB6LnXcS (Shortcut Models) | 8.00 | R1 | Major architectural contribution; stronger overall but a different kind of contribution |
| ShjMHfmPs0 (Self-Consuming MAD) | 6.67 | R2 | Directly related topic (self-consuming loops); accepted but Neon has a concrete method + broader validation |
| Xr5iINA3zU (Collapse or Thrive) | 5.75 | R2 | Related topic (synthetic data); rejected with mixed scores |
| JORAfH2xFd (Stability Iterative Retraining) | 6.75 | R2 | Related topic; accepted but primarily analysis, not method |
| yitH9xAHQs (Forewarned is Forearmed) | 6.00 | R2 | LLM data synthesis; weaker than Neon |

**Bracket (Round 1):** 7.0–8.0 (clearly above the 5.75–6.75 range of related self-consuming papers; below 8.0 of architectural contributions)

**Narrowing:** The paper's strengths—elegant method, rigorous theory, broad validation, SOTA results—place it well above the 6-range papers. The main limiting factor is the unresolved co-optimization attribution issue, which prevents the headline claim from being fully clean. This is a significant but bounded weakness. Score rounded to 7.5.

MY FINAL SCORE: <score>7.5</score>
MY FINAL DECISION: <decision>Accept</decision>
I have thoroughly verified all reviewer claims against the paper. Let me now produce the final consolidated review.

---

## Summary

Neon introduces a remarkably simple post-hoc method for improving generative models: briefly fine-tune on the model's own synthetic outputs (producing a degraded checkpoint θ_s), then extrapolate away from the degradation via θ_Neon = (1+w)θ_r − wθ_s. The paper proves that mode-seeking inference samplers create anti-alignment between synthetic and real-data gradients, explaining both why naive self-training degrades models and why reversing that degradation improves them. Experiments span diffusion, flow matching, autoregressive, and few-step models on CIFAR-10, FFHQ, and ImageNet, with the headline result being xAR-L reaching FID 1.02 on ImageNet-256 using 0.36% additional compute.

## Strengths

1. **Rigorous theoretical foundation (Section 3.1, Theorems 1–2).** The paper proves that mode-seeking samplers (temperature<1, top-k, CFG, finite-step ODE solvers) induce a predictable negative inner product between synthetic and real-data population gradients. This provides a formal explanation for both the failure of naive self-training and the success of Neon — going beyond the empirical observations of prior work on model collapse.

2. **Impressive empirical breadth with consistent improvements across four model families (Sections 4.1–4.3).** Neon improves EDM-VP (CIFAR-10: 1.78→1.38; FFHQ-64: 2.39→1.12), flow matching (CIFAR-10: 3.5→2.32), xAR-L (ImageNet-256: 1.28→1.02), VAR-d16 (3.30→2.01), and IMM (ImageNet-256, 8-step: 1.98→1.46). The consistency across diffusion, flow matching, autoregressive, and few-step architectures makes a strong case that the method captures a general phenomenon.

3. **Demonstrated mechanism via precision-recall analysis (Figures 4, 6).** The paper shows that Neon works by trading precision for recall, redistributing probability mass from over-represented to under-represented modes. This is directly measured with established metrics and provides clear evidence for the claimed mechanism.

4. **Cross-architecture transferability (Section 4.4, Figure 8).** Synthetic data from one model architecture (flow matching, IMM) improves another (EDM-VP) — a capability that competing architecture-specific methods (DDO, SIMS, Discriminator Guidance) do not offer.

5. **Robustness to practical conditions (Section 4.4, Figures 9–10).** Neon works with as few as 1k synthetic samples, across varying base model qualities (compensating for 40% reduction in real data), and is robust to synthetic data quality (CFG scale 1–3 yields near-identical FIDs).

6. **Efficiency.** The method requires <1% additional training compute in most settings, with no auxiliary models, no inference modifications, and no new real data.

## Weaknesses

### Major

1. **Figure 4 contains a verifiable caption sign error, and the optimal w ≈ -0.5 (interpolation toward θ_s) contradicts the paper's central w > 0 framing, without adequate explanation.**
   - **Caption error (line 193):** "w = -1 corresponds to the model directly trained on synthetic data, i.e., θ_Neon = θ_r." This is wrong: at w = -1, θ_Neon = (1+(-1))θ_r − (-1)θ_s = θ_s, not θ_r.
   - **Data/framing contradiction:** The parser description and figure data show the FID minimum at w ≈ -0.5, which corresponds to θ_Neon = 0.5θ_r + 0.5θ_s — interpolation toward θ_s. Yet the caption asserts "w > 0 corresponds to the negative extrapolation regime where Neon demonstrates its improvement capability."
   - **Unresolved theoretical tension:** The paper's "When interpolation (not extrapolation) helps" section (line 171) attributes w < 0 optima to "diversity-seeking samplers" that are "rare in practice." But the EDM-VP on CIFAR-10 uses default inference settings (standard ODE solver, no CFG), which Theorem 2 classifies as mode-seeking — predicting w > 0. The paper neither acknowledges this discrepancy nor explains why a mode-seeking sampler gives an interpolation-favorable result in a core quantitative figure. This undermines the claimed universality of the w > 0 regime and its attribution to specific sampler properties.

2. **No controlled experimental comparison against the specific methods the paper positions itself against.** The Introduction and Background (lines 26, 60) explicitly contrast Neon with DDO, SIMS, Discriminator Guidance, and Self-Play Fine-Tuning, claiming Neon is simpler and more universal. Yet none of these methods appear in any shared experiment — the paper compares only against a published reference number (UCGM's 1.06). Without a controlled comparison on the same architectures and evaluation protocol, the claimed advantages over these specific competitors are asserted rather than demonstrated.

3. **Compute efficiency figures likely undercount total cost.** The reported "0.36% additional training compute" (line 209) and similar numbers appear to count only the fine-tuning step (step 2 of Algorithm 1). Step 1 — generating the synthetic dataset S via inference through a large model with CFG — also has material cost. For xAR-L, generating 750k ImageNet-256 images through a large autoregressive model involves substantial inference compute that is not reflected. The paper uses "additional training compute" (line 9) as its consistent phrasing, suggesting only training is counted. This should be explicitly clarified, and the inference cost should be disclosed for an honest efficiency accounting.

### Minor

4. **The theoretical conditions of Theorem 1 depend on quantities (η₀, η₁, m, M, cos φ) that are not estimated for any experimental model.** The theory provides qualitative intuition but not a verifiable quantitative prediction. The sufficient condition for anti-alignment (‖ε‖_{H_d} < (mη₀/(M(1+η₁)))(−cos φ)) is never checked against actual models. The A-MONO curvature-density coupling condition (footnote 2) required for diffusion/flow models is stated without justification or empirical verification. This limits the theory's role to intuition rather than explanation.

5. **No variance or confidence intervals on FID.** The claimed SOTA improvement (1.02 vs. 1.06, a 0.04 difference) could fall within estimation noise. Standard FID estimates from 50k samples have non-trivial variance, and without error bars or repeated-run statistics, the statistical reliability of this specific claim is unclear.

### Trivial

6. **The Figure 4 caption sign error** (w = -1 mapping to θ_Neon = θ_r instead of θ_s) is a concrete factual error that should be corrected regardless.

## Nice-to-Haves

- A controlled comparison table with at least one competing method (DDO, SIMS, or Discriminator Guidance) applied to a shared base model would substantiate the comparative claims.
- Estimating the theoretical quantities (η₀, η₁, cos φ) for one model would strengthen the theory-experiment connection.
- Reporting standard errors for headline FID numbers would address statistical reliability concerns.

## Removed Points

*Weaknesses from reviewers that were removed after verification against the paper:*

- **Criticism about "10k/50k split for hyperparameter search is standard but means reported numbers are best among searched configurations"** — This is standard practice in the field and not a weakness. The paper follows established evaluation methodology. Removed as a nitpick.

- **Criticism that "the paper should clarify whether competing methods also had hyperparameters jointly optimized"** — The paper compares against published numbers where methodology is documented by the original authors. This level of cross-paper detail is not standard. Removed as scope creep.

- **Criticism about "no discussion of when Neon does not work"** — The paper includes a CIFAR-10C null result showing no improvement from corrupted image data, which is a meaningful negative result. Removed; the paper does address this.

- **Strength Finder's claim about Theorem 1's sufficient condition being "a formal explanation beyond prior work"** — Retained and merged into Strength 1; this is a legitimate strength.

- **Criticism that the characterization of competing methods' limitations is unquantified** — The paper correctly identifies architectural constraints (e.g., DDO cannot apply to likelihood-free models). Quantifying "how much this matters" is unnecessary when the limitation is architectural. Removed.

## Novel Insights

The harsh critic correctly identifies that Figure 4's caption has a sign error and that the optimal w ≈ -0.5 for a standard unconditional diffusion model (EDM-VP on CIFAR-10, using a standard ODE solver) creates a genuine tension with the paper's w > 0 framing. The paper's "When interpolation helps" section attributes w < 0 to diversity-seeking samplers, which it claims are "rare in practice." But the EDM-VP sampler is classified by Theorem 2 as mode-seeking, which should give w > 0. The paper never flags or explains this contradiction. However, the broader empirical pattern across all experiments — especially the autoregressive + CFG models where w* ≈ 1.0 (Figure 6) — still supports Neon's effectiveness as a method. The tension is primarily in the framing and in the scope of the theoretical claim, not in the method's validity.

## Suggestions

1. **Correct the Figure 4 caption sign error** (w = -1 corresponds to θ_Neon = θ_s, not θ_r).
2. **Acknowledge and explain** why EDM-VP on CIFAR-10 (standard ODE solver, no CFG) has its optimal merge weight at w ≈ -0.5 despite Theorem 2 predicting w > 0 for mode-seeking samplers. Either revise the scope of the theoretical claim or explain which second-order effects (curvature, model error magnitude) cause the discrepancy.
3. **Add a controlled comparison** with at least one competing method (e.g., apply SIMS to EDM-VP on CIFAR-10, or DDO to xAR-L on ImageNet-256) to substantiate the comparative claims about simplicity and universality.
4. **Disclose what is included in the "additional compute" figures** — specifically, whether the inference cost of generating the synthetic dataset S is counted, and provide the full cost if it is not.
5. **Add confidence intervals or standard errors** for the headline FID numbers, especially the SOTA claim of 1.02 vs. 1.06.

## Score and Decision

**Score: 6.0**  
**Decision: Borderline Accept — revision required**

The paper presents a genuinely interesting idea, strong theoretical grounding, and impressively broad empirical validation. The method is simple, efficient, and works across diverse architectures — these are real contributions.

However, two significant issues must be addressed before acceptance: (1) the Figure 4 caption error and the unacknowledged tension between the w > 0 framing and the w ≈ -0.5 optimum for a standard unconditional diffusion model; and (2) the lack of controlled comparisons against the specific methods the paper positions itself against. The compute accounting issue also needs clarification. These are resolvable in revision and do not invalidate the core contribution.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Reject</decision>
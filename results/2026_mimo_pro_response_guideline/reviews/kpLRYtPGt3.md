Now I have enough data to finalize my assessment. Let me compile the full review.

Based on my calibration:

**Round 1 bracket:** 6.5–8.0 (clearly above rejected papers at 3-4, above borderline accepts at 5-6, competitive with strong accepts at 7-8)

**Round 2 narrowing:** 6.5–7.5 (comparable to CCA at 7.0, Improved Consistency Training at 7.0, above Self-Consuming MAD at 6.67, below CADS/Shortcut Models at 8.0)

**Final score:** 7.0

The paper is above the 6.67 anchors (MAD paper — Neon provides the solution to the problem MAD identifies), comparable to the 7.0 anchors (CCA — narrower scope requiring original data; Improved Consistency Training — specific to one architecture), and below the 8.0 anchors (CADS, Shortcut Models — cleaner theoretical claims, fewer caveats). The A-MONO gap and joint optimization concern prevent a higher score, but the paper's novelty, universality, SOTA results, and simplicity strongly support acceptance.

---

## Summary

This paper introduces Neon, a remarkably simple post-hoc method for improving generative models by negatively extrapolating from the degradation caused by self-training. The three-step method (generate synthetic data, fine-tune briefly, merge parameters) is grounded in a theoretical framework showing that mode-seeking inference samplers create predictable anti-alignment between synthetic and real-data population gradients. Neon achieves state-of-the-art FID 1.02 on ImageNet-256 with xAR-L using only 0.36% additional compute, and is demonstrated across diffusion, flow matching, autoregressive, and few-step model architectures.

## Strengths

- **Extreme simplicity and practical efficiency**: Algorithm 1 is three lines — generate synthetic data, fine-tune briefly, merge parameters via θ_Neon = (1+w)θ_r − wθ_s. No auxiliary models, no likelihood computation, no inference modifications, no access to original training data. The headline result uses only 0.36% additional compute (line 209).

- **New state-of-the-art on ImageNet-256**: xAR-L achieves FID 1.02 (from 1.28 baseline), surpassing UCGM's 1.06, using only 750k synthetic samples (Section 4.2, Figure 5). Even with just 1k samples, xAR-L reaches FID 1.05, indicating the degradation direction stabilizes extremely quickly.

- **Demonstrated universality across four fundamentally different model families**: Diffusion (EDM-VP), flow matching, autoregressive (VAR, xAR), and few-step generators (IMM) on CIFAR-10, FFHQ-64, and ImageNet (Sections 4.1–4.3). This breadth exceeds prior methods like DDO (inapplicable to flow matching/IMM), Discriminator Guidance and SIMS (diffusion-specific).

- **Clean theoretical framework**: Theorems 1 and 2 establish that mode-seeking samplers guarantee cos φ < 0 (Theorem 2), which combined with small model error implies anti-alignment s < 0 (Theorem 1), enabling risk reduction via negative extrapolation (Equation 4). This provides a falsifiable, mechanistic explanation rather than an ad-hoc trick.

- **Compelling precision-recall analysis**: Figure 4 shows Neon trades precision for recall — redistributing mass from over-represented to under-represented modes — directly validating the theoretical framework. The dynamics intensify with longer fine-tuning as predicted by w* ≈ −s/(αz) (line 203).

- **Comprehensive ablation studies**: Cross-architecture transfer (Figure 8 — IMM data improves EDM-VP), base model quality robustness (Figure 9 — Neon + 30k real data ≈ full 50k), synthetic data quality sensitivity (Figure 10 — robust for γ ∈ [1,3]), and CIFAR-10C null result confirming Neon exploits model-specific bias rather than generic OOD signals (line 249).

## Weaknesses

### Fatal
None

### Major

- **A-MONO assumption for diffusion/flow matching is unverified**: The theoretical guarantee for diffusion and flow matching models requires the A-MONO assumption (footnote 2, line 161): that the conditional expectation of gradient magnitudes increases with log-density. This is stated but never proven or empirically verified — it is declared in a footnote and relegated to Appendix B.7. This is the weakest theoretical link and covers half the architectures tested. The paper's Contribution C2 claims to "prove rigorously" that mode-seeking samplers guarantee effectiveness, but this proof is conditional on A-MONO for diffusion/flow models. The empirical results validate Neon for these architectures, but the theoretical claims should more carefully distinguish unconditional (autoregressive) vs. conditional (diffusion/flow) guarantees.

- **Joint optimization of w and γ for autoregressive/few-step models conflates Neon with hyperparameter re-tuning**: For autoregressive and few-step models (Sections 4.2–4.3), reported FID improvements come from jointly optimizing (w, γ) via grid search (line 207: "we jointly optimize both the merge weight w and CFG scale γ"). Figure 6 shows that γ-only optimization (w=0) gives FID 3.01 vs. the joint optimum of 2.01 for VAR-d16. A cleaner ablation would report results with γ fixed at the base model's optimal setting and only w varied, to isolate Neon's contribution from CFG re-tuning. The diffusion/flow matching experiments (Section 4.1) do not involve this issue and show clean improvements, which mitigates but does not eliminate this concern for the headline xAR-L result.

### Minor

- **Typo in Theorem 1 statement**: Line 134 writes "s = ⟨r_s, P r_s⟩" but the definition at line 110 defines "s := ⟨r_d, P r_s⟩". The former is a self-inner product (always non-negative for P ≻ 0); the latter is the real-vs-synthetic gradient alignment that makes anti-alignment meaningful. This appears to be a typographical error (subscript d lost) that would confuse readers verifying the result.

- **"< 1% compute" claim slightly overstated**: The abstract claims "typically uses less than 1% additional training compute." This holds for xAR (0.36%), VAR (0.64%), EDM-VP/FFHQ (0.85%), and IMM (<0.005%), but flow matching on CIFAR-10 requires 3.2% and EDM-VP on CIFAR-10 requires 1.75% (line 185-186). The word "typically" provides cover, but as the main practical selling point, a slight qualification would improve accuracy.

- **Sample efficiency variance across architectures deserves more analysis**: VAR-d16 requires |S| ≥ 90k (line 225: "performance degrades with |S| < 90k") while xAR models work with 1k samples (line 209). This 90× difference in sample efficiency between related autoregressive architectures is noted but not analyzed. The theoretical framework (finite |S| effects, Appendix B.10) could potentially explain this, but the connection is not made.

### Trivial
None

## Nice-to-Haves
- Sensitivity plot of FID vs. w for the headline xAR-L/ImageNet result at optimal budget (currently only shown for EDM-VP/CIFAR-10 in Figure 4)
- Report w-only results (γ fixed at base model optimal) alongside joint (w,γ) optimization for autoregressive models to cleanly isolate Neon's contribution
- Provide empirical evidence for A-MONO — even showing denoising gradient magnitudes correlate with log-density across ImageNet classes would strengthen the theory for half the model families
- Direct numerical comparison with DDO on shared benchmarks (e.g., EDM on CIFAR-10) to help readers calibrate improvements
- Analyze the cosine similarity between θ_s − θ_r computed from different random seeds to quantify variance of the degradation direction

## Removed Points
These points are flagged to be removed, treat them with caution.
- The harsh critic's concern about the strength finder's "rigorous theoretical grounding" claim is partially valid — the theory is clean and well-motivated but the rigor is conditional for diffusion/flow. This is retained as a major weakness rather than removed.
- Formatting/style nitpicks from any reviewer source are removed per policy.

## Novel Insights
The paper's genuinely novel insight is reframing model collapse/degradation from self-training as a structured, anti-aligned gradient signal that can be systematically reversed. The key non-obvious contribution is connecting the sign of the gradient alignment to the mode-seeking property of inference samplers — a standard practitioner choice that was previously viewed only as a quality-diversity trade-off. This connection unifies the treatment across architectures and provides both theoretical grounding and practical guidance. The precision-recall mechanistic explanation (self-training concentrates mass on over-represented modes; negative extrapolation redistributes it) goes beyond a purely mathematical result to provide actionable intuition.

## Suggestions
- Fix the typo in Theorem 1 (⟨r_s, P r_s⟩ → ⟨r_d, P r_s⟩)
- Qualify the "< 1% compute" claim to "< 3%" or explicitly note the flow matching/EDM-VP exceptions
- Add w-only ablation (γ fixed) for autoregressive headline results
- Either prove or empirically validate A-MONO, or qualify Contribution C2 to distinguish unconditional vs. conditional guarantees
- Analyze the 90× sample efficiency gap between xAR and VAR architectures

---

**Calibration Anchors:**

| Anchor Paper | Avg Score | Round | Comparison |
|---|---|---|---|
| Self-Consuming Generative Models Go MAD | 6.67 | 1 | Studies the problem Neon solves; Neon is more practical and achieves SOTA |
| Post-hoc Discriminator Guidance (PDG) | 3.00 | 1 | Similar post-hoc improvement theme but much narrower (GANs only, marginal improvements) |
| Dynamic Negative Guidance of Diffusion Models | 6.25 | 1 | Principled negative guidance but diffusion-only, limited to MNIST/CIFAR-10 |
| Self-distillation for diffusion | 3.00 | 1 | Self-training related but much weaker contribution |
| Minority Guidance for Diffusion Models | 5.25 | 1 | Diffusion-only, narrower scope, missing baselines |
| Augmented Conditioning for Training Image Gen | 4.00 | 1 | Synthetic data for training, but rejected with limited novelty |
| Diffusion Curriculum | 4.00 | 1 | Synthetic-to-real data curriculum, rejected |
| Improved Techniques for Training Consistency Models | 7.00 | 2 | Single architecture improvement; Neon is more universal |
| PaRa: Personalizing T2I via Parameter Rank Reduction | 7.50 | 2 | Post-hoc parameter modification; different domain, narrower scope |
| CCA: Guidance-Free AR Visual Generation | 7.00 | 2 | AR-specific, requires original data; Neon is more universal and novel |
| HART: Hybrid Autoregressive Transformer | 6.80 | 2 | AR generation model; different contribution type |
| Representative Guidance | 7.33 | 2 | Diffusion sampling improvement; narrower scope |
| Self-Consuming Generative Models Go MAD | 6.67 | 2 | Foundational study; Neon provides the practical solution |
| On Stability of Iterative Retraining | 6.75 | 2 | Theoretical study of self-training stability; complementary |
| CADS: Condition-Annealed Diffusion Sampling | 8.00 | 1 | Principled diffusion sampling, achieved SOTA 1.70; Neon surpasses this but has theoretical gap |
| One Step Diffusion via Shortcut Models | 8.00 | 1 | New model family; different type of contribution |
| Real-Fake: Effective Training Data Synthesis | 6.00 | 1 | Synthetic data for classification; narrower |
| Not All LLM-Generated Data Are Equal | 7.50 | 2 | Data weighting for LLM synthetic data; different domain |

**Round 1 bracket:** 6.5–8.0
**Round 2 narrowing:** 6.5–7.5
**Final score:** 7.0

The paper sits clearly above the 6.67 MAD paper (which studies the problem Neon solves) and the 7.0 CCA paper (narrower, requires original data). It is below the 8.0 CADS paper (cleaner theory, no unverified assumptions). The A-MONO gap and joint optimization concern are real but mitigated by empirical evidence and clean diffusion/flow results. This is a strong, well-executed paper with a genuinely novel and counterintuitive insight that merits acceptance.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>
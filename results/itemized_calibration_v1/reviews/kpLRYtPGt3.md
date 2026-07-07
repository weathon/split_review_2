Now I have enough calibration data. Let me compile the final review.

## Summary

Neon introduces a post-hoc parameter merge that reverses the degradation from fine-tuning a generative model on its own synthetic outputs. The paper proves that mode-seeking inference samplers create predictable anti-alignment between synthetic and real-data gradients, and shows that negative extrapolation corrects this bias. Experiments across diffusion, flow matching, autoregressive, and few-step models on ImageNet, CIFAR-10, and FFHQ demonstrate consistent FID improvements, including a SOTA result of 1.02 on ImageNet-256 (xAR-L).

## Strengths

1. **Genuinely novel and non-obvious idea.** The core insight — that self-training degradation is a *structured* signal anti-aligned with the real-data gradient, and that reversing it via a simple parameter merge improves the model — is clever and counterintuitive. This is not an incremental modification.

2. **Remarkable simplicity with strong results.** The method is a single post-hoc parameter merge (Equation 2). The SOTA result on ImageNet-256 (FID 1.02, surpassing UCGM's 1.06) is clearly documented with provenance from a public xAR-L checkpoint. The FID improvement from 1.28 to 1.02 is substantial (Section 4.2).

3. **Unusually broad empirical validation.** Neon is tested across four distinct model families (diffusion, flow matching, autoregressive, few-step), three datasets (ImageNet, CIFAR-10, FFHQ), and multiple scales. The IMM results (Figure 7) are particularly striking: Neon with 4 steps nearly matches the base model's 8-step quality.

4. **Well-motivated theoretical framework.** The theory (Section 3.1) provides a clear sufficient condition for Neon to work (anti-alignment between synthetic and real gradients) and links it concretely to mode-seeking samplers. Theorems 1 and 2 establish a formal chain from inference sampler properties → gradient anti-alignment → risk reduction. The toy Gaussian study (Figure 2) effectively visualizes the intuition.

5. **Extensive ablations that test boundary conditions.** The transferability experiment (Section 4.4), base-model-quality sensitivity (Figure 9), and synthetic-data-quality sensitivity (Figure 10) probe the method's assumptions. The finding that Neon compensates for a ~40% reduction in real training data (Section 4.4) is practically meaningful.

## Weaknesses

### Fatal
None.

### Major

1. **Missing baseline: continued fine-tuning on the original real data.** The paper's framing emphasizes that Neon "requires no new real data." However, the most natural baseline — using the same fine-tuning budget (0.36–3.2% of training compute) to continue training on the *original* real data (or a held-out subset) — is never run in the main experiments. The toy study (Figure 2) compares Neon against an "oracle improvement" using 4× more real data, but this comparison is not carried into the main empirical evaluation. If continued real-data fine-tuning for the same budget achieves similar or better FID gains, Neon's benefit may not stem from the anti-alignment mechanism specifically — it could simply reflect a benefit from additional training at a reduced learning rate. The CIFAR-10 EDM experiments (where the base model trained on 50k images) offer the most cost-effective testbed. This is an evidential gap rather than a structural flaw, but it weakens the attribution of *why* Neon works.

### Minor

2. **Compute accounting ambiguity.** The "% additional training compute" figures (e.g., 0.36% for xAR-L, 0.85% for EDM-VP on FFHQ-64) are not clearly scoped. It is not stated whether these include the cost of *generating* the synthetic dataset S. For the 750k-sample xAR-L result, generation with a large autoregressive model is non-trivial. The paper should either (a) confirm that generation costs are negligible for the configurations used (the 1k-sample result achieving FID 1.05 is relevant here), (b) report total compute including generation, or (c) clearly separate the two components.

3. **Precision-recall tradeoff discussion lacks practical operating point analysis.** The paper frames the precision decrease and recall increase as a net positive from an FID perspective (Section 4.1, Figure 4), which is accurate. However, a drop in precision from ~0.95 to ~0.87 (VAR-d16, Figure 6) could be unacceptable for applications requiring high-fidelity generation (e.g., medical imaging, content creation). The paper does not discuss whether the FID-optimal operating point is desirable for such use cases, or whether alternative (w, γ) combinations might be preferred when precision matters.

4. **EDM-VP baseline discrepancy unexplained.** The main EDM-VP experiment (Section 4.1) uses a conditional CIFAR-10 model with FID 1.78, while the transfer experiment (Section 4.4) uses an unconditional EDM-VP model with FID 1.97. The paper notes the difference (conditional vs. unconditional) but does not explain *why* different variants are used across experiments. This could confuse readers comparing results across sections.

### Trivial

5. **Figure 4 caption error.** The caption states "w = -1 corresponds to the model directly trained on synthetic data, i.e., θ_Neon = θ_r." Plugging w = -1 into Equation 2 gives θ_Neon = θ_s (the model fine-tuned on synthetic data), not θ_r. The mapping for w = -1 should be θ_Neon = θ_s.

6. **Undefined theoretical term in main text.** The theoretical analysis (footnote 1) invokes "directional smoothness" as a sufficient condition but defers its definition to Appendix B.4 without any characterization in the main text. This makes the core theoretical condition opaque for non-specialist readers.

## Nice-to-Haves

- Empirically estimate the anti-alignment signal s = ⟨r_d, P r_s⟩ for at least one model by computing gradients on held-out real-data vs. synthetic-data batches at θ_r. A measured negative value would directly confirm the mechanism that the theory guarantees only through sufficient conditions.
- Extend the precision-recall discussion to identify alternative (w, γ) operating points for applications that prioritize precision over FID.
- Jointly tune the hyperparameter (w, γ) across diffusion/flow models as was done for autoregressive models — Figure 6 suggests this interaction is important.

## Removed Points

These points were raised in the input review but are removed per filtering rules:

- "Theorem 2's result for diffusion/flow models relies on an assumption (A-MONO) deferred to Appendix B.7 — without seeing this appendix, it's difficult to assess whether the assumption is restrictive." → Removed per rule: the parser strips appendix content from all papers; the assumption and its justification exist in the original submission.

- "Theorem 1's constants (m, M, η₀, η₁) are never estimated empirically." → This describes a feature of theoretical analysis that provides qualitative understanding rather than quantitative guarantees, which the paper explicitly acknowledges. Not a structural weakness.

- "The Taylor expansion assumes local convexity..." → The paper already notes in footnote 1 that local convexity is sufficient but not necessary and cites a weaker condition. The deferred definition ("directional smoothness") is noted as Trivial weakness #6.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Add the continued-real-data-fine-tuning baseline for at least one model family (CIFAR-10 EDM is the most cost-effective) to disentangle whether Neon's benefit comes from the anti-alignment mechanism or from additional training at a reduced learning rate.
- Clarify the scope of "% additional compute" figures: state explicitly whether synthetic data generation costs are included, and if not, report them separately or note that near-optimal FID is reachable with 1k samples where generation cost is negligible.
- Explain why the EDM-VP transfer experiment uses an unconditional model while the main experiment uses a conditional one (different public checkpoints or different experimental goals).
- Correct the Figure 4 caption mapping for w = -1.
- Briefly characterize "directional smoothness" in the main text or note it as a standard smoothness condition on the loss landscape.

## Score and Decision

**Calibration anchors consulted across rounds:**

| Anchor | Path | Avg Score | Round | Itemized? | Comparison |
|--------|------|-----------|-------|-----------|------------|
| Strong Model Collapse | et5l9qPUhm.md | 8.00 | 1 | Yes | Stronger theory, weaker experiments; comparable overall quality |
| Dynamic Negative Guidance | 6p74UyAdLa.md | 6.25 | 1 | Yes | Weaker empirical validation (limited to MNIST/CIFAR-10, no FID); my paper is substantially stronger |
| Model Merging (Uncertainty) | D7KJmfEDQP.md | 6.00 | 1 | Yes | Thin experimental section, missing baselines; my paper has much more thorough validation |
| KD to Mitigate Model Collapse | 8TbqoP3Rjg.md | 2.00 | 1 | Yes | Poor presentation, lacks novelty; not comparable |
| Representative Guidance | gWgaypDBs8.md | 7.33 | 2 | Yes | Similar originality (+4), but limited to one dataset/resolution; my paper broader |
| Diffusion-NPO | iJi7nz5Cxc.md | 7.00 | 2 | Yes | Strong results but concern about not differing from existing methods; my paper more novel |

**Round 1 bracket:** 7.5–8.5. The paper's novelty, breadth of validation, and SOTA results placed it clearly above the 6–7 range anchors (DNG, Model Merging). The Strong Model Collapse anchor (8.00) validated that papers with significant evidential gaps can still score 8.0 when the contribution is strong. My paper's missing baseline (continued real-data fine-tuning) is comparable in severity to that anchor's weaknesses.

**Round 2 narrowing:** Comparing against Representative Guidance (7.33) and Diffusion-NPO (7.00), my paper has broader empirical validation and a more novel core idea. The single major weakness (missing baseline) is an evidential gap but does not invalidate the demonstrated results. The paper's theoretical grounding, breadth of architectures tested, and extensive ablations all exceed the 7-range anchors.

**Final score:** The paper makes a genuinely novel, well-supported contribution with SOTA results across diverse architectures. The primary weakness is the missing baseline that would strengthen causal attribution, not a flaw in the results themselves. This places the paper solidly at 8.0 — a clear accept with room for improvement through the suggested revisions.

MY FINAL SCORE: <score>8.0</score>
MY FINAL DECISION: <decision>Accept</decision>
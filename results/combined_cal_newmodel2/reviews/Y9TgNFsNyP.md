I now have all the information needed to construct the final review. Let me compose it.

---

## Summary

This paper introduces FF-Erase, the first machine unlearning framework specifically designed for Forward-Forward (FF) models — a biologically plausible alternative to backpropagation where layer-wise greedy optimization replaces end-to-end gradient flow. The method uses a guidance model to produce target goodness distributions and minimizes KL-divergence toward those targets, enabling stable forgetting while preserving model utility. The paper also proposes G-MIA, a membership inference attack that leverages the layer-wise goodness vectors naturally produced by FF models for verifying unlearning effectiveness.

## Strengths

1. **Novel and well-motivated problem identification (Section 1).** The paper is the first to formalize machine unlearning for FF models. It correctly identifies two concrete failure modes of standard gradient-based unlearning on FF models: (a) layer-wise update directions can diverge during unlearning because FF layers are optimized independently rather than through backpropagation, and (b) the independent training makes it unclear how much each layer's goodness should be penalized, causing some layers to over-forget while others retain residual effects.

2. **Clean and architecturally appropriate method design (Section 4.1).** The goodness-guidance mechanism is a natural fit for the FF architecture. Using a guidance model to produce stable target goodness distributions and minimizing KL-divergence toward those targets directly addresses the instability problem without requiring backpropagation across layers. The "forgetting forward" / "recovering forward" decomposition is conceptually clear and matched to FF training mechanics.

3. **G-MIA is practically useful and empirically validated (Section 5, Figure 3).** G-MIA leverages goodness vectors — which are the natural output of FF model inference — for membership inference. It consistently outperforms standard black-box final-layer MIA across all tested datasets and architectures, and sometimes matches white-box attacks on deeper models (VGG13, CIFAR-100). This fills a genuine gap for unlearning verification in FF settings where full model access may not be available.

4. **Thorough ablation study on guidance model trade-offs (Table 1).** The systematic exploration of α₁ (data proportion) and α₂ (epoch proportion) for both mini-retrained and fast-distilled guidance models provides concrete, actionable guidance for practitioners. The R.G.M. (random guidance model) baseline convincingly demonstrates that the guidance model is necessary, not incidental.

## Weaknesses

### Fatal
None.

### Major

1. **Insufficient comparison baselines.** The paper asserts that "existing unlearning methods are not feasible for FF models" (Section 1) but only empirically tests vanilla gradient ascent (GA) against the proposed method. While the paper provides architectural arguments for why BP-based methods would fail on FF models (Section 1, Appendix A), these are not experimentally validated. The lack of alternative baselines is particularly noticeable because FF-Erase itself uses a distillation-like approach (guidance model + KL-divergence), making a distillation-based unlearning method like Bad Teacher (Chundawat et al., 2023a) a natural baseline that could be adapted. Without at least one non-GA baseline, the empirical scope of the contribution is narrower than the paper's framing as the first method to overcome all existing methods' infeasibility.

2. **Complete absence of statistical variance reporting.** All results — accuracy values (Table 1, Figure 4), G-MIA scores (Figure 4c, Figure 5c), and timing measurements (Table 1) — are reported as single-run values without standard deviations, confidence intervals, or multiple seeds. This is a significant gap because: (a) the G-MIA scores that separate effective from ineffective unlearning are very close (e.g., FF-Erase(D) G-MIA ACC of 0.5245 vs. RE's 0.532 — a difference of 0.0075), making it impossible to assess whether these differences are meaningful or noise; (b) timing measurements are reported to sub-second precision (e.g., 583.5s vs 426.7s in Table 1) without any indication of run-to-run variability.

### Minor

1. **G-MIA categorization overstates information constraint.** The paper categorizes G-MIA as a "black-box" attack, but standard black-box MIA assumes access only to final-layer predictions/logits (as the paper itself notes in Section 2: "Black-box MIAs... only use the model's final prediction output"). G-MIA requires per-layer goodness vectors from the target model, which is more information. While goodness vectors are the natural output of FF models during inference, the framing overstates G-MIA's practical advantage relative to the standard definition it claims to improve upon. A more precise label (e.g., "output-feature access" or describing the exact threat model used) would better represent the method's setting.

2. **KL-divergence choice not motivated.** The forgetting forward loss (Equation 5) uses KL-divergence without discussion or ablation of alternatives (e.g., reverse KL, JS divergence, L2 distance on goodness distributions). Since the guidance framework is the paper's core contribution, a brief justification for this design choice would strengthen the methodological rationale.

3. **G-MIA synthetic data assumption unexplored.** G-MIA assumes attackers can generate in-distribution synthetic data via model inversion (Section 5, line 200). Model inversion on FF models is itself an unexplored problem, and the paper does not probe how G-MIA's accuracy degrades as synthetic data quality decreases.

### Trivial
None.

## Nice-to-Haves

- All experiments use a fixed 20% forgetting ratio. Testing with 1%, 5%, 50% would probe the method's boundaries and practical limits.
- Extending to non-image tasks (e.g., the text or graph domains mentioned in Section 2's related work on FF algorithms) would broaden demonstrated generality.
- Timing measurements could benefit from multiple runs to distinguish systematic differences from measurement noise.

## Removed Points

The following points from the harsh critic input were removed for the reasons stated:

- **Missing hyperparameter values (ε₁, ε₂, λ, K):** REMOVED — these may be specified in the appendix, which was stripped by the parser. The instructions prohibit penalizing missing appendix content.
- **Main text limited to VGG13 on CIFAR-10:** REMOVED — the paper explicitly states other results are in Appendix C. This is a space limitation, not an evaluative weakness.
- **"Penicillin" analogy about baseline testing:** REMOVED — the hyperbolic framing overstates the issue. The paper provides architectural reasoning for why BP-based methods fail. The remaining weakness about limited baselines is retained but stated in measured terms.
- **Missing related works:** REMOVED per instructions — the reviewer cannot verify claimed omissions.
- **Formatting/style nitpicks:** REMOVED per instructions.

## Novel Insights

None beyond the paper's own contributions. The reviews confirm the paper's core novelty (first FF unlearning framework, G-MIA verification) but surface evaluation limitations that the paper does not fully address — specifically around baseline breadth and statistical rigor. No unexpected analytical insight emerged from the reviews beyond what the paper itself communicates.

## Suggestions

1. Add at least one non-GA baseline adapted to the FF setting. A distillation-based method (e.g., adapting Bad Teacher's framework) is the most natural choice since FF-Erase itself uses a guidance model with KL-divergence.
2. Report all key results (accuracy, G-MIA scores, timing) with at least 3–5 random seeds and include standard deviations or confidence intervals.
3. Add a brief discussion of why KL-divergence was chosen over alternative divergence measures for the forgetting forward loss.
4. Probe G-MIA's sensitivity to synthetic data quality with a controlled degradation experiment.

## Score and Decision

**Calibration summary:** Across the anchor papers retrieved and itemized, the paper under review sits between the low-scoring reject anchors (PPU at 3.0, UGradSL at 3.0, MASIMU at 2.5) and the borderline/accept anchors (Utility and Complexity at 6.60, accept). It is clearly stronger than the 3.0-level papers (better novelty, clearer methodology, thorough ablation) but shares key weaknesses with the 5.25-level rejected papers (Unlearning via Sparse Representations, Deep Unlearning): limited baseline comparisons and absence of variance/statistical rigor. The round-1 bracket was 4–6. Round 2 narrowed this: the paper's itemized weaknesses (favorability -0.28 for baseline insufficiency, +0.64 for no variance) are comparable to those in the 5.25 anchors, while its strengths (favorability 13–14) are slightly higher. Unlike the 6.60 accepted anchor (which compensated evaluation gaps with strong theoretical contributions), this paper offers no theoretical guarantees to offset its empirical gaps.

**Final score: 5.0. Decision: Reject.** The paper tackles a real gap with a clean method and a good ablation study, but the evaluation is undermined by two well-separated weaknesses: only one non-trivial baseline (GA) is tested, and there is no variance reporting at all. These gaps prevent the empirical claims from being fully substantiated in their current form, placing the paper below the acceptance threshold. The core ideas are sound and the weaknesses are fixable — the paper could be competitive with a strengthened evaluation.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>